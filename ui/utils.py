from shiny import Session, ui
from urllib.parse import urlparse, parse_qs

def error(
        id: str,
        selector: str,
        message: str = "Please select exactly one option!",
        where: str = "afterEnd"
    ):
    ui.remove_ui(selector=f"#{id}")
    status = ui.help_text(
        ui.span(
            {"style": "color:red; text-align: center;"},
            message
        ),
        id=id
    )
    ui.insert_ui(ui=status, selector=selector, where=where)

def error_clear(id: str | list[str]):
    if not isinstance(id, list):
        id = [id]
    for i in id:
        ui.remove_ui(selector=f"#{i}")

def get_prolific_id(session: Session) -> str | None:
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
    prolific_id = (
        query_dict
        .get("PROLIFIC_PID")
        .replace("{{", "")
        .replace("}}", "")
    )
    return prolific_id

scroll_top = ui.tags.script(
    """
    Shiny.addCustomMessageHandler('scroll_top', function(message) {
      window.scrollTo(0, 0);
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

def validate_age(age: tuple[str]) -> bool:
    if age == ():
        return False
    return True

def validate_race(race: tuple[str]) -> bool:
    if race == ():
        return False
    else:
        for r in race:
            if not r.startswith("race_"):
                return False
        if len(race) > 1 and "race_skip" in race:
            return False
    return True
