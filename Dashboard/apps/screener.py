import pandas as pd
from dash import Dash, dcc, html, Input, Output,callback,dash_table

# -- Import and clean data (importing csv into pandas)
#read the csv file with given path

# df.reset_index(inplace=True)
# print(df[:5])

# ------------------------------------------------------------------------------
# App layout
def screen():
    df = pd.read_csv("data/screener.csv",index_col = 0)
    dates = df['Expiry Date'].unique().tolist()
    print(dates)
    layout = html.Div(
        children=[
            dcc.Dropdown(
                id="filter_dropdown",
                options=[{"label": st, "value": st} for st in dates],
                placeholder="-Select a Expiry Date-",
                multi=True,
                clearable = True,
                disabled = False,
                style = {'display': True},
            ),
            dash_table.DataTable(
                id="table-container",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
            )
        ]
    )


    @callback(
        Output("table-container", "data"),
        Input("filter_dropdown", "value")
    )
    def display_table(state):
        dff = df[df['Expiry Date'].isin(state)]
        return dff.to_dict("records")

    return layout
if '__name__' == '__main__':
    screen()
