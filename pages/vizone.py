# ------------------------------- IMPORTS ------------------------------
import pandas as pd
import colorsys
import random
import re
import dash
import math
import dash_cytoscape
import dash_bio as dashbio
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

import dash_daq as daq
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from collections import Counter  

from Bio import AlignIO, Phylo
from Bio.Align.Applications import MafftCommandline

import base64
import io
import datetime

from pages import navigation


# --------------------------- CREATE PAGE ------------------------------

dash.register_page(__name__, path = '/vizone')



# ----------------------------- LAYOUT ---------------------------------


layout = html.Div([
            navigation.navbar,
            dbc.Row([
                dbc.Row([
                    html.H3('Search for your gene'),
                    html.P('Please upload files below for visualisation.'),
                ], style={
                    'margin-left' : '40px',
                    'margin-top' : '60px',
                    'margin-bottom' : '10px',
                    'width': '96%', 
                    }
                ),    
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div(id = 'cytoscape-phylo'),
                        ], width = 4),
                        dbc.Col(width = 1),
                        dbc.Col([
                            html.Div(id = 'operon-graph'),
                        ],  width = 7),
                    ],style={
                        'margin-left' : '10px', 
                        'margin-top' : '5px',
                        'margin-bottom' : '5px',
                        'postion': 'relative', 
                        }
                    )]),
                ], className = 'h-auto'),
            ]),       
    ])