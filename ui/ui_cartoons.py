from api import add_choices, get_choices, top_param
import os
from pathlib import Path
from shiny import ui

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

# UI for the cartoon selection page
cartoons_ui = ui.nav_panel(
    None,
    # Cartoons (as clickable buttons)
    ui.row(
        ui.column(2),
        # Make the two cartoons be clickable image buttons
        ui.column(
            4,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button(
                    "farside1", "", icon=ui.img(src=selected[0], height="500px")
                ),
            ),
        ),
        ui.column(
            4,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button(
                    "farside2", "", icon=ui.img(src=selected[1], height="500px")
                ),
            ),
        ),
        ui.column(2),
    ),
    # Add select boxes below the cartoon images
    ui.row(
        ui.column(3),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"}, ui.input_checkbox("farside1_sel", "")
            ),
        ),
        ui.column(2),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"}, ui.input_checkbox("farside2_sel", "")
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
                ui.input_action_button("submit", "Submit", width="100%"),
            ),
        ),
        ui.column(5),
    ),
    value="panel_cartoon",
)
