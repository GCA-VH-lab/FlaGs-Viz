# TAKES IN THE USER INPUT AND CREATES THE LOGO




def create_fig(start, end, domain_list = None):
    '''
    Creating a protein logo figure including the domain inside it.
    Args:
        start: User input start of protein
        end: User input end of protein
        domain_list: contains any domains specified by user
    Returns:
        Returns a figure (graph) with protein and and its domains
    '''

    # Lists to store shape specifics
    # arrowList = []
	# domainList = []
	# accession_List = []
	# gene_start_list=[]
	# gene_end_list=[]


    arrowList = []
    domainList = []
    xList_gene = []
    yList_gene = []
    xList_domain = []
    yList_domain = []

    # Merging the two traces (protein + domain) into one plot
    fig, ax = plt.subplots(1, 2, sharey = 'row', figsize=(x, y), gridspec_kw={'width_ratios': [5, 15]})    

    # Create a trace for the accession
    for i, row in protein_coords_df.iterrows():
        if row['accession'] == antitoxin:
            # Extracting coordinates
            protein_start = 1
            protein_end = (row['size'])*factor_length
            arrow_head = ((protein_end-protein_start)*(1/8))*factor_length
            
            # Setting shape specifics
            xList_gene = [protein_start, protein_start, protein_end-arrow_head, protein_end, protein_end-arrow_head, protein_start]
            yList_gene = [y_level-arrow_width, y_level+arrow_width, y_level+arrow_width, y_level, y_level-arrow_width, y_level-arrow_width]
            arrowList.append(fig.add_trace(go.Scatter(x=xList_gene, y=yList_gene, fill="toself", fillcolor='#d9d9d9', opacity=0.5, line=(dict(color='#bfbfc0')), mode='lines+text')))

            # Itterate through the domain data and get info for domains
            for i, row in relevant_domains_df.iterrows():
                domain_protein = row['Accession']
                database = row['database']
                domain_name = row['domain']
                domain_start = int(row['query_hmm'].split('-')[0])*factor_length
                domain_end = int(row['query_hmm'].split('-')[1])*factor_length
                domain_size = (domain_end - domain_start)*factor_length
                domain_score = row['score']
                domain_color = domain_color

                if antitoxin == domain_protein:
                    xList_domain = [domain_start, domain_start, domain_end, domain_end, domain_start]
                    yList_domain = [y_level-arrow_width, y_level+arrow_width, y_level+arrow_width, y_level-arrow_width, y_level-arrow_width]
                    domainList.append(fig.add_trace(go.Scatter(x=xList_domain, y=yList_domain, fill="toself", hoverinfo = 'none', fillcolor=domain_color, line=dict(color=domain_color, width = 0), opacity = domain_opacity, mode='lines', name = domain_name)))                                     

                    # 6c. Placing domain anontation above the domain.
                    text_x = domain_start + (domain_size/2)
                    fig.add_annotation(x = text_x, y = y_level, xref='x', yref='y', text = domain_name, font = dict(color = "black", size = 8, family = "Open Sans"), showarrow = False)

            # Graph specifics
            fig.update_xaxes(visible = False)
            fig.update_yaxes(
                visible = True, 
                showgrid = False, 
                showline = False,
                range = [-2, 2], 
                automargin = True, 
                showticklabels = False, 
                titlefont = dict(family = 'Open Sans', size = 8))
            fig.update_layout(
                autosize=False, 
                width=300, 
                height=300, 
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor = transparent_background, 
                plot_bgcolor = transparent_background, 
                showlegend = False
            )
            
    return fig