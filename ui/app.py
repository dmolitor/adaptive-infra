from pathlib import Path
from shiny import App, Inputs, Outputs, Session, reactive, ui
import shinyswatch
from ui_survey import survey_ui
from ui_intro import intro_ui
from ui_no_consent import no_consent_ui
from ui_outro import outro_ui
from ui_pages import screening_questions
from ui_postsurvey import postsurvey_ui
from utils import get_prolific_id

"""
This script lays out the UI and the logic for the majority of the front-facing
survey (Shiny app). To see the specific pages (e.g. the intro page, the cartoon
page, or the outro page) see `ui_intro.py`, `ui_cartoons.py`, or `ui_outro.py`,
respectively.
"""

# Set file paths relative to app.py instead of being absolute
cur_dir = Path(__file__).resolve().parent

# load css
ui.include_css(
    cur_dir / "table-styles.css"
)

# This chunk lays out the design of the whole app
app_ui = ui.page_fluid(
    # Bootswatch Simplex theme: browse themes here [https://bootswatch.com/]
    shinyswatch.theme.simplex(),
    ui.br(),
    # Cornell Logo on each page
    ui.panel_title(ui.img(src="cornell-reduced-red.svg", height="45px")),
    ui.navset_hidden(
        intro_ui,
        survey_ui,
        screening_questions,
        outro_ui,
        no_consent_ui,
        postsurvey_ui,
        id="hidden_tabs"
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    """This function handles all the logic for the app"""
    
    # Logic for 'Next Page' button on landing page
    @reactive.Effect
    @reactive.event(input.next_page_prolific_screening)
    def _():   
        # Get the consent value; either 'consent_agree' or 'consent_disagree'
        sel_value = input.consent()
        # If 'consent_agree' proceed with the survey
        if sel_value == "consent_agree":
            # Autofill the 'Prolific ID' text entry
            ui.update_text(
                id="prolific_id",
                label=(
                    "What is your Prolific ID? Please note that this response "
                    + "should auto-fill with the correct ID."
                ),
                value=get_prolific_id(session)
            )
            # Switch tabs to the Prolific questions tab
            ui.update_navs("hidden_tabs", selected="panel_prolific_q")
        # Otherwise, exit the interview
        else:
            ui.update_navs("hidden_tabs", selected="panel_no_consent")

    @reactive.Effect
    @reactive.event(input.next_page_survey)
    def _():
        ui.update_navs("hidden_tabs", selected="panel_survey")

    @reactive.Effect
    @reactive.event(input.next_page_postsurvey)
    def _():
        ui.update_navs("hidden_tabs", selected="panel_postsurvey")

# Runs the app. Intakes the UI and the server logic from above.
# `static_assets` ensures that all `ui.img` calls can reference image
# filepaths.
app = App(app_ui, server, static_assets=str(cur_dir.parent / "assets"))
