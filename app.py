from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Matrix Management Tool")

# ui.nav_spacer()  # Push the navbar items to the right

# footer = ui.input_select("var", "Select variable", choices=[" ", " "])


ui.input_file(
    "file1", "Upload Master File", accept=[".xlsx"], multiple=False, width="100%"
)

ui.input_file(
    "file2", "Upload File to Compare", accept=[".xlsx"], multiple=False, width="100%"
)

ui.input_file(
    "file3", "Upload Archive File", accept=[".xlsx"], multiple=False, width="100%"
)

with ui.navset_pill(id="tab"):
    with ui.nav_panel("Tools"):
        with ui.layout_columns():
            with ui.card():
                "Geisler Matrix File"

                @render.data_frame
                def render_master_file():
                    pass

            with ui.card():
                "Desired Process"
                ui.input_checkbox("checkbox", "Walk through each step?", False)
                ui.input_action_button("action_button_0", "Analyze")
                ui.hr()
                ui.input_action_button("action_button_1", "Priority [< Left]")
                ui.input_action_button("action_button_2", "Priority [Right >]")
                ui.input_action_button("action_button_3", "Split Characters")
                ui.input_action_button("action_button_4", "Combine Characters")
                ui.input_action_button("action_button_5", "Edit Breakdown")
                ui.input_action_button("action_button_6", "Custom")

            with ui.card():
                "Other Data"
                ui.input_selectize(
                    "selectize_1",
                    "Select an option below:",
                    {"1A": "File 1", "1B": "File 2", "1C": "File 3"},
                )

                @render.data_frame
                def render_slave_file():
                    pass

    with ui.nav_panel("Archive"):

        @render.data_frame
        def display_archive_total():
            pass

    with ui.nav_panel("Archive Edit"):
        "Edit the master archive here"

    with ui.nav_panel("Single File"):
        ui.input_selectize(
            "selectize_2",
            "Select an option below:",
            {"1A": "File 1", "1B": "File 2", "1C": "File 3"},
        )

        @render.data_frame
        def display_single_file():
            pass


# with ui.nav_panel("Page 1"):
#     with ui.navset_card_underline(title="Matrix Data"):
#         "Test 123"
#     #     with ui.nav_panel("Plot"):
#     #         pass

#     #     with ui.nav_panel("Table"):
#     #         pass


# with ui.nav_panel("Page 2"):
#     "This is the second 'page'."
