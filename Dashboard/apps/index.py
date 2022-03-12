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

data_stock_IV = pd.read_csv("data/ADANIPORTS.csv",index_col=0)
data_stock = functions.all()

list_stock = list(data_stock['stock_name'].unique())
print(list_stock)
month_list = {1 : "Jan", 2 : "Feb", 3 : "March", 4 : "April", 5 : "May", 6 : "June", 7 : "July", 8 : "Aug", 9 : "Sept", 10 : "Oct", 11 : "Nov", 12 : "Dec"}
year = [2015,2016,2017,2018,2019,2020,2021]



layout = html.Div([

    # offcanvas,


    html.Div([
        html.Div([
            # html.Div(id='live_text1'),
            html.Div([html.H3("HELLO")], id='live_text1'),

        ], className="create_container two columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text2'),

        ], className="create_container two columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text3'),

        ], className="create_container two columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text4'),

        ], className="create_container two columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text5'),

        ], className="create_container two columns", style={'text-align': 'center'}),

        html.Div([
            html.Div(id='live_text6'),

        ], className="create_container two columns", style={'text-align': 'center'}),

    ], className="row flex-display"),


    html.Div([
        html.Div([
            html.Div([
                html.P('Select Symbol', className = 'fix_label', style = {'color': 'white'}),
                dcc.Dropdown(id = 'select_country',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             value = 'ADANIPORTS',
                             placeholder = 'Select Symbol',
                             options = [{'label': c, 'value': c}
                                        for c in list_stock], className = 'dcc_compon'),

                html.P('Select Year', className = 'fix_label', style = {'color': 'white', 'margin-top': '30px'}),
                dcc.RangeSlider(id = 'slider_year',
                           included = True,
                           updatemode='drag',
                           tooltip={'always_visible': True},
                           min = 2015,
                           max = 2022,
                           step = 1,
                           value = [2018,2020],
                           marks = {str(yr): str(yr) for yr in range(2015, 2022, 1)},
                           className = 'dcc_compon1'),

                html.P('Select Platform', className = 'fix_label', style = {'color': 'white', 'margin-top': '30px'}),
                dcc.Dropdown(id='radio_items',
                             multi=False,
                             clearable=True,
                             disabled=False,
                             style={'display': True},
                             value=1,
                             placeholder='Select Countries',
                             options=[{'label': month_list[c], 'value': c}
                                      for c in month_list], className='dcc_compon'),

                ], className = "create_container  columns"),

        html.Div([
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': 'hover'}),

                 ], className="create_container  columns"),
        ],className = "create_container four columns"),



        html.Div([
            html.Div([
            dcc.Graph(id = 'candlestick_chart',
                      config = {'displayModeBar': 'hover'}),

                    ], className = "create_container eight columns"),

            html.Div([
            dcc.Graph(id = 'volume_chart',
                      config = {'displayModeBar': 'hover'}),

                    ], className = "create_container2 eight columns"),


                ],className = "create_container eight columns"),

    ], className = "row flex-display"),

        html.Div([
            html.Div([
                    dcc.Graph(id = 'log_chart',
                              config = {'displayModeBar': 'hover'}),

                ], className = "create_container seven columns"),

            html.Div([
                    dcc.Graph(id = 'log_returns_chart',
                              config = {'displayModeBar': 'hover'}),

                ], className = "create_container five columns"),

            ],className = "row flex-display"),

        html.Div([
                html.Div([
                    html.Div([
                    dcc.Graph(id = 'IV_monthly_chart',
                              config = {'displayModeBar': 'hover'}),

                            ], className = "create_container nine columns"),

                    html.Div([
                    dcc.Graph(id = 'vol_chart',
                              config = {'displayModeBar': 'hover'}),

                            ], className = "create_container2 eight columns"),
                        ],className = "create_container nine columns"),


                html.Div([
                    html.P('Select Year', className = 'fix_label', style = {'color': 'white', 'margin-top': '30px'}),
                    dcc.Dropdown(id='radio_item',
                                 multi=False,
                                 clearable=True,
                                 disabled=False,
                                 style={'display': True},
                                 value=2015,
                                 placeholder='Select Year',
                                 options=[{'label': c, 'value': c}
                                          for c in year], className='dcc_compon'),

                    ], className = "create_container three columns"),




            ], className = "row flex-display"),
        html.Div([
            dcc.Graph(id='IV_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container twelve  columns"),

        # html.Div([
        #     html.Div(id = "tradingview_c0997")
        # ],className= "tradingview-widget-container"),



], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})


@callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("open-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)

def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback([Output('IV_monthly_chart', 'figure')],
          [Output('vol_chart', 'figure')],
          [Input('radio_item', 'value')],
          [Input('select_country', 'value')])
def update_graph(radio_item,select_country):
    year = radio_item


    data1 = data_stock_IV.copy()
    data1['Date'] = pd.to_datetime(data1['Date'], format='%y%m%d', infer_datetime_format=True)
    data = data1[(data1['Date'] >= datetime(year, 1, 1)) & (data1['Date'] <= datetime(year, 12, 31))]

    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lst = []
    max_lst = []
    min_lst = []
    RV = []
    for mon in months:
        num_days = monthrange(year, mon)[1]
        dummy = data[(data['Date'] >= datetime(year, mon, 1)) & (data['Date'] <= datetime(year, mon, num_days))]
        lst.append(dummy['IV'].values)
        max_IV = dummy['IV'].max()
        min_IV = dummy['IV'].min()
        max_lst.append(max_IV)
        min_lst.append(min_IV)
        # dummy.loc[:,'Log returns'] = np.log10(dummy['value'] / dummy['value'].shift()) * 100
        # dummy.loc[:,'variance'] = (dummy['Log returns'] ** 2) / 100
        # sum_variance = math.sqrt(dummy['variance'].sum() / 100) * 100 * math.sqrt(252)
        sum_variance = 30
        RV.append(sum_variance)

    N = 12  # Number of boxes

    # generate an array of rainbow colors by fixing the saturation and lightness of the HSL
    # representation of colour and marching around the hue.
    # Plotly accepts any CSS color format, see e.g. http://www.w3schools.com/cssref/css_colors_legal.asp.
    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]

    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(
        y=lst[i],
        marker_color=c[i],
        name = month_list.get(i+1)
    ) for i in range(int(N))])
    fig.add_trace((go.Bar(x=list(month_list.values()), y=RV, opacity=1, marker_color='#010915', name="Realised Vol")))
    # format the layout
    fig.update_layout(autosize=False, width=950, height=600,
                      title=go.layout.Title(text="Historical IV data of  :" + " " + "stock"),
                      plot_bgcolor='#010915',
                      paper_bgcolor='#010915',
                      titlefont={'color': 'white', 'size': 20},
                      xaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                             'gridcolor': '#e5e5e5', 'showgrid': False},
                      yaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                             'gridcolor': '#e5e5e5', 'showgrid': False},
                      legend_font_color='white',
                      legend_font_size=12,
                      hovermode="x unified",
                      hoverlabel=dict(
                          bgcolor="#010915",
                          font_size=16,
                          font_family="Overpass",
                          font_color="white"
                      ),
                      yaxis_range=[20, 90]
                      )

    stock = select_country
    data_ = data_stock.copy()
    data1_ = data_[data_['stock_name'] == stock]
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    monthly_returns = []
    for month in months:
        num_days = monthrange(year, month)[1]
        dummy = data1_[(data1_['trading_date'] >= datetime(year, month, 1)) & (
                    data1_['trading_date'] <= datetime(year, month, num_days))]
        close_list = list(dummy['close'])
        try:
            monthly_returns.append(((close_list[-1] - close_list[0]) / close_list[0]) * 100)
        except:
            monthly_returns.append(0)

    color_plate = []
    for i in monthly_returns:
        if i > 0:
            color_plate.append("#31c453")
        else:
            color_plate.append("#e62020")
    # Plot
    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(x=list(month_list.values()),
               y=monthly_returns,
               marker_color = color_plate))
    fig1.update_layout(barmode='stack')
    fig1.update_layout(autosize=False, width=950, height=600,
                      title=go.layout.Title(text="Monthly returns of :" + " " + stock + " ,year : " + str(year)),
                      plot_bgcolor='#010915',
                      paper_bgcolor='#010915',
                      titlefont={'color': 'white', 'size': 20},
                      xaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                             'gridcolor': '#e5e5e5', 'showgrid': False},
                      yaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                             'gridcolor': '#e5e5e5', 'showgrid': False},
                      legend_font_color='white',
                      legend_font_size=10,
                      hovermode="x unified",
                      hoverlabel=dict(
                          bgcolor="#010915",
                          font_size=16,
                          font_family="Overpass",
                          font_color="white"
                      )
                      )


    return fig1,fig
@callback(
    Output('IV_chart', 'figure'),
    [Input('select_country', 'value')],
    [Input('slider_year', 'value')],
    [Input('radio_items', 'value')]
    )
