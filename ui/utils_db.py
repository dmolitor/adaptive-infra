import requests as req
import os
import time
import traceback
from utils_prolific import pause_prolific_study

"""
This script defines utility functions for interacting with the database.
To see all the api endpoints utilized here, see `/api/main.py`.
"""

env_vars = os.environ

ADAPTIVE_TESTING = env_vars.get("ADAPTIVE_TESTING")
API_HOST_PORT = env_vars["API_HOST_PORT"]
STOPPAGE_THRESHOLD = float(env_vars["STOPPAGE_THRESHOLD"])
STUDY_MAX_N = float(env_vars["STUDY_MAX_N"])
WARMUP_N = float(env_vars["WARMUP_N"])

if ADAPTIVE_TESTING is not None and ADAPTIVE_TESTING:
    network = "localhost"
else:
    network = "api"

# Construct the url for querying the API
api_url = f"http://{network}:{API_HOST_PORT}"


def with_retry(f):
    """A decorator to retry API queries if they fail"""

    def wrapper(*args, **kwargs):
        iter = 0
        while iter < 10:
            try:
                result = f(*args, **kwargs)
                return result
            except Exception:
                time.sleep(0.1)
                iter += 1
                exception_message = traceback.format_exc()
        raise ConnectionError(exception_message)

    return wrapper


@with_retry
def current_batch(deactivate: bool = False):
    """Retrieves the current batch information"""
    current_batch_request = req.get(
        api_url + f"/bandit/batch/current/?deactivate={deactivate}"
    )
    current_batch_request.raise_for_status()
    current_batch = current_batch_request.json()
    return current_batch


@with_retry
def current_context(batch_id: int):
    """Retrieves (randomly) the context for the current user session"""
    context_request = req.get(api_url + f"/randomize?batch_id={batch_id}")
    context_request.raise_for_status()
    context = context_request.json()
    ## TODO: Remove this at some point (currently helpful for interactive use)
    print(f"context:\n{context}")
    return context


def current_pi():
    """Retrieves the current-batch individual pi values"""
    cur_batch = current_batch()
    resp = req.get(api_url + "/bandit/batch")
    resp.raise_for_status()
    [cur_params] = [x for x in resp.json() if x["batch"]["id"] == cur_batch["id"]]
    pi_vals = [x["pi"] for x in cur_params["pi"]]
    for i in range(len(pi_vals) - 1, 0, -1):
        pi_vals[i] = pi_vals[i] - pi_vals[(i - 1)]
    return pi_vals


def decrement_batch_remaining(batch_id: int, active: bool = True):
    """Decrement the batch `remaining` parameter. Can also deactivate batch"""
    (
        req.post(
            api_url
            + f"/bandit/batch/decrement?batch_id={str(batch_id)}"
            + f"&active={active}"
        ).raise_for_status()
    )


def finished_warmup() -> True:
    if num_responses() > WARMUP_N:
        return True
    return False


@with_retry
def get_batch_id(batch_id: int):
    """Get specific batch"""
    batch_request = req.get(api_url + f"/bandit/batch?batch_id={str(batch_id)}")
    batch_request.raise_for_status()
    batch = batch_request.json()
    return batch


def increment_batch(
    batch_id: int, remaining: int, active: bool = True, maximum: bool = True
):
    """Ping the api to create a new batch in the Batch database table"""
    (
        req.post(
            api_url + "/bandit/batch",
            json={
                "batch_id": batch_id,
                "remaining": remaining,
                "active": active,
                "maximum": maximum,
            },
        ).raise_for_status()
    )


def initialize_bandit(bandit: dict) -> None:
    """Function to create the initial Bandit database table"""
    bandit_req = req.get(api_url + "/bandit")
    bandit_req.raise_for_status()
    if not bandit_req.json():
        req.post(api_url + "/bandit", json=bandit).raise_for_status()


@with_retry
def is_duplicate_id(prolific_id: str) -> bool:
    """Checks if user response already exists"""
    resp = req.post(api_url + f"/responses/duplicated?prolific_id={prolific_id}")
    resp.raise_for_status()
    return resp.json()

@with_retry
def num_responses() -> int:
    resp_request = req.get(api_url + "/responses")
    resp_request.raise_for_status()
    return len(resp_request.json())


def submit(
    response_form,
    batch_id: int | None,
    batch_size: int | None,
    maximum: bool | None,
    noconsent: bool = False,
) -> None:
    """
    Handles the logistics of submitting the response form. If the individual
    has already submitted a response, nothing happens. Otherwise, if the form is
    flagged as "noconsent" it will be submitted to the NoConsent table,
    otherwise it is stored in the Responses table.
    """
    duplicate_response = is_duplicate_id(response_form.prolific_id)
    # If the response is a duplicate we just want to do nothing.
    if duplicate_response:
        return None
    response_form.validate_data()
    response_form_data = response_form.generate_form()
    if noconsent:
        submit_response_noconsent(response_form_data)
    else:
        submit_response(response_form_data)
    # Update batches and corresponding parameters if the form is valid
    # and if we have ended the warm-up phase of receiving responses
    if not response_form.garbage and finished_warmup():
        update_batch(batch_id, batch_size, maximum=maximum)
    # If we have exceeded the max number of survey responses, pause the
    # Prolific study
    if num_responses() >= STUDY_MAX_N:
        print("Max number of respondents required; stopping Prolific study")
        pause_prolific_study()


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


def update_batch(batch_id: int, remaining: int, maximum: bool):
    """
    Decrement batch counter, and create new batch/pi/parameters as necessary.
    Also check if any arm exceeds the stoppage threshold. If so, pause the
    Prolific survey.
    """
    batch = get_batch_id(batch_id)
    ready_to_update = batch["remaining"] <= 1
    batch_is_active = batch["active"]
    if ready_to_update and batch_is_active:
        decrement_batch_remaining(batch["id"], active=False)
        increment_batch(batch["id"], remaining=remaining, maximum=maximum)
        # Check if any of the new arm pi values exceed stoppage threshold
        pi_vals = current_pi()
        print(f"Current pi vals: {pi_vals}")
        # If any pi values exceed stoppage threshold
        if any([x >= STOPPAGE_THRESHOLD for x in pi_vals]):
            pause_prolific_study()
    elif ready_to_update and not batch_is_active:
        decrement_batch_remaining(batch["id"], active=False)
    else:
        decrement_batch_remaining(batch["id"])
