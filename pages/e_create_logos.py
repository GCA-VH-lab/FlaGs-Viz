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
import urllib

# Import pages
from pages import navigation

# Import functions
from functions.drawing_logos import *

# Import layout specifics
from assets.color_scheme import *


# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/create_logos')




# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
    html.Link(href='../assets/custom.css'),
    navigation.navbar,
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Col(
                        html.H6('Gene Start:')
                    ),
                    dbc.Col(
                        html.H6('Length (aa):')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id='input-length', 
                            type='number', 
                            value=100, 
                            style={'width': '80px'}
                        )
                    )
                ], style={
                    'width': 4,
                    'padding': '20px'
                }),
                dbc.Col([
                    html.Label('Gene Color:'),
                    daq.ColorPicker(
                        id='input-color',
                        value={'hex': '#000000'}
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
                            id='input-domain-start',
                            type='number',
                            value=1,
                            style={'width': '80px'}
                        )
                    ),
                    dbc.Col(
                        html.H6('Domain End:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id='input-domain-end',
                            type='number',
                            value=20,
                            style={'width': '80px'}
                        )
                    ),
                    dbc.Col(
                        html.H6('Domain Name:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id='input-domain-name',
                            type='text',
                            value=''
                        )
                    ),
                    dbc.Col(
                        html.Button(
                            'Add Domain', 
                            id='button-add-domain', 
                            style={'margin-left': '20px'})
                    ),
                ], style={
                    'width': 3,
                    'padding': '20px'
                }),
                dbc.Col([
                    html.Label('Domain Color:'),
                    daq.ColorPicker(
                        id='input-domain-color',
                        value={'hex': '#000000'}
                    ),
                ], style={
                    'width': 2,
                    'padding': '20px'
                })
            ], style={'padding': '20px'}),
            html.Hr(),
            dbc.Row(
                html.Div(id='domain-table-container')
            ), 
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Col(
                        html.H6('Mutation Name:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id='input-mutation-name',
                            type='text',
                            value=''
                        )
                    ),
                    dbc.Col(
                        html.H6('Mutation Position:')
                    ),
                    dbc.Col(
                        dcc.Input(
                            id='input-mutation-position',
                            type='number',
                            value=''
                        )
                    ),
                    dbc.Col(
                        html.Button(
                            'Add Mutation', 
                            id='button-add-mutation', 
                            style={'margin-left': '20px'})
                    ),
                ], style={
                    'width': 3,
                    'padding': '20px'
                })
            ]),
            html.Hr(),
            dbc.Row(
                html.Div(id='mutation-table-container')
            ), 
            dbc.Row([
                html.Button(
                    'Create Logo', 
                    id='button-create',
                    style={'padding':'10px'}
                )
        ],  style={'padding' : '20px'}),
            dbc.Row([
                html.Button(
                    'Download Logo', 
                    id='button-download',
                    style={'padding':'10px'}
                )
        ],  style={'padding' : '20px'})
        ], width={
            'size': 4,
            'offset': 0},
            style={
                'height': '90vh',
                'background': container_background}),
        dbc.Col([], style={'width': 1}),
        dbc.Col([
            dcc.Graph(id='arrow-output'),
        ], width={
            'size': 7,
            'offset': 0},
            style={
                'height': '90vh',
                'background': container_background})
    ], style={'padding': '60px'})
])




# ------------------------------ LISTS ---------------------------------

# List to store the added domains
domains = []
mutations = []

# Define the domain table columns
# domain_columns = [
#     {'name': 'Domain Name', 'id': 'name'},
#     {'name': 'Domain Start', 'id': 'start'},
#     {'name': 'Domain End', 'id': 'end'},
#     {'name': 'Domain Color', 'id': 'color'},
#     {'name': '', 'id': 'remove', 'presentation': 'markdown'}
# ]


# --------------------------- CALLBACKS --------------------------------


@callback(
    Output('mutation-table-container', 'children'),
    [Input('button-add-mutation', 'n_clicks')],
    [
        State('input-mutation-name', 'value'),
        State('input-mutation-position', 'value'),
    ],
)
def update_domain_table(n_clicks, mutation_name, mutation_position):
    if n_clicks:
        # Create a new mutation dictionary
        mutation = {
            'Name': mutation_name,
            'Position': mutation_position,
        }
        # Append the mutation to the list
        mutations.append(mutation)

    # Create the table data
    table_data = pd.DataFrame(mutations)

    # Create the table
    table = dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in table_data.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(248, 248, 248)',
            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(230, 230, 230)',
            },
        ],
    )

    return table






@callback(
    Output('domain-table-container', 'children'),
    [Input('button-add-domain', 'n_clicks')],
    [
        State('input-domain-start', 'value'),
        State('input-domain-end', 'value'),
        State('input-domain-name', 'value'),
        State('input-domain-color', 'value'),
    ],
)
def update_domain_table(n_clicks, domain_start, domain_end, domain_name, domain_color):
    if n_clicks:
        # Create a new domain dictionary
        domain = {
            'Name': domain_name,
            'Start': domain_start,
            'End': domain_end,
            'Color': domain_color['hex'],
        }
        # Append the domain to the list
        domains.append(domain)

    # Create the table data
    table_data = pd.DataFrame(domains)

    # Create the table
    table = dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in table_data.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(248, 248, 248)',
            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(230, 230, 230)',
            },
        ],
    )

    return table







@callback(
    Output('arrow-output', 'figure'),
    [
        Input('button-create', 'n_clicks'), 
        Input('domain-table-container', 'children')
    ],
    [
        State('input-length', 'value'), 
        State('input-color', 'value')
     ]
)
def generate_arrow(n_clicks, domains, length, logo_color):
    if n_clicks is None:
        return {}

    data = domains['props']['data']
    domains_list = pd.DataFrame(data)

    # Create the arrow using Matplotlib
    logo = create_fig(length, logo_color, domains_list)

    # Return the figure as a dictionary for Dash graph
    return logo 




@callback(
    Output('button-download', 'href'),
    Input('button-download', 'n_clicks')
)
def download_svg(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return 'data:image/svg+xml;charset=utf-8,' + urllib.parse.quote(get_svg_data(), safe='')

def get_svg_data():
    # Generate the SVG data for the arrow shape
    svg_data = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' \
               '<path d="M0,0 L90,0 L100,50 L90,100 L0,100 Z" fill="black" stroke="black" stroke-width="1" />' \
               '</svg>'
    return svg_data