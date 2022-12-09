import dash
import ete3
from dash import dcc, html
import plotly.express as px
from ete3 import Tree


# Phylo class
class TreePlotter:
    '''
    A function for creating a phyologenetic tree from a .nw file.
    '''
    def __init__(self, tree):
        self.tree = tree
    
    def get_x_coords(self):
        # Retrives the x coordinates
        xcoords = self.tree.depths()

        if not max(xcoords.values()):
            xcoords = self.tree.depths(unit_branch_lengths=True)
        return xcoords

    def get_y_coords(self, dist = 6):
        maxheight = self.tree.count_terminals()
        ycoords = dict((taxon, i * dist) 
                    for i, taxon in enumerate((self.tree.get_terminals())))

        def calc_row(clade):
            for subclade in clade:
                if subclade not in ycoords:
                    calc_row(subclade)
            ycoords[clade] = (ycoords[clade.clades[0]] +
                                ycoords[clade.clades[-1]]) / 2

        if self.tree.root.clades:
            calc_row(self.tree.root)

        return ycoords

    def get_clade_lines(self, orientation='horizontal', 
                        y_curr=0, x_start=0, x_curr=0, y_bot=0, y_top=0,
                        line_color='rgb(25,25,25)', line_width=0.5):
        """define a shape of type 'line', for branch
        """
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

    def draw_clade(self, clade, x_start, line_shapes,line_color='rgb(15,15,15)', line_



