from shiny import ui

# UI for the demographics collection page
demographics_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            {"style": "text-align: justify;"},
            ui.div(
                ui.HTML(
                    "This section has the purpose of collecting information "
                    + "on age, race, ethnicity, and sex. This will allow us "
                    + "to contextualize our results. It is important to us "
                    + "that you answer these questions honestly."
                )
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.HTML("What is your age?"),
            ui.input_text("resp_age_text", "", ""),
            ui.input_checkbox_group(
                id="resp_age_check",
                label="",
                choices={"age_skip": "Prefer not to disclose"},
                width="100%",
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.input_checkbox_group(
                id="resp_race",
                label=ui.HTML("What is your race? Check all that apply."),
                choices={
                    "race_aian": "American Indian or Alaska Native",
                    "race_asian": "Asian",
                    "race_black": "Black or African American",
                    "race_nhpi": "Native Hawaiian or Pacific Islander",
                    "race_white": "White",
                    "race_other": "Other",
                    "race_skip": "Prefer not to disclose",
                },
                width="100%",
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.input_radio_buttons(
                id="resp_ethnicity",
                label="Are you Hispanic, Latino, or of Spanish origin?",
                choices={0: "No", 1: "Yes", 2: "Prefer not to disclose"},
                selected="",
                width="100%",
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.input_radio_buttons(
                id="resp_sex",
                label="What is your sex?",
                choices={0: "Female", 1: "Male", 2: "Prefer not to disclose"},
                selected="",
            ),
        ),
        ui.column(3),
    ),
    # 'Next' button for navigating through the survey
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.div(
                {"style": "text-align: right;"},
                ui.input_action_button("next_page_survey", "Next page \u27a4"),
            ),
        ),
        ui.column(3),
    ),
    ui.br(),
    value="panel_demographics",
)
