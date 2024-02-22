from pathlib import Path
from shiny import ui

"""
This script lays out the UI for the cartoon comparison page. It also does a
bit of data prep via the API to ensure the database is storing essential data.
"""

# Set file paths relative to ui_cartoons.py instead of being absolute
cur_dir = Path(__file__).resolve().parent

# UI for the cartoon selection page
postsurvey_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.input_radio_buttons(
            'attention1',
            ui.HTML('Which candidate was older?'),
            {0: 'Candidate 1',
             1: 'Candidate 2',
             2: "I don't know"}),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
                  ui.div(
                      ui.HTML('This section has the purpose of collecting information on age, race, ethnicity, and sex. This will allow us to contextualize our results. It is important to us that you answer these questions honestly.')
                  )),
        ui.column(3),
    ),
    ui.row(
        ui.column(3),
        ui.input_text('demo1',
                      ui.HTML('What is your age?'),
                      width='100%'),
                      ui.output_text_verbatim("age1"),
        ui.column(3),
    ),
    # 'Next' button for navigating through the survey
    ui.row(
        ui.column(5),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("submit", "Next page", width="100%"),
            ),
        ),
        ui.column(5),
    ),
    value="panel_postsurvey",
)
