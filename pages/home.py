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

import requests
import urllib.request


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



# --------------------------- FLAGS COLOR ------------------------------

# Color codes for the operon plot copied from FlaGs
def random_color(h=None):
    if not h:
        c = int((random.randrange(0,100,5))*3.6)/100
    d = 0.5
    e = 0.5
    return _hls2hex(c, d, e)
        
def _hls2hex(c, d, e):
	return '#%02x%02x%02x' %tuple(map(lambda f: int(f*255),colorsys.hls_to_rgb(c, d, e)))

def outliner(item):
	if item =='#ffffff':
		return '#bebebe'
	elif item =='#f2f2f2':
		return '#008000'
	elif item =='#f2f2f3':
		return '#000080'
	else:
		return item


color={}
colorDict={}



# ----------------------- ACCESSING SERVER DATA ------------------------

# Reads the queueDir HTML and retrives the runs and dates
storred_runs = 'http://130.235.240.53/scripts/writable/queueDir/'
server_table = pd.read_html(storred_runs)
server_df = server_table[0]
submissions = server_df.loc[:, 'Name':'Last modified'].dropna()
submitters = server_df.loc[:, 'Name'].dropna()


def test_url(s):
    '''
    Uses the URL to operon file to check if the URL is accessible 
    (i.e if the submission is still stored).
    '''
    link_operon = f'http://130.235.240.53/scripts/writable/{submission_components(s)[0]}%23{submission_components(s)[2]}/{submission_components(s)[1]}_flagsOut_TreeOrder_operon.tsv'
    return link_operon

def operon_url(email, email_name, sub_id):
    # Reads URL of operon file
    link_operon = f'http://130.235.240.53/scripts/writable/{email}%23{sub_id}/{email_name}_flagsOut_TreeOrder_operon.tsv'
    operon_file = pd.read_csv(link_operon, delimiter = '\t', header = None)
    return operon_file

def phylo_url(email, email_name, sub_id):
    # Reads URL of phylo tree (newick format)
    link_phylo_ladder = f'http://130.235.240.53/scripts/writable/{email}%23{sub_id}/{email_name}_flagsOut_ladderTree.nw'
    read_url = urllib.request.urlopen(link_phylo_ladder)
    string = read_url.read().decode()
    phylo_file = io.StringIO(string)
    tree = Phylo.read(phylo_file, "newick")
    return tree




# ----------------------- FETCHING SERVER DATA -------------------------

# Lists
runs = []
email_runs = []
all_runs_list = []
stored_runs_list = []


def email_search(email):
    '''
    Validates that the user's email is found in the queueDir and 
    fetches the user email, email_name, and the FlaGs submission_id
    '''
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        if s.startswith(email):
            email = email.split('#')[0]
            email_name = email.split('@')[0]
            code = re.search('#(.*).run', s)
            submission_id = code.group(1)
    return email, email_name, submission_id


def run_finished(url):
    '''
    Validates the existance of an URL link. In this case used to check
    if a submission is still stored on the server
    '''
    response = requests.head(url)
    return response.status_code in range(200, 400)


def selected_submission(option):
    '''
    Once the user selects one of their runs from the dropdown menu, 
    files for generating graphs are retrived from the server.
    '''
    sub = str(submissions[submissions['Last modified']==option]['Name'])
    code = re.search('#(.*).run', sub)
    submission_id = code.group(1)
    return submission_id


def submission_components(submission):
    '''
    For a run, the key components are split for easier access. Used 
    for filling out the URL links
    '''
    email = submission.split('#')[0]
    email_name = submission.split('@')[0]
    code = re.search('#(.*).run', submission)
    submission_id = code.group(1)
    return email, email_name, submission_id


def submission_lists(email):
    all_runs_list = []
    stored_runs_list = []
    '''
    Outputs necessary lists for checking the email against the runs.
    all_runs_list = all runs in queueDir associated with the email
    stored_runs_list = only the server stored runs for the email
    '''
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        # Find all runs associated with the email from the queueDir
        if s.startswith(email) and s not in all_runs_list:
            all_runs_list.append(s)
            # Find all runs that are still accessible (stored) by 
            # testing the URL for one of the ouput files (operon.tsv)
            if run_finished(test_url(s)) == True:
                run = str(submissions[submissions['Name']==s]['Last modified'])
                run_date = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', run)
                submission_id = run_date.group(0)
                # Add only unique runs' submission_id to list
                if submission_id not in stored_runs_list:
                    stored_runs_list.append(submission_id)
                stored_runs_list.sort(reverse=True)
    return all_runs_list, stored_runs_list



