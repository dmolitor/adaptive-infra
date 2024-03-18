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
