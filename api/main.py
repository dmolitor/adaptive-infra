from connect import engine
from db import (
    generate_bandit,
    generate_bandit_metadata,
    generate_parameters,
    generate_response,
    get_bandit,
    get_metadata,
    get_parameters,
    get_responses,
    increment,
    update_params
)
from fastapi import FastAPI
from randomize import html_format, randomize
from tables import BanditJSON, ParametersJSON, ResponseJSON

"""
This script creates the API and defines the endpoints to access.
"""

# Create the API
api = FastAPI()

# Base endpoint to check if it's alive.
@api.get("/")
def root():
    return "Hello World!"

# Endpoint to retrieve all the responses
@api.get("/responses")
def responses():
    responses = get_responses(engine)
    return responses

# Endpoint to send response data to
@api.post("/responses")
def response_gen(response: ResponseJSON):
    generate_response(
        consent=response.consent,
        prolific_id=response.prolific_id,
        in_usa=response.in_usa,
        commitment=response.commitment,
        captcha=response.captcha,
        candidate_preference=response.candidate_preference,
        candidate_older=response.candidate_older,
        candidate_older_truth=response.candidate_older_truth,
        age=response.age,
        race=response.race,
        ethnicity=response.ethnicity,
        sex=response.sex,
        discriminated=response.discriminated,
        engine=engine
    )
    return True

# Endpoint to add Bandit
@api.post("/bandit")
def bandit_gen(bandit: BanditJSON):
    bandit_labels = bandit.labels
    bandit_params = bandit.params
    bandit_meta = bandit.meta
    # This generates a Bandit instance with as many arms as provided
    generate_bandit(labels=bandit_labels, engine=engine)
    # This initializes a table with Beta-Bernoulli parameters for each arm
    generate_parameters(
        labels=bandit_labels,
        params=bandit_params,
        engine=engine
    )
    # This generates the metadata table with metadata for each bandit arm
    generate_bandit_metadata(
        labels=bandit_labels,
        meta=bandit_meta,
        engine=engine
    )
    return True

# Endpoint to retrieve the Bandit
@api.get("/bandit")
def bandit():
    bandit = get_bandit(engine)
    return bandit

# Endpoint to retrieve the parameters
@api.get("/bandit/parameters")
def bandit_parameters():
    params = get_parameters(engine)
    return params

# Endpoint to retrieve the metadata
@api.get("/bandit/metadata")
def bandit_metadata():
    metadata = get_metadata(engine)
    return metadata

# Endpoint to update the parameters for a specific Bandit arm
@api.post("/bandit/parameters/{arm_id}")
def update_parameters(arm_id: int, params: ParametersJSON):
    new_params = params.params
    update_params(arm_id=arm_id, params=new_params, engine=engine)
    return True

# Endpoint to update the parameters for a specific Bandit arm
@api.post("/bandit/parameters")
def increment_parameters(arm_id: int, alpha: bool = False, beta: bool = False):
    increment(arm_id, engine, alpha, beta)
    return True

# Endpoint to get randomized content for within-context comparison
@api.get("/randomize")
def randomize_context():
    context_data = randomize(engine=engine)
    html_formatted_context = html_format(context_data)
    return html_formatted_context
