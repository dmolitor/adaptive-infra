from init_db import context
from pathlib import Path
from shiny import ui

"""
This script lays out the UI for the cartoon comparison page. It also does a
bit of data prep via the API to ensure the database is storing essential data.
"""

# Set file paths relative to ui_cartoons.py instead of being absolute
cur_dir = Path(__file__).resolve().parent

# UI for the survey questions
survey_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: justify;"},
                ui.HTML(
                    "Imagine you are voting in a primary contest for "
                    + "governor. You will be asked to choose between two "
                    + "candidates, who are both of the party you prefer."
                )
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    # Survey tables
    ui.row(
        ui.column(3),
        # Make the two cartoons be clickable image buttons
            ui.column(
                6,
                ui.div(
                    ui.HTML(context["html_content"]),
                ),
            ),
        ui.column(3),
    ),
    # Add select boxes below the survey tables
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.input_radio_buttons(
                id="candidate",
                label="Which of these two candidates do you prefer?",
                choices={0: "Candidate 1", 1: "Candidate 2"},
                selected="",
                width="100%"
            )
        ),
        ui.column(3),
    ),
    # 'Next' button for navigating through the survey
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.div(
                {"style": "text-align: right;"},
                ui.input_action_button("next_page_attention", "Next page \u27A4"),
            )
        ),
        ui.column(3)
    ),
    value="panel_survey"
)
