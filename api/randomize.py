import random
from sqlalchemy import Engine
from sqlmodel import Session, select
from tables import Bandit
from typing import List

# do we want to seed this or allow that as an option?

def randomize_choice_order() -> List[int]:
    """Randomize whether the older candidate is shown first"""
    age_orders = [[0,1],[-1,0]]
    print(random.sample([0, 1], 1))
    return age_orders[random.sample([0, 1], 1)]

def randomize_context(engine: Engine) -> int:
    """Randomize which bandit arm is shown to the user"""
    with Session(engine) as session:
        bandit = session.exec(select(Bandit)).all()
        arm_ids = [arm.id for arm in bandit]
        arm_labels = [arm.label for arm in bandit]
    return target_arm

def randomize_context_items(input: List[str]) -> List[str]:
    """Randomize which order context characteristics are shown"""
    rand = random.sample(input, len(input))
    return rand

## `randomize` and `html_format` together form `main.py/randomize_context`
## which returns all the context-relevant data, randomized on all three levels
## - Randomize order in which candidates are shown
## - Randomize which bandit context (arm) is shown
## - Randomize the order in which context characteristics are shown
def randomize(engine: Engine) -> dict:
    """Randomize choice order and bandit arm. Return candidates as a dict"""
    choice_order = randomize_choice_order()
    target_arm = randomize_context(engine)
    with Session(engine) as session:
        bandit = (
            session
            .exec(select(Bandit).where(Bandit.id == target_arm))
            .one()
        )
        bandit_meta = bandit.meta
        first = bandit_meta[choice_order[0]].model_dump()
        second = bandit_meta[choice_order[1]].model_dump()
        out = {"first": first, "second": second}
        return out

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
    