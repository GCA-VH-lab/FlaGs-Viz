# PAGE 4 - CREATING LOGOS

# Import packages
import dash 
from dash import html, dcc, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_daq as daq
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

# Import pages
from pages import navigation

# Import functions
from functions.drawing_logos import *

# Import layout specifics
from assets.color_scheme import *

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/create_logos')



# List to store the added domains
domains = []

# Define the domain table columns
domain_columns = [
    {"name": "Domain Name", "id": "name"},
    {"name": "Domain Start", "id": "start"},
    {"name": "Domain End", "id": "end"},
    {"name": "Domain Color", "id": "color"},
    {"name": "", "id": "remove", "presentation": "markdown"}
]



# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
    navigation.navbar,
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Col(
                        html.H6('Gene Start:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-start", 
                            type="number", 
                            value=1, 
                            style={'width': '80px'}
                        )
                    ),
                    dbc.Col(
                        html.H6('Gene End:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-end", 
                            type="number", 
                            value=100, 
                            style={'width': '80px'}
                        )
                    )
                ], style={
                    'width': 4,
                    'padding': '20px'
                }),
                dbc.Col([
                    html.Label("Arrow Color:"),
                    daq.ColorPicker(
                        id="input-color",
                        value={"hex": "#000000"}
                    ),
                ], style={
                    'width': 2,
                    'padding': '20px'
                })
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Col(
                        html.H6('Domain Start:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-domain-start",
                            type="number",
                            value=1,
                            style={'width': '80px'}
                        )
                    ),
                    dbc.Col(
                        html.H6('Domain End:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-domain-end",
                            type="number",
                            value=20,
                            style={'width': '80px'}
                        )
                    ),
                    dbc.Col(
                        html.H6('Domain Name:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-domain-name",
                            type="text",
                            value=""
                        )
                    ),
                    dbc.Col(
                        html.Button(
                            "Add Domain", 
                            id="button-add-domain", 
                            style={'margin-left': '20px'})
                    ),
                ], style={
                    'width': 3,
                    'padding': '20px'
                }),
                dbc.Col([
                    dbc.Col(
                        html.Label("Domain Color:"),
                        style={'margin-left': '20px'}
                    ),
                    dbc.Col(
                        daq.ColorPicker(
                            id="input-domain-color",
                            value={"hex": "#FF0000"}
                        )
                    ),
                ], style={
                    'width': 2,
                    'padding': '20px'
                }),
            ], style={'padding': '20px'}),
            dbc.Row(html.Div(id="domain-table-container")), 
            dbc.Row(html.Button("Generate Arrow", id="button-generate"))
        ], width={
            'size': 4,
            'offset': 0},
            style={
                'height': '90vh',
                'background': container_background}),
        dbc.Col([], style={'width': 1}),
        dbc.Col([
            dcc.Graph(id="arrow-output"),
        ], width={
            'size': 7,
            'offset': 0},
            style={
                'height': '90vh',
                'background': container_background})
    ], style={'padding': '60px'})
])





@callback(
    Output("arrow-output", "figure"),
    [
        Input("button-generate", "n_clicks"),
        Input('input-color', 'value')
    ],
    [State("input-start", "value"),
     State("input-end", "value")]
)
def generate_arrow(n_clicks, start, end):
    if n_clicks is None:
        return {}

    # Create the arrow using Matplotlib
    logo = create_fig(start, end)

    # Return the figure as a dictionary for Dash graph
    return logo 




@callback(
    dash.dependencies.Output("domain-table-container", "children"),
    [dash.dependencies.Input("button-add-domain", "n_clicks")],
    [
        dash.dependencies.State("input-domain-start", "value"),
        dash.dependencies.State("input-domain-end", "value"),
        dash.dependencies.State("input-domain-name", "value"),
        dash.dependencies.State("input-domain-color", "value"),
    ],
)
def update_domain_table(n_clicks, domain_start, domain_end, domain_name, domain_color):
    if n_clicks:
        # Create a new domain dictionary
        domain = {
            "Name": domain_name,
            "Start": domain_start,
            "End": domain_end,
            "Color": domain_color["hex"],
        }
        # Append the domain to the list
        domains.append(domain)

    # Create the table data
    table_data = pd.DataFrame(domains)

    # Create the table
    table = dash_table.DataTable(
        data=table_data.to_dict("records"),
        columns=[{"name": col, "id": col} for col in table_data.columns],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
        style_data_conditional=[
            {
                "if": {"row_index": "even"},
                "backgroundColor": "rgb(248, 248, 248)",
            },
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "rgb(230, 230, 230)",
            },
        ],
    )

    return table


