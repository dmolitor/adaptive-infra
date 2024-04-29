from init_db import BATCH_SIZE
from pathlib import Path
from shiny import App, Inputs, Outputs, Session, reactive, ui
import shinyswatch
import time
from ui_consent import screening_questions
from ui_demographics import demographics_ui
from ui_intro import intro_ui
from ui_no_consent import no_consent_ui
from ui_outro import outro_ui
from ui_postsurvey import attention_ui
from ui_survey import survey_ui
from utils_db import current_batch, current_context, submit
from utils_ui import (
    error,
    error_clear,
    get_prolific_id,
    scroll_bottom,
    scroll_top,
    validate_age,
    validate_race,
    which_is_older,
    ResponseForm
)

"""
This script lays out the UI and the logic for the majority of the front-facing
survey (Shiny app). To see the specific elements (e.g. the intro page, the
consent elements, the survey page, the demographics page, etc.) see the 
corresponding `ui_{element}.py` file, respectively.

This script also handles transferring user response data to the database as
well as indicating when to update survey batches and their corresponding
parameters
"""

# Set file paths relative to app.py instead of being absolute
cur_dir = Path(__file__).resolve().parent

# This chunk lays out the design of the whole app
app_ui = ui.page_fluid(
    # Bootswatch Simplex theme: browse themes here [https://bootswatch.com/]
    shinyswatch.theme.simplex(),
    # Import CSS styling
    ui.head_content(ui.include_css(cur_dir / "assets" / "table-styles.css")),
    # Add scripts to scroll to the top and bottom of the page
    scroll_top,
    scroll_bottom,
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
        demographics_ui,
        id="hidden_tabs"
    )
)

