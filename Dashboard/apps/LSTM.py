import dash
from dash import Dash, dcc, html, Input, Output,State,callback
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import plotly.express as px
from calendar import monthrange
from datetime import date, timedelta, datetime
import functions
import dash_bootstrap_components as dbc
import math
import tensorflow as tf


nifty = np.load('D:/Lognormal/code/apps/nifty.npy',allow_pickle=True)
arr_nifty = nifty[0:5]
date_data_nifty = nifty[5:]
start_nifty = str(date_data_nifty[0])
end_nifty = str(date_data_nifty[1])
# arr_nifty = [17410.22, 17394.346, 17372.746, 17398.535, 17418.943]
arr_nifty = arr_nifty.reshape(5,)
arr_nifty = np.array(arr_nifty, dtype=int)


banknifty = np.load('D:/Lognormal/code/apps/banknifty.npy',allow_pickle=True)
arr_banknifty = banknifty[0:5]
date_data_banknifty = banknifty[5:]
start_banknifty = str(date_data_banknifty[0])
end_banknifty = str(date_data_banknifty[1])
# arr_banknifty = [17410.22, 17394.346, 17372.746, 17398.535, 17418.943]
arr_banknifty = arr_banknifty.reshape(5,)
arr_banknifty = np.array(arr_banknifty, dtype=int)

###########################################################################################################################################
# BANKNIFTY LSTM SCREENER
fig2 = go.Figure()
fig2.update_layout(autosize=False, width=700, height=400)
fig2.add_trace(go.Scatter(y=arr_banknifty,
                         mode='lines+markers', name='BankNifty 50 Index',
                         marker_line_width=2, marker_size=16,
                         marker_color='#fac69b',
                         fill='toself',
                         fillcolor='#ff6978', ))

fig2.add_hline(y=arr_banknifty[-1], line_dash="dot",
              annotation_text="Week Last day prediction : " + str(arr_banknifty[-1]),
              annotation_position="bottom right", line_color='black')

fig2.add_hline(y=arr_banknifty[0], line_dash="dot",
              annotation_text="Week First day prediction : " + str(arr_banknifty[0]),
              annotation_position="bottom left", line_color='red')
fig2.add_hline(y=np.amax(arr_banknifty), line_dash="dot",
              annotation_text="Week most Bullish day prediction : " + str(np.amax(arr_banknifty)),
              annotation_position="top left", line_color='green')

fig2.add_hline(y=np.amin(arr_banknifty), line_dash="dot",
              annotation_text="Week most Bearish day prediction : " + str(np.amin(arr_banknifty)),
              annotation_position="top right", line_color='red')

fig2.add_vline(x=0, line_dash="dot", line_color='black')
fig2.add_vline(x=arr_banknifty.shape[0] - 1, line_dash="dot", line_color='black')
fig2.update_layout(
    width = 1300, height=800,
    xaxis_title="Days",
    yaxis_title="Index Price",
    title="BankNifty 50 Weekly prediction, trained from :" + start_banknifty + " to " + end_banknifty,
    font=dict(
        family="Courier New, monospace",
        size=16,
        color="#1f150d"
    ),
    plot_bgcolor='#fceded',
    paper_bgcolor='#ffffff',
)
fig2.update_xaxes(tick0=2, dtick=1)

# BANKNIFTY LSTM SCREENER
###########################################################################################################################################



###########################################################################################################################################
# NIFTY LSTM SCREENER
fig1 = go.Figure()
fig1.update_layout(autosize=False, width=700, height=400)
fig1.add_trace(go.Scatter(y=arr_nifty,
                         mode='lines+markers', name='Nifty 50 Index',
                         marker_line_width=2, marker_size=16,
                         marker_color='#fac69b',
                         fill='toself',
                         fillcolor='#a3ff99', ))

fig1.add_hline(y=arr_nifty[-1], line_dash="dot",
              annotation_text="Week Last day prediction : " + str(arr_nifty[-1]),
              annotation_position="bottom right", line_color='black')

fig1.add_hline(y=arr_nifty[0], line_dash="dot",
              annotation_text="Week First day prediction : " + str(arr_nifty[0]),
              annotation_position="bottom left", line_color='red')
fig1.add_hline(y=np.amax(arr_nifty), line_dash="dot",
              annotation_text="Week most Bullish day prediction : " + str(np.amax(arr_nifty)),
              annotation_position="top left", line_color='green')

fig1.add_hline(y=np.amin(arr_nifty), line_dash="dot",
              annotation_text="Week most Bearish day prediction : " + str(np.amin(arr_nifty)),
              annotation_position="top right", line_color='red')

fig1.add_vline(x=0, line_dash="dot", line_color='black')
fig1.add_vline(x=arr_nifty.shape[0] - 1, line_dash="dot", line_color='black')
fig1.update_layout(
    width = 1300, height=800,
    xaxis_title="Days",
    yaxis_title="Index Price",
    title="Nifty 50 Weekly prediction, trained from :" + start_nifty + " to " + end_nifty,
    font=dict(
        family="Courier New, monospace",
        size=16,
        color="#1f150d"
    ),
    plot_bgcolor='#F1FFFA',
    paper_bgcolor='#ffffff',
)
fig1.update_xaxes(tick0=2, dtick=1)

# NIFTY LSTM SCREENER
###########################################################################################################################################

layout = html.Div([

    html.Div([
        html.Div([
            # html.Div(id='live_text1'),
            html.Div(id='live_text1'),

        ], className="create_container four columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text2'),

        ], className="create_container four columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text3'),

        ], className="create_container four columns", style={'text-align': 'center'}),

    ], className="row flex-display"),

    html.Div([
        dcc.Graph(id='LSTM-nifty-chart',
                  config={'displayModeBar': 'hover'},
                  figure=fig1),

    ], className="create_container twelve  columns"),

    html.Div([
        dcc.Graph(id='LSTM-banknifty-chart',
                  config={'displayModeBar': 'hover'},
                  figure=fig2),

    ], className="create_container twelve  columns"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