def update_graph_IV(select_country, slider_year, radio_items):
    stock = select_country
    month = radio_items
    year = slider_year

    num_days = monthrange(year[0], month)[1]

    data = data_stock_IV.copy()
    # data1 = data[data['stock_name'] == stock]
    data1 = data
    data1['Date'] = data1['Date'].apply(lambda x: datetime.fromisoformat(x).date())
    data1['Expiry'] = data1['Expiry'].apply(lambda x: datetime.fromisoformat(x).date())
    data2 = data1[
        (data1['Date'] >= datetime(year[0], month, 1).date()) & (data1['Date'] <= datetime(year[1], month, num_days).date())]

    fig = go.Figure()
    fig.update_layout(autosize=False, width=1250,height=600,
                       title=go.layout.Title(text="Historical IV data of  :" + " " + stock),
                       plot_bgcolor='#010915',
                       paper_bgcolor='#010915',
                       titlefont={'color': 'white', 'size': 20},
                       xaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5','showgrid' : False},
                       yaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5','showgrid' : False},
                       legend_font_color='white',
                       legend_font_size=10,
                       hovermode="x unified",
                       hoverlabel=dict(
                          bgcolor="#010915",
                          font_size=16,
                          font_family="Overpass",
                          font_color = "white"
                                      )
                       )
    fig.add_trace(go.Scatter(x=data2['Date'], y=data2['IV'], mode='lines+markers', name='Closing Price', marker_line_width=2,
                               marker_size=16, marker_color='#06FF00',
                               hoverinfo='text',
                               hovertext=
                               '<b>Implied Volatility</b>: ' + data2['IV'].astype(str) + '<br>' +
                               '<b>Expiry Date</b>: ' + data2['Expiry'].astype(str) + '<br>' +
                               '<b>Strike Price</b>: ' + data2['Strike Price'].astype(str) + '<br>' +
                               '<b>Underlying</b>: ' + data2['value'].astype(str) + '<br>' +
                               '<b>Date</b>: ' + data2['Date'].astype(str) + '<br>' +
                               '<b>Days to Expiry</b>: ' + data2['days_to_expiry'].astype(str) + '<br>'
                               ))
    return fig

@callback(
    Output('live_text1', 'children'),
    Output('live_text2', 'children'),
    [Input('select_country', 'value')],
    [Input('slider_year', 'value')],
    [Input('radio_items', 'value')]
    )

