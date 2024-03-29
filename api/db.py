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
    engine: None | Engine
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
    generate_parameters(
        labels=labels,
        batch_id=batch_id,
        params=params,
        engine=engine
    )
    # Generate new values in the `Pi` table
    generate_pi(labels=labels, batch_id=batch_id, pi=pi, engine=engine)

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

def generate_no_consent(batch_id: int, consent: bool, engine: Engine):
    """Generate a row in the NoConsent database table"""
    with Session(engine) as session:
        no_consent_obj = NoConsent(batch_id=batch_id, consent=consent)
        session.add(no_consent_obj)
        session.commit()

def generate_parameters(
    labels: List[str],
    batch_id: int,
    params: dict,
    engine: None | Engine
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
            arm: Bandit = (
                session
                .exec(
                    select(Bandit).where(Bandit.label == label)
                )
                .one()
            )
            arm_params = params[label]
            param_obj = Parameters(
                arm_id=arm.id,
                batch_id=batch_id,
                alpha = arm_params["alpha"],
                beta = arm_params["beta"]
            )
            session.add(param_obj)
            session.commit()
        session.commit()

def generate_pi(
    labels: List[str],
    batch_id: int,
    pi: dict,
    engine: None | Engine
):
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
            arm: Bandit = (
                session
                .exec(
                    select(Bandit).where(Bandit.label == label)
                )
                .one()
            )
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
    candidate_preference: int | None,
    candidate_older: int | None,
    candidate_older_truth: int | None,
    age: int | None,
    race: str | None,
    ethnicity: str | None,
    sex: str | None,
    discriminated: bool | None,
    garbage: bool,
    engine: None | Engine
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
            candidate_preference=candidate_preference,
            candidate_older=candidate_older,
            candidate_older_truth=candidate_older_truth,
            age=age,
            race=race,
            ethnicity=ethnicity,
            sex=sex,
            discriminated=discriminated,
            garbage=garbage
        )
        session.add(response_obj)
        session.commit()
    return True

def get_bandit(engine) -> List[Bandit]:
    """Retrieve a list of all bandit arms"""
    with Session(engine) as session:
        bandit = session.exec(select(Bandit)).all()
        out = list()
        for arm in bandit:
            out.append({
                "arm": arm,
                "parameters": arm.parameters,
                "metadata": arm.meta,
                "pi": arm.pi,
                "responses": arm.responses
            })
    return out

def get_batch(batch_id: int, engine: Engine):
    """Retrieve a specific Batch"""
    with Session(engine) as session:
        out = []
        batch = session.exec(select(Batch).where(Batch.id == batch_id)).one()
    return batch

def get_batches(engine):
    """Retrieve a list of all batch values"""
    with Session(engine) as session:
        out = []
        batch = session.exec(select(Batch)).all()
        for b in batch:
            out.append({"batch": b, "parameters": b.parameters, "pi": b.pi})
    return out

def get_current_batch(engine: Engine):
    """Get the batch id for the current batch"""
    with Session(engine) as session:
        batch = (
            session.exec(
                select(Batch)
                .where(Batch.remaining > 0)
                .where(Batch.active == True)
            )
            .one()
        )
    return batch

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
        out = []
        for param in params:
            out.append({"parameters": param, "batch": param.batch})
    return out

def get_pi(engine):
    """Retrieve a list of all pi values"""
    with Session(engine) as session:
        pi = session.exec(select(Pi)).all()
        out = []
        for p in pi:
            out.append({"pi": p, "batch": p.batch})
    return out

def get_responses(engine: None | Engine):
    """Retrieve a list of all responses"""
    with Session(engine) as session:
        responses = session.exec(select(Response)).all()
    return responses

def increment_batch(
    batch_id: int,
    remaining: int,
    active: bool,
    engine: None | Engine
):
    bandit = get_bandit(engine=engine)
    # For each arm, collect successes and failures
    labels = []
    params = {}
    for arm in bandit:
        arm = arm["arm"]
        arm_label = arm.label
        # Construct the labels for each arm
        labels.append(arm_label)
        # Construct updated alpha and beta parameters for each arm
        with Session(engine) as session:
            arm_params = (
                session.exec(
                    select(Parameters)
                    .where(Parameters.arm_id == arm.id)
                    .where(Parameters.batch_id == batch_id)
                )
                .one()
            )
            arm_batch_responses = (
                session.exec(
                    select(Response)
                    .where(Response.arm_id == arm.id)
                    .where(Response.batch_id == batch_id)
                    .where(Response.garbage != True)
                )
                .all()
            )
            successes = 0
            failures = 0
            for response in arm_batch_responses:
                if response.discriminated is True:
                    successes += 1
                elif response.discriminated is False:
                    failures += 1
            params[arm_label] = {
                "alpha": arm_params.alpha + successes,
                "beta": arm_params.beta + failures
            }
    # Construct updated Pi value for each arm
    pi = draw_arms(params)
    # Now update the `Batch`, `Parameters` and `Pi` tables
    generate_batch(
        labels=labels,
        remaining=remaining,
        active=active,
        pi=pi,
        params=params,
        engine=engine
    )