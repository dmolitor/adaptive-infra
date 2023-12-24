import requests as req

# Do this programatically (with env vars)
api_url = "http://api:80"

# Functions for retrieving and updating items in the database
def add_response(choice: str):
    req.post(api_url + "/responses", json={"choice": choice}).raise_for_status()

def add_choices(choices_json: dict):
    req.post(api_url + "/choices", json=choices_json).raise_for_status()

def get_responses():
    request = req.get(api_url + "/responses")
    request.raise_for_status()
    return request.json()

def get_choices():
    request = req.get(api_url + "/choices")
    request.raise_for_status()
    return request.json()

def is_alive():
    if req.get(api_url).status_code != 200:
        raise req.exceptions.Timeout("Failed to connect!")
    return True

def update_choice(choice: str, choice_update: dict):
    req.patch(api_url + f"/choices/{choice}", json=choice_update).raise_for_status()

def get_choice(choice: str):
    request = req.get(api_url + "/choices/" + choice)
    request.raise_for_status()
    return request.json()

def success(choice: str):
    req.post(api_url + "/choices/" + choice + "/success").raise_for_status()

def failure(choice: str):
    req.post(api_url + "/choices/" + choice + "/failure").raise_for_status()

def update_parameters():
    req.post(api_url + "/choices/parameters").raise_for_status()

def top_expected_values(n: int | None = None):
    if n is None:
        url = api_url + "/choices/top/mean/"
    else:
        url = api_url + "/choices/top/mean/?n=" + str(n)
    request = req.get(url)
    request.raise_for_status()
    return request.json()

def top_param(n: int | None = None):
    if n is None:
        url = api_url + "/choices/top/param/"
    else:
        url = api_url + "/choices/top/param/?n=" + str(n)
    request = req.get(url)
    request.raise_for_status()
    return request.json()
