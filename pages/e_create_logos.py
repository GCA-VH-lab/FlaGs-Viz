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

dash.register_page(__name__, path = '/create_logos', name='Create Logos')





# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
    html.Link(href='../assets/custom.css'),
    navigation.navbar,
    dbc.Row([
        dbc.Col([
            dbc.Container([
                dbc.Row([
                    html.H5('Base'),
                    html.Br(),
                    dbc.Col([
                        'Length (aa):',
                        dcc.Input(
                            id='input-length', 
                            type='number', 
                            value=100)
                    ]),
                    dbc.Col([
                        html.Label('Gene Color:'),
                        daq.ColorPicker(
                            id='input-color',
                            value={'rgb': {'r': 237, 'g': 237, 'b': 237, 'a': 1}}
                        ),
                    ])
                ]),
            ],  style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                    'margin-top': '20px'
                },
            ),
            dbc.Row(),
            dbc.Container([
                dbc.Row([
                    html.H5('Domains'),
                    dbc.Col([
                        dbc.Row([
                            'Domain Start:', 
                            dcc.Input(
                                id='input-domain-start',
                                type='number',
                                value=1,
                            )
                        ]),
                        dbc.Row([
                            'Domain End:',
                            dcc.Input(
                                id='input-domain-end',
                                type='number',
                                value=20
                            )
                        ], style={'margin-top':'20px'}),
                        dbc.Row([
                            'Domain Name:', 
                            dcc.Input(
                                id='input-domain-name',
                                type='text',
                                value=''
                            )
                        ], style={'margin-top':'20px'}),
                        dbc.Button(
                            'Add Domain', 
                            id='button-add-domain',
                            color = 'secondary',
                            outline = False,
                            style={'margin-top':'30px'}
                        )
                    ], style={
                        'margin-left': '10px',
                        'margin-right': '20px'}),
                    dbc.Col([
                        html.Label('Domain Color:'),
                        daq.ColorPicker(
                            id='input-domain-color',
                            value={'rgb': {'r': 98, 'g': 220, 'b': 209, 'a': 0.45}}
                        ),
                    ])
                ]),
            ], style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                    'margin-top': '20px'
                }),
            dbc.Container([
                html.H5('Mutations'),
                dbc.Row([
                    dbc.Col([
                        'Name:',
                        dcc.Input(
                            id='input-mutation-name',
                            type='text',
                            value='',
                        )
                    ], width=4),
                    dbc.Col(width=1),
                    dbc.Col([
                        'Position:',
                        dcc.Input(
                            id='input-mutation-position',
                            type='number',
                            value='',
                        ),
                    ], width=4),
                    dbc.Col(width=1),
                    dbc.Col([
                        dbc.Button(
                            'Add', 
                            id='button-add-mutation',
                            color = 'secondary',
                            outline = False,
                            style={'margin-top':'20px'}
                        )
                    ], width=2),
                ])
            ], style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                    'margin-top': '20px'
            }),
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        'Reset', 
                        id='button-reset',
                        color = 'danger',
                        outline = True,
                        style={'width': '100%'}
                    )
                ],  width=5),
                dbc.Col(width=1),
                dbc.Col([
                    dbc.Button(
                        'Create Logo', 
                        id='button-create',
                        color = 'dark',
                        outline = False,
                        style={'width': '100%'}
                    )
                ],  width=5),
            ], style={
                'padding': '10px',
                'margin-left':'10px',
                'margin-top':'30px',
                'justify':'10px'}),
        ], width={
            'size': 4,
            'offset': 0},
            style={
                'height': '95-120vh',
                'background': container_background,
                'border-radius': '10px'}),
        dbc.Col([], style={'width': 1}),
        dbc.Col([
            dbc.Container([
                dbc.Col(
                    [
                        dbc.Tooltip(
                            '''To download the logo, bring your cursor
                            to the upper right side of the 
                            plot area until the tool bar displays, 
                            then click on the camera icon.''',
                            target='info-icon',
                            placement='auto',
                            trigger='hover',
                        ),
                    ], width=11
                ),
                dbc.Col(
                    dbc.Col(
                        dbc.Button(
                            '?',
                            id='info-icon',
                            color='primary',
                            outline=True,
                            className='rounded-circle',
                            style={'font-size': '24px', 'cursor': 'pointer'},
                        ),
                    ),
                ),
                dcc.Loading(
                    dcc.Graph(
                        id='arrow-output', 
                        style={'margin-top': '20px'},
                        config={"toImageButtonOptions": {"format": "svg", "filename": "protein_logo"}}
                    )
                )
            ],  style={
                    'background-color': white,
                    'border-radius': '10px', 
                    'padding':'20px',
                    'margin-top': '20px'}
            ),
            dbc.Row(),
            dbc.Container(
                'Domains',
                id='domain-table-container',
                style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                    'margin-top': '20px'} 
            ),
            dbc.Row(),
            dbc.Container(
                'Mutations',
                id='mutation-table-container',
                style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                    'margin-top': '20px'} 
            ),
        ], width={
            'size': 7,
            'offset': 0},
            style={
                'height': '95-120vh',
                'background': container_background,
                'border-radius': '10px', })
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
    [Input('button-reset', 'n_clicks')],
    [
        State('input-mutation-name', 'value'),
        State('input-mutation-position', 'value'),
    ],
)
def update_mutation_table(n_clicks, reset_clicks, mutation_name, mutation_position):
    if reset_clicks and reset_clicks > 0:
        # Reset the mutations list to an empty list
        mutations.clear()
        # Return an empty div to clear the table
        return html.Div()

    if n_clicks and n_clicks > 0:
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
        style_table={
            'overflowX': 'auto',
            'font-family': 'Helvetica',
            'border': '1px solid black'
        },
        style_cell={
            'textAlign': 'center',
            'font-family': 'Helvetica',
            'border': '1px solid black'
        },
        style_header={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font-family': 'Helvetica',
            'border': '1px solid black'
        },
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
    [Input('button-reset', 'n_clicks')],
    [
        State('input-domain-start', 'value'),
        State('input-domain-end', 'value'),
        State('input-domain-name', 'value'),
        State('input-domain-color', 'value'),
    ],
)
def update_domain_table(n_clicks, reset_clicks, domain_start, domain_end, domain_name, domain_color):
    if reset_clicks and reset_clicks > 0:
        # Reset the domains list to an empty list
        domains.clear()
        # Return an empty div to clear the table
        return html.Div()

    if n_clicks and n_clicks > 0:
        # Create a new domain dictionary
        domain = {
            'Name': domain_name,
            'Start': domain_start,
            'End': domain_end,
            'Color': rgba_to_hex(domain_color['rgb']),
        }
        # Append the domain to the list
        domains.append(domain)

    # Create the table data
    table_data = pd.DataFrame(domains)

    # Create the table
    table = dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in table_data.columns],
        style_table={
            'overflowX': 'auto',
            'font-family': 'Helvetica',
            'border': '1px solid black'
        },
        style_cell={
            'textAlign': 'center',
            'font-family': 'Helvetica',
            'border': '1px solid black'
        },
        style_header={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font-family': 'Helvetica',
            'border': '1px solid black'
        },
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
        Input('domain-table-container', 'children'), 
        Input('mutation-table-container', 'children'),
        Input('button-reset', 'n_clicks')
    ],
    [
        State('input-length', 'value'), 
        State('input-color', 'value')
     ]
)
def generate_arrow(n_clicks, domains, mutations, reset_clicks, length, logo_color):
    if reset_clicks and reset_clicks > 0:
        return placeholder_graph()

    if n_clicks is None:
        return placeholder_graph()

    data_domains = domains['props']['data']
    domains_list = pd.DataFrame(data_domains)

    data_mutations = mutations['props']['data']
    mutations_list = pd.DataFrame(data_mutations)

    # Create the arrow using Matplotlib
    logo = create_fig(length, logo_color, domains_list, mutations_list)

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



    
