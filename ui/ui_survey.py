from shiny import ui

"""
This script lays out the UI for the option comparison page. Note
that each pair of options is connected to a specific context.
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
                    "Imagine you are booking a short-term rental on an online "
                    + "platform for a vacation. Which posting would you pick?"
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
                    id="options"
                ),
            ),
        ui.column(3)
    ),
    # Add select boxes below the survey tables
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.input_radio_buttons(
                id="option",
                label="Which of these two options do you prefer?",
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
                ui.input_action_button("next_page_outro", "Next page \u27A4"),
            )
        ),
        ui.column(3)
    ),
    value="panel_survey"
)