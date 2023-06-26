# FUNCTION FOR CREATING THE OPERON PLOT W/ DOMAINS

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
from assets import color_scheme
from data.preping_data import * 

# Import functions 




# --------------------------- FLAGS COLORS -----------------------------

# Color codes for the operon plot (copied from FlaGs)

# Color codes for the operon plot (copied from FlaGs)
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




# --------------------------- INPUT FILES -----------------------------

def generate_plot_domains(operon_file, domain_file):
    operon_df = create_operon_df(operon_file)
    domain_df = create_domain_df(domain_file)
    
    # 1. Instanciating the figure
    fig1 = make_subplots(shared_yaxes = True, shared_xaxes = True)
    fig2 = make_subplots(shared_yaxes = True, shared_xaxes = True)

    # 1.2 Creaties empty lists to store all traces
    arrowList = []
    annotations_fam_nr_list = []
    annotations_domain_name_list = []
    accession_operons_List = []
    accession_domains_List = []
    y_tick_marks = []
    labels = []
    row = []
    traceB_map = dict()
    domainList = []
    coordList = []
    scoreList = []
    xList_domain = []
    yList_domain = []
    trace1A_list = []   # traces for the operons - operon graph
    trace1B_list = []   # traces for the domains - operon grpah
    traceB_list = []    # traces for the domains - domain graph


    # 2.2 Iterates through the operon df file and creates variables
    count = 0
    for i, row in operon_df.iterrows():
        organism = operon_df['organism'][i].replace('_', ' ')
        id_q = operon_df['query_accession'][i]
        id_g = operon_df['gene_accession'][i]
        gene_start = int(operon_df['gene_start'][i])
        gene_end = int(operon_df['gene_end'][i])
        gene_length = int(operon_df['gene_length'][i])
        gene_direction = operon_df['gene_direction'][i]
        group_number = operon_df['hmlgs_group'][i]
        y_level = (operon_df['y_level'][i] * 5) * -1
        accession_operons_List.append(group_number)  

        # 2.2.1 If the gene is too short it adds some extra length,
        # otherwise the arrow will be too small and invert on itself
        if gene_length < 100:
            gene_start = gene_start-50
            gene_end = gene_end+50
        else:
            gene_start = gene_start
            gene_end = gene_end

        # # 2.2.2 Color codes as from the original FlaGs code
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
        elif gene_start == 1:                    
            colorDict[group_number]=str('#000000')
        elif 'pseudogene_' in id_g:
            colorDict[group_number]=str('#f2f2f3') 
        elif 'tRNA_' in id_g:
            colorDict[group_number]=str('#f2f2f2')
        else:
            if group_number not in colorDict:
                colorDict[group_number] = random_color()

        # 2.2.3 Specifying the arrow's dimensions
        arrow_head = 120
        arrow_width = 1.2

        # 2.2.4 Text to show when hovering with the courser over the arrow
        if gene_start == 1 or group_number == 0:
            hover_text = (f'Accession: {id_g}<br>'
                        f'Species: {organism}<br>'
                        f'Size: {gene_length/3}aa')
        else: 
            hover_text = (f'Accession: {id_g}<br>'
                        f'Species: {organism}<br>'
                        f'Size: {gene_length/3}aa<br>'
                        f'Homologous group: {group_number}')

        # 2.2.5 Creates arrow coordinates based on the info from the
        # operon .tsv file and stores the in the appropriate list
        if gene_direction == '-':
            xList_gene = [gene_start+arrow_head, 
                        gene_start, 
                        gene_start+arrow_head, 
                        gene_end, 
                        gene_end, 
                        gene_start+arrow_head]
            yList_gene = [y_level-arrow_width, 
                        y_level, 
                        y_level+arrow_width, 
                        y_level+arrow_width, 
                        y_level-arrow_width, 
                        y_level-arrow_width]
            arrowList.append(
                fig1.add_trace(
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
            xList_gene = [gene_start, 
                        gene_start, 
                        gene_end-arrow_head, 
                        gene_end, 
                        gene_end-arrow_head, 
                        gene_start]
            yList_gene = [y_level-arrow_width, 
                        y_level+arrow_width, 
                        y_level+arrow_width, 
                        y_level, 
                        y_level-arrow_width, 
                        y_level-arrow_width] 
            arrowList.append(
                fig1.add_trace(
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
        
        # 2.2.6 Displaying the homologous group number inside each arrow
        text_x = gene_start + (gene_length/2.2)
        if group_number != 0 and gene_start != 1 and 'pseudogene_' not in id_g and 'tRNA_' not in id_g:
            annotations_fam_nr_list.append(
                fig1.add_annotation(
                    x = text_x, 
                    y = y_level, 
                    xref='x', 
                    yref='y', 
                    text = int(group_number), 
                    font = dict(family = 'Helvetica',
                                color = '#73767c', 
                                size = 12), 
                    showarrow = False))


        # 2.2.7 Iterating through domains file
        for i, row in domain_df.iterrows():
            domain_protein = row['domain_code']
            domain_name = row['domain']
            domain_score = row['score']
            domain_e_value = row['e_value']
            accession_domains_List.append(domain_protein)
            if gene_direction == '+':
                domain_start = gene_start + (int(row['domain_start']) * 3)
                domain_size = (int(row['domain_end']) - int(row['domain_start'])) * 3
                domain_end = domain_start + domain_size
                text_x = domain_start + (domain_size/2.2)
            elif gene_direction == '-':
                domain_start = gene_end - (int(row['domain_start']) * 3)
                domain_size = (int(row['domain_end']) - int(row['domain_start'])) * 3
                domain_end = domain_start - domain_size
                text_x = domain_start - (domain_size/2.2)

            # Text to show when hovering with the cursor over the arrow
            hover_text = f'Domain: {domain_name}<br>Domain size: {domain_size/3}aa'

            # 6b. If a gene has additional information about domains (i.e. same id is found in second file), then these will also be drawn inside the arrow.
            if id_g == domain_protein and group_number>0:
                if gene_end-arrow_head < domain_end < gene_end and gene_direction == '+':
                    xList_domain = [domain_start, 
                                domain_start, 
                                gene_end-arrow_head, 
                                (gene_end-arrow_head) + (gene_end-domain_end), 
                                (gene_end-arrow_head) + (gene_end-domain_end), 
                                gene_end-arrow_head, 
                                domain_start]
                    yList_domain = [y_level-arrow_width, 
                                y_level+arrow_width, 
                                y_level+arrow_width, 
                                y_level+arrow_width/2,  
                                y_level-arrow_width/2, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)                                       
                elif gene_start < domain_start < gene_end+arrow_head and gene_direction == '-':
                    xList_domain = [gene_start+arrow_head, 
                                (gene_start+arrow_head) + (domain_start-gene_end),  
                                (gene_start+arrow_head) + (domain_start-gene_end), 
                                gene_start+arrow_head, 
                                domain_start, 
                                domain_start, 
                                gene_start+arrow_head]
                    yList_domain = [y_level-arrow_width, 
                                y_level-arrow_width/2, 
                                y_level+arrow_width/2, 
                                y_level+arrow_width,  
                                y_level+arrow_width, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))                                       
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)
                elif gene_start >= domain_end and gene_direction == '-':
                    xList_domain = [gene_start+arrow_head, 
                                domain_end,
                                gene_start+arrow_head, 
                                domain_start, 
                                domain_start, 
                                gene_start+arrow_head]
                    yList_domain = [y_level-arrow_width, 
                                y_level,
                                y_level+arrow_width,  
                                y_level+arrow_width, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines',
                                name = domain_protein), 
                                len(fig1.data)))                                       
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)                                        
                elif domain_end <= gene_end and domain_start > gene_start+arrow_head and gene_direction == '-':           
                    xList_domain = [domain_start, 
                                domain_start, 
                                domain_end, 
                                domain_end, 
                                domain_start]
                    yList_domain = [y_level-arrow_width, 
                                y_level+arrow_width, 
                                y_level+arrow_width, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain,
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)
                elif domain_start >= gene_start and gene_direction == '-':
                    xList_domain = [domain_start+arrow_head, 
                                domain_start, 
                                domain_start+arrow_head, 
                                domain_end, 
                                domain_end, 
                                domain_start+arrow_head]
                    yList_domain = [y_level-arrow_width, 
                                y_level, 
                                y_level+arrow_width, 
                                y_level+arrow_width, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)
                elif domain_start <= gene_start and domain_end < gene_end-arrow_head and gene_direction == '+':
                    xList_domain = [domain_start, 
                                domain_start, 
                                domain_end, 
                                domain_end, 
                                domain_start]
                    yList_domain = [y_level-arrow_width, 
                                y_level+arrow_width, 
                                y_level+arrow_width, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))                                          
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)
                elif domain_start <= gene_start and domain_end <= gene_end and gene_direction == '+':
                    xList_domain = [domain_start, 
                                domain_start, 
                                domain_end-arrow_head, 
                                domain_end, 
                                domain_end-arrow_head, 
                                domain_start]
                    yList_domain = [y_level-2, 
                                y_level+arrow_width, 
                                y_level+arrow_width, 
                                y_level, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))                                       
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)
                elif domain_end <= gene_end and domain_start >= gene_start:
                    xList_domain = [domain_start, 
                                domain_start, 
                                domain_end, 
                                domain_end, 
                                domain_start]
                    yList_domain = [y_level-arrow_width, 
                                y_level+arrow_width, 
                                y_level+arrow_width, 
                                y_level-arrow_width, 
                                y_level-arrow_width]
                    trace1B_list.append((
                        go.Scatter(x=xList_domain, 
                                y=yList_domain, 
                                fill="toself", 
                                hoveron = 'fills',
                                hoverinfo = 'text',
                                text = hover_text,
                                fillcolor= colorDict[int(group_number)], 
                                line=(dict(color = outliner(colorDict[group_number]))), 
                                opacity = 0.7, 
                                mode='lines', 
                                name = domain_protein), 
                                len(fig1.data)))        
                    fig1.add_trace(trace1B_list[-1][0], row = 1, col = 1)

                # Group all fig.2 traces that have the same ID in column = 0  
                if domain_protein not in traceB_map.keys():
                    traceB_map[domain_protein] = []
                traceB_map[domain_protein].append(len(fig2.data) - 1)

                # 6c. Annotating each domain with name
                if group_number != 0 and 'pseudogene_' not in id_g and 'tRNA_' not in id_g:
                    annotations_domain_name_list.append(
                        fig1.add_annotation(
                            x = text_x, 
                            y = y_level+2.5, 
                            xref='x', 
                            yref='y', 
                            text = domain_name, 
                            font = dict(
                                color = "#73767c", 
                                size = 8, 
                                family = "Helvetica"), 
                            showarrow = False))
                else:
                    pass



    # 8. Changing the download format of the .html as .svg instead of the defaul .png
    config = {'toImageButtonOptions': {'format': 'svg','filename': 'FlaGs','scale': 1}}

    # 9. Scales and sets the graph size
    number_of_queries = (int(len(operon_file.iloc[:, 0].unique()) * 8))
    upper = 10
    lower = (int(number_of_queries) + int(number_of_queries/4)) * -1

    # 9A. Operon graph layout
    fig1.update_layout(
        xaxis = dict(visible = False,
                    showgrid = False,
                    showline = False,
                    showticklabels = False),
        yaxis = dict(visible = False,
                    showgrid = False,
                    showline = False,
                    showticklabels = False, 
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
        plot_bgcolor = 'rgba(0,0,0,0)',
        clickmode = 'event+select')
    fig1.update_traces(marker_size = 20)
 
    return fig1



def get_operon_graph_dimensions(operon_file):
    '''
    Sets the correct width of the graph container so the correct 
    operon is displayed with its corresponding node on the y-axis level.
    Args:
        operon_file: The operon.tsv file generated by FlaGs
    Returns:
        y_vh: y-level viewport height (%) should the y_vh of the 
        phyogeny plot. 
    '''
    length = len(operon_file.iloc[:, 0].unique()) * 8
    y_vh = str(length) + 'vh'

    return y_vh
