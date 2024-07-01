from connect import engine
from db import (
    decrement_batch,
    generate_bandit,
    generate_bandit_metadata,
    generate_batch,
    generate_no_consent,
    generate_response,
    get_bandit,
    get_batch,
    get_batches,
    get_current_batch,
    get_metadata,
    get_no_consent,
    get_parameters,
    get_pi,
    get_pi_batch,
    get_responses,
    get_response_n,
    increment_batch,
    is_duplicate_id,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from randomize import html_format, randomize
from response_models import BanditJSON, BatchJSON, NoConsentJSON, ResponseJSON

"""
This script creates the API and defines all the available endpoints.
The code for each endpoint calls the functions in `/api/db.py`. These
functions do the actual grunt work. So to understand what happens for each
endpoint, look at the corresponding functions in `db.py`.
"""

# Create the API
api = FastAPI()

# Configure CORS
origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Base endpoint to check if it's alive.
@api.get("/")
def root():
    return "Welcome to our adaptive experiment!"


# Endpoints for working with responses ------------------------------------


# Endpoint to retrieve all the responses
@api.get("/responses")
def responses():
    responses = get_responses(engine)
    return responses


# Endpoint to retrieve all records from the NoConsent table
@api.get("/responses/noconsent")
def no_consent():
    noconsent = get_no_consent(engine)
    return noconsent


# Endpoint to send response data to
@api.post("/responses")
def response_gen(response: ResponseJSON):
    generate_response(
        consent=response.consent,
        arm_id=response.arm_id,
        batch_id=response.batch_id,
        context_batch_id=response.context_batch_id,
        prolific_id=response.prolific_id,
        in_usa=response.in_usa,
        commitment=response.commitment,
        captcha=response.captcha,
        option_preference=response.option_preference,
        option_attention=response.option_attention,
        option_attention_truth=response.option_attention_truth,
        age=response.age,
        race=response.race,
        ethnicity=response.ethnicity,
        sex=response.sex,
        discriminated=response.discriminated,
        garbage=response.garbage,
        engine=engine,
    )
    return True


# Endpoint to get the number of responses
@api.get("/responses/n")
def response_n(filter: bool = False):
    n = get_response_n(engine, filter)
    return n


# Endpoint to send responses with no consent to
@api.post("/responses/noconsent")
def no_consent_gen(response: NoConsentJSON):
    generate_no_consent(
        batch_id=response.batch_id, consent=response.consent, engine=engine
    )
    return True


# Endpoint for checking if user has already submitted response
@api.post("/responses/duplicated")
def is_duplicate(prolific_id: str):
    return is_duplicate_id(prolific_id, engine)


# Endpoints for working with the Bandit table -----------------------------


# Endpoint to retrieve the Bandit table
@api.get("/bandit")
def bandit():
    bandit = get_bandit(engine)
    return bandit


# Endpoint to add the Bandit table
@api.post("/bandit")
def bandit_gen(bandit: BanditJSON):
    bandit_labels = bandit.labels
    bandit_params = bandit.params
    bandit_meta = bandit.meta
    bandit_pi = bandit.pi
    bandit_batch = bandit.batch
    # This generates a Bandit instance with as many arms as provided
    generate_bandit(labels=bandit_labels, engine=engine)
    # This generates the metadata table with metadata for each bandit arm
    generate_bandit_metadata(labels=bandit_labels, meta=bandit_meta, engine=engine)
    # Generate the `Batch`, `Parameters`, and `Pi` tables
    generate_batch(
        labels=bandit_labels,
        remaining=bandit_batch["remaining"],
        active=bandit_batch["active"],
        pi=bandit_pi,
        params=bandit_params,
        engine=engine,
    )
    return True


# Endpoints for working with the Parameters table -------------------------


# Endpoint to retrieve the parameters
@api.get("/bandit/parameters")
def bandit_parameters():
    params = get_parameters(engine)
    return params


# Endpoints for working with the Metadata table ---------------------------


# Endpoint to retrieve the metadata
@api.get("/bandit/metadata")
def bandit_metadata():
    metadata = get_metadata(engine)
    return metadata


# Endpoints for working with the Pi table ---------------------------------


# Endpoint to retrieve the Pi table
@api.get("/bandit/pi")
def bandit_pi():
    pi = get_pi(engine)
    return pi


# Endpoint to retrieve Pi values for a specific batch
@api.get("/bandit/pi/batch")
def bandit_pi_batch(batch_id: str):
    pi = get_pi_batch(batch_id, engine)
    return pi


# Endpoints for working with Batches --------------------------------------


# Endpoint to retrieve the Batch table
@api.get("/bandit/batch")
def bandit_batches(batch_id: int | None = None):
    if batch_id is not None:
        batch = get_batch(batch_id, engine)
    else:
        batch = get_batches(engine)
    return batch


# Endpoint to get the current Batch object
@api.get("/bandit/batch/current")
def cur_batch(deactivate: bool = False):
    batch = get_current_batch(engine, deactivate)
    return batch


# Endpoint to get randomized content for within-context comparison
@api.get("/randomize")
def randomize_context(batch_id: int):
    context_data = randomize(batch_id=batch_id, engine=engine)
    html_formatted_context = html_format(context_data)
    return html_formatted_context


# Endpoint to increment the Batch (including Parameters and Pi)
@api.post("/bandit/batch")
def increment_bandit_batch(batch: BatchJSON):
    batch_id = batch.batch_id
    batch_remaining = batch.remaining
    batch_active = batch.active
    batch_max = batch.maximum
    new_batch = increment_batch(
        batch_id, batch_remaining, batch_active, maximum=batch_max, engine=engine
    )
    return new_batch


# Endpoint to decrement the `remaining` parameter of a batch
@api.post("/bandit/batch/decrement")
def decrement_batch_id(batch_id: int, active: bool = True):
    decrement_batch(batch_id, active, engine)
    return True
