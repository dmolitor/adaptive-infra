from shiny import ui

"""
This script lays out the UI for the survey exit page.
"""

duplicates_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.div(
                {
                    "style": (
                        "font-size: 1.5vw; height: 80vh; display: flex; "
                        + "flex-direction: column; align-items: center; "
                        + "justify-content: center;"
                    )
                },
                ui.markdown("**Thank you!**"),
                ui.markdown(
                    "You have already submitted a response. You will be "
                    + "redirected automatically to Prolific shortly. "
                    + "If you are not automatically redirected, you may need to "
                    + "manually return the study. Thank you for your time!"
                ),
            ),
        ),
        ui.column(3),
    ),
    value="panel_duplicate",
)
