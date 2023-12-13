from shiny import ui

outro_ui = ui.nav(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {
                    "style": (
                        "font-size: 3vw; height: 80vh; display: flex; "
                        + "flex-direction: column; align-items: center; "
                        + "justify-content: center;"
                    )
                },
                ui.markdown("**Thank you!**"),
                "Your response has been recorded"
            ),
        ),
        ui.column(3)
    ),
    value="panel_outro"
)
