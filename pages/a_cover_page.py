# THE FRONT COVER PAGE

# Import packages
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, callback, dcc

# Import functions

# Import pages
from pages import navigation

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/', name='Home')



# ------------------------------ LAYOUT --------------------------------
# Define the front page layout
layout = html.Div([
    navigation.navbar,
    html.Br(),
    dbc.Row([
        html.H5('''Welcome to FlaGs Viz. Here you can visualise your WebFlaGs
        results with or without domain search. Even make your own custom 
        protein logos with domains.''')
    ], style = {        
        'margin-left' : '40px',
        'margin-right' : '40px',
        'margin-top' : '40px'}),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(
                    src='./assets/option_0.png',  # Path to your black and white image
                    id='image1',
                    top=True,
                    className='hover-image',
                ),
                dbc.CardBody([
                        html.H4('Find Submission', className='card-title'),
                        html.P(
                            '''We're working on allowing you to access your 
                            runs directly from our server. Stay tuned.''',
                            className='card-text',
                        ),
                        dbc.Button(
                            'Loading...',
                            color='secondary',
                            #href='/find_submission',
                        ),
                    ]),
                ],
                style={'width': '22rem'},
                className='mb-3',
            ),
            width=3,
            align='center',
        ),
        dbc.Col(
            dbc.Card( [
                dbc.CardImg(
                    src='./assets/option_1.png', 
                    id='image2',
                    top=True,
                    className='hover-image',
                ),
                dbc.CardBody([
                        html.H4('Upload Local Files', className='card-title'),
                        html.P(
                            '''Did you run WebFlaGs with domain search? Or 
                            maybe not? You can view your your WebFlaGs 
                            results here.''',
                            className='card-text',
                        ),
                        dbc.Button(
                            'This one!',
                            color='primary',
                            href='/view_domains',
                        ),
                    ]),
                ],
                style={'width': '22rem'},
                className='mb-3',
            ),
            width=3,
            align='center',
        ),
        dbc.Col(
            dbc.Card( [
                dbc.CardImg(
                    src='./assets/option_2.png', 
                    id='image1',
                    top=True,
                    className='hover-image',
                ),
                dbc.CardBody([
                        html.H4('3 Domain Databases', className='card-title'),
                        html.P(
                            '''If you have your hands on a super special 
                            domain search file, you can see all the 
                            database domain hits here. ''',
                            className='card-text',
                        ),
                        dbc.Button(
                            'Take me here',
                            color='primary',
                            href='/3_databases',
                        ),
                    ]),
                ],
                style={'width': '22rem'},
                className='mb-3',
            ),
            width=3,
            align='center',
        ),
        dbc.Col(
            dbc.Card( [
                dbc.CardImg(
                    src='./assets/option_3.png',  # Path to your black and white image
                    id='image1',
                    top=True,
                    className='hover-image',
                ),
                dbc.CardBody([
                        html.H4('Create Logos', className='card-title'),
                        html.P(
                            '''When you need a quick custom protein logo
                            visualisation with domains
                            and/or mutataions.''',
                            className='card-text',
                        ),
                        dbc.Button(
                            "Let's Draw",
                            color='primary',
                            href='/create_logos',
                        ),
                    ]),
                ],
                style={'width': '22rem'},
                className='mb-3',
            ),
            width=3,
            align='center',
        ),
        # Repeat the above code for the other columns
    ], style={
        'margin-left' : '40px',
        'margin-right' : '40px',
        'margin-top' : '20px'
        }),
])
