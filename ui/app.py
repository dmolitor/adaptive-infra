from pathlib import Path
from shiny import App, Inputs, Outputs, Session, reactive, ui
import shinyswatch
from ui_survey import survey_ui
from ui_intro import intro_ui
from ui_no_consent import no_consent_ui
from ui_outro import outro_ui
from ui_consent import screening_questions
from ui_postsurvey import postsurvey_ui, attention_ui
from utils import error, error_clear, get_prolific_id

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
        attention_ui,
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
        # Grab consent value
        consent = input.consent()
        # Clear all errors (there may be none; that's fine)
        error_clear(id="consent_status")
        # If neither button is selected, don't let user proceed
        if consent not in ["consent_agree", "consent_disagree"]:
            error(
                id="consent_status",
                selector="#consent",
                message="This field is required",
                where="beforeEnd"
            )
        # If they consent, proceed
        elif consent == "consent_agree":
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
        # Otherwise, bring them to the exit page
        else:
            ui.update_navs("hidden_tabs", selected="panel_no_consent")
    
    # Logic for 'Next Page' on the consent page
    @reactive.Effect
    @reactive.event(input.next_page_survey)
    def _():
        # Grab the following values: captcha, prolific_id, location, commitment
        captcha = input.captcha()
        prolific_id = input.prolific_id()
        location = input.location()
        commitment = input.commitment()
        # Are we ready to proceed?
        proceed = True
        # Clear all errors (there may be none; that's fine)
        error_clear(
            id=["captcha_status",
                "prolific_id_status",
                "location_status",
                "commitment_status"]
        )
        # Ensure prolific ID has been entered
        if prolific_id == "" or prolific_id is None:
            error(
                id="prolific_id_status",
                selector="#prolific_id",
                message="* This field is required"
            )
            proceed = False
        # Ensure location has been entered
        if location not in ["0", "1"]:
            error(
                id="location_status",
                selector="#location",
                message="* This field is required",
                where="beforeEnd"
            )
            proceed = False
        # Ensure commitment has been entered
        if commitment not in ["0", "1", "2"]:
            error(
                id="commitment_status",
                selector="#commitment",
                message="* This field is required",
                where="beforeEnd"
            )
            proceed = False
        # Ensure captcha value is entered
        if captcha == "" or captcha is None:
            error(
                id="captcha_status",
                selector="#captcha",
                message="* This field is required"
            )
            proceed = False
        if proceed:
            ui.update_navs("hidden_tabs", selected="panel_survey")
    
    # Logic for 'Next Page' on the primary survey page
    @reactive.Effect
    @reactive.event(input.next_page_attention)
    def _():
        # Grab the following values: candidate
        candidate = input.candidate()
        # Clear all errors (there may be none; that's fine)
        error_clear(id="candidate_status")
        # Ensure candidate choice has been selected
        if candidate not in ["0", "1"]:
            error(
                id="candidate_status",
                selector="#candidate",
                message="* This field is required",
                where="beforeEnd"
            )
        else:
            ui.update_navs("hidden_tabs", selected="panel_attention")

    @reactive.Effect
    @reactive.event(input.next_page_postsurvey)
    def _():
        ui.update_navs("hidden_tabs", selected="panel_postsurvey")

    @reactive.Effect
    @reactive.event(input.next_page_end)
    def _():
        ui.update_navs("hidden_tabs", selected="panel_outro")

# Runs the app. Intakes the UI and the server logic from above.
# `static_assets` ensures that all `ui.img` calls can reference image
# filepaths.
app = App(app_ui, server, static_assets=str(cur_dir.parent / "assets"))
