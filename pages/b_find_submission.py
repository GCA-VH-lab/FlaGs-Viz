# PAGE 1: FIND SERVER STORED SUBMISSIONS

# Import packages
import dash 
from dash import html
import dash_bootstrap_components as dbc


# Import pages
from pages import navigation

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/find_submission')



# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
            navigation.navbar,
            dbc.Row([
                'Hi'
            ])
 
    ])