# --------------------- CREATING PLOTS FROM DATA------------------------

# 1. PHYLO PLOT
def get_tree_plot(tree):
    # Read a newick file and returns a phylo tree plot.
    def get_x_coords(tree):
        # Calculates the x coordinates
        xcoords = tree.depths()
        if not max(xcoords.values()):
            xcoords = tree.depths(unit_branch_lengths=True)
        return xcoords


    def get_y_coords(tree, dist = 5):
        '''
        Calculates the y coordinates for the tree that are evenly 
        spaced apart
        '''
        maxheight = tree.count_terminals()
        ycoords = dict((taxon, i * dist) 
                    for i, taxon in enumerate((tree.get_terminals())))

        def calc_row(clade):
            '''
            Calculates y coordinates for the non-terminal nodes of the 
            tree by averaging the y coordinates of their child nodes.
            '''
            for subclade in clade:
                if subclade not in ycoords:
                    calc_row(subclade)
            ycoords[clade] = (ycoords[clade.clades[0]] +
                                ycoords[clade.clades[-1]]) / 2

        if tree.root.clades:
            calc_row(tree.root)

        return ycoords

    # The coordinates
    x_coords = get_x_coords(tree)
    y_coords = get_y_coords(tree)


    def get_clade_lines(orientation='horizontal', 
                        y_curr=0, x_start=0, x_curr=0, y_bot=0, y_top=0,
                        line_color='rgb(25,25,25)', 
                        line_width=0.5):
        '''
        Defines a shape for a branch of the tree, either horizontal or 
        vertical, based on the specified orientation and the provided 
        x and y coordinates.
        '''
        branch_line=dict(type= 'line',
                        layer='below',
                        line=dict(color=line_color, 
                                width=line_width)
                        )
        if orientation=='horizontal':
            branch_line.update(x0=x_start,
                            y0=y_curr,
                            x1=x_curr,
                            y1=y_curr)
        elif orientation=='vertical':
            branch_line.update(x0=x_curr,
                            y0=y_bot,
                            x1=x_curr,
                            y1=y_top)
        else:
            raise ValueError("Line type can be 'horizontal' or 'vertical'")
        
        return branch_line 



    def draw_clade(clade, x_start, line_shapes,line_color='rgb(15,15,15)', line_width=1):
        '''
        Draws the branches by getting the x and y coordinates of the 
        current clade, and then draws a horizontal line from the start 
        to the current clade. If the current clade has children, 
        it also draws a vertical line connecting all of the children and
        then calls itself on each child to draw the branches for those
        clades.
        '''
        
        x_curr = x_coords[clade]
        y_curr = y_coords[clade]
    
        # Draw a horizontal line from start to here
        branch_line=get_clade_lines(orientation = 'horizontal', 
                                    y_curr = y_curr, 
                                    x_start = x_start, 
                                    x_curr = x_curr,  
                                    line_color = line_color, 
                                    line_width = line_width)
    
        line_shapes.append(branch_line)
    
        if clade.clades:
            # Draw a vertical line connecting all children
            y_top = y_coords[clade.clades[0]]
            y_bot = y_coords[clade.clades[-1]]
        
            line_shapes.append(get_clade_lines(orientation = 'vertical', 
                                            x_curr = x_curr, 
                                            y_bot = y_bot, 
                                            y_top = y_top,
                                            line_color = line_color, 
                                            line_width = line_width))
        
            # Draw descendants
            for child in clade:
                draw_clade(child, x_curr, line_shapes)

    
    line_shapes=[]
    draw_clade(tree.root, 0, line_shapes, 
                line_color='rgb(25,25,25)', line_width=1)  


    my_tree_clades=x_coords.keys()
    X = []
    Y = []
    text = []

    for cl in my_tree_clades:
        X.append(x_coords[cl])
        Y.append(y_coords[cl])
        text.append(cl.name)

    # Setting the graph size 
    number_of_terminals = (tree.count_terminals() * 8)
    y_upper = -10
    y_lower = number_of_terminals + int(number_of_terminals/4)
    x_lower = -0.25
    x_upper = max(tree.depths().values()) + 3

    nodes = dict(type = 'scatter',
            x = X,
            y = Y,
            mode = 'markers+text',
            textposition = "middle right",
            marker = dict(color = 'black', size = 5),
            text = text,
            hoverinfo = 'text')

    layout = dict(
                font = dict(family = 'Helvetica', size = 12),
                autosize = False,
                showlegend = False,
                xaxis = dict(
                        showline = False,  
                        zeroline = False,
                        showgrid = False,
                        constrain = 'range',
                        range = [x_lower, x_upper]),
                yaxis = dict(
                        visible = False, 
                        showline = False,  
                        zeroline = False,
                        showgrid = False,
                        showticklabels = False,
                        constrain = 'range',
                        range = [y_lower, y_upper]), 
                hovermode = 'closest',
                shapes = line_shapes,
                paper_bgcolor = 'rgba(0,0,0,0)', 
                plot_bgcolor = 'rgba(0,0,0,0)',
                margin = dict(
                    l = 0,
                    r = 0,
                    b = 0,
                    t = 0,
                    pad = 0, 
                    autoexpand = False),
            )
    
    fig_phylo = go.Figure(data = [nodes], layout = layout )

    return fig_phylo


