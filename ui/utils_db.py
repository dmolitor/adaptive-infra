import requests as req
import os

"""
This script defines utility functions for interacting with the database.
To see all the api endpoints utilized here, see `/api/main.py`.
"""

env_vars = os.environ

ADAPTIVE_TESTING = env_vars.get("ADAPTIVE_TESTING")
# Get the outward facing port at which the API is exposed
API_HOST_PORT = 80 # env_vars["API_HOST_PORT"]

if ADAPTIVE_TESTING is not None and ADAPTIVE_TESTING:
    network = "localhost"
else:
    network = "api"

# Construct the url for querying the API
api_url = f"http://{network}:{API_HOST_PORT}"

def current_batch():
    """Retrieves the current batch information"""
    current_batch_request = req.get(api_url + "/bandit/batch/current/")
    current_batch_request.raise_for_status()
    current_batch = current_batch_request.json()
    return current_batch

def current_context(batch_id: int):
    """Retrieves (randomly) the context for the current user session"""
    context_request = req.get(api_url + f"/randomize?batch_id={batch_id}")
    context_request.raise_for_status()
    context = context_request.json()
    ## TODO: Remove this at some point (currently helpful for interactive use)
    print(f'context:\n{context}')
    return context

def decrement_batch_remaining(batch_id: int, active: bool = True):
    """Decrement the batch `remaining` parameter. Can also deactivate batch"""
    (
        req
        .post(
            api_url 
            + f"/bandit/batch/decrement?batch_id={str(batch_id)}"
            + f"&active={active}"
        )
        .raise_for_status()
    )

def get_batch_id(batch_id: int):
    """Get specific batch"""
    batch_request = req.get(
        api_url + f"/bandit/batch?batch_id={str(batch_id)}"
    )
    batch_request.raise_for_status()
    batch = batch_request.json()
    return batch

def increment_batch(batch_id: int, remaining: int, active: bool = True):
    """Ping the api to create a new batch in the Batch database table"""
    (
        req
        .post(
            api_url + "/bandit/batch",
            json={
                "batch_id": batch_id,
                "remaining": remaining,
                "active": active
            }
        )
        .raise_for_status()
    )

def initialize_bandit(bandit: dict) -> None:
    """Function to create the initial Bandit database table"""
    bandit_req = req.get(api_url + "/bandit")
    bandit_req.raise_for_status()
    if not bandit_req.json():
        req.post(api_url + "/bandit", json=bandit).raise_for_status()

def submit(
    response_form: dict,
    batch_id: int | None,
    batch_size: int | None,
    noconsent: bool = False
) -> None:
    """
    Handles the logistics of submitting the response form. If the form is
    flagged as "noconsent" it will be submitted to the NoConsent table,
    otherwise it is stored in the Responses table.
    """
    response_form.validate_data()
    response_form_data = response_form.generate_form()
    if noconsent:
        submit_response_noconsent(response_form_data)
    else:
        submit_response(response_form_data)
    # Update batches and corresponding parameters if appropriate
    if not response_form.garbage:
        update_batch(batch_id, batch_size)

def submit_response(form: dict) -> None:
    """Submit a filled-out survey form via the API"""
    url = api_url + "/responses"
    req.post(url, json=form).raise_for_status()

def submit_response_noconsent(form: dict) -> None:
    """Submit a survey form when consent is declined via the API"""
    url = api_url + "/responses/noconsent"
    resp_form = {}
    for key in ["batch_id", "consent"]:
        resp_form[key] = form[key]
    req.post(url, json=resp_form).raise_for_status()

def update_batch(batch_id: int, remaining: int):
    """
    Decrement batch counter, and create new batch/pi/parameters as necessary.
    """
    batch = get_batch_id(batch_id)
    ready_to_update = batch["remaining"] <= 1
    batch_is_active = batch["active"]
    if ready_to_update and batch_is_active:
        decrement_batch_remaining(batch["id"], active=False)
        increment_batch(batch["id"], remaining=remaining)
    elif ready_to_update and not batch_is_active:
        decrement_batch_remaining(batch["id"], active=False)
    else:
        decrement_batch_remaining(batch["id"])
