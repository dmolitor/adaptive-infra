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

# Initialize the bandit (all its arms and corresponding parameters)
bandit = {"labels": ["a", "b", "c", "d"], "params": {"alpha": 1, "beta": 1}}
req.post(api_url + "/bandit", json=bandit).raise_for_status()

def submit_response(form: dict):
    """Submit a filled-out survey form via the API"""
    url = api_url + "/responses"
    req.post(url, json=form).raise_for_status()
