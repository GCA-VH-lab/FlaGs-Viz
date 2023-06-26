# PAGE 1: FIND SERVER STORED SUBMISSIONS

# Import packages
import dash 
from dash import html
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


# Import pages
from pages import navigation

# Import functions
from functions.acessing_server import *
from functions.fetching_server_data import *
from functions.phylogeny_tree import *
from functions.operon_plot import *


# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/find_submission', name='Submissions')




# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
            navigation.navbar,
            dbc.Row([
                html.H4('Find Your Submission'),
                html.Hr(),
                dbc.Row([
                    html.P('''Search for your FlaGs 
                    submission with your e-mail
                    address.
                    Please note that we store each store
                    each submission for a limited time
                    only. If you cannot find them use 
                    the option below of uploading the 
                    results sent to your e-mail instead. 
                    ''')
                ],  style={
                        'margin-left' : '20px',
                        'margin-top' : '50px',
                        'margin-bottom' : '10px',
                        'width': '70%', 
                        }),
                dbc.Row([
                    dbc.Col([
                        dcc.Input(
                            id = 'insert-email',
                            placeholder = ' example@mail.com',
                            style = {
                                'margin-left' : '0px',
                                'margin-bottom': '10px',
                                'width': '100%',
                                'height': '40px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderRadius': '5px',
                                'textAlign': 'left'
                            }
                        ), 
                    ]),
                    dbc.Col([
                        dbc.Button(
                            'Search',
                            id = 'upload-submission',
                            className='mb-3',
                            color = 'dark',
                            outline = True,
                            n_clicks = 0,
                            style = {
                                'height': '40px',
                            })
                        ]),
                    dbc.Col([
                        html.Div(id = 'runs')
                    ],  style = {'margin-left' : '0px'}),
                ], style = {
                    'margin-left' : '40px',
                    'margin-top' : '5px',
                    'margin-bottom' : '10px',
                    'width': '80%'})           
        ], style={
        'margin-left' : '40px',
        'margin-top' : '60px',
        'margin-bottom' : '10px',
        'width': '96%'
        }),
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
                }
        )
    ]
) 




# ------------------------------ ACTIONS -------------------------------

# ACTION 1: Submitting search using e-mail address
@callback(
    Output('runs', 'children'),
    [  
        Input('insert-email', 'value'),
        Input('upload-submission', 'n_clicks'),
    ]
)
def find_submission(value, n_clicks):
    # Takes the user input e-mail input and checks for (1) correct 
    # email format, (2) if the email has been used for FlaGs submissions,
    # (3) if there are any runs stored for the give e-mail. In the case
    # that there are runs, it returns a dropdown menu with all stored runs
    changed_id = [p['prop_id'] for p in ctx.triggered][0]   # Reset n_clicks
    if 'upload-submission' in changed_id:
        # Check if proper email address is inserted
        if '@' not in value:
            children = html.Div(
                            dbc.Col([
                                dbc.Alert('''
                                    The e-mail format is not accepted.
                                    ''',
                                    color = 'danger',
                                    style = {
                                        'height': '40px',
                                        'width': '480px',
                                        'textAlign': 'center', 
                                        'padding': '8px'
                                    }
                                )
                            ])
                        )
            return children
        else:
            # Check if email has been used to get FlaGs results
            all_runs = submission_lists(value)[0]
            options_list = submission_lists(value)[1]
            if len(all_runs) == 0:
                children = html.Div(
                            dbc.Col([
                                dbc.Alert('''
                                    The e-mail address did not match any of 
                                    our stored results. Please use the
                                    the same e-mail address as for your FlaGs 
                                    submission.
                                    ''',
                                    color = 'warning',
                                    style = {
                                        'height': '65px',
                                        'width': '480px',
                                        'textAlign': 'left-center', 
                                        'padding': '8px'
                                    }
                                )
                            ])
                        )
            else:
                # Check if there are any server stored runs for email
                if len(options_list) == 0:
                    children = html.Div(
                            dbc.Col([
                                dbc.Alert('''
                                    There are currently no results
                                    stored on our server associated with
                                    this e-mail address. Try uploading the 
                                    FlaGs result files below instead.
                                    ''',
                                    color = 'info',
                                    style = {
                                        'height': '65px',
                                        'width': '480px',
                                        'textAlign': 'left-center', 
                                        'padding': '8px'
                                    }
                                )
                            ])
                        )
                else:
                    children = html.Div(
                                dbc.Col([
                                    dcc.Dropdown(
                                        id = 'submissions',
                                        options = options_list,
                                        placeholder = '''Please select a 
                                        submission to view''',
                                        style = {
                                            'width': '280px',
                                            'height': '40px',
                                            'textAlign': 'center',
                                            'borderRadius': '5px'})
                                ])
                            )
            return children