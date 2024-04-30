import os
import requests as req

PROLIFIC_API_TOKEN = os.environ["PROLIFIC_TOKEN"]
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