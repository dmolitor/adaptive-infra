import random
import numpy as np
import pandas as pd
from sqlalchemy import Engine
from sqlmodel import Session, select
from tables import Bandit
from typing import List

# do we want to seed this or allow that as a configurable param (maybe in .env or database)?
rng = np.random.default_rng(seed=2024)

batch_metadata = {'bid_0': 
                  {
                          'arm1': 0.25,
                          'arm2': 0.5,
                          'arm3': 0.75,
                          'arm4': 1 
                      }
                  }

def randomize_age_order(ages) -> List[int]:
    """Randomize whether the older candidate is shown first"""
    return random.sample(ages, 2)

# def randomize_context(engine: Engine) -> int:
def randomize_context(batch_id, batch_metadata) -> int:
    """Randomize which bandit arm is shown to the user"""
    # with Session(engine) as session:
    #     bandit = session.exec(select(Bandit)).all()
    #     arm_ids = [arm.id for arm in bandit]
    #     arm_labels = [arm.label for arm in bandit]
    
    # get pi values for batch id
    batch_pi = batch_metadata['bid_'+str(batch_id)]
    runif = np.random.uniform(low = 0.0, high = 1.0, size = 1)

    # return context id based on probabilities in dictionary
    if runif <= batch_pi['arm1']:
        return 1
    elif runif > batch_pi['arm1'] and runif <= batch_pi['arm2']:
        return 2
    elif runif > batch_pi['arm2'] and runif <= batch_pi['arm3']:
        return 3
    elif runif > batch_pi['arm3'] and runif <= batch_pi['arm4']:
        return 4
    else:
        return -9

def randomize_context_items(input: List[str]) -> List[str]:
    """Randomize which order context characteristics are shown"""
    rand = random.sample(input, len(input))
    return rand

print(randomize_context(0, batch_metadata))

## `randomize` and `html_format` together form `main.py/randomize_context`
## which returns all the context-relevant data, randomized on all three levels
## - Randomize order in which candidates are shown
## - Randomize which bandit context (arm) is shown
## - Randomize the order in which context characteristics are shown
# def randomize(engine: Engine) -> dict:
#     """Randomize choice order and bandit arm. Return candidates as a dict"""
#     choice_order = randomize_choice_order()
#     target_arm = randomize_context(engine)

def randomize(batch_id, batch_metadata):
    ages = [70, 26]
    age_rand = randomize_age_order(ages)

    context_id = randomize_context(batch_id, batch_metadata)

    # this would ideally be the information selected via the output of
    # the random context selector
    # e.g., this would be the characteristics associated
    # with each respective context_id
    bandit_meta =  {
                "political_experience": ["Member of Congress", "State legislator"],
                "name": ["Joseph", "Daniel"],
                "career_experience": ["Restaurant owner", "Small business owner"],
            }

    out = {'first': {'age': age_rand[0]},
           'second': {'age': age_rand[1]}
           }
    for i,j in bandit_meta.items():
        rand_items = randomize_context_items(j)
        out['first'][i] = rand_items[0]
        out['second'][i] = rand_items[1]
    return out


print(randomize(0, batch_metadata))

responses = [{'id': 0,
             'chose_younger': 1,
             'arm': 1
             },
             {'id': 1,
             'chose_younger': 1,
             'arm': 4
             },
             {'id': 2,
             'chose_younger': 0,
             'arm': 3
             },
             {'id': 3,
             'chose_younger': 0,
             'arm': 2
             },
             {'id': 4,
             'chose_younger': 1,
             'arm': 4
             }]

def update_posterior(sim, responses: List) -> List:
    """Update posterior probabilities based on responses"""
    resp_df = pd.DataFrame(responses)
    alpha_upd = resp_df.groupby('arm')['chose_younger'].sum().sort_index().tolist()
    beta_upd = resp_df.assign(chose_older = resp_df['chose_younger'] == 0).\
        groupby('arm')['chose_older'].sum().sort_index().tolist()

    draws = {i: np.random.beta(alpha_upd[i] + 10,
                            beta_upd[i] + 10,
                            size=sim) for i in range(len(alpha_upd))}
    draws_array = np.array([draws[i] for i in range(len(alpha_upd))])
    draws_mean = (draws_array.argmax(axis=0)[:,None] == np.arange(4)).astype(int).mean(axis=0)
    return np.cumsum(draws_mean)

    # with Session(engine) as session:
    #     bandit = (
    #         session
    #         .exec(select(Bandit).where(Bandit.id == target_arm))
    #         .one()
    #     )
    #     bandit_meta = bandit.meta
    #     first = bandit_meta[choice_order[0]].model_dump()
    #     second = bandit_meta[choice_order[1]].model_dump()
    #     out = {"first": first, "second": second}
        # return out

print(update_posterior(100, responses))

def html_format(input: dict) -> str:
    """Format the candidates as an HTML table for the UI"""
    first = input["first"]
    second = input["second"]
    names = (
        f"<tr><td>Name</td><td>{first['name']}</td>"
        + f"<td>{second['name']}<br></td></tr>"
    )
    ages = (
        f"<tr><td>Ages</td><td>{first['age']}<br></td>"
        + f"<td>{second['age']}<br></td></tr>"
    )
    pexp = (
        "<tr><td>Political experience</td>"
        + f"<td>{first['political_experience']}</td>"
        + f"<td>{second['political_experience']}</td></tr>"
    )
    cexp = (
        "<tr><td>Career experience</td>"
        + f"<td>{first['career_experience']}</td>"
        + f"<td>{second['career_experience']}</td></tr>"
    )
    # Names and ages should always show up first
    context_data = [names, ages]
    # Randomize the order of the other two elements
    randomized_context_data = randomize_context_items([pexp, cexp])
    html_content = (
        "<table><tbody><tr><th></th><th>Candidate 1"
        + "</th><th>Candidate 2</th></tr>"
        + "".join(context_data + randomized_context_data)
        + "</tbody></table>"
    )
    context = {
        "arm_id": first["arm_id"],
        "context": input,
        "html_content": html_content
    }
    return context
    