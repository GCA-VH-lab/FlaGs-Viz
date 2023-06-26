# PAGE 2: UPLOAD LOCAL FILES TO VISUALISE FLAGS RESULT

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
from functions.phylogeny_tree import *
from functions.operon_w_domains import *
from functions.operon_plot import *

# Import layout specifics
from assets.color_scheme import *

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/view_domains', name='FlaGs Domain Search')




# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
    navigation.navbar,
        dbc.Row([
            dbc.Container([
                html.H4('Upload Files'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.H6('Choose phylogenetic tree file (ladderTree.nw)'),
                        dcc.Upload(
                            id = 'upload-phylo-file-domains',
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
                            }),
                    ]),
                    dbc.Col([
                        html.H6('Choose operon file (operon.tsv)'),
                        dcc.Upload(
                            id = 'upload-operon-file-domains',
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
                        html.H6('Choose domain search file (dom_out.txt)'),
                        dcc.Upload(
                            id = 'upload-domain-file-domains',
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
                        dbc.Col(
                            [
                                html.H4('Results'),
                                dbc.Tooltip(
                                    '''If no domain file is uploaded, 
                                    the original FlaGs output will be 
                                    displayed. Hover over proteins for 
                                    more info.''',
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
                            dbc.Col([
                                dcc.Loading(
                                    html.Div(id = 'upload-phylo-domains'),
                                )
                            ], width = 4),
                            dbc.Col(width = 1),
                            dbc.Col([
                                dcc.Loading(
                                    html.Div(id = 'upload-operon-domains'),
                                )
                            ],  width = 7),
                        ], style={
                            'margin-left' : '0px', 
                            'margin-top' : '5px',
                            'margin-bottom' : '5px',
                            'postion': 'relative', 
                            }),
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
    Output('upload-phylo-domains', 'children'),
    Input('upload-phylo-file-domains', 'contents'),
    State('upload-phylo-file-domains', 'filename'),
    State('upload-phylo-file-domains', 'last_modified'),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    # Takes uploaded phylo files by user and returns phylo plot with 
    # the function below
    if list_of_contents is not None:
        children = [
            generate_phylo_plot(c, n, d) for c, n, d in 
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def generate_phylo_plot(contents, filename, date):
    # Reads the uploaded file into the application, decodes, and returns
    # the phylo tree container.
    content_type, content_string = contents.split(',')    
    decoded = base64.b64decode(content_string)
    try:
        if 'nw' in filename:
            tree = Phylo.read(io.StringIO(decoded.decode('utf-8')), 'newick')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
                    dcc.Graph(
                        id = 'phylo-plot',
                        animate = False,
                        responsive = True,
                        figure = get_tree_plot(tree),
                        style = {
                            'display': 'block',
                            'margin-left': '10px', 
                            'margin-top': '0px',
                            'margin-bottom': '10px',
                            'height': generate_phylo_dimensions(tree)
                        },
                    config = {
                            'displaylogo': False,
                            'toImageButtonOptions': {
                                    'format': 'svg',
                                    'filename': filename,
                                    'scale': 1}
                            }
                    )
                ], style={
                    'margin-left' : '0px', 
                    'margin-top' : '50px',
                    'margin-bottom' : '10px',
                    'postion': 'relative', 
                    'top': 0,
                    'z-index': 0})



@callback(
    Output('upload-operon-domains', 'children'),
    Input('upload-operon-file-domains', 'contents'),
    State('upload-operon-file-domains', 'filename'),
    State('upload-operon-file-domains', 'last_modified'),
    Input('upload-domain-file-domains', 'contents'),
    State('upload-domain-file-domains', 'filename'),
    State('upload-domain-file-domains', 'last_modified')
)
def update_output(operon_contents, operon_names, operon_dates, domain_contents, domain_names, domain_dates):
   
    # Takes input for for phylo and operons, domains not uploaded
    if operon_contents is not None and domain_contents is None:
        operon_file = parse_file_contents(operon_contents[0], operon_names[0])
        return html.Div([
                    dcc.Graph(
                        id = 'operon-plot',
                        animate = False,
                        responsive = True,
                        figure = generate_operon(operon_file),
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

    # Takes input for for phylo, operons, and domains
    if operon_contents is not None and domain_contents is not None:
        operon_file = parse_file_contents(operon_contents[0], operon_names[0])
        domain_file = parse_file_contents(domain_contents[0], domain_names[0])
        return html.Div([
                    dcc.Graph(
                        id = 'operon-plot',
                        animate = False,
                        responsive = True,
                        figure = generate_plot_domains(operon_file, domain_file),
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




    