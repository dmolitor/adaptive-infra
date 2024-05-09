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
                    "Please read the descriptions of the fictional "
                    + "immigrants carefully. Then, please indicate which "
                    + "of the two you would personally prefer to see "
                    + "admitted to the United States."
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
                label=(
                    "Which of these two immigrant profiles would you select "
                    + "for admission to the United States?"
                ),
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