# FUNCTION FOR CREATING THE PHYLOGENY TREE

# Import packages
import pandas as pd 
from Bio import AlignIO, Phylo
import plotly.graph_objs as go


# Import page




def get_tree_plot(tree):
    '''
    Generates a phylogenetic tree plot from tree.nw using plotly's cytoscape.
    Args:
        tree: Phylogenetic tree object.
    Returns:
        fig_phylo: Plotly figure object representing the phylogenetic tree plot.
    '''


    # Read a newick file and returns a phylo tree plot.
    def get_x_coords(tree):
        '''
        Calculates the x coordinates of the tree nodes.
        Args:
            tree: Phylogenetic tree file, tree.nw.
        Returns:
            xcoords: Dictionary mapping tree nodes to their x coordinates.
        '''
        xcoords = tree.depths()
        if not max(xcoords.values()):
            xcoords = tree.depths(unit_branch_lengths=True)
        return xcoords


    def get_y_coords(tree, dist = 5):
        '''
        Calculates the y coordinates of the tree nodes.
        Args:
            tree: Phylogenetic tree file, tree.nw.
            dist: Distance between y-levels.
        Returns:
            ycoords: Dictionary mapping tree nodes to their y coordinates.
        '''
        maxheight = tree.count_terminals()
        ycoords = dict((taxon, i * dist) 
                    for i, taxon in enumerate((tree.get_terminals())))

        def calc_row(clade):
            '''
            Calculates y coordinates for the non-terminal nodes of the tree
            by averaging the y coordinates of their child nodes.
            Args:
                clade: Phylogenetic tree clade object.
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
        vertical, based on the specified orientation and the provided x
        and y coordinates.
        Args:
            orientation: Orientation of the branch ('horizontal' or 'vertical').
            y_curr: Current y-coordinate.
            x_start: Start x-coordinate.
            x_curr: Current x-coordinate.
            y_bot: Bottom y-coordinate.
            y_top: Top y-coordinate.
            line_color: Color of the branch line.
            line_width: Width of the branch line.
        Returns:
            branch_line: Shape object representing the branch line.
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
        Draws the branches of the phylogenetic tree.
        Args:
            clade: Phylogenetic tree clade object.
            x_start: Start x-coordinate.
            line_shapes: List to store the shape objects representing the branches.
            line_color: Color of the branch lines.
            line_width: Width of the branch lines.
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
    Args:
        operon_file: The operon.tsv file generated by FlaGs
    Returns:
        y_vh_phylo: y-level viewport height (%) should the y_vh of the 
        operon plot. 
    '''
    organism = tree.count_terminals() * 8
    y_vh_phylo = str(organism) + 'vh'

    return y_vh_phylo


