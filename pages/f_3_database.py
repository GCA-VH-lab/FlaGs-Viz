#PAGE 2: UPLOAD LOCAL FILES TO VISUALISE FLAGS RESULT

# Import packages
import dash 
from dash import html
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64
import io

# Import pages
from pages import navigation

# Import functions
from functions.multi_databases import *
from functions.operon_w_domains import *
from functions.operon_plot import *

# Import layout specifics
from assets.color_scheme import *

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/3_databases', name='3 Domain Databases')



# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
    navigation.navbar,
        dbc.Row([
            dbc.Container([
                html.H4('Upload Files'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.H6('Choose operon file (operon.tsv)'),
                        dcc.Upload(
                            id = 'upload-operon-file-3db',
                            children = html.Div([
                                'Drag and Drop or ',
                                html.A('Select File')]),
                            multiple = True,
                            style={
                                'width': '100%',
                                'height': '50px',
                                'lineHeight': '50px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                            })
                    ]),
                    dbc.Col([
                        html.H6('Choose domain search file (.out)'),
                        dcc.Upload(
                            id = 'upload-domain-file-3db',
                            children = html.Div([
                                'Drag and Drop or ',
                                html.A('Select File')]),
                            multiple = True,
                            style={
                                'width': '100%',
                                'height': '50px',
                                'lineHeight': '50px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                            })
                    ])
                ]),
            ],  style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                }),
        ], style={
            'padding':'40px',
        }),
        dbc.Row([
            dbc.Container([
                dbc.Row([
                    dbc.Row([
                        dbc.Col(
                            [
                                html.H4('Results'),
                                dbc.Tooltip(
                                    '''The order of the databases from 
                                    top the bottom is PFAM, Pdb, and CDD ''',
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
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dcc.Loading(
                                    html.Div(id = 'results-3db')
                                )
                            ], style={
                                'margin-left' : '0px', 
                                'margin-top' : '5px',
                                'margin-bottom' : '5px',
                                'postion': 'relative', 
                                }),
                            ], align='left',),
                    ]),
                ], 
                className = 'h-auto'),
            ],  style={
                    'background-color': page_background,
                    'border-radius': '10px', 
                    'padding':'20px',
                }),
        ], style={
            'padding':'40px',
            }
        ),        
 ])


# ----------------------------- LAYOUT ---------------------------------


@callback(
    Output('results-3db', 'children'),
    Input('upload-operon-file-3db', 'contents'),
    State('upload-operon-file-3db', 'filename'),
    State('upload-operon-file-3db', 'last_modified'),
    Input('upload-domain-file-3db', 'contents'),
    State('upload-domain-file-3db', 'filename'),
    State('upload-domain-file-3db', 'last_modified')
)
def update_output(operon_contents, operon_names, operon_dates, domain_contents, domain_names, domain_dates):
   
    if operon_contents is not None and domain_contents is not None:
        operon_file = parse_file_contents(operon_contents[0], operon_names[0])
        domain_file = parse_file_contents(domain_contents[0], domain_names[0])
        return html.Div([
                    dcc.Graph(
                        id = 'operon-plot',
                        animate = False,
                        responsive = True,
                        figure = create_3db(operon_file, domain_file),
                        style = {
                            'display': 'block',
                            'margin-left': '0px', 
                            'margin-top': '10px',
                            'margin-bottom': '10px',
                            'height': get_operon_graph_dimensions(operon_file)
                        },
                        config = {
                                'displaylogo': False,
                                'toImageButtonOptions': {
                                        'format': 'svg',
                                        'filename': operon_names[0],
                                        'scale': 1}
                                }
                    )
                ], style={
                    'margin-left' : '0px', 
                    'margin-top' : '50px',
                    'margin-bottom' : '10px',
                    'postion': 'relative', 
                    'width': '100%',
                    'top': 0,
                    'z-index': 0}
            )
    else:
        return {}


