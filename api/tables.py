from enum import Enum
from numpy.random import Generator, PCG64
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, col, select
from sqlalchemy import Engine

## TODO: Trying to figure out how to generate probabilities as part of the Choice class
## See line 28!!
# Distribution class for specifying the distribution of each

generator = Generator(PCG64())

class Family(Enum):
    beta = generator.beta
    binomial = generator.binomial
    normal = generator.normal
    poisson = generator.poisson

# Classes for FastAPI and SQLModel

# JSON Choices object
class ChoicesJSON(BaseModel):
    choices: List[str]
    distribution: str
    params: dict

# JSON Response object
class ResponseJSON(BaseModel):
    choice: str

# SQL Choices table
class Choice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str
    distribution: str ## TODO: put stuff here!!!
    parameter: float
    successes: int | None = 0
    failures: int | None = 0
    responses: List["Response"] = Relationship(back_populates="choice")

# SQLModel for updating choices
class ChoiceUpdate(SQLModel):
    item: Optional[str] = None
    parameter: Optional[float] = None
    successes: Optional[int] = None
    failures: Optional[int] = None

# SQL Responses table
class Response(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # choice: str
    # TODO: Add in Choices table
    choice_id: int = Field(foreign_key="choice.id")
    choice: Choice = Relationship(back_populates="responses")

# Functions for the API to work with database objects

def create_tables(engine):
    # Create tables in Postgres
    SQLModel.metadata.create_all(engine)

def generate_choices(
        choices: List[str],
        distribution: str,
        params: dict,
        engine: None | Engine
    ):
    with Session(engine) as session:
        for choice in choices:
            param = Family[distribution.lower()].value(**params).item()
            choice_obj = Choice(
                item=choice,
                distribution=distribution,
                parameter=param
            )
            session.add(choice_obj)
            session.commit()
        session.commit()

def generate_response(choice: str, engine: None | Engine):
    with Session(engine) as session:
        choice_obj = session.exec(select(Choice).where(Choice.item == choice))
        # choice_id = choice_obj.one().id
        response_obj = Response(choice=choice_obj.one())
        session.add(response_obj)
        session.commit()
    return True

def get_responses(engine: None | Engine):
    with Session(engine) as session:
        responses = session.exec(select(Response)).all()
        out = list()
        for response in responses:
            out.append({"response": response, "choice": response.choice})
    return out

def update_choice(choice: str, choice_update: ChoiceUpdate, engine: Engine):
    with Session(engine) as session:
        choice_obj = session.exec(select(Choice).where(Choice.item == choice))
        choice_obj = choice_obj.one()
        choice_data = choice_update.model_dump(exclude_unset=True)
        for key, value in choice_data.items():
            setattr(choice_obj, key, value)
        session.add(choice_obj)
        session.commit()
        # session.refresh(choice_obj)

def get_choice(choice: str, engine: Engine) -> Choice:
    with Session(engine) as session:
        choice = session.exec(select(Choice).where(Choice.item == choice)).one()
    return choice

def get_choices(engine):
    with Session(engine) as session:
        choices = session.exec(select(Choice)).all()
        out = list()
        for choice in choices:
            out.append({"choice": choice, "responses": choice.responses})
    return out

def success(choice: str, engine: Engine):
    with Session(engine) as session:
        choice_obj = get_choice(choice=choice, engine=engine)
        choice_obj.successes += 1
        session.add(choice_obj)
        session.commit()

def failure(choice: str, engine: Engine):
    with Session(engine) as session:
        choice_obj = get_choice(choice=choice, engine=engine)
        choice_obj.failures += 1
        session.add(choice_obj)
        session.commit()

def update_params(engine: Engine):
    with Session(engine) as session:
        choices = session.exec(select(Choice)).all()
        for choice in choices:
            successes = choice.successes + 1 # Add one because starting prior is Beta(1, 1)
            failures = choice.failures + 1
            params = {"a": successes, "b": failures, "size": 1}
            param = Family[choice.distribution.lower()].value(**params).item()
            choice.parameter = param
            session.add(choice)
            session.commit()

def get_choice_params(engine: Engine):
    with Session(engine) as session:
        out = dict()
        choices = session.exec(select(Choice)).all()
        for choice in choices:
            out[choice.item] = {
                "parameter": choice.parameter,
                "successes": choice.successes,
                "failures": choice.failures
            }
        return out

def top_expected_value(engine: Engine, n: int = 1):
    params = get_choice_params(engine)
    params = {
        k: {
            "mean": (
                (params[k]["successes"] + 1)
                / (params[k]["successes"] + params[k]["failures"] + 2)
            ),
            "successes": params[k]["successes"],
            "failures": params[k]["failures"]
        } for k in params.keys()
    }
    params_sorted = dict(
        sorted(params.items(), key=lambda x: x[1]["mean"], reverse=True)
    )
    selected_items = dict(list(params_sorted.items())[:n])
    return selected_items

def top_parameter(engine: Engine, n: int = 1):
    params = get_choice_params(engine)
    params = {k: v["parameter"] for k, v in params.items()}
    params_sorted = dict(
        sorted(params.items(), key=lambda x: x[1], reverse=True)
    )
    selected_items = dict(list(params_sorted.items())[:n])
    return selected_items
