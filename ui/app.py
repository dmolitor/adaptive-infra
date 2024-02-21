from api import add_response, failure, success, top_param, update_parameters
from pathlib import Path
from shiny import App, reactive, ui
import shinyswatch
from ui_survey import survey_ui, selected
from ui_intro import intro_ui
from ui_outro import outro_ui
from ui_pages import screening_questions

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
    Path(__file__).parent / "table-styles.css"
)

# This chunk lays out the design of the whole app
app_ui = ui.page_fluid(
    shinyswatch.theme.simplex(),
    ui.br(),
    ui.panel_title(ui.img(src="cornell-reduced-red.svg", height="45px")),
    ui.navset_hidden(
        # Intro Page
        intro_ui,
        # Cartoon Display
        survey_ui,
        screening_questions,
        # Goodbye Page
        outro_ui,
        id="hidden_tabs",
    ),
)


def server(input, output, session):
    """This function handles all the logic for the app"""

    # Logic for 'Submit' button
    @reactive.Effect
    @reactive.event(input.submit)
    def _():
        # These values indicate which of the two options were selected
        farside_sel_vals = [input.farside1_sel(), input.farside2_sel()]
        ui.remove_ui(selector="#submit_status")
        # If neither or both options were selected, don't let the user proceed
        if sum(farside_sel_vals) != 1:
            submit_status = ui.help_text(
                ui.span(
                    {"style": "color:red; text-align: center;"},
                    "Please select only one option!",
                ),
                id="submit_status",
            )
            ui.insert_ui(ui=submit_status, selector="#submit", where="afterEnd")
        # Otherwise proceed with the selected option
        else:
            # key1 and key2 are the two cartoons being compared
            key1 = selected[0]
            key2 = selected[1]
            # If the first cartoon was selected, update the success and failure
            if farside_sel_vals[0] is True:
                add_response(key1)
                success(key1)
                failure(key2)
            # Do the same if it was the second cartoon selected
            else:
                add_response(key2)
                success(key2)
                failure(key1)
            # Now that the response has been recorded, we can regenerate the
            # parameter for each cartoon. This means, for each cartoon,
            # generating a random draw from its posterior distribution.
            # Each cartoon's parameter (the probability a user will pick it)
            # is Beta distributed with \alpha = (number of successes + 1) and
            # \beta = (number of failures + 1).
            # NOTE: For each comparison, only two of the cartoons are selected.
            # For all the ones not selected, their parameter distribution is
            # not updated.
            update_parameters()
            # Once parameters are updated, usher the user to the outro page.
            ui.update_navs("hidden_tabs", selected="panel_outro")

    # @reactive.Effect
    # @reactive.event(input.consent)
    # def _():


    # Logic for the 'Get Started' button
    # name button something distinct to each ui element
    
    # create helper function that does all the steps (that's like next_page)
    @reactive.Effect
    @reactive.event(input.next_page_prolific_screening)
    def _():   
        # # Have the user select between the cartoons with the two highest random
        # # draws from their parameter distributions.
        selected = list(top_param(n=2).keys())
        # # Now that cartoons have been selected, switch to the comparison tab
        #ui.update_navs("hidden_tabs", selected="panel_cartoon")
        ui.update_navs("hidden_tabs", selected="panel_prolific_q")
        # Update the selection options with the new cartoons
        ui.update_action_button(
            id="farside1", label="", icon=ui.img(src=selected[0], height="500px")
        )
        ui.update_action_button(
            id="farside2", label="", icon=ui.img(src=selected[1], height="500px")
        )

    @reactive.Effect
    @reactive.event(input.next_page_survey)
    def _():   
        # # Now that cartoons have been selected, switch to the comparison tab
        ui.update_navs("hidden_tabs", selected="panel_survey")


    # Logic for selecting cartoon checkboxes
    @reactive.Effect
    @reactive.event(input.farside1)
    def _():
        """
        Ensure that clicking on the first image also updates the corresponding
        checkbox
        """
        # What is the current value of the first checkbox
        sel_value = input.farside1_sel()
        # We need to switch it from False to True or vice versa
        new_sel_value = not sel_value
        # Update the checkbox with the new value
        ui.update_checkbox(id="farside1_sel", label="", value=new_sel_value)

    @reactive.Effect
    @reactive.event(input.farside2)
    def _():
        """
        Ensure that clicking on the second image also updates the corresponding
        checkbox. Exactly the same as the function above!
        """
        sel_value = input.farside2_sel()
        new_sel_value = not sel_value
        ui.update_checkbox(id="farside2_sel", label="", value=new_sel_value)


# Runs the app. Intakes the UI and the server logic from above.
# `static_assets` ensures that all `ui.img` calls can reference image
# filepaths.
app = App(app_ui, server, static_assets=str(cur_dir.parent / "assets"))
