import os
from pathlib import Path
from shiny import App, reactive, render, ui
from shiny.types import ImgData

app_ui = ui.page_fluid(
    ui.panel_title(ui.markdown("**Which Cartoon is Funnier**"), "Cartoon Comparison"),
    ui.navset_hidden(
        ui.nav(
            None,
            ui.br(),
            ui.row(
                ui.column(4, ui.output_image("farside1", fill=True, height="600px")),
                ui.column(4, ui.output_image("farside2", fill=True, height="600px")),
                ui.column(4, ui.output_image("farside3", fill=True, height="600px"))
            ),
            value="panel1"
        ),
        ui.nav(
            None,
            ui.br(),
            ui.row(
                ui.column(4, ui.output_image("farside6", fill=True, height="600px")),
                ui.column(4, ui.output_image("farside5", fill=True, height="600px")),
                ui.column(4, ui.output_image("farside4", fill=True, height="600px"))
            ),
            value="panel2"
        ),
        id="hidden_tabs"
    ),
    ui.br(),
    ui.row(ui.column(5), ui.column(2, ui.input_action_button("next", "Next")), ui.column(5)),
    ui.hr()
)


def server(input, output, session):
    
    # Render all the images
    
    @output
    @render.image
    def farside1():
        cur_dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(cur_dir / "img" / "fs_01.jpeg"), "height": "100%"}
        return img
    
    @output
    @render.image
    def farside2():
        cur_dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(cur_dir / "img" / "fs_02.jpeg"), "height": "100%"}
        return img
    
    @output
    @render.image
    def farside3():
        cur_dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(cur_dir / "img" / "fs_03.jpeg"), "height": "100%"}
        return img
    
    @output
    @render.image
    def farside4():
        cur_dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(cur_dir / "img" / "fs_01.jpeg"), "height": "100%"}
        return img
    
    @output
    @render.image
    def farside5():
        cur_dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(cur_dir / "img" / "fs_02.jpeg"), "height": "100%"}
        return img
    
    @output
    @render.image
    def farside6():
        cur_dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(cur_dir / "img" / "fs_03.jpeg"), "height": "100%"}
        return img
    
    # Update the panel when the user clicks 'Next'
    @reactive.Effect
    @reactive.event(input.next)
    def _():
        print(input.next())
        panel_val = "panel" + str((int(input.next()) % 2) + 1)
        print(panel_val)
        ui.update_navs("hidden_tabs", selected=panel_val)


app = App(app_ui, server)


# if __name__ == "__main__":
#     print(Path(__file__).resolve().parent)
#     print(Path(__file__).resolve())
