from shiny import ui

"""
This script lays out the UI for the survey landing page.
"""

intro_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.h1(
                {"style": "text-align: center; font-size: 45px;"},
                ui.markdown("**Welcome to our study!**"),
            ),
            ui.div(
                {"style": "text-align: center;"},
                ui.img(src="fs_intro.avif", height="400px"),
            ),
            ui.br(),
            ui.div(
                {"style": "text-align: justify; font-size: 20px;"},
                ui.markdown(
                    "Thank you so much for participating in this brief survey to improve the understanding of human decision-making."
                    + "This survey requests personal information limited to age, race, ethnicity, sex, and location."
                    + "We estimate that this survey should take at most 1.5 minutes to complete."
                    + "Please read this page carefully and check the box at the bottom of the page if you agree to participate."
                    + "You must be 18 years old or older to participate."
                ),
            ),
        ),
        ui.column(3),
    ),
    ui.row(
        ui.column(5),
        ui.column(
            2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("get_started", "Get Started"),
            ),
        ),
        ui.column(5),
    ),
    ui.br(),
)
