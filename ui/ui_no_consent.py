from shiny import ui
from utils_prolific import prolific_redirect

"""
This script lays out the UI for the exit landing page
if the user doesn't consent.
"""

no_consent_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.div(
                {"style": "text-align: center;"},
                ui.br(),
                ui.br(),
                ui.br(),
                ui.markdown(
                    "*As you do not wish to participate in this study, you "
                    + "will be redirected automatically to Prolific shortly. "
                    + "If you are not redirected automatically, you may "
                    + "also click the following link to return to Prolific: "
                    + f"[{prolific_redirect('noconsent')}]"
                    + f"({prolific_redirect('noconsent')}).*"
                ),
            ),
        ),
        ui.column(3),
    ),
    value="panel_no_consent",
)
