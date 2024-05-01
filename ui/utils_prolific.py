import os
import requests as req

PROLIFIC_API_TOKEN = os.environ["PROLIFIC_TOKEN"]
PROLIFIC_COMPLETION_INVALID = os.environ["PROLIFIC_COMPLETION_INVALID"]
PROLIFIC_COMPLETION_NOCONSENT = os.environ["PROLIFIC_COMPLETION_NOCONSENT"]
PROLIFIC_COMPLETION_VALID = os.environ["PROLIFIC_COMPLETION_VALID"]
PROLIFIC_STUDY_ID = os.environ["PROLIFIC_STUDY_ID"]
base_url = "https://api.prolific.com/api/v1/"

def pause_prolific_study() -> None:
    print(f"Pausing study {PROLIFIC_STUDY_ID}")
    resp = req.post(
        url=base_url + f"studies/{PROLIFIC_STUDY_ID}/transition/",
        json={"action": "PAUSE"},
        headers={"Authorization": "Token " + PROLIFIC_API_TOKEN}
    )
    resp.raise_for_status()

def prolific_redirect(case):
    base_url = "https://app.prolific.com/submissions/complete?cc="
    if case == "valid":
        url = base_url + PROLIFIC_COMPLETION_VALID
    elif case == "invalid":
        url = base_url + PROLIFIC_COMPLETION_INVALID
    elif case == "noconsent":
        url = base_url + PROLIFIC_COMPLETION_NOCONSENT
    return url