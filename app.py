import sqlite3
from shiny import reactive, req
from shiny.express import input, render, ui
from shiny.types import FileInfo
import pandas as pd


ui.page_opts(title="Matrix Management Tool")

# ui.nav_spacer()  # Push the navbar items to the right

# footer = ui.input_select("var", "Select variable", choices=[" ", " "])


def read_in_tables(tables_or_tablenames):
    """Read in database tables"""
    # req(input.file1())
    # file: list[FileInfo] | None = input.file1()
    # if file is not None:
    #     # creating file path

    # dbfile = "C:\\Users\\daneg\\Documents\\Geisler_Matrix_Database.db"
    dbfile = "C:\\Users\\dgibbo03\\OneDrive - New York Institute of Technology\\Geisler_Matrix_Manager\\Geisler_Matrix_Database.db"
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(dbfile)
    # creating cursor
    cur = con.cursor()
    # reading all table names
    table_list = [
        a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    ]
    # print(table_list)
    index_table = None
    list_of_tabledata = []
    table_names = []
    query_string = "SELECT * FROM "
    for index, each_table in enumerate(table_list):
        query_string = query_string + table_list[index][0]
        table_names.append(table_list[index][0])
        if index == 0:
            index_table = pd.read_sql_query(query_string, con)
            # print(index_table)
        else:
            list_of_tabledata.append(pd.read_sql_query(query_string, con))
            # print(pd.read_sql_query(query_string, con))
        query_string = "SELECT * FROM "
    # Be sure to close the connection
    # table_names.remove("sqlite_sequence")
    con.close()
    table_names.remove("sqlite_sequence")
    list_of_tabledata.insert(0, index_table)
    # print("Here!")
    if tables_or_tablenames == 0:
        return list_of_tabledata
    elif tables_or_tablenames == 1:
        return table_names
    # else:
    #     print("File is None")
    #     return


ui.input_file(
    "file1",
    "Upload Master Archive Database",
    accept=[".db"],
    multiple=False,
    width="100%",
)

ui.input_file(
    "file2",
    "Upload Nexus/TNT File to Compare or Change",
    accept=[".nex", ".tnt"],
    multiple=False,
    width="100%",
)

with ui.navset_pill(id="tab"):
    with ui.nav_panel("Tools"):
        with ui.layout_columns():
            with ui.card():
                table_names = read_in_tables(1)
                if table_names is not None:
                    ui.input_selectize(
                        "selectize_4",
                        "Select an option below:",
                        table_names,
                    )
                else:
                    ui.input_selectize(
                        "selectize_4",
                        "Select an option below:",
                        [""],
                    )

                @render.data_frame
                def render_master_file():
                    table_list = read_in_tables(0)
                    table_names = read_in_tables(1)
                    if table_list is not None and table_names is not None:
                        dropdown_selection = input.selectize_4()
                        # print(dropdown_selection)
                        selected_table_index = table_names.index(dropdown_selection)
                        selected_table = table_list[selected_table_index]
                        return render.DataGrid(
                            selected_table, filters=True, width="100%"
                        )

            with ui.card():
                "Desired Process"
                ui.input_checkbox("checkbox", "Walk through each step?", False)
                ui.input_action_button("action_button_0", "Analyze")
                with ui.layout_column_wrap(width=1 / 2):
                    ui.input_action_button("Move_Back", "< Back"),
                    ui.input_action_button("Move_Forward", "Forward >"),
                ui.hr()
                ui.input_action_button("action_button_1", "Generate Instructions File")
                ui.input_action_button("action_button_2", "Generate New Nexus File")
                ui.input_action_button("action_button_3", "Change Old Nexus File")
                ui.input_action_button("action_button_4", "Customize Edit")
                ui.input_action_button("action_button_5", "Edit Breakdown")

            with ui.card():
                table_names = read_in_tables(1)
                if table_names is not None:
                    ui.input_selectize(
                        "selectize_3",
                        "Select an option below:",
                        table_names,
                    )
                else:
                    ui.input_selectize(
                        "selectize_3",
                        "Select an option below:",
                        [""],
                    )

                @render.data_frame
                def render_slave_file():
                    table_list = read_in_tables(0)
                    table_names = read_in_tables(1)
                    if table_list is not None and table_names is not None:
                        dropdown_selection = input.selectize_3()
                        # print(dropdown_selection)
                        selected_table_index = table_names.index(dropdown_selection)
                        selected_table = table_list[selected_table_index]
                        return render.DataGrid(
                            selected_table, filters=True, width="100%"
                        )

    # with ui.nav_panel("Archive"):

    #     @render.data_frame
    #     def display_archive_total():
    #         pass

    with ui.nav_panel("Single File View"):
        table_names = read_in_tables(1)
        # dict_keys = range(len(table_names))
        if table_names is not None:
            ui.input_selectize(
                "selectize_1",
                "Select a table below:",
                table_names,
            )
        else:
            ui.input_selectize("selectize_1", "Select a table below:", [""])

        @render.data_frame
        def display_single_table():
            # req(input.file1())
            table_list = read_in_tables(0)
            table_names = read_in_tables(1)
            # print(index_table)
            if table_list is not None and table_names is not None:
                dropdown_selection = input.selectize_1()
                # print(dropdown_selection)
                selected_table_index = table_names.index(dropdown_selection)
                selected_table = table_list[selected_table_index]
                return render.DataGrid(
                    selected_table, filters=True, width="100%", selection_mode="row"
                )

    with ui.nav_panel("Single File Edit"):
        if table_names is not None:
            ui.input_selectize(
                "selectize_2",
                "Select an option below:",
                table_names,
            )
        else:
            ui.input_selectize(
                "selectize_2",
                "Select an option below:",
                [""],
            )

        @render.data_frame
        def display_single_file():
            # req(input.file1())
            table_list = read_in_tables(0)
            table_names = read_in_tables(1)
            # print(index_table)
            if table_list is not None and table_names is not None:
                dropdown_selection = input.selectize_2()
                selected_table_index = table_names.index(dropdown_selection)
                selected_table = table_list[selected_table_index]
                # print("Position 2")
                return render.DataGrid(
                    selected_table, filters=True, width="100%", editable=True
                )

        ui.input_action_button(
            "action_button_update", "Update Database With Current Edits"
        )


def read_in_archive_file():
    req(input.file1())
    file: list[FileInfo] | None = input.file1()
    if file is not None:
        all_raw_data = pd.read_excel(
            file[0]["datapath"], sheet_name="All Data", index_col=None
        )
        return all_raw_data


# with ui.nav_panel("Page 1"):
#     with ui.navset_card_underline(title="Matrix Data"):
#         "Test 123"
#     #     with ui.nav_panel("Plot"):
#     #         pass

#     #     with ui.nav_panel("Table"):
#     #         pass


# with ui.nav_panel("Page 2"):
#     "This is the second 'page'."
