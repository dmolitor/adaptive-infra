import json
from randomize import draw_arms
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, select
from tables import Bandit, Batch, Metadata, NoConsent, Parameters, Pi, Response
from typing import List

"""
This script provides utility function for the API to interact with the
Postgres db.
"""


def create_tables(engine: Engine):
    """Creates the tables specified in `tables.py` in the Postgres db"""
    SQLModel.metadata.create_all(engine)


def deactivate_batch(batch_id: int, engine: Engine):
    """Deactivate a currently active batch"""
    with Session(engine) as session:
        batch_obj = session.exec(select(Batch).where(Batch.id == batch_id)).one()
        batch_obj.active = False
        session.add(batch_obj)
        session.commit()


def decrement_batch(batch_id: int, active: bool, engine: Engine):
    """Decrement the `remaining` parameter of a given batch"""
    with Session(engine) as session:
        batch_obj = session.exec(select(Batch).where(Batch.id == batch_id)).one()
        batch_obj.remaining = batch_obj.remaining - 1
        batch_obj.active = active
        session.add(batch_obj)
        session.commit()


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


def generate_batch(
    labels: List[str],
    remaining: int,
    active: bool,
    pi: dict,
    params: dict,
    engine: None | Engine,
):
    """
    Initialize our Bandit pi (% of sims each arm is max discriminatory) table
    as well as the batch table.

    `params` should be a dictionary as described above in `generate_parameters`

    E.g.
    labels = ["arm1", "arm2", "arm3", "arm4"]
    """
    # Generate new row in the `Batch` table
    with Session(engine) as session:
        batch_obj = Batch(remaining=remaining, active=active)
        session.add(batch_obj)
        session.commit()
        batch_id = batch_obj.id
    # Generate new values in the `Parameters` table
    generate_parameters(labels=labels, batch_id=batch_id, params=params, engine=engine)
    # Generate new values in the `Pi` table
    generate_pi(labels=labels, batch_id=batch_id, pi=pi, engine=engine)
    return batch_obj


def generate_bandit_metadata(labels: List[str], meta: dict, engine: None | Engine):
    """
    Initialize our Bandit metadata table
    """
    with Session(engine) as session:
        for label in labels:
            # Get the corresponding Bandit arm
            arm: Bandit = session.exec(
                select(Bandit).where(Bandit.label == label)
            ).one()
            arm_meta = meta[label]
            ## TODO: This entire part could be abstracted to create
            ## Metadata table from an arbitrarty set of metadata
            prior_trips = arm_meta["prior_trips"]
            education = arm_meta["education"]
            reason = arm_meta["reason"]
            origin = arm_meta["origin"]
            profession = arm_meta["profession"]
            for trips, ed, reason, origin, prof in zip(
                prior_trips, education, reason, origin, profession
            ):
                metadata_obj = Metadata(
                    arm_id=arm.id,
                    prior_trips=trips,
                    education=ed,
                    reason=reason,
                    origin=origin,
                    profession=prof,
                )
                session.add(metadata_obj)
                session.commit()


def generate_no_consent(batch_id: int, consent: bool, engine: Engine):
    """Generate a row in the NoConsent database table"""
    with Session(engine) as session:
        no_consent_obj = NoConsent(batch_id=batch_id, consent=consent)
        session.add(no_consent_obj)
        session.commit()


def generate_parameters(
    labels: List[str], batch_id: int, params: dict, engine: None | Engine
):
    """
    Initialize our Bandit parameters table

    `params` is a dictionary with keys equal to `labels` and the values
    being a dictionary containing "alpha" and "beta" values parameterizing
    the beta distribution in each arm. E.g.
    ```
    params: {
        "arm1": {"alpha": 1, "beta": 1},
        "arm2": {"alpha": 1, "beta": 1},
        "arm3": {"alpha": 1, "beta": 1},
        "arm4": {"alpha": 1, "beta": 1}
    }
    ```
    """
    with Session(engine) as session:
        for label in labels:
            # Get the corresponding Bandit arm
            arm: Bandit = session.exec(
                select(Bandit).where(Bandit.label == label)
            ).one()
            arm_params = params[label]
            print(f"{label}: {arm_params}")
            ## TODO: Is there a way to make this distribution agnostic.
            ## E.g. we could switch from Bernoulli with beta prior to
            ## a Gaussian with a Gaussian prior and the code stays the same?
            param_obj = Parameters(
                arm_id=arm.id,
                batch_id=batch_id,
                alpha=arm_params["alpha"],
                beta=arm_params["beta"],
            )
            session.add(param_obj)
            session.commit()


def generate_pi(labels: List[str], batch_id: int, pi: dict, engine: None | Engine):
    """
    Initialize our Bandit Pi table

    `pi` should be a dictionary where the keys are the `labels`, and the values
    are floats indicating the % of realizations drawn from the posterior
    distribution of each arm that the corresponding arm is the max/min
    discriminatory context.

    E.g.
    pi = {"arm1": 0.25, "arm2": 0.5, "arm3": 0.75, "arm4": 1}
    """
    # Generate new values in the `Pi` table
    with Session(engine) as session:
        for label in labels:
            # Get the corresponding Bandit arm
            arm: Bandit = session.exec(
                select(Bandit).where(Bandit.label == label)
            ).one()
            # Get corresponding pi value
            arm_pi = pi[label]
            pi_obj = Pi(batch_id=batch_id, arm_id=arm.id, pi=arm_pi)
            session.add(pi_obj)
            session.commit()


