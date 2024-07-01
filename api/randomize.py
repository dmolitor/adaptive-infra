import numpy as np
import random
from sqlalchemy import Engine
from sqlmodel import Session, select
from tables import Bandit, Batch
from typing import List

"""
This script handles all elements of randomization for the survey.
These steps include:
    - Randomize order in which candidates are shown
    - Randomize which bandit context (arm) is shown
    - Randomize the order in which context characteristics are shown
"""

# Create random number generator
rng = np.random.default_rng()


def draw_arms(params: dict, max: bool, n_sim: int = int(1e5)) -> dict:
    """
    Take parameters for each bandit arm's posterior beta distribution,
    pull `n_sim` draws from the distribution, and calculate cumulative fraction
    of draws that each arm is the max/min discriminatory arm.

    E.g.
    ```
    input = {
        "arm3": {"alpha": 1, "beta": 1},
        "arm1": {"alpha": 3, "beta": 7},
        "arm2": {"alpha": 7, "beta": 3}
    }

    draw_arms(input)
    # {'arm3': 0.296921, 'arm1': 0.312308, 'arm2': 1.0}
    ```
    """
    array_list = []
    ## TODO: same complaint. Want to make this distribution agnostic.
    for value in params.values():
        # For each arm generate `n_sim` draws from the posterior beta dist.
        array_list.append(rng.beta(a=value["alpha"], b=value["beta"], size=n_sim))
    # Combine these into a 2-d numpy array
    matrix = np.vstack(array_list)
    # Which arm generates the max/min value for each row
    if max:
        target_indices = np.argmax(matrix, axis=0)
    else:
        target_indices = np.argmin(matrix, axis=0)
    # Now replace the matrix with 1s in the target indices and 0s elsewhere
    target_indices_arr = np.zeros_like(matrix)
    target_indices_arr[target_indices, np.arange(matrix.shape[1])] = 1
    # Now take the mean (fraction of 'wins') for each arm
    arm_means = np.cumsum(np.mean(target_indices_arr, axis=1))
    # Reformat as a dictionary with arm labels as keys
    arm_means_dict = {}
    for key, value in zip(params.keys(), arm_means):
        arm_means_dict[key] = float(value)
    return arm_means_dict


def html_format(input: dict) -> str:
    """Format the candidates as an HTML table for the UI"""
    first = input["first"]
    second = input["second"]
    prior_trips = (
        f"<tr><td>Prior trips to the U.S.</td><td>{first['prior_trips']}</td>"
        + f"<td>{second['prior_trips']}<br></td></tr>"
    )
    education = (
        f"<tr><td>Education</td><td>{first['education']}<br></td>"
        + f"<td>{second['education']}<br></td></tr>"
    )
    reason = (
        f"<tr><td>Reason for application</td><td>{first['reason']}<br></td>"
        + f"<td>{second['reason']}<br></td></tr>"
    )
    origin = (
        "<tr><td>Country of origin</td>"
        + f"<td>{first['origin']}</td>"
        + f"<td>{second['origin']}</td></tr>"
    )
    profession = (
        "<tr><td>Profession</td>"
        + f"<td>{first['profession']}</td>"
        + f"<td>{second['profession']}</td></tr>"
    )
    # This is for any features that should always show up first
    context_data = []
    # Randomize the order of the other two elements
    randomized_context_data = randomize_context_items(
        [prior_trips, education, reason, origin, profession]
    )
    html_content = (
        "<table><tbody><tr><th></th><th>Immigrant 1"
        + "</th><th>Immigrant 2</th></tr>"
        + "".join(context_data + randomized_context_data)
        + "</tbody></table>"
    )
    context = {
        "arm_id": first["arm_id"],
        "context": input,
        "html_content": html_content,
    }
    return context


def randomize(batch_id: int, engine: Engine) -> dict:
    """Randomize choice order and bandit arm. Return candidates as a dict"""
    target_arm = randomize_context(batch_id, engine)
    with Session(engine) as session:
        # Retrieve the context profiles
        bandit = session.exec(select(Bandit).where(Bandit.id == target_arm)).one()
        profile_meta = [profile.model_dump() for profile in bandit.meta]
        # 'Horizontally' randomize each candidate characteristic
        # Then separate the randomized characteristics into separate profiles
        first = {}
        second = {}
        for key in profile_meta[1].keys():
            combined_profiles = [profile_meta[0][key], profile_meta[1][key]]
            combined_profiles = random.sample(combined_profiles, 2)
            first[key] = combined_profiles[0]
            second[key] = combined_profiles[1]
        out = {"first": first, "second": second}
        return out


def randomize_context(batch_id: int, engine: Engine) -> int:
    """Randomize which bandit arm is shown to the user"""
    runif = float(rng.uniform(low=0.0, high=1.0, size=1)[0])
    with Session(engine) as session:
        batch = session.exec(select(Batch).where(Batch.id == batch_id)).one()
        batch_pi = [pi.model_dump() for pi in batch.pi]
        batch_pi_sorted = sorted(batch_pi, key=lambda x: x["pi"])
        for pi in batch_pi_sorted:
            if runif <= pi["pi"]:
                return pi["arm_id"]
    raise Exception("Failed to find a suitable `pi` value")


def randomize_context_items(input: List[str | int]) -> List[str | int]:
    """Randomize which order context characteristics are shown"""
    rand = random.sample(input, len(input))
    return rand
