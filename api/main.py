from connect import engine, url
from db import (
    create_tables,
    generate_choices,
    generate_response,
    get_choice,
    get_choices,
    get_responses,
    failure,
    success,
    top_expected_value,
    top_parameter,
    update_choice,
    update_params,
)
from fastapi import FastAPI
from tables import ChoiceUpdate, ChoicesJSON, ResponseJSON

"""
This script creates the API and defines the endpoints to access.
"""

# Create the API
api = FastAPI()


# Base endpoint to check if it's alive.
@api.get("/")
def root():
    return None


# Endpoint to retrieve all the responses
@api.get("/responses")
def responses():
    responses = get_responses(engine)
    return responses


# Endpoint to send response data to
@api.post("/responses")
def response_gen(response: ResponseJSON):
    generate_response(choice=response.choice, engine=engine)
    return True


# Endpoint to retrieve all the items
@api.get("/choices")
def choices():
    choices = get_choices(engine)
    return choices


# Endpoint to retrieve a specific item
@api.get("/choices/{choice}")
def choice(choice: str):
    choice_obj = get_choice(choice=choice, engine=engine)
    return choice_obj


# Endpoint to update a specific item
@api.patch("/choices/{choice}")
def choice_update(choice: str, choice_update: ChoiceUpdate):
    update_choice(choice=choice, choice_update=choice_update, engine=engine)
    return True


# Endpoint to add choices
@api.post("/choices")
def choice_gen(choices: ChoicesJSON):
    generate_choices(
        choices=choices.choices,
        distribution=choices.distribution,
        params=choices.params,
        engine=engine,
    )
    return True


# Endpoint to update the parameters for all items
@api.post("/choices/parameters")
def choice_parameters():
    update_params(engine=engine)
    return True


# Endpoint to get the top n items by parameter expected value
@api.get("/choices/top/mean/")
def choice_top_mean(n: int | None = None):
    if n is None:
        n = 1
    choices = top_expected_value(engine=engine, n=n)
    return choices


# Endpoint to get the top n items by paramter value
@api.get("/choices/top/param/")
def choice_top_param(n: int | None = None):
    if n is None:
        n = 1
    choices = top_parameter(engine=engine, n=n)
    return choices


# Endpoint to increment an item's `successes` field by 1
@api.post("/choices/{choice}/success")
def choice_success(choice: str):
    success(choice=choice, engine=engine)
    return True


# Endpoint to increment an item's `failures` field by 1
@api.post("/choices/{choice}/failure")
def choice_failure(choice: str):
    failure(choice=choice, engine=engine)
    return True
