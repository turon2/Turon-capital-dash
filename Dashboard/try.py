import dash
import pandas as pd

from dash import dash_table as dt
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")

app = dash.Dash(__name__)

states = df.State.unique().tolist()

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id="filter_dropdown",
            options=[{"label": st, "value": st} for st in states],
            placeholder="-Select a State-",
            multi=True,
            value=df.State.values,
        ),
        dt.DataTable(
            id="table-container",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records")
        )
    ]
)


@app.callback(
    Output("table-container", "data"),
    Input("filter_dropdown", "value")
)
def display_table(state):
    dff = df[df.State.isin(state)]
    return dff.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
