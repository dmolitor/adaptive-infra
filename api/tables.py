from pydantic import BaseModel
from typing import List
from sqlmodel import Field, Relationship, SQLModel

"""
This script creates data validation models for the API and constructs
tables to insert and work with the data in the Postgres db.
"""

class ParametersJSON(BaseModel):
    """Validate parameters updated via the api"""
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
            "a": {
                "names": ["Laurie Schmitt", "Allison O'Connell"],
                "ages": [49, 62],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "b": {
                "names": ["Laurie Schmitt", "Allison O'Connell"],
                "ages": [49, 62],
                "political_exp": ["No experience", "No experience"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "c": {
                "names": ["Tanisha Rivers", "Keisha Mosely"],
                "ages": [70, 26],
                "political_exp": ["Member of Congress", "State legislator"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            },
            "d": {
                "names": ["Tanisha Rivers", "Keisha Mosely"],
                "ages": [49, 62],
                "political_exp": ["No experience", "No experience"],
                "career_exp": ["Restaurant owner", "Small business owner"]
            }
        }
        ```
    """
    labels: List[str] | None
    meta: dict

class Bandit(SQLModel, table=True):
    """
    A class for creating and working with the `bandit` table in Postgres.

    id: A unique ID (auto-generated by SQLModel)
    label: The label of the bandit arm (same as `ResponseJSON.choice`)
    parameters: A list of the arm's Bernoulli (p) param's Beta params over time
    """
    id: int | None = Field(default=None, primary_key=True)
    label: str
    parameters: List["Parameters"] = Relationship(back_populates="arm")
    meta: List["Metadata"] = Relationship(back_populates="arm")

class Metadata(SQLModel, table=True):
    """
    A class for representing all the metadata that goes along with
    each Bandit arm (aka context).
    """
    id: int | None = Field(default=None, primary_key=True)
    arm_id: int = Field(foreign_key="bandit.id")
    name: str
    age: int
    political_experience: str
    career_experience: str
    arm: Bandit = Relationship(back_populates="meta")

class Parameters(SQLModel, table=True):
    """
    A class for working with the `parameters` table in Postgres.
    Each arm is a Bernoulli distribution indexed by parameter theta.
    Theta is assumed to be Beta distributed indexed by parameters alpha
    and beta. For each user submission we will store the current posterior
    parameter values for each arm's theta.

    id: A unique ID (auto-generated)
    arm_id: The corresponding bandit arm the parameters correspond to
    alpha: The corresponding arm's alpha parameter value
    beta: The corresponding arm's beta parameter value
    """
    id: int | None = Field(default=None, primary_key=True)
    arm_id: int = Field(foreign_key="bandit.id")
    alpha: int = 1
    beta: int = 1
    arm: Bandit = Relationship(back_populates="parameters")

## TODO: Try to de-duplicate the code between Response and ResponseJSON

class Response(SQLModel, table=True):
    """
    A class for creating and working with the `response` table in Postgres.

    id: A unique user ID (auto-generated by SQLModel)
    consent: Does the user consent to the study
    prolific_id: User's prolific ID
    in_usa: Are they located in the U.S.?
    commitment: Do they commit to providing thoughful answers?
    captcha: Verifying they are a real person
    candidate_preference: Which candidate they prefer
    candidate_older: Attention check; which candidate is older?
    age: Demographics
    race: Demographics
    ethnicity: Demographics
    sex: Demographics
    """
    id: int | None = Field(default=None, primary_key=True)
    consent: bool
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

class ResponseJSON(BaseModel):
    """
    A class for validating response data submitted via the API
    """
    consent: bool
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