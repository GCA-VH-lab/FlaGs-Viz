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
from functions.operon_plot import *

# Import layout specifics
from assets.color_scheme import *

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/upload_files')



# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
            navigation.navbar,
            dbc.Row([
                html.H4('Upload Files'),
                html.Hr(),
                html.P('''Browse for FlaGs resilt
                files on your local machine.''')
            ],  style={
                    'margin-left' : '20px',
                    'margin-top' : '5px',
                    'margin-bottom' : '10px',
                    'width': '80%', 
                    }),
            dbc.Row([
                dbc.Col([
                    html.H6('''Choose phylogenetic 
                    tree file (ladderTree.nw)'''),
                    dcc.Upload(
                        id = 'upload-phylo-file',
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
                    html.H6('''Choose operon file
                    (operon.tsv)'''),
                    dcc.Upload(
                        id = 'upload-operon-file',
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
            ],  style={
                    'margin-left' : '40px',
                    'margin-top' : '5px',
                    'margin-bottom' : '10px',
                    'width': '80%'}),
            dbc.Row([
                html.H4('Results'),
                html.Hr(),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div(id = 'server-phylo'),
                        ], width = 4),
                        dbc.Col(width = 1),
                        dbc.Col([
                            html.Div(id = 'server-operon'),
                        ],  width = 7),
                    ], style={
                        'margin-left' : '0px', 
                        'margin-top' : '5px',
                        'margin-bottom' : '5px',
                        'postion': 'relative', 
                        }),
                    dbc.Row([
                        dbc.Col([
                            html.Div(id = 'upload-phylo'),
                        ], width = 4),
                        dbc.Col(width = 1),
                        dbc.Col([
                            html.Div(id = 'upload-operon'),
                        ],  width = 7),
                    ], style={
                        'margin-left' : '0px', 
                        'margin-top' : '5px',
                        'margin-bottom' : '5px',
                        'postion': 'relative', 
                        })
                    ]),
            ], 
            className = 'h-auto',
            style={
                'margin-left' : '40px',
                'margin-top' : '60px',
                'margin-bottom' : '10px',
                'width': '96%'
                })
 ])


# ----------------------------- LAYOUT ---------------------------------

@callback(
    Output('upload-phylo', 'children'),
    Input('upload-phylo-file', 'contents'),
    State('upload-phylo-file', 'filename'),
    State('upload-phylo-file', 'last_modified'),
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
    Output('upload-operon', 'children'),
    Input('upload-operon-file', 'contents'),
    State('upload-operon-file', 'filename'),
    State('upload-operon-file', 'last_modified'),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    # Takes uploaded operon files by user and returns opeon plot with 
    # the function below
    if list_of_contents is not None:
        children = [
            generate_operon_plot(c, n, d) for c, n, d in 
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def generate_operon_plot(contents, filename, date):
    content_type, content_string = contents.split(',')    
    
    decoded = base64.b64decode(content_string)
    try:
        if 'tsv' in filename:
            operon_file = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter='\t', header=None)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
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
                                        'filename': filename,
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
