import os
from pathlib import Path
from shiny import App, reactive, render, ui
from shiny.types import ImgData
import shinyswatch
from ui_cartoons import cartoons, cartoons_ui
from ui_intro import intro_ui
from ui_outro import outro_ui

# Set absolute file paths relative to app.py
cur_dir = Path(__file__).resolve().parent

app_ui = ui.page_fluid(
    shinyswatch.theme.solar(),
    ui.br(),
    ui.panel_title(ui.markdown("**Far Side Forecaster**"), "Far Side Forecaster"),
    ui.hr(),
    ui.navset_hidden(
        # Intro Page
        intro_ui,
        # Cartoon Display
        cartoons_ui,
        outro_ui,
        id="hidden_tabs"
    )
)


def server(input, output, session):
    
    # Logic for 'Next' button
    @reactive.Effect
    @reactive.event(input.submit)
    def _():
        farside_sel_vals = [
            input.farside1_sel(),
            input.farside2_sel()
        ]
        ui.remove_ui(selector="#submit_status")
        # Only proceed if one image is selected
        if sum(farside_sel_vals) != 1:
            submit_status = ui.help_text(
                ui.span(
                    {"style": "color:red; text-align: center;"},
                    "Please select only one option!"
                ),
                id="submit_status"
            )
            ui.insert_ui(ui=submit_status, selector="#submit", where="afterEnd")
        else:
            ui.update_navs("hidden_tabs", selected="panel_outro")
    
    # Logic for 'Get Started'
    @reactive.Effect
    @reactive.event(input.get_started)
    def _():
        ui.update_navs("hidden_tabs", selected="panel_cartoon")
    
    
    # Logic for selecting cartoon checkboxes
    @reactive.Effect
    @reactive.event(input.farside1)
    def _():
        sel_value = input.farside1_sel()
        new_sel_value = not sel_value
        ui.update_checkbox(id="farside1_sel", label="", value=new_sel_value)

    @reactive.Effect
    @reactive.event(input.farside2)
    def _():
        sel_value = input.farside2_sel()
        new_sel_value = not sel_value
        ui.update_checkbox(id="farside2_sel", label="", value=new_sel_value)


app = App(app_ui, server, static_assets=str(cur_dir / "img"))
