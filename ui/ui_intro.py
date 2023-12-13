from shiny import ui

intro_ui = ui.nav(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.h1(
                {"style": "text-align: center; font-size: 45px;"},
                ui.markdown("**Welcome to the Far Side Forecaster**")
            ),
            ui.div(
                {"style": "text-align: center;"},
                ui.img(src="fs_intro.avif", height="400px")
            ),
            ui.br(),
            ui.div(
                {"style": "text-align: justify; font-size: 20px;"},
                ui.markdown(
                    "The Far Side is an iconic, beloved comic strip."
                    + " However, scientists have long debated, which is the"
                    + " most-loved Far Side cartoon of all? This survey seeks"
                    + " to answer this thorny, theoretical query.\n\n"
                    + "To help us determine the most beloved Far Side of all"
                    + " time, you will be shown a pair of cartoons. Simply"
                    + " select the one you like better and submit your answer."
                )
            )
        ),
        ui.column(3)
    ),
    ui.row(
        ui.column(5),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("get_started", "Get Started")
            )
        ),
        ui.column(5)
    ),
    ui.br()
)