def update_cards(select_country, slider_year, radio_items):

    stock = select_country
    month = radio_items
    year = slider_year
    num_days = monthrange(year[0], month)[1]
    data = data_stock.copy()
    data1 = data[data['stock_name'] == stock]
    data2 = data1[
        (data1['trading_date'] >= datetime(year[0], month, 1)) & (
                    data1['trading_date'] <= datetime(year[1], month, num_days))]
    high = data2['close'].max()
    low = data2['close'].min()
    high_date_data = str(data2.iloc[data2['close'].argmax()]['trading_date'].date())
    low_date_data = str(data2.iloc[data2['close'].argmin()]['trading_date'].date())
    range_data = round(high - low)
    live1 =  [
               html.H6(children = 'High of : ' + stock,
                       style={'textAlign': 'center',
                              'color': 'white'}
                       ),
               html.P('{0:,.0f}'.format(high),
                      style={'textAlign': 'center',
                             'color': '#06FF00',
                             'fontSize': 40}
                      ),
               html.P('Date:  ' + ' ' + high_date_data,
                      style = {
                          'textAlign': 'center',
                          'color': '#06FF00',
                          'fontSize': 15,
                          'margin-top': '-18px'}
                      )

    ]

    live2 = [
        html.H6(children='Low of : ' + stock,
                style={'textAlign': 'center',
                       'color': 'white'}
                ),
        html.P('{0:,.0f}'.format(low),
               style={'textAlign': 'center',
                      'color': '#0FECE9',
                      'fontSize': 40}
               ),
        html.P('Date:  ' + ' ' + low_date_data,
               style={
                   'textAlign': 'center',
                   'color': '#0FECE9',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               )

    ]

    return live1, live2

@callback(
    Output('live_text3', 'children'),
    Output('live_text4', 'children'),
    [Input('select_country', 'value')],
    [Input('slider_year', 'value')],
    [Input('radio_items', 'value')]
    )

def update_cards(select_country, slider_year, radio_items):
    stock = select_country
    month = radio_items
    year = slider_year

    num_days = monthrange(year[0], month)[1]

    data = data_stock_IV.copy()
    # data1 = data[data['stock_name'] == stock]
    data1 = data
    data1['Date'] = data1['Date'].apply(lambda x: datetime.fromisoformat(x).date())
    data1['Expiry'] = data1['Expiry'].apply(lambda x: datetime.fromisoformat(x).date())
    data2 = data1[
        (data1['Date'] >= datetime(year[0], month, 1).date()) & (
                    data1['Date'] <= datetime(year[1], month, num_days).date())]
    high = data2['IV'].max()
    low = data2['IV'].min()
    high_date_data = str(data2.iloc[data2['IV'].argmax()]['Date'])
    low_date_data = str(data2.iloc[data2['IV'].argmin()]['Date'])
    high_expiry_date_data = str(data2.iloc[data2['IV'].argmax()]['Expiry'])
    low_expiry_date_data = str(data2.iloc[data2['IV'].argmin()]['Expiry'])
    high_days_to_expiry_data = str(data2.iloc[data2['IV'].argmax()]['days_to_expiry'])
    low_days_to_expiry_data = str(data2.iloc[data2['IV'].argmin()]['days_to_expiry'])
    high_underlying_data = str(data2.iloc[data2['IV'].argmax()]['Underlying'])
    low_underlying_data = str(data2.iloc[data2['IV'].argmin()]['Underlying'])
    high_strikeprice_data = str(data2.iloc[data2['IV'].argmax()]['Strike Price'])
    low_strikeprice_data = str(data2.iloc[data2['IV'].argmin()]['Strike Price'])
    range_data = round(high - low)
    live3 =  [
               html.H6(children = 'High IV of : ' + stock,
                       style={'textAlign': 'center',
                              'color': 'white'}
                       ),
               html.P('{0:,.0f}'.format(high),
                      style={'textAlign': 'center',
                             'color': '#FFFF00',
                             'fontSize': 40}
                      ),
               html.P('Date:  ' + ' ' + high_date_data,
                      style = {
                          'textAlign': 'center',
                          'color': 'white',
                          'fontSize': 15,
                          'margin-top': '-18px'}
                      ),
               html.P('Expiry Date:  ' + ' ' + high_expiry_date_data,
               style={
                   'textAlign': 'center',
                   'color': 'white',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               ),
               html.P('Days to Expiry:  ' + ' ' + high_days_to_expiry_data,
               style={
                   'textAlign': 'center',
                   'color': 'white',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               ),
                html.Br(),
                html.P('Underlying Price:  ' + ' ' + high_underlying_data,
                       style={
                           'textAlign': 'center',
                           'color': '#FFFF00',
                           'fontSize': 15,
                           'margin-top': '-18px'}
                       ),
                html.P('Strike Price:  ' + ' ' + high_strikeprice_data,
                       style={
                           'textAlign': 'center',
                           'color': '#FFFF00',
                           'fontSize': 15,
                           'margin-top': '-18px'}
                       )

    ]

    live4 = [
        html.H6(children='Low IV of : ' + stock,
                style={'textAlign': 'center',
                       'color': 'white'}
                ),
        html.P('{0:,.0f}'.format(low),
               style={'textAlign': 'center',
                      'color': '#ff3624',
                      'fontSize': 40}
               ),
        html.P('Date:  ' + ' ' + low_date_data,
               style={
                   'textAlign': 'center',
                   'color': 'white',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               ),
        html.P('Expiry Date:  ' + ' ' + low_expiry_date_data,
               style={
                   'textAlign': 'center',
                   'color': 'white',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               ),
        html.P('Days to Expiry:  ' + ' ' + low_days_to_expiry_data,
               style={
                   'textAlign': 'center',
                   'color': 'white',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               ),
        html.Br(),
        html.P('Underlying Price:  ' + ' ' + low_underlying_data,
               style={
                   'textAlign': 'center',
                   'color': '#ff3624',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               ),
        html.P('Strike Price:  ' + ' ' + low_strikeprice_data,
               style={
                   'textAlign': 'center',
                   'color': '#ff3624',
                   'fontSize': 15,
                   'margin-top': '-18px'}
               )

    ]

    return live3, live4
@callback([Output('candlestick_chart', 'figure')],
              [Output('volume_chart', 'figure')],
              [Output('log_chart', 'figure')],
              [Output('log_returns_chart', 'figure')],
              [Output('pie_chart', 'figure')],
              [Input('select_country', 'value')],
              [Input('slider_year', 'value')],
              [Input('radio_items', 'value')])

def update_graph(select_country, slider_year, radio_items):
    stock = select_country
    month = radio_items
    year = slider_year

    num_days = monthrange(year[0], month)[1]

    data = data_stock.copy()
    data1 = data[data['stock_name'] == stock]
    data2 = data1[
        (data1['trading_date'] >= datetime(year[0], month, 1)) & (data1['trading_date'] <= datetime(year[1], month, num_days))]


################################## PIE CHART ################################################################################3
    pie_data, pie_label = functions.returns(data_df = data2)

    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', '#f5700a', '#930af5', '#f50ab6']

    fig5 = go.Figure(data=[go.Pie(labels=pie_label,
                                 values=pie_data['Trend'].count())])
    fig5.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig5.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig5.update_layout(autosize=False, width = 360, height=400,
                      plot_bgcolor='#010915',
                      paper_bgcolor='#010915',
                      titlefont={'color': 'white', 'size': 20},
                      legend_font_color='white',
                      legend_font_size=10,
                      hovermode="x unified",
                      hoverlabel=dict(
                          bgcolor="#010915",
                          font_size=16,
                          font_family="Overpass",
                          font_color="white"
                      )
                      )



##########################################################################################################################

    log_returns = functions.log_returns(data_df = data2)
    fig2 = go.Figure()
    fig2.update_layout(autosize=False, width=700, height=350,
                       title=go.layout.Title(text="Returns of :" + " " + stock),
                       plot_bgcolor='#010915',
                       paper_bgcolor='#010915',
                       titlefont={'color': 'white', 'size': 20},
                       xaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5', 'showgrid' : False},
                       yaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5','showgrid' : False},
                       legend_font_color='white',
                       legend_font_size=10
                       )
    fig2.add_trace(go.Scatter(x=log_returns.index,y=log_returns,marker_color='#06FF00'))
    st_dev2 = np.std(log_returns.to_list())
    mean2 = np.mean(log_returns.to_list())
    fig2.add_hline(y=st_dev2, line_dash="dot",
                  annotation_text="Std.Dev return : " + str(st_dev2),
                  annotation_hovertext="Std.Dev return",
                  annotation_bgcolor="white",
                  annotation_position="top left",line_color='white')

    fig2.add_hline(y=mean2, line_dash="dot",
                   annotation_text="MEAN return : " + str(mean2),
                   annotation_hovertext = "MEAN return",
                   annotation_bgcolor="white",
                   annotation_position="top right", line_color='yellow')


    fig3 = px.histogram(x=log_returns)

    # fig3 = px.histogram(x=log_returns, color_discrete_sequence=['#31c48d'])
    # group_labels = ['Log Return distribution']  # name of the dataset
    # fig3 = ff.create_distplot([log_returns], group_labels,colors = ["#31c48d"])
    fig3.update_layout(autosize=False, width=600, height=350,
                       title=go.layout.Title(text="Returns of :" + " " + stock),
                       plot_bgcolor='#010915',
                       paper_bgcolor='#010915',
                       titlefont={'color': 'white', 'size': 20},
                       xaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5'},
                       yaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5'},
                       legend_font_color='white',
                       legend_font_size=10
                       )

    fig4 = px.bar(data2, x='trading_date', y='volume')
    fig4.update_layout(autosize=False, width=850, height=250,
                       plot_bgcolor='#010915',
                       paper_bgcolor='#010915',
                       titlefont={'color': 'white', 'size': 20},
                       xaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5', 'showgrid' : False},
                       yaxis={'color': 'white', 'gridwidth': 0.1, 'linecolor': 'white', 'linewidth': 1,
                              'gridcolor': '#e5e5e5', 'showgrid' : False},
                       legend_font_color='white',
                       legend_font_size=10
                       )

    fig = go.Figure(data=[go.Candlestick(x=data2['trading_date'],
                                             open=data2['open'],
                                             high=data2['high'],
                                             low=data2['low'],
                                             close=data2['close'])],

                    layout=go.Layout(
                        title=go.layout.Title(text="Historical data of :" + " " + stock),
                        plot_bgcolor='#010915',
                        paper_bgcolor='#010915',
                        titlefont={'color': 'white','size': 20},
                        xaxis= {'color' : 'white', 'gridwidth' : 0.1, 'linecolor' : '#C4F5FC', 'linewidth' : 1, 'gridcolor' : '#e5e5e5'},
                        yaxis = {'color': 'white', 'gridwidth' : 0.1, 'linecolor' : '#C4F5FC', 'linewidth' : 1, 'gridcolor' : '#e5e5e5'},
                        width = 850,
                        height = 500
                    )
                    )

    return fig,fig4,fig2,fig3,fig5

