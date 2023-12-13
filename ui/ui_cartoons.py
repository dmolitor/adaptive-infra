import os
from pathlib import Path
import random
from shiny import ui

class Cartoons:
    def __init__(self):
        self.selected = None

cur_dir = Path(__file__).resolve().parent
cartoons = Cartoons()
cartoon_fps = [
    file for file
    in os.listdir(str(cur_dir / "img"))
    if file != ".DS_Store"
]
cartoons.selected = random.sample(cartoon_fps, 2)

# Cartoons Shiny App UI
cartoons_ui = ui.nav(
    None,
    # Cartoons (as clickable buttons)
    ui.row(
        ui.column(2),
        ui.column(4,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button(
                    "farside1", "",
                    icon=ui.img(src=cartoons.selected[0], height="500px")
                )
            )
        ),
        ui.column(4,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button(
                    "farside2", "",
                    icon=ui.img(src=cartoons.selected[1], height="500px")
                )
            )
        ),
        ui.column(2)
    ),
    # Select boxes below cartoons
    ui.row(
        ui.column(3),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_checkbox("farside1_sel", "")
            )
        ),
        ui.column(2),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_checkbox("farside2_sel", "")
            )
        ),
        ui.column(3)
    ),
    # 'Next' button for navigating through the survey
    ui.row(
        ui.column(5),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("submit", "Submit", width="100%")
            )
        ),
        ui.column(5)
    ),
    value="panel_cartoon"
)
