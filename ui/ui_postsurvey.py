from pathlib import Path
from shiny import ui

"""
This script lays out the UI for the cartoon comparison page. It also does a
bit of data prep via the API to ensure the database is storing essential data.
"""

# Set file paths relative to ui_cartoons.py instead of being absolute
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
             width='100%'),
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
            ),
        ),
        ui.column(5),
    ),
    value="panel_attention",
)

postsurvey_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
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
            ui.input_radio_buttons('demo1',
                        ui.HTML('What is your age?'),
                        {'age_response': ui.div(ui.input_text('age',
                                                       "",
                                                       ""),
                                                       ui.output_text_verbatim('age'),
                                                       width='100%'),
                         'skip': 'Prefer not to disclose'}),
                        
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                ui.HTML('What is your race? Check all that apply.')
            ),
            ui.div(
            ui.input_checkbox('race_aian', 'American Indian or Alaska Native', False),
            ui.output_ui("race_aian_value"),
            ui.input_checkbox('race_asian', 'Asian', False),
            ui.output_ui("race_asian_value"),
            ui.input_checkbox('race_black', 'Black or African American', False),
            ui.output_ui("race_black_value"),
            ui.input_checkbox('race_nhpi', 'Native Hawaiian or Pacific Islander', False),
            ui.output_ui("race_nhpi_value"),
            ui.input_checkbox('race_white', 'White', False),
            ui.output_ui("race_white_value"),
            ui.input_checkbox('race_other', 'Other', False),
            ui.output_ui("race_other_value"),
            ui.input_checkbox('race_skip', 'Prefer not to disclose', False),
            ui.output_ui("race_skip_value"),
        ),
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
    value="panel_postsurvey",
)
