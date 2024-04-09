from shiny import ui

"""
This script lays out the UI for the candidate comparison page. Note
that each pair of candidates is connected to a specific context.
A context is the same as one arm of the multi-armed bandit.
"""

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
    # NOTE: Survey tables get dynamically generated in `/ui/app.py`
    ui.row(
        ui.column(3),
            ui.column(
                6,
                ui.div(
                    id="candidates"
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

## All UI elements added below are in pre-testing and may or may not end up getting used

# 1)
survey_ui_immigrant = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: justify;"},
                ui.HTML(
                    "Please read the descriptions of the potential immigrants carefully. Then, please indicate which of the two immigrants you would personally prefer to see admitted to the United States."
                )
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    # NOTE: Survey tables get dynamically generated in `/ui/app.py`
    ui.row(
        ui.column(3),
            ui.column(
                6,
                ui.div(
                    id="candidates"
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
                label="Which of these two individuals do you prefer?",
                choices={0: "Immigrant 1", 1: "Immigrant 2"},
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

# 2)
survey_ui_applicant = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: justify;"},
                ui.HTML(
                    "You will be given the descriptions for two job applicants. Please read the descriptions carefully. Then, indicate which of the two applicants you would personally select for a retail job."
                )
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    # NOTE: Survey tables get dynamically generated in `/ui/app.py`
    ui.row(
        ui.column(3),
            ui.column(
                6,
                ui.div(
                    id="candidates"
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
                label="Which of these two applicants do you prefer?",
                choices={0: "Applicant 1", 1: "Applicant 2"},
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

# 3)
survey_ui_auto = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: justify;"},
                ui.HTML(
                    "Please read the descriptions of the potential auto repair establishments carefully. Then, please indicate which of the two you would choose for an auto inspection."
                )
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    # NOTE: Survey tables get dynamically generated in `/ui/app.py`
    ui.row(
        ui.column(3),
            ui.column(
                6,
                ui.div(
                    id="candidates"
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
                label="Which of these two shops do you prefer?",
                choices={0: "Option 1", 1: "Option 2"},
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

# 4)
survey_ui_community = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: justify;"},
                ui.HTML(
                    "Please read the descriptions of the following communities. Then, indicate the community where you would prefer to live."
                )
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    # NOTE: Survey tables get dynamically generated in `/ui/app.py`
    ui.row(
        ui.column(3),
            ui.column(
                6,
                ui.div(
                    id="candidates"
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
                label="Which of these two communities do you prefer?",
                choices={0: "Community 1", 1: "Community 2"},
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

# ... Any other similar questions can just be inserted same as above