from api import add_choices, get_choices, top_param
import os
from pathlib import Path
from shiny import ui
from htmltools import head_content

"""
This script lays out the UI for the cartoon comparison page. It also does a
bit of data prep via the API to ensure the database is storing essential data.
"""

# Set file paths relative to ui_cartoons.py instead of being absolute
cur_dir = Path(__file__).resolve().parent

# Get a list of all the potential options (cartoons) the user will pick from
items = [file for file in os.listdir(str(cur_dir / "img")) if file != ".DS_Store"]

# Add choices to the database if choices don't exist in there yet
if not get_choices():
    choices_json = {
        "choices": items,
        "distribution": "beta",
        "params": {"a": 1, "b": 1, "size": 1},
    }
    add_choices(choices_json)

# Grab the two cartoons with the top randomly generated parameter values.
# All the cartoon parameters start with an uninformative prior Beta(1, 1)
selected = list(top_param(n=2).keys())

# UI for the survey questions
survey_ui = ui.nav_panel(
    ui.head_content(ui.include_css("table-styles.css")),
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
                  ui.HTML('Imagine you are voting in a primary contest for governor. You will be asked to choose between two candidates, who are both of the party you prefer.'),
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
                    ui.HTML("<table><tbody><tr><th></th><th>Candidate 1</th><th>Candidate 2</th></tr><tr><td>Name</td><td>First Name</td><td>First Name<br></td></tr><tr><td>Ages</td><td>Age 1<br></td><td>Age 2<br></td></tr><tr><td>Political experience</td><td>Pol Experience 1</td><td>Pol Experience 2</td></tr><tr><td>Career experience</td><td>Career 1</td><td>Career 2</td></tr></tbody></table><br>Which of these two candidates do you prefer?<br>"),
                ),
            ),
        ui.column(3),
    ),
    # Add select boxes below the survey tables
    ui.row(
        ui.column(3),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"}, ui.input_checkbox("farside1_sel", "Candidate 1")
            ),
        ),
        ui.column(2),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"}, ui.input_checkbox("farside2_sel", "Candidate 2")
            ),
        ),
        ui.column(3),
    ),
    # 'Next' button for navigating through the survey
    ui.row(
        ui.column(5),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("next_page_attention", "Next page", width="100%"),
            ),
        ),
        ui.column(5),
    ),
    value="panel_survey",
)
