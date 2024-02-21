from shiny import ui

"""
This script lays out the UI for the "I don't consent" landing page.
"""

no_consent_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(2),
        ui.column(
            8,
            ui.div(
                {
                    "style": "text-align: center;"
                },
                ui.br(),
                ui.br(),
                ui.br(),
                ui.markdown(
                    "*As you do not wish to participate in this study, please "
                    + "close this survey and return your submission on "
                    + "Prolific by selecting the 'Stop without completing' "
                    + "button.*"
                )
            ),
        ),
        ui.column(2),
    ),
    value="panel_no_consent",
)
