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

dash.register_page(__name__, path = '/')



# ------------------------------ LAYOUT --------------------------------
# Define the front page layout
layout = html.Div([
    navigation.navbar,
    dbc.Row([
        html.H5('''Welcome to Flags Viz. You can either try to find recent runs
        stored on the server or upload your own. Or maybe even mamke your own 
        genes and domains''')
    ], style = {        
        'margin-left' : '40px',
        'margin-right' : '40px',
        'margin-top' : '40px'}),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(
                    src="./assets/04_b&w.png",  # Path to your black and white image
                    id="image1",
                    top=True,
                    className="hover-image",
                ),
                dbc.CardBody([
                        html.H4("Find Submission", className="card-title"),
                        html.P(
                            '''Recently run WebFlags? You may access your
                            submission if it is still stored on our server''',
                            className="card-text",
                        ),
                        dbc.Button(
                            "Let's Go",
                            color="primary",
                            href="/find_submission",
                        ),
                    ]),
                ],
                style={"width": "22rem"},
                className="mb-3",
            ),
            width=3,
            align="center",
        ),
        dbc.Col(
            dbc.Card( [
                dbc.CardImg(
                    src="./assets/04_b&w.png",  # Path to your black and white image
                    id="image2",
                    top=True,
                    className="hover-image",
                ),
                dbc.CardBody([
                        html.H4("Upload Files", className="card-title"),
                        html.P(
                            '''Couldn't find your submission or you have older
                            WebFlags runs, upload and view them here''',
                            className="card-text",
                        ),
                        dbc.Button(
                            "Let's Go",
                            color="primary",
                            href="/upload_files",
                        ),
                    ]),
                ],
                style={"width": "22rem"},
                className="mb-3",
            ),
            width=3,
            align="center",
        ),
        dbc.Col(
            dbc.Card( [
                dbc.CardImg(
                    src="./assets/04_b&w.png",  # Path to your black and white image
                    id="image1",
                    top=True,
                    className="hover-image",
                ),
                dbc.CardBody([
                        html.H4("View Domains", className="card-title"),
                        html.P(
                            '''Did you run WebFlags with the domain search?
                            Then you can view and interact with them here ''',
                            className="card-text",
                        ),
                        dbc.Button(
                            "Let's Go",
                            color="primary",
                            href="/view_domains",
                        ),
                    ]),
                ],
                style={"width": "22rem"},
                className="mb-3",
            ),
            width=3,
            align="center",
        ),
        dbc.Col(
            dbc.Card( [
                dbc.CardImg(
                    src="./assets/04_b&w.png",  # Path to your black and white image
                    id="image1",
                    top=True,
                    className="hover-image",
                ),
                dbc.CardBody([
                        html.H4("Create Logos", className="card-title"),
                        html.P(
                            '''Did you run WebFlags with the domain search?
                            Then you can view and interact with them here ''',
                            className="card-text",
                        ),
                        dbc.Button(
                            "Let's Go",
                            color="primary",
                            href="/create_logos",
                        ),
                    ]),
                ],
                style={"width": "22rem"},
                className="mb-3",
            ),
            width=3,
            align="center",
        ),
        # Repeat the above code for the other columns
    ], style={
        'margin-left' : '40px',
        'margin-right' : '40px',
        'margin-top' : '20px'
        }),
])
