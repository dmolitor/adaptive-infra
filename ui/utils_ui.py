import requests as req
from shiny import Session, ui
from urllib.parse import urlparse, parse_qs
from utils_db import api_url

"""
This script defines utility functions for interacting with the user interface.
"""


class ResponseForm:
    """A class to collect all user-submitted data"""

    def __init__(self) -> "ResponseForm":
        self.consent: bool = None
        self.arm_id: int = None
        self.batch_id: int = None
        self.context_batch_id: int = None
        self.prolific_id: str | None = None
        self.in_usa: bool | None = None
        self.commitment: str | None = None
        self.captcha: str | None = None
        self.option_preference: int | None = None
        self.option_attention: int | None = None
        self.option_attention_truth: int | None = None
        self.age: int | None = None
        self.ethnicity: str | None = None
        self.race: str | None = None
        self.sex: str | None = None
        self.discriminated: bool | None = None
        self.garbage: bool = False

    def generate_form(self) -> dict:
        """Generate a dictionary containing user responses"""
        out = {
            "consent": self.consent,
            "arm_id": self.arm_id,
            "batch_id": self.batch_id,
            "context_batch_id": self.context_batch_id,
            "prolific_id": self.prolific_id,
            "in_usa": self.in_usa,
            "commitment": self.commitment,
            "captcha": self.captcha,
            "option_preference": self.option_preference,
            "option_attention": self.option_attention,
            "option_attention_truth": self.option_attention_truth,
            "age": self.age,
            "ethnicity": self.ethnicity,
            "race": self.race,
            "sex": self.sex,
            "discriminated": self.discriminated,
            "garbage": self.garbage,
        }
        return out

    def validate_data(self) -> None:
        # Indicator if the response is garbage or not
        garbage = False
        responses_req = req.get(api_url + "/responses")
        responses_req.raise_for_status()
        responses = responses_req.json()
        prolific_ids = [response["prolific_id"] for response in responses]
        # If a Prolific ID has already responded, mark as garbage
        if self.prolific_id in prolific_ids:
            garbage = True
        if not self.in_usa:
            garbage = True
        if self.commitment in ["no", "unsure"]:
            garbage = True
        if self.captcha.lower() != "purple":
            garbage = True
        if self.option_attention != self.option_attention_truth:
            garbage = True
        if isinstance(self.age, float) or isinstance(self.age, int):
            self.age = int(self.age)
        else:
            self.age = None
        self.garbage = garbage


def error(
    id: str,
    selector: str,
    message: str = "Please select exactly one option!",
    where: str = "afterEnd",
):
    """Inserts an error message after a user interface element"""
    ui.remove_ui(selector=f"#{id}")
    status = ui.help_text(
        ui.span({"style": "color:red; text-align: center;"}, message), id=id
    )
    ui.insert_ui(ui=status, selector=selector, where=where)


def error_clear(id: str | list[str]):
    """Removes all error messages from a user interface element"""
    if not isinstance(id, list):
        id = [id]
    for i in id:
        ui.remove_ui(selector=f"#{i}")


def empty_age(age: tuple[str]) -> bool:
    """Check if age is a non-empty result"""
    if age == ():
        return True
    return False


def get_prolific_id(session: Session) -> str | None:
    """Retrieves the current user's Prolific ID from the URL"""
    url = session.input[".clientdata_url_search"]()
    # Parse the URL
    parsed_url = urlparse(url)
    # Parse the query element of the URL into a dictionary
    query_dict = parse_qs(parsed_url.query)
    # 'Unbox' single item lists
    query_dict = {k: v[0] if len(v) == 1 else v for k, v in query_dict.items()}
    # Handle cases where there is no ID to parse in URL
    if query_dict == {}:
        return None
    # Get the Prolific ID
    prolific_id = query_dict.get("PROLIFIC_PID")
    if isinstance(prolific_id, str):
        prolific_id = prolific_id.replace("{{", "").replace("}}", "")
    else:
        return None
    return prolific_id


def validate_age(age: tuple[str]) -> bool:
    """Check if age is a non-empty result"""
    try:
        for a in age:
            int(a)
        return True
    except:
        return False


def validate_race(race: tuple[str]) -> bool:
    """Check if race is a non-empty result"""
    if race == ():
        return False
    else:
        for r in race:
            if not r.startswith("race_"):
                return False
        if len(race) > 1 and "race_skip" in race:
            return False
    return True


def which_is_older(context: dict) -> int:
    """Which of two candidates is older"""
    context = context["context"]
    candidate1 = context["first"]
    candidate2 = context["second"]
    if candidate1["age"] >= candidate2["age"]:
        return 0
    else:
        return 1


def which_is_college_ed(context: dict) -> int:
    context = context["context"]
    candidate1 = context["first"]
    candidate2 = context["second"]
    if candidate1["education"] == "College degree":
        return 0
    else:
        return 1


# Define small JS scripts to scroll to the top and bottom of a page and to
# redirect to an external URL

redirect_url = ui.tags.script(
    """
    Shiny.addCustomMessageHandler('redirect_url', function(message) {
        window.location = message;
    });
    """
)

scroll_bottom = ui.tags.script(
    """
    Shiny.addCustomMessageHandler('scroll_bottom', function(message) {
      setTimeout(() => {
        window.scrollTo(0, document.body.scrollHeight);
      }, 0);
    });
    """
)

scroll_top = ui.tags.script(
    """
    Shiny.addCustomMessageHandler('scroll_top', function(message) {
      window.scrollTo(0, 0);
    });
    """
)