def server(input: Inputs, output: Outputs, session: Session):

    """This function handles all the logic for the app"""
    
    # Initialize the response form
    response_form = ResponseForm()

    # Logic for 'Next Page' button on landing page.
    # 
    # This function uses the async keyword because we want to call the 
    # Javascript 'scroll' script (defined above), that will scroll
    # to the top of the page. This requires us to 'await' the result, and
    # await can only be called in an async cur_context.
    @reactive.Effect
    @reactive.event(input.next_page_prolific_screening)
    async def _():
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
            await session.send_custom_message("scroll_bottom", "")
        # If they consent, proceed
        elif consent == "consent_agree":
            # Autofill the 'Prolific ID' text entry
            ui.update_text(
                id="prolific_id",
                label=ui.HTML(
                    "What is your Prolific ID? Please note that this response "
                    + "should auto-fill with the correct ID."
                ),
                value=get_prolific_id(session)
            )
            await session.send_custom_message("scroll_top", "")
            # Switch tabs to the Prolific questions tab
            ui.update_navs("hidden_tabs", selected="panel_prolific_q")
            # Update the response form
            response_form.consent = True
        # Otherwise, bring them to the exit page
        else:
            await session.send_custom_message("scroll_top", "")
            ui.update_navs("hidden_tabs", selected="panel_no_consent")
            # Update the response form
            response_form.consent = False
            # Submit the response form and handle batch/parameter updating
            # Get the current batch
            cur_batch = current_batch()
            response_form.batch_id = cur_batch["id"]
            submit(response_form, None, None, noconsent=True)
    
    # Logic for 'Next Page' on the consent page
    @reactive.Effect
    @reactive.event(input.next_page_dem)
    async def _():
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
            await session.send_custom_message("scroll_top", "")
            ui.update_navs("hidden_tabs", selected="panel_demographics")
            # Update the response form
            response_form.prolific_id = prolific_id
            if location == "1":
                response_form.in_usa = True
            else:
                response_form.in_usa = False
            if commitment == "1":
                response_form.commitment = "yes"
            elif commitment == "2":
                response_form.commitment = "unsure"
            else:
                response_form.commitment = "no"
            response_form.captcha = captcha
        else:
            await session.send_custom_message("scroll_bottom", "")
    
    @reactive.Effect
    @reactive.event(input.next_page_survey)
    async def _():
        # Grab user input values from the survey
        resp_age_text = input.resp_age_text()
        resp_age_check = input.resp_age_check()
        resp_race = input.resp_race()
        resp_ethnicity = input.resp_ethnicity()
        resp_sex = input.resp_sex()
        # Clear all errors (there may be none; that's fine)
        error_clear(
            id=["resp_age_status",
                "resp_race_status",
                "resp_ethnicity_status",
                "resp_sex_status"]
        )
        # Are we ready to proceed?
        proceed = True
        # Ensure one and only one age value is entered
        if resp_age_text == "" and not validate_age(resp_age_check):
            error(
                id="resp_age_status",
                selector="#resp_age_check",
                message="* This field is required",
                where="beforeEnd"
            )
            proceed = False
        elif resp_age_text != "" and validate_age(resp_age_check):
            error(
                id="resp_age_status",
                selector="#resp_age_check",
                message="* Invalid entry",
                where="beforeEnd"
            )
            proceed = False
        # Ensure valid race value(s) are selected
        if not validate_race(resp_race) and len(resp_race) > 1:
            error(
                id="resp_race_status",
                selector="#resp_race",
                message="* Invalid entry",
                where="beforeEnd"
            )
            proceed = False
        elif not validate_race(resp_race):
            error(
                id="resp_race_status",
                selector="#resp_race",
                message="* This field is required",
                where="beforeEnd"
            )
            proceed = False
        # Validate ethnicity entry
        if resp_ethnicity not in ["0", "1", "2"]:
            error(
                id="resp_ethnicity_status",
                selector="#resp_ethnicity",
                message="* This field is required",
                where="beforeEnd"
            )
            proceed = False
        # Validate sex entry
        if resp_sex not in ["0", "1", "2"]:
            error(
                id="resp_sex_status",
                selector="#resp_sex",
                message="* This field is required",
                where="beforeEnd"
            )
            proceed = False
        if proceed:
            await session.send_custom_message("scroll_top", "")
            # Retrieve the current context and dynamically generate the
            # survey tables. See `/ui/ui_survey.py`!
            
            # Catch any errors at this step
            iter = 0
            success = False
            while iter < 5 and not success:
                try:
                    cur_batch = current_batch()
                    cur_context = current_context(cur_batch["id"])
                    success = True
                except:
                    time.sleep(0.1)
                    cur_batch = current_batch()
                    cur_context = current_context(cur_batch["id"])
                    iter += 1
            if not success:
                raise ConnectionError("API query failed after 5 retries")

            ui.insert_ui(
                ui.HTML(cur_context["html_content"]),
                selector="#candidates",
                where="afterBegin"
            )
            ui.update_navs("hidden_tabs", selected="panel_survey")
            # Update the response form
            response_form.arm_id = cur_context["arm_id"]
            response_form.context_batch_id = cur_batch["id"]
            older_candidate = which_is_older(cur_context)
            response_form.candidate_older_truth = older_candidate
            if resp_age_text != "":
                response_form.age = int(resp_age_text)
            if "race_skip" not in resp_race:
                if len(resp_race) == 1:
                    response_form.race = resp_race[0]
                else:
                    response_form.race = ", ".join(resp_race)
            if resp_ethnicity == "0":
                response_form.ethnicity = "hisp_latin_spanish_no"
            elif resp_ethnicity == "1":
                response_form.ethnicity = "hisp_latin_spanish_yes"
            if resp_sex == "0":
                response_form.sex = "female"
            elif resp_sex == "1":
                response_form.sex = "male"
        else:
            await session.send_custom_message("scroll_bottom", "")
    
    # Logic for 'Next Page' on the primary survey page
    @reactive.Effect
    @reactive.event(input.next_page_attention)
    async def _():
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
            await session.send_custom_message("scroll_bottom", "")
        else:
            await session.send_custom_message("scroll_top", "")
            ui.update_navs("hidden_tabs", selected="panel_attention")
            # Update the response form
            response_form.candidate_preference = int(candidate)
            older_candidate = response_form.candidate_older_truth
            if response_form.candidate_preference == older_candidate:
                response_form.discriminated = False
            else:
                response_form.discriminated = True

    @reactive.Effect
    @reactive.event(input.next_page_outro)
    async def _():
        # Grab the following values: attention
        attention = input.attention()
        # Clear all errors (there may be none; that's fine)
        error_clear(id="attention_status")
        # Ensure candidate choice has been selected
        if attention not in ["0", "1", "2"]:
            error(
                id="attention_status",
                selector="#attention",
                message="* This field is required",
                where="beforeEnd"
            )
            await session.send_custom_message("scroll_bottom", "")
        else:
            await session.send_custom_message("scroll_top", "")
            ui.update_navs("hidden_tabs", selected="panel_outro")
            # Update the response form
            response_form.candidate_older = int(attention)
            # Ensure user is rolled into the current active batch
            cur_batch = current_batch()
            response_form.batch_id = cur_batch["id"]
            # Submit the response form and handle batch/parameter updating
            submit(response_form, response_form.batch_id, BATCH_SIZE)

# Runs the app. Intakes the UI and the server logic from above.
# `static_assets` ensures that all `ui.img` calls can reference image
# filepaths.
app = App(app_ui, server, static_assets=str(cur_dir / "assets"))
