from shiny import ui

"""
This script lays out the UI for the survey landing page.
"""

prolific_q_ui = ui.nav_panel(
    None,
    ui.row(
        5,
        ui.column(3),
        ui.input_text('prolific_id',
                      'What is your Prolific ID? Please note that this response should auto-fill with the correct ID.'),
                      ui.output_text_verbatim("value"),
    ui.br(),
    ),
    ui.row(
        5,
        ui.column(3),
        ui.input_radio_buttons(
            'location',
            'Are you located in the U.S.?',
            {1: 'Yes',
             0: 'No'})
    ),
    ui.br(),
value="panel_prolific_q",
)
