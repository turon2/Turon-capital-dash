import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app import app
import functions


# app = dash.Dash(__name__, meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}], external_stylesheets=[dbc.themes.CYBORG])
from apps import index,screener

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
# dropdown = dbc.DropdownMenu(
#     children=[
#         dbc.DropdownMenuItem("Home", href="/home"),
#         dbc.DropdownMenuItem("Index", href="/index"),
#         dbc.DropdownMenuItem("Screener", href="/screener"),
#     ],
#     nav = True,
#     in_navbar = True,
#     menu_variant="dark",
#     label = "Explore",
# )
#
# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#             html.A(
#                 # Use row and col to control vertical alignment of logo / brand
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Img(src="/assets/lognormal.png", height="100px"),lg = 3,width = 6),
#                         dbc.Col(dbc.NavbarBrand("Turon Capital"),lg = 12,width = 6),
#                     ],
#                     align="left",
#                     # no_gutters=True,
#                 ),
#                 href="/home",
#             ),
#             dbc.NavbarToggler(id="navbar-toggler2"),
#             dbc.Collapse(
#                 dbc.Nav(
#                     # right align dropdown menu with ml-auto className
#                     [dropdown], className="ml-auto", navbar=True
#                 ),
#                 id="navbar-collapse2",
#                 navbar=True,
#             ),
#         ]
#     ),
#     color="dark",
#     dark=True,
#     className="mb-2",
# )
#
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
#
# for i in [2]:
#     app.callback(
#         Output(f"navbar-collapse{i}", "is_open"),
#         [Input(f"navbar-toggler{i}", "n_clicks")],
#         [State(f"navbar-collapse{i}", "is_open")],
#     )(toggle_navbar_collapse)
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="/home")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="/index"),
#                 dbc.DropdownMenuItem("Page 3", href="/screener"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="Turon Capital",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )
navbar = html.Div([
            dbc.Row([
                dbc.Col(html.Img(src="/assets/final.png", height="105px"),lg = 3,width = 6),
                dbc.Col(dbc.Button("HOME", color="success", className="inline-block", outline = True, href = "/home")),
                dbc.Col(dbc.Button("MAIN", color="success", className="inline-block", outline = True, href = "/home")),
                dbc.Col(dbc.Button("SCREENER", color="success", className="inline-block", outline = True, href = "/screener")),
                dbc.Col(dbc.Button("ABOUT US", color="success", className="inline-block", outline = True, href = "/index")),
            ]),
            # dbc.Row([
            #     # dbc.Col(html.Img(src="/assets/try.png", height="205px"),lg = 3,width = 6),
            #     dbc.Col(dbc.Button("HOME", color="success", className="inline-block", outline = True, href = "/home")),
            #     dbc.Col(dbc.Button("MAIN", color="success", className="inline-block", outline = True, href = "/home")),
            #     dbc.Col(dbc.Button("SCREENER", color="success", className="inline-block", outline = True, href = "/screener")),
            #     dbc.Col(dbc.Button("ABOUT US", color="success", className="inline-block", outline = True, href = "/index")),
            # ]),
            # html.Div([
            # # dbc.Button("Success", color="success", className="me-1", outline = True),
            # dbc.Button("Success", color="success", className="me-2", outline = True),
            # ],className = "inline-block"),
        ], className="create_container")
# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/index':
        return index.layout
    elif pathname == '/screener':
        df = functions.screen()
        print(df.columns)
        return screener.layout
    else:
        return index.layout

app = app.server

if __name__ == '__main__':
    app.run(debug=True)