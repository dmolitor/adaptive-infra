from shiny import ui

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
                        "font-size: 3vw; height: 80vh; display: flex; "
                        + "flex-direction: column; align-items: center; "
                        + "justify-content: center;"
                    )
                },
                ui.markdown("**Thank you!**"),
                "Your response has been recorded",
            ),
        ),
        ui.column(3),
    ),
    value="panel_outro",
)