def generate_response(
    consent: bool,
    arm_id: int,
    batch_id: int,
    context_batch_id: int,
    prolific_id: str | None,
    in_usa: bool | None,
    commitment: str | None,
    captcha: str | None,
    option_preference: int | None,
    option_attention: int | None,
    option_attention_truth: int | None,
    age: int | None,
    race: str | None,
    ethnicity: str | None,
    sex: str | None,
    discriminated: bool | None,
    garbage: bool,
    engine: None | Engine,
):
    """Add a user's responses (filled out survey form) to the database"""
    with Session(engine) as session:
        response_obj = Response(
            consent=consent,
            arm_id=arm_id,
            batch_id=batch_id,
            context_batch_id=context_batch_id,
            prolific_id=prolific_id,
            in_usa=in_usa,
            commitment=commitment,
            captcha=captcha,
            option_preference=option_preference,
            option_attention=option_attention,
            option_attention_truth=option_attention_truth,
            age=age,
            race=race,
            ethnicity=ethnicity,
            sex=sex,
            discriminated=discriminated,
            garbage=garbage,
        )
        session.add(response_obj)
        session.commit()
    return True


def get_bandit(engine) -> List[Bandit]:
    """Retrieve a list of all bandit arms"""
    with Session(engine) as session:
        bandit = session.exec(select(Bandit)).all()
    return bandit


def get_batch(batch_id: int, engine: Engine):
    """Retrieve a specific Batch"""
    with Session(engine) as session:
        batch = session.exec(select(Batch).where(Batch.id == batch_id)).one()
    return batch


def get_batches(engine):
    """Retrieve a list of all batch values"""
    with Session(engine) as session:
        batches = session.exec(select(Batch)).all()
    return batches


def get_current_batch(engine: Engine, deactivate: bool = False):
    """Get the batch id for the current batch"""
    with Session(engine) as session:
        batches = session.exec(
            select(Batch).where(Batch.remaining > 0).where(Batch.active == True)
        ).all()
        # If batch is greater than 1 then there are multiple active batches.
        # If deactivated == True, all batches that are not the most recent
        # (the one with the highest value for its id) should be deactivated.
        current_batch: Batch = max(batches, key=lambda x: x.id)
        if len(batches) > 1 and deactivate:
            ids = [batch.id for batch in batches]
            for id in ids:
                if id != current_batch.id:
                    deactivate_batch(batch_id=id, engine=engine)
    return current_batch


def get_metadata(engine):
    """Retrieve a list of all metadata items"""
    with Session(engine) as session:
        metadata = session.exec(select(Metadata)).all()
    return metadata


def get_no_consent(engine: Engine):
    """Retrieves all records from the NoConsent table"""
    with Session(engine) as session:
        noconsent = session.exec(select(NoConsent)).all()
    return noconsent


def get_parameters(engine: Engine):
    """Retrieve a list of all bandit arm parameters"""
    with Session(engine) as session:
        params = session.exec(select(Parameters)).all()
    return params


def get_pi(engine):
    """Retrieve a list of all pi values"""
    with Session(engine) as session:
        pi = session.exec(select(Pi)).all()
    return pi


def get_pi_batch(batch_id: int, engine):
    """Retrieve pi values for a specific batch"""
    with Session(engine) as session:
        pi = session.exec(select(Pi).where(Pi.batch_id == batch_id)).all()
    return pi


def get_responses(engine: None | Engine):
    """Retrieve a list of all responses"""
    with Session(engine) as session:
        responses = session.exec(select(Response)).all()
    return responses


def get_response_n(engine, filter: bool = False):
    """Retrieve the number of responses"""
    with Session(engine) as session:
        if filter:
            responses = session.exec(
                select(Response).where(Response.garbage is not True)
            ).all()
        else:
            responses = get_responses(engine)
        return len(responses)


def increment_batch(
    batch_id: int, remaining: int, active: bool, maximum: bool, engine: None | Engine
):
    bandit = get_bandit(engine=engine)
    # For each arm, collect successes and failures
    labels = []
    params = {}
    for arm in bandit:
        arm_label = arm.label
        # Construct the labels for each arm
        labels.append(arm_label)
        # Construct updated alpha and beta parameters for each arm
        with Session(engine) as session:
            arm_params = session.exec(
                select(Parameters)
                .where(Parameters.arm_id == arm.id)
                .where(Parameters.batch_id == batch_id)
            ).one()
            arm_batch_responses = session.exec(
                select(Response)
                .where(Response.arm_id == arm.id)
                .where(Response.batch_id == batch_id)
                .where(Response.garbage != True)
            ).all()
            successes = 0
            failures = 0
            ## TODO: related to the above. Is there a way to update the
            ## posterior distribution in a distribution-agnostic way?
            for response in arm_batch_responses:
                if response.discriminated is True:
                    successes += 1
                elif response.discriminated is False:
                    failures += 1
            params[arm_label] = {
                "alpha": arm_params.alpha + successes,
                "beta": arm_params.beta + failures,
            }
    # Construct updated Pi value for each arm
    pi = draw_arms(params, max=maximum)
    print(f"Batch: {batch_id}\n{json.dumps(pi, indent=4)}")
    # Now update the `Batch`, `Parameters` and `Pi` tables
    new_batch = generate_batch(
        labels=labels,
        remaining=remaining,
        active=active,
        pi=pi,
        params=params,
        engine=engine,
    )
    return new_batch


def is_duplicate_id(prolific_id: str, engine: Engine) -> bool:
    """Checks if a prolific ID has already submitted a response"""
    with Session(engine) as session:
        resp_obj = session.exec(
            select(Response).where(Response.prolific_id == prolific_id)
        ).all()
        if len(resp_obj) > 0:
            return True
        else:
            return False
