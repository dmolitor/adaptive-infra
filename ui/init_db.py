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

# Initialize the bandit table if it does not already exist
if not req.get(api_url + "/bandit").json():
    # Initialize the bandit (all its arms and corresponding parameters)
    bandit = {
        "labels": ["arm1", "arm2", "arm3", "arm4"],
        "params": {"alpha": 1, "beta": 1},
        "meta": {
            "arm1": {
                "names": ["Joseph", "Daniel"],
                "ages": [70, 26],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "arm2": {
                "names": ["John", "David"],
                "ages": [67, 29],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "arm3": {
                "names": ["Timothy", "Paul"],
                "ages": [64, 32],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "arm4": {
                "names": ["Yi-Tser", "Robert"],
                "ages": [61, 35],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            }
        }
    }
    req.post(api_url + "/bandit", json=bandit).raise_for_status()

# Initialize the within-context comparison data
# Get randomized context comparison data
context_request = req.get(api_url + "/randomize")
context_request.raise_for_status()
context = context_request.json()

def submit_response(form: dict) -> None:
    """Submit a filled-out survey form via the API"""
    url = api_url + "/responses"
    req.post(url, json=form).raise_for_status()

def increment_params(
    arm_id: int,
    alpha: bool = False,
    beta: bool = False
) -> None:
    post = req.post(
        api_url
        + f"/bandit/parameters?arm_id={str(arm_id)}&alpha={alpha}&beta={beta}"
    )
    post.raise_for_status()
