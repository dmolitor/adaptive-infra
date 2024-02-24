from pathlib import Path
from shiny import ui

"""
This script lays out the UI for the cartoon comparison page. It also does a
bit of data prep via the API to ensure the database is storing essential data.
"""

# Set file paths relative to current file
cur_dir = Path(__file__).resolve().parent

# UI for the cartoon selection page
attention_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.input_radio_buttons(
                'attention1',
                ui.HTML('Which candidate was older?'),
                {0: 'Candidate 1',
                1: 'Candidate 2',
                2: "I don't know"},
                width='100%'
            )
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
                ui.input_action_button("next_page_postsurvey", "Next page \u27A4"),
            )
        ),
        ui.column(5),
    ),
    value="panel_attention",
)

postsurvey_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            {"style": "text-align: justify; font-size: 20px;"},
            ui.div(
                ui.HTML('This section has the purpose of collecting information on age, race, ethnicity, and sex. This will allow us to contextualize our results. It is important to us that you answer these questions honestly.')
            )
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
                  ui.HTML('What is your age?'),
                  ui.div(ui.input_text('age',"",""),
                         ui.output_text_verbatim('age')),
                         ui.input_radio_buttons('demo1',
                                                '',
                                                {'skip': 'Prefer not to disclose'})),
                        
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.input_checkbox_group(
                id="race",
                label=ui.HTML("What is your race? Check all that apply."),
                choices={
                    "race_aian": "American Indian or Alaska Native",
                    "race_asian": "Asian",
                    "race_black": "Black or African American",
                    "race_nhpi": "Native Hawaiian or Pacific Islander",
                    "race_white": "White",
                    "race_other": "Other",
                    "race_skip": "Prefer not to disclose"
                }
            )
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
                  ui.input_radio_buttons('demo3',
                                         'Are you Hispanic, Latino, or of Spanish origin?',
                                         {0: 'No',
                                          1: 'Yes',
                                          2: 'Prefer not to disclose'},
                  )
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
                  ui.input_radio_buttons('demo4',
                                         'What is your sex?',
                                         {0: 'Female',
                                          1: 'Male',
                                          2: 'Prefer not to disclose'},
                  )
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
                ui.input_action_button("next_page_end", "Next page \u27A4"),
            ),
        ),
        ui.column(5),
    ),
    ui.br(),
    value="panel_postsurvey",
)
