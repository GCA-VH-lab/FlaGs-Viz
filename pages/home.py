#!/bin/env python3


# This script generates the FlaGs graphical output with imporved interactivity 
# where the user can filter, select, click, and get more info about the data. 
#
# Run the applicatuib with "python app.py" and visit 
# http://127.0.0.1:8050/ in your web browser.


# ------------------------------- IMPORTS ------------------------------
import pandas as pd
import colorsys
import random
import re
import dash
import math
import dash_cytoscape
import dash_bio as dashbio
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State

import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

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

dash.register_page(__name__, path = '/home')



# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
            navigation.navbar,
            dbc.Row([
                dbc.Row([
                    html.H4('Upload Files'),
                    html.Hr(),
                    dbc.Row([
                        dbc.Row([
                            html.Div([
                                dbc.Button(
                                    'Find Your Submission',
                                    id = 'button-web',
                                    className ='mb-3',
                                    color = 'dark',
                                    n_clicks = 0),
                                dbc.Collapse(
                                    html.Div([
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
                                                'margin-top' : '5px',
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
                                    ]),
                                    id = 'collapse-web',
                                    is_open = False
                                )
                            ])
                        ]),
                        html.Br(),
                        dbc.Row([
                            html.Div([
                                dbc.Button(
                                    'Upload Your Local Files',
                                    id = 'button-local',
                                    className='mb-3',
                                    n_clicks = 0,
                                    color = 'dark'),
                                dbc.Collapse(
                                    html.Div([
                                        dbc.Row([
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
                                            ], style={
                                                'margin-left' : '40px',
                                                'margin-top' : '5px',
                                                'margin-bottom' : '10px',
                                                'width': '80%'})
                                    ]),
                                    id = 'collapse-local',
                                    is_open = False
                                )
                            ])
                        ])
                    ]),
                ], style={
                    'margin-left' : '40px',
                    'margin-top' : '60px',
                    'margin-bottom' : '10px',
                    'width': '96%'
                    }
                ),    
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
                ], className = 'h-auto',
                style = {
                    'margin-left' : '40px',
                    'margin-top' : '60px',
                    'margin-bottom' : '10px',
                    'width': '96%'
                }),
            ]),       
    ])



# ------------------------------ ACTIONS -------------------------------



# Creates a phylo graph based on the selected run
@callback(
    Output('server-phylo', 'children'),
    Input('insert-email', 'value'),
    Input('submissions', 'value')
)
def update_output(email, selected):
    # From the selected run it finds the submission id and generates fig 
    if selected != '':
        sub_id = selected_submission(selected)
        email_name = email.split('@')[0]
        phylo_file = phylo_url(email, email_name, sub_id)
        phylo_plot = dcc.Loading(
                    children = [
                        html.Div([   
                            html.H6('Viewing submission: ' + sub_id),
                            html.Hr(),
                            dcc.Graph(
                                id = 'phylo-plot',
                                animate = False,
                                responsive = True,
                                figure = get_tree_plot(phylo_file),
                                style = {
                                    'display': 'block',
                                    'margin-left': '10px', 
                                    'margin-top': '0px',
                                    'margin-bottom': '10px',
                                    'height': generate_phylo_dimensions(phylo_file)
                                },
                            config = {
                                    'displaylogo': False,
                                    'toImageButtonOptions': {
                                            'format': 'svg',
                                            'filename': sub_id,
                                            'scale': 1}
                                    }
                            )], style={
                                'margin-left' : '30px', 
                                'margin-top' : '50px',
                                'margin-bottom' : '10px',
                                'postion': 'relative', 
                                'top': 0,
                                'z-index': 0})],
                    color = 'dark',
                    type = 'dot')
        return phylo_plot
         

# Creates the operon graph based on the selected run
@callback(
    Output('server-operon', 'children'),
    Input('insert-email', 'value'),
    Input('submissions', 'value')
    )
def update_output(email, selected):
    if selected != '':
        sub_id = selected_submission(selected)
        email_name = email.split('@')[0]
        operon_file = operon_url(email, email_name, sub_id)
        operon_plot = dcc.Loading(
                    children = [
                        html.Div([
                            html.H6('Viewing submission: ' + sub_id),
                            html.Hr(),
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
                                                'filename': sub_id,
                                                'scale': 1}
                                        })
                                ], style={
                                    'margin-left' : '0px', 
                                    'margin-top' : '50px',
                                    'margin-bottom' : '10px',
                                    'postion': 'relative', 
                                    'width': '95%',
                                    'top': 0,
                                    'z-index': 0})],
                    color = 'dark',
                    type = 'dot')
        
        return operon_plot






# Collapsing the submission and upload buttons
@callback(
    Output("collapse-web", "is_open"),
    [Input("button-web", "n_clicks")],
    [State("collapse-web", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-local", "is_open"),
    [Input("button-local", "n_clicks")],
    [State("collapse-local", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
