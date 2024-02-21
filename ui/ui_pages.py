from shiny import ui

"""
This script lays out the UI for the survey landing page.
"""

screening_questions = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.input_text(
                id="prolific_id",
                label=(
                    "What is your Prolific ID? Please note that this response "
                    + "should auto-fill with the correct ID."
                ),
                value="",
                width="100%"
            )
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
        ui.input_radio_buttons(
            'location',
            'Are you located in the U.S.?',
            {1: 'Yes',
             0: 'No'},
             width='100%')
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
        ui.input_radio_buttons(
            'commitment1',
            ui.HTML('We care about the quality of our data. For us to accurately understand decision-making, it is important that you provide thoughtful answers to each question in the survey.<br><br>Do you commit to providing thoughtful answers to the questions in the survey?'),
            {1: 'Yes, I will',
             2: "I can't promise either way",
             0: 'No, I will not'},
             width='100%')
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
        ui.input_text('commitment2',
                      ui.HTML('The following question is to verify that you are a real person.<br><br>Please enter the word purple in the box below.'),
                      width='100%'),
                      ui.output_text_verbatim("value2"),
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("next_page_survey", "Next page"),
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
value="panel_prolific_q",
)