def generate_phylo_dimensions(tree):
    '''
    Sets the correct width of the graph container so the correct 
    operon is displayed with its corresponding node on the y-axis level.
    '''
    organism = tree.count_terminals() * 8
    y_vh_phylo = str(organism) + 'vh'

    return y_vh_phylo



# 2. OPERON PLOT
def generate_operon(operon_file):
    '''
    Returns an operon plot figure generated from operon.tsv file. 
    This is a really bad function but in summary it first gets all the
    required data from the operon file. It adds another column where the
    rows belonging to the same operon are assigned the same y-axis value.
    Finally, the function creates a scatter plot of the genes using the 
    data from the lists and returns the plot figure.
    '''
    operon_data = {
        'organism': [],
        'query_accession': [],
        'gene_accession': [],
        'hmlgs_group': [],
        'gene_direction': [],
        'gene_start': [],
        'gene_end': [],
        'gene_length': [],
        'y_level': [],
    }

    for g in operon_file.iloc[:, 0]:
        if g != '':
            org = g.split('|')[1]
            operon_data['organism'].append(str(org))

            q_acc = g.split('|')[0]
            operon_data['query_accession'].append(str(q_acc))

    for g in operon_file.iloc[:, 9]:
        if g != '':
            operon_data['y_level'].append(int(0))
            g_acc = g.split('#')[0]
            operon_data['gene_accession'].append(str(g_acc))

    operon_data['hmlgs_group'] = list(operon_file.iloc[:, 4].astype(int))
    operon_data['gene_direction'] = list(operon_file.iloc[:, 3].astype(str))
    operon_data['gene_start'] = list(operon_file.iloc[:, 5].astype(int))
    operon_data['gene_end'] = list(operon_file.iloc[:, 6].astype(int))
    operon_data['gene_length'] = list(operon_file.iloc[:, 1].astype(int))
    

    operon_df_org = pd.DataFrame.from_dict(operon_data)
    operon_df_org['y_level'] = operon_df_org.groupby('query_accession', sort = False).ngroup()
    operon_df = operon_df_org

    fig = go.Figure()

    arrowList = []
    annotations_fam_nr_list = []
    y_tick_marks = []
    labels = []
    row = []

    count = 0
    for i, row in operon_df.iterrows():
        organism = operon_df['organism'][i].replace('_', ' ')
        id_q = operon_df['query_accession'][i]
        id_g = operon_df['gene_accession'][i]
        start = operon_df['gene_start'][i]
        end = operon_df['gene_end'][i]
        length = operon_df['gene_length'][i]
        direction = operon_df['gene_direction'][i]
        group_number = operon_df['hmlgs_group'][i]
        y_level = (operon_df['y_level'][i] * 5) * -1

        if length < 100:
            start = start-50
            end = end+50
        else:
            start = start
            end = end

        center=int(group_number)+1
        noProt=int(group_number)+2
        noProtP=int(group_number)+3
        noColor=int(group_number)+4

        color[noColor]='#ffffff'
        color[center]='#000000'
        color[noProt]='#f2f2f2'
        color[noProtP]='#f2f2f3'

        if group_number == 0:
            colorDict[group_number]=str('#ffffff')
        elif start == 1:                    
            colorDict[group_number]=str('#000000')
        elif 'pseudogene_' in id_g:
            colorDict[group_number]=str('#f2f2f3') 
        elif 'tRNA_' in id_g:
            colorDict[group_number]=str('#f2f2f2')
        else:
            if group_number not in colorDict:
                colorDict[group_number] = random_color()

        arrow_head = 120
        arrow_width = 1.2

        if start == 1 or group_number == 0:
            hover_text = (f'Accession: {id_g}<br>'
                        f'Species: {organism}<br>'
                        f'Length: {length}nt')
        else: 
            hover_text = (f'Accession: {id_g}<br>'
                        f'Species: {organism}<br>'
                        f'Length: {length}nt<br>'
                        f'Homologous group: {group_number}')

        if direction == '-':
            xList_gene = [start+arrow_head, 
                        start, start+arrow_head, 
                        end, 
                        end, 
                        start+arrow_head]
            yList_gene = [y_level-arrow_width, 
                        y_level, 
                        y_level+arrow_width, 
                        y_level+arrow_width, 
                        y_level-arrow_width, 
                        y_level-arrow_width]
            arrowList.append(
                fig.add_trace(
                    go.Scatter(x = xList_gene, 
                            y = yList_gene,
                            hoveron = 'fills',
                            hoverinfo = 'text',
                            text = hover_text,
                            fill = 'toself', 
                            fillcolor = colorDict[int(group_number)], 
                            opacity = 0.5,
                            line = (dict(color = outliner(colorDict[group_number]))), 
                            mode = 'lines')))
        else:
            xList_gene = [start, 
                        start, 
                        end-arrow_head, 
                        end, 
                        end-arrow_head, 
                        start]
            yList_gene = [y_level-arrow_width, 
                        y_level+arrow_width, 
                        y_level+arrow_width, 
                        y_level, y_level-arrow_width, 
                        y_level-arrow_width] 
            arrowList.append(
                fig.add_trace(
                    go.Scatter(x = xList_gene, 
                            y = yList_gene,
                            hoveron = 'fills',
                            hoverinfo = 'text',
                            text = hover_text,
                            fill = 'toself', 
                            fillcolor = colorDict[int(group_number)], 
                            opacity = 0.5, 
                            line = (dict(color = outliner(colorDict[group_number]))), 
                            mode = 'lines')))

        text_x = start + (length/2.2)
        if group_number != 0 and start != 1 and 'pseudogene_' not in id_g and 'RNA_' not in id_g:
            annotations_fam_nr_list.append(
                fig.add_annotation(
                    x = text_x, 
                    y = y_level, 
                    xref='x', 
                    yref='y', 
                    text = int(group_number), 
                    font = dict(family = 'Helvetica',
                                color = '#73767c', 
                                size = 12), 
                    showarrow = False))
        else:
            pass
   
        if organism not in labels:
            labels += [organism]
            y_tick_marks += [y_level]

    number_of_queries = (int(len(operon_file.iloc[:, 0].unique()) * 8))
    upper = 10
    lower = (int(number_of_queries) + int(number_of_queries/4)) * -1

    fig.update_layout(
                    xaxis = dict(visible = False,
                                showgrid = False,
                                showline = False,
                                showticklabels = False),
                    yaxis = dict(visible = False,
                                showgrid = False,
                                showline = False,
                                showticklabels = False, 
                                tickvals = y_tick_marks,
                                ticktext = labels,
                                constrain = 'range',
                                range = [lower, upper],
                                ),
                    margin = dict(l=0,
                                r=0,
                                b=0,
                                t=0,
                                pad=0, 
                                autoexpand = False),
                    showlegend = False, 
                    autosize = False,
                    paper_bgcolor = 'rgba(0,0,0,0)', 
                    plot_bgcolor = 'rgba(0,0,0,0)')

    return fig


def get_operon_graph_dimensions(operon_file):
    # Sets the correct width of the graph container so the correct 
    # operon is displayed with its corresponding node on the y-axis level.
    length = len(operon_file.iloc[:, 0].unique()) * 8
    y_vh = str(length) + 'vh'

    return y_vh




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



# ACTION 2: Upload own phylo files
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
