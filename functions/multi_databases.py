import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import colorsys
import random
from itertools import islice


# Import packages
import pandas as pd
import dash
import colorsys
import random
import math
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import base64
import io
from collections import Counter  


# Import specifics
from assets.color_scheme import *

# Import functions
from data.preping_data import * 



#From FlaGs script
def postscriptSize(item):
    if int(item)<1000:
        return(0)
    else:
        return(int(item)/1000)
newQ=0

def operonFamily(item):
    if item==0:
        return ' '
    elif item==center:
        return ' '
    elif item==noProt:
        return ' '
    elif item==noProtP:
        return ' '
    elif item==noColor:
        return ' '
    else:
        return item

# Colours
def random_color(h=None):
    if not h:
        c = int((random.randrange(0,100,5))*3.6)/100
    d = 0.5
    e = 0.5
    return _hls2hex(c, d, e)
        
def _hls2hex(c, d, e):
	return '#%02x%02x%02x' %tuple(map(lambda f: int(f*255),colorsys.hls_to_rgb(c, d, e)))

def outliner (item):
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
domain_colors = {}


def create_3db(operon_file, domain_file):

    operon_df = create_operon_df(operon_file)
    domain_df = create_domain_3db_df(domain_file)

    # 1. Merging the two traces into one plot
    fig = make_subplots(shared_yaxes = True, shared_xaxes = True)


    # 3. All lists
    arrowList = []
    domainList = []
    xList_gene = []
    yList_gene = []
    xList_domain = []
    yList_domain = []
    y_tick_marks = []
    labels = []
    genes = []


     # 2.2 Iterates through the operon df file and creates variables
    count = 0

    # Create a set for faster membership checks
    colorDict = {}

    # Iterate over rows using DataFrame indexing
    y_level = 0
    for i in range(len(operon_df)):
        organism = operon_df.loc[i, 'organism'].replace('_', ' ')
        id_q = operon_df.loc[i, 'query_accession']
        id_g = operon_df.loc[i, 'gene_accession']
        gene_start = int(operon_df.loc[i, 'gene_start'])
        gene_end = int(operon_df.loc[i, 'gene_end'])
        gene_length = int(operon_df.loc[i, 'gene_length'])
        gene_direction = operon_df.loc[i, 'gene_direction']
        group_number = operon_df.loc[i, 'hmlgs_group']
        y_level = (operon_df.loc[i, 'y_level'] * 5) * -2

        # Adjust gene start and end positions if the gene is too short
        if gene_length < 150:
            gene_start -= 40
            gene_end += 40

        # Color codes as from the original FlaGs code
        center = group_number + 1
        noProt = group_number + 2
        noProtP = group_number + 3
        noColor = group_number + 4

        color = {
            noColor: '#ffffff',
            center: '#000000',
            noProt: '#f2f2f2',
            noProtP: '#f2f2f3'
        }

        if group_number == 0:
            colorDict[group_number] = '#ffffff'
        elif gene_start == 1:
            colorDict[group_number] = '#000000'
        elif 'pseudogene_' in id_g:
            colorDict[group_number] = '#f2f2f3'
        elif 'tRNA_' in id_g:
            colorDict[group_number] = '#f2f2f2'
        else:
            if group_number not in colorDict:
                colorDict[group_number] = random_color()  # Replace with your random color generation logic

        # Text to show when hovering with the cursor over the arrow
        if gene_start == 1 or group_number == 0:
            hover_text = f'Accession: {id_g}<br>Species: {organism}<br>Size: {gene_length / 3}aa'
        else:
            hover_text = f'Accession: {id_g}<br>Species: {organism}<br>Size: {gene_length / 3}aa<br>Homologous group: {group_number}'

        # Precompute constant values
        arrow_head = 150
        arrow_width = 3
        domain_diff = 1
        top_domain_opacity = 0.6
        middle_domain_opacity = 0.6
        bottom_domain_opacity = 0.6

        # Create arrow coordinates based on the gene information
        if gene_direction == '-':
            xList_gene = [gene_start + arrow_head, gene_start, gene_start + arrow_head, gene_end, gene_end, gene_start + arrow_head]
            yList_gene = [y_level - arrow_width, y_level, y_level + arrow_width, y_level + arrow_width, y_level - arrow_width, y_level - arrow_width]
        else:
            xList_gene = [gene_start, gene_start, gene_end - arrow_head, gene_end, gene_end - arrow_head, gene_start]
            yList_gene = [y_level - arrow_width, y_level + arrow_width, y_level + arrow_width, y_level, y_level - arrow_width, y_level - arrow_width]

        arrowList.append(
            fig.add_trace(
                go.Scatter(
                    x=xList_gene,
                    y=yList_gene,
                    hoveron='fills',
                    hoverinfo='text',
                    text=hover_text,
                    fill='toself',
                    fillcolor=colorDict[int(group_number)],
                    opacity=0.3,
                    line=dict(color=outliner(colorDict[group_number])),
                    mode='lines'
                )
            )
        )

        # Display homologous group number inside each arrow
        text_x = gene_start + (gene_length / 2.2)
        if group_number != 0 and gene_start != 1 and 'pseudogene_' not in id_g and 'tRNA_' not in id_g:
            fig.add_annotation(
                x=text_x,
                y=y_level,
                xref='x',
                yref='y',
                text=int(group_number),
                font=dict(family='Helvetica', color='#73767c', size=12),
                showarrow=False
            )

        # Iterate over domain_df using DataFrame indexing
        for j in range(len(domain_df)):
            row = domain_df.loc[j]
            domain_start_original = int(row['domain_start']) * 3
            domain_size = (int(row['domain_end']) * 3) - (int(row['domain_start']) * 3)
            domain_name = row['domain']
            database = row['database']
            id2 = row['domain_accession']

            # Setting the domain colour
            if domain_name not in domain_colors:
                domain_colors[domain_name] = random_color()
            domain_color = domain_colors[domain_name]

            # Text to show when hovering with the cursor over the arrow
            hover_text = f'Domain: {domain_name}<br>Domain size: {domain_size/3}aa'

            # 1. PFAM domains
            if database == 'pfam':
                y_level_d = y_level + 2
                if id2 == id_g:
                    domain_start = gene_start + domain_start_original
                    domain_end = domain_start + domain_size
                    if domain_end <= gene_end-arrow_head and gene_direction == '+':
                        xList_domain = [domain_start, domain_end, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines')))
                    elif domain_start >= gene_start+arrow_head and gene_direction == '-': 
                        xList_domain = [domain_start, domain_end, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines')))
                    elif domain_end > gene_end-arrow_head and gene_direction == '+':
                        xList_domain = [domain_start, domain_end, gene_end-arrow_head, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines')))
                    elif domain_start < gene_start+arrow_head and gene_direction == '-':
                        xList_domain = [domain_start, domain_end, domain_end, gene_start+arrow_head, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines')))
                    else:
                        print(f'missing description {database}')

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 10, family = "Helvetica"), showarrow = False)

            # 2. PDB domains
            if database == 'pdb':
                if id2 == id_g:
                    domain_start = gene_start + domain_start_original
                    domain_end = domain_start + domain_size
                    y_level_d = y_level
                    if domain_end > gene_end-arrow_head and gene_direction == '+':
                        xList_domain = [domain_start, gene_end-arrow_head/3, domain_end, gene_end-arrow_head/3, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines')))
                    elif domain_start < gene_start+arrow_head and gene_direction == '-':
                        xList_domain = [domain_end, gene_start+arrow_head/3, domain_start, gene_start+arrow_head/3, domain_end, domain_end]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = middle_domain_opacity, mode='lines')))
                    elif domain_end <= gene_end-arrow_head and gene_direction == '+':
                        xList_domain = [domain_start, domain_end, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines')))
                    elif domain_start >= gene_start+arrow_head and gene_direction == '-': 
                        xList_domain = [domain_start, domain_end, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = top_domain_opacity, mode='lines')))
                    else:
                        print(f'missing description {database}')

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 10, family = "Open Sans"), showarrow = False)

            # 3. CDD domains
            if database == 'cdd':
                if id2 == id_g:
                    y_level_d = y_level - 2
                    domain_start = gene_start + domain_start_original
                    domain_end = domain_start + domain_size
                    if domain_end <= gene_end-arrow_head and gene_direction == '+':  # just a square
                        xList_domain = [domain_start, domain_end, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines')))
                    elif domain_start >= gene_start+arrow_head and gene_direction == '-': 
                        xList_domain = [domain_start, domain_end, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines')))
                    elif domain_end > gene_end-arrow_head and gene_direction == '+':
                        xList_domain = [domain_start, gene_end-arrow_head, domain_end, domain_start, domain_start]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines')))
                    elif domain_start < gene_start+arrow_head and gene_direction == '-':
                        xList_domain = [gene_start+arrow_head, domain_end, domain_end, domain_start, gene_start+arrow_head]
                        yList_domain = [y_level_d-domain_diff, y_level_d-domain_diff, y_level_d+domain_diff, y_level_d+domain_diff, y_level_d-domain_diff]
                        domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'text',  hoveron='fills', text=hover_text, fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = bottom_domain_opacity, mode='lines')))
                    else:
                        print(f'missing description {database}')

                    # 6c. Placing domain anontation inside the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level_d, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 10, family = "Open Sans"), showarrow = False)

        # 7. Setting the y labels i.e. the organism name and accession nr etc.
        y_tick_marks += [y_level]
        labels += [organism]


    # 8. Changing the download format of the .html as .svg instead of the defaul .png
    config = {'toImageButtonOptions': {'format': 'svg','filename': 'FlaGs','scale': 1}}


    # 9. Scales and sets the graph size
    number_of_queries = (int(len(operon_file.iloc[:, 0].unique()) * 8))
    upper = 20
    lower = ((int(number_of_queries) + int(number_of_queries/4)) * -1)

    max_x_value = number_of_queries/1

    min_x = int(min(operon_df[['gene_start', 'gene_end']].min()))
    max_x = int(max(operon_df[['gene_start', 'gene_end']].max()))


    # 9A. Operon graph layout
    fig.update_xaxes(visible = False)
    fig.update_yaxes(
        visible = True, 
        showgrid = False, 
        showline = False, 
        range = [-max_x_value-4, 4], 
        automargin = True, 
        showticklabels = True,
        zeroline = False, 
        tickvals = y_tick_marks, 
        ticktext = labels, 
        ticklen = 20, 
        tickmode = 'array', 
        titlefont = dict(family = 'Helvetica', size = 8))
    fig.update_layout(
        autosize=True,
        paper_bgcolor=transparent_background, 
        plot_bgcolor=transparent_background, 
        showlegend = False)
 
    return fig