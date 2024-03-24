from pydantic import BaseModel
from typing import List

"""
This script creates response models for validating data submitted with FastAPI.
"""

class BatchJSON(BaseModel):
    """Validate Batch increments updated via the api"""
    batch_id: int
    remaining: int
    active: bool

class NoConsentJSON(BaseModel):
    """Validate responses with no consent"""
    batch_id: int
    consent: bool

class ResponseJSON(BaseModel):
    """
    A class for validating response data submitted via the API
    """
    consent: bool
    arm_id: int
    batch_id: int
    context_batch_id: int
    prolific_id: str | None
    in_usa: bool | None
    commitment: str | None
    captcha: str | None
    candidate_preference: int | None
    candidate_older: int | None
    candidate_older_truth: int | None
    age: int | None
    race: str | None
    ethnicity: str | None
    sex: str | None
    discriminated: bool | None
    garbage: bool

class ParametersJSON(BaseModel):
    """Validate Parameters data"""
    params: dict

class BanditJSON(ParametersJSON):
    """
    A class for validating Bandit data submitted via the API

    labels: A list of arm labels
    params: A dictionary of initial parameters for the distributions
        e.g. {'a': 1, 'b': 1} for a Beta(1, 1) prior distribution.
        See the Parameters class below. NOTE: We could initialize
        with different prior values for alpha and beta by changing
        params: dict to params: List[dict] and initializing the
        choice for each distinct arm.
    meta: A dictionary of metadata for each arm (context). This
        dictionary should follow the following format. Its keys should
        be exactly the `labels` above. Each value should be another
        dictionary containing the data for the candidates/job applicants
        to be compared within each context. E.g. as follows:
        ```
        "meta": {
            "arm1": {
                "names": ["Laurie Schmitt", "Allison O'Connell"],
                "ages": [49, 62],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "arm2": {
                "names": ["Laurie Schmitt", "Allison O'Connell"],
                "ages": [49, 62],
                "political_exp": ["No experience", "No experience"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "arm3": {
                "names": ["Tanisha Rivers", "Keisha Mosely"],
                "ages": [70, 26],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "arm4": {
                "names": ["Tanisha Rivers", "Keisha Mosely"],
                "ages": [49, 62],
                "political_exp": ["No experience", "No experience"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            }
        }
        ```
    pi: A dictionary of pi values (a fraction of the realizations) drawn
        from each arm indicating the percentage of indicating how
        frequently the corresponding arm was the max/min discriminatory
        context. E.g. as follows:
        ```
        "pi": {"arm1": 0.25, "arm2": 0.5, "arm3": 0.75, "arm4": 1}
        ```
    batch: A dictionary containing the initial batch values. E.g.:
        ```
        "batch": {"remaining": 1}
        ```
    """
    labels: List[str] | None
    meta: dict
    pi: dict
    batch: dict