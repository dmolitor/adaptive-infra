from pathlib import Path
from shiny import ui

"""
This script lays out the UI for the attention check page.
"""

# Set file paths relative to current file
cur_dir = Path(__file__).resolve().parent

# UI for the candidate attention check
attention_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.input_radio_buttons(
                id="attention",
                label=ui.HTML("Which immigrant had a higher education level?"),
                choices={
                    0: "Immigrant 1",
                    1: "Immigrant 2",
                    2: "I don't know"
                },
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
                ui.input_action_button(
                    "next_page_outro",
                    "Next page \u27A4"
                ),
            )
        ),
        ui.column(3),
    ),
    value="panel_attention",
)
