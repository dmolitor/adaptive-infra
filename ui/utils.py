from shiny import Session
from urllib.parse import urlparse, parse_qs

def get_prolific_id(session: Session) -> str | None:
    url = session.input[".clientdata_url_search"]()
    # Parse the URL
    parsed_url = urlparse(url)
    # Parse the query element of the URL into a dictionary
    query_dict = parse_qs(parsed_url.query)
    # 'Unbox' single item lists
    query_dict = {k: v[0] if len(v) == 1 else v for k, v in query_dict.items()}
    # Get the Prolific ID
    prolific_id = query_dict.get("prolific_id")
    return prolific_id
