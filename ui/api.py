import requests as req
import os

env_vars = os.environ

ADAPTIVE_TESTING = env_vars.get("ADAPTIVE_TESTING")
# Get the outward facing port at which the API is exposed
API_HOST_PORT = env_vars["API_HOST_PORT"]

if ADAPTIVE_TESTING is not None and ADAPTIVE_TESTING:
    network = "localhost"
else:
    network = "api"

# Construct the url for querying the API
api_url = f"http://{network}:{API_HOST_PORT}"

"""
These are convenience functions for using the api. To see the underlying api
code, checkout `/api/main` and `/api/tables`.
"""


def add_response(choice: str):
    """User submits a selection. This response is recorded in the database"""
    req.post(api_url + "/responses", json={"choice": choice}).raise_for_status()


def add_choices(choices_json: dict):
    """Initialize the full set of choices from which the user can select"""
    req.post(api_url + "/choices", json=choices_json).raise_for_status()


def get_responses():
    """Retrieves all responses from the database"""
    request = req.get(api_url + "/responses")
    request.raise_for_status()
    return request.json()


def get_choices():
    """Retrieves the set of all choices from which the user can select"""
    request = req.get(api_url + "/choices")
    request.raise_for_status()
    return request.json()


def is_alive():
    """Check to see if the api is alive and accepting connections"""
    if req.get(api_url).status_code != 200:
        raise req.exceptions.Timeout("Failed to connect!")
    return True


def update_choice(choice: str, choice_update: dict):
    """Update some element(s) of one of the choices"""
    req.patch(api_url + f"/choices/{choice}", json=choice_update).raise_for_status()


def get_choice(choice: str):
    """Retrieve a choice and accompanying metadata"""
    request = req.get(api_url + "/choices/" + choice)
    request.raise_for_status()
    return request.json()


def success(choice: str):
    """Adds +1 to the choice.successes field of one of the choices"""
    req.post(api_url + "/choices/" + choice + "/success").raise_for_status()


def failure(choice: str):
    """Adds +1 to the choice.failures field of one of the choices"""
    req.post(api_url + "/choices/" + choice + "/failure").raise_for_status()


def update_parameters():
    """Generates a new random choice.parameter field for all the choices"""
    req.post(api_url + "/choices/parameters").raise_for_status()


def top_expected_values(n: int | None = None):
    """Calculates and extracts the top `n` choices with the highest mean"""
    if n is None:
        url = api_url + "/choices/top/mean/"
    else:
        url = api_url + "/choices/top/mean/?n=" + str(n)
    request = req.get(url)
    request.raise_for_status()
    return request.json()


def top_param(n: int | None = None):
    """Extracts the top `n` choices with the highest parameter (theta) draws"""
    if n is None:
        url = api_url + "/choices/top/param/"
    else:
        url = api_url + "/choices/top/param/?n=" + str(n)
    request = req.get(url)
    request.raise_for_status()
    return request.json()

def submit_response(form: dict):
    """Submit a filled-out survey form via the API"""
    url = api_url + "/responses"
    req.post(url, json=form).raise_for_status()
