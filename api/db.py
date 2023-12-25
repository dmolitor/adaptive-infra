from enum import Enum
from numpy.random import Generator, PCG64
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, select
from tables import Choice, ChoiceUpdate, Response
from typing import List

"""
This script provides utility function for the API to interact with the
Postgres db.
"""

# Create an enumeration of distribution functions to draw random samples from.
generator = Generator(PCG64())


class Family(Enum):
    """
    This will be useful when initializing choices in the database. Each choice
    will have a corresponding parameter distribution and will grab its
    distribution function from this enum when we need to generate a random
    value from its PDF.
    """

    beta = generator.beta
    # The ones below are not used right now
    binomial = generator.binomial
    normal = generator.normal
    poisson = generator.poisson


def create_tables(engine):
    """Creates the tables specified in `tables.py` in the Postgres db"""
    SQLModel.metadata.create_all(engine)


def failure(choice: str, engine: Engine):
    """
    Update an item in a specific way. Increment the number of `successes` by 1
    """
    with Session(engine) as session:
        choice_obj = get_choice(choice=choice, engine=engine)
        choice_obj.failures += 1
        session.add(choice_obj)
        session.commit()


def generate_choices(
    choices: List[str], distribution: str, params: dict, engine: None | Engine
):
    """
    Initialize our universe of choices in the database
    along with their corresponding parameter distributions and initial
    random draws from their PDFs.
    """
    with Session(engine) as session:
        for choice in choices:
            param = Family[distribution.lower()].value(**params).item()
            choice_obj = Choice(item=choice, distribution=distribution, parameter=param)
            session.add(choice_obj)
            session.commit()
        session.commit()


def get_choice(choice: str, engine: Engine) -> Choice:
    """Retrieve a specific item (specified by its name) from the database"""
    with Session(engine) as session:
        choice = session.exec(select(Choice).where(Choice.item == choice)).one()
    return choice


def get_choices(engine):
    """Retrieve a list of all items and corresponding responses"""
    with Session(engine) as session:
        choices = session.exec(select(Choice)).all()
        out = list()
        for choice in choices:
            out.append({"choice": choice, "responses": choice.responses})
    return out


def get_choice_params(engine: Engine):
    """
    Return a dictionary. The keys are the names of each item and the values
    are another dictionary containing each item's number of successes,
    failures, and currect parameter estimates.
    """
    with Session(engine) as session:
        out = dict()
        choices = session.exec(select(Choice)).all()
        for choice in choices:
            out[choice.item] = {
                "parameter": choice.parameter,
                "successes": choice.successes,
                "failures": choice.failures,
            }
        return out


def generate_response(choice: str, engine: None | Engine):
    """Add a user's response (what item they picked) to the database"""
    with Session(engine) as session:
        choice_obj = session.exec(select(Choice).where(Choice.item == choice))
        response_obj = Response(choice=choice_obj.one())
        session.add(response_obj)
        session.commit()
    return True


def get_responses(engine: None | Engine):
    """Retrieve a list of all responses and corresponding choices"""
    with Session(engine) as session:
        responses = session.exec(select(Response)).all()
        out = list()
        for response in responses:
            out.append({"response": response, "choice": response.choice})
    return out


def success(choice: str, engine: Engine):
    """
    Update an item in a specific way. Increment the number of `successes` by 1
    """
    with Session(engine) as session:
        choice_obj = get_choice(choice=choice, engine=engine)
        choice_obj.successes += 1
        session.add(choice_obj)
        session.commit()


def top_expected_value(engine: Engine, n: int = 1):
    """
    Return a dictionary. The keys are the names of each item and the values
    are another dictionary containing each item's number of successes,
    failures, and currect parameter expected values. The dictionary is
    sorted in decreasing order by the magnitude of the expected value
    and the top `n` are selected.
    """
    params = get_choice_params(engine)
    params = {
        k: {
            "mean": (
                (params[k]["successes"] + 1)
                / (params[k]["successes"] + params[k]["failures"] + 2)
            ),
            "successes": params[k]["successes"],
            "failures": params[k]["failures"],
        }
        for k in params.keys()
    }
    params_sorted = dict(
        sorted(params.items(), key=lambda x: x[1]["mean"], reverse=True)
    )
    selected_items = dict(list(params_sorted.items())[:n])
    return selected_items


def top_parameter(engine: Engine, n: int = 1):
    """
    Return a dictionary. The keys are the names of each item and the values
    are each item's current parameter estimate. The dictionary is
    sorted in decreasing order by the magnitude of the parameter estimate
    and the top `n` are selected.
    """
    params = get_choice_params(engine)
    params = {k: v["parameter"] for k, v in params.items()}
    params_sorted = dict(sorted(params.items(), key=lambda x: x[1], reverse=True))
    selected_items = dict(list(params_sorted.items())[:n])
    return selected_items


def update_choice(choice: str, choice_update: ChoiceUpdate, engine: Engine):
    """
    Pick a specific item from the database and
    update specific features of that item. See `ChoiceUpdate` to see what
    fields can get updated
    """
    with Session(engine) as session:
        choice_obj = session.exec(select(Choice).where(Choice.item == choice))
        choice_obj = choice_obj.one()
        choice_data = choice_update.model_dump(exclude_unset=True)
        for key, value in choice_data.items():
            setattr(choice_obj, key, value)
        session.add(choice_obj)
        session.commit()


def update_params(engine: Engine):
    """
    Draw random values from each item's parameter distribution. This is
    specifically helpful for updating parameter estimates after an item's
    posterior distribution has been updated. For many items this will
    re-draw a value from its paramter PDF although it has not changed.
    """
    with Session(engine) as session:
        choices = session.exec(select(Choice)).all()
        for choice in choices:
            successes = (
                choice.successes + 1
            )  # Add one because starting prior is Beta(1, 1)
            failures = choice.failures + 1
            params = {"a": successes, "b": failures, "size": 1}
            param = Family[choice.distribution.lower()].value(**params).item()
            choice.parameter = param
            session.add(choice)
            session.commit()
