from fastapi import FastAPI
from connect import engine, engine_url
from tables import (
    Choice,
    ChoiceUpdate,
    ChoicesJSON,
    Response,
    ResponseJSON,
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
    update_params
)
from typing import List

api = FastAPI()

@api.get("/")
def root():
    return None

@api.get("/responses")
def responses():
    responses = get_responses(engine)
    return responses

@api.post("/responses")
def response_gen(response: ResponseJSON):
    generate_response(choice=response.choice, engine=engine)
    return True

@api.get("/choices")
def choices():
    choices = get_choices(engine)
    return choices

@api.get("/choices/{choice}")
def choice(choice: str):
    choice_obj = get_choice(choice=choice, engine=engine)
    return choice_obj

@api.patch("/choices/{choice}")
def choice_update(choice: str, choice_update: ChoiceUpdate):
    update_choice(choice=choice, choice_update=choice_update, engine=engine)
    return True

@api.post("/choices")
def choice_gen(choices: ChoicesJSON):
    generate_choices(
        choices=choices.choices,
        distribution=choices.distribution,
        params=choices.params,
        engine=engine
    )
    return True

@api.post("/choices/parameters")
def choice_parameters():
    update_params(engine=engine)
    return True

@api.get("/choices/top/mean/")
def choice_top_mean(n: int | None = None):
    if n is None:
        n = 1
    choices = top_expected_value(engine=engine, n=n)
    return choices

@api.get("/choices/top/param/")
def choice_top_param(n: int | None = None):
    if n is None:
        n = 1
    choices = top_parameter(engine=engine, n=n)
    return choices

@api.post("/choices/{choice}/success")
def choice_success(choice: str):
    choice_obj = success(choice=choice, engine=engine)
    return True

@api.post("/choices/{choice}/failure")
def choice_failure(choice: str):
    choice_obj = failure(choice=choice, engine=engine)
    return True
