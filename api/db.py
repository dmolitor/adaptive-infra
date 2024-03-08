from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, select
from tables import Bandit, Metadata, Parameters, Response 
from typing import List

"""
This script provides utility function for the API to interact with the
Postgres db.
"""

def create_tables(engine: Engine):
    """Creates the tables specified in `tables.py` in the Postgres db"""
    SQLModel.metadata.create_all(engine)

def generate_bandit(labels: List[str], engine: None | Engine):
    """
    Initialize our Bandit table
    """
    with Session(engine) as session:
        for label in labels:
            arm = Bandit(label=label)
            session.add(arm)
            session.commit()
        session.commit()

def generate_bandit_metadata(
    labels: List[str],
    meta: dict,
    engine: None | Engine
):
    """
    Initialize our Bandit metadata table
    """
    with Session(engine) as session:
        for label in labels:
            # Get the corresponding Bandit arm
            arm: Bandit = (
                session
                .exec(
                    select(Bandit).where(Bandit.label == label)
                )
                .one()
            )
            arm_meta = meta[label]
            names = arm_meta["names"]
            ages = arm_meta["ages"]
            pexps = arm_meta["political_exp"]
            cexps = arm_meta["career_exp"]
            for name, age, pexp, cexp in zip(names, ages, pexps, cexps):
                metadata_obj = Metadata(
                    arm_id=arm.id,
                    name=name,
                    age=age,
                    political_experience=pexp,
                    career_experience=cexp
                )
                session.add(metadata_obj)
                session.commit()
        # TODO: Is this last session.commit really necessary???
        session.commit()

def get_bandit(engine):
    """Retrieve a list of all bandit arms"""
    with Session(engine) as session:
        bandit = session.exec(select(Bandit)).all()
        out = list()
        for arm in bandit:
            out.append({
                "arm": arm,
                "parameters": arm.parameters,
                "metadata": arm.meta
            })
    return out

def get_metadata(engine):
    """Retrieve a list of all metadata items"""
    with Session(engine) as session:
        metadata = session.exec(select(Metadata)).all()
    return metadata

def generate_parameters(
    labels: List[str],
    params: dict,
    engine: None | Engine
):
    """
    Initialize our Bandit parameters table
    """
    with Session(engine) as session:
        for label in labels:
            # Get the corresponding Bandit arm
            arm: Bandit = (
                session
                .exec(
                    select(Bandit).where(Bandit.label == label)
                )
                .one()
            )
            param_obj = Parameters(
                arm_id=arm.id,
                alpha = params["alpha"],
                beta = params["beta"]
            )
            session.add(param_obj)
            session.commit()
        session.commit()

def get_parameters(engine):
    """Retrieve a list of all bandit arm parameters"""
    with Session(engine) as session:
        params = session.exec(select(Parameters)).all()
    return params

def generate_response(
    consent: bool,
    prolific_id: str | None,
    in_usa: bool | None,
    commitment: str | None,
    captcha: str | None,
    candidate_preference: int | None,
    candidate_older: int | None,
    candidate_older_truth: int | None,
    age: int | None,
    race: str | None,
    ethnicity: str | None,
    sex: str | None,
    discriminated: bool | None,
    engine: None | Engine
):
    """Add a user's responses (filled out survey form) to the database"""
    with Session(engine) as session:
        response_obj = Response(
            consent=consent,
            prolific_id=prolific_id,
            in_usa=in_usa,
            commitment=commitment,
            captcha=captcha,
            candidate_preference=candidate_preference,
            candidate_older=candidate_older,
            candidate_older_truth=candidate_older_truth,
            age=age,
            race=race,
            ethnicity=ethnicity,
            sex=sex,
            discriminated=discriminated
        )
        session.add(response_obj)
        session.commit()
    return True

def get_responses(engine: None | Engine):
    """Retrieve a list of all responses"""
    with Session(engine) as session:
        responses = session.exec(select(Response)).all()
    return responses

def update_params(arm_id: int, params: dict, engine: Engine):
    """
    Update the Beta-Bernoulli distribution parameters for a specific bandit arm
    """
    with Session(engine) as session:
        param_obj = Parameters(
            arm_id=arm_id,
            alpha=params["alpha"],
            beta=params["beta"]
        )
        session.add(param_obj)
        session.commit()
    return True

def increment(
    arm_id: int,
    engine: Engine,
    alpha: bool = False,
    beta: bool = False
):
    """
    Increment the Beta-Bernoulli distribution params for a specific bandit arm
    """
    with Session(engine) as session:
        params = (
            session
            .exec(
                select(Parameters).where(Parameters.arm_id == arm_id)
            )
            .all()
        )
        last_param = max(params, key=lambda x: x.id)
        new_alpha = last_param.alpha
        new_beta = last_param.beta
        if alpha:
            new_alpha += 1
        if beta:
            new_beta += 1
        update_params(arm_id, {"alpha": new_alpha, "beta": new_beta}, engine)