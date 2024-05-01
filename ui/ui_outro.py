from shiny import ui
from utils_prolific import prolific_redirect

"""
This script lays out the UI for the survey exit page.
"""

outro_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.div(
                {
                    "style": (
                        "font-size: 1vw; height: 10vh; display: flex; "
                        + "flex-direction: column; align-items: center; "
                        + "justify-content: center;"
                    )
                },
                ui.markdown("**Thank you!**"),
                ui.markdown(
                    "Your response has been recorded and you will be "
                    + "redirected automatically to Prolific shortly. "
                    + "If you are not redirected automatically, you may "
                    + "also click the following link to return to Prolific: "
                    + f"{prolific_redirect('valid')}."
                )
            ),
        ),
        ui.column(3),
    ),
    value="panel_outro",
)
