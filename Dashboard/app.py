import dash
import dash_bootstrap_components as dbc
from flask import Flask


app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
                external_stylesheets=[dbc.themes.CYBORG],
                suppress_callback_exceptions=True)

server = app.server
