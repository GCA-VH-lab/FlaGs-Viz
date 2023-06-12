# TAKES IN THE USER INPUT AND CREATES THE LOGO

# Import packages
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import colorsys

# Import layout specifics
from assets.color_scheme import *




def darken_color(color, percentage):
    # Extract the RGB values and alpha channel from the color
    r = color['r']
    g = color['g']
    b = color['b']
    a = color['a']

    # Calculate the darkening factor
    factor = 1 - (percentage / 100)

    # Darken each RGB channel by applying the darkening factor
    new_r = max(0, int(r * factor))
    new_g = max(0, int(g * factor))
    new_b = max(0, int(b * factor))

    # Return the updated color with the original alpha value
    return {'r': new_r, 'g': new_g, 'b': new_b, 'a': a}



def calculate_upper_point_y(x0, y0, x1, y1):
    slope = (y1 - y0) / (x1 - x0)
    upper_y = y0 + slope * (10 - x0)  # Assuming upper x coordinate is 10
    return upper_y




def create_fig(length, logo_color, domains_list = None, mutations_list = None):
    '''
    Creating a protein logo figure including the domain inside it.
    Args:
        length: Length of the protein arrow
        logo_color: Color of the protein arrow
        domain_list: contains any domains specified by user
    Returns:
        Returns a figure (graph) with protein and and its domains
    '''
    if length == 0:
        return {}
    else:
        arrow_start = 0
        arrow_end = length
        arrow_width = 6
        arrow_point = arrow_width / 2
        arrow_head = length * 0.1
        arrow_minus_head = length - arrow_head
        x_padding = 50
        y_padding = 20
        fill_color = logo_color['rgb']
        outline_color = darken_color(fill_color, 30)  # Make outline darker
        outline_width = 2  # Adjust the outline width as needed

        shapes = [
            {
                'type': 'path',
                'path': f'M0,0 L{arrow_minus_head},0 L{length},{arrow_point} L{arrow_minus_head},{arrow_width} L0,{arrow_width} Z',
                'fillcolor': fill_color,
                'line': {
                    'width': arrow_width,
                    'color': fill_color
                },
                'xref': 'x',
                'yref': 'y',
                'x0': arrow_start,
                'y0': 0,
                'x1': arrow_end,
                'y1': arrow_width
            },
            {
                'type': 'path',
                'path': f'M0,0 L{arrow_minus_head},0 L{length},{arrow_point} L{arrow_minus_head},{arrow_width} L0,{arrow_width} Z',
                'fillcolor': 'rgba({}, {}, {}, {})'.format(fill_color['r'], fill_color['g'], fill_color['b'], fill_color['a']),
                'line': {
                    'width': arrow_width - outline_width,
                    'color': 'rgba({}, {}, {}, {})'.format(outline_color['r'], outline_color['g'], outline_color['b'], outline_color['a'])
                },
                'xref': 'x',
                'yref': 'y',
                'x0': arrow_start,
                'y0': 0,
                'x1': arrow_end,
                'y1': arrow_width
            }
        ]
        annotations = []
        if len(domains_list) > 0:
            for index, row in domains_list.iterrows():
                domain_name = row['Name']
                domain_start = row['Start']
                domain_end = row['End']
                domain_color = row['Color']
                domain_middle = domain_start+((domain_end-domain_start)/2)
                domain_end_head = (arrow_end*arrow_point)/domain_end 

                # Create a shape that matches the arrow shape
                arrow_shape = f'''
                    M{domain_start},{arrow_width-5.75} 
                    L{arrow_minus_head},{arrow_width-5.75} 
                    L{length-0.5},{arrow_point} 
                    L{arrow_minus_head},{arrow_width-0.25} 
                    L{domain_start},{arrow_width-0.25} 
                    Z'''

                if domain_end <= arrow_minus_head:
                    # Domain ends within the area before the arrow head
                    domain_shape = f'''
                        M{domain_start},{arrow_width-5.75} 
                        L{domain_end},{arrow_width-5.75} 
                        L{domain_end},{arrow_width-0.25} 
                        L{domain_start},{arrow_width-0.25} 
                        Z'''
                elif domain_end > arrow_minus_head and domain_end < arrow_end:
                    # Domain ends withing the arrow head
                    domain_shape = f'''
                        M{domain_start},{arrow_width-5.75} 
                        L{arrow_minus_head},{arrow_width-5.75} 
                        L{domain_end},{domain_end_head} 
                        L{domain_end},{domain_end_head} 
                        L{arrow_minus_head},{arrow_width-0.25} 
                        L{domain_start},{arrow_width-0.25} 
                        Z'''
                else:
                    # Domain covers the full arrow head
                    domain_shape = arrow_shape


                shapes.append(
                    {
                        'type': 'path',
                        'path': domain_shape,
                        'fillcolor': domain_color,  # Customize the fill color for the highlighted area
                        'line': {
                            'width': 0
                        },
                        'xref': 'x',
                        'yref': 'y',
                        'x0': arrow_start,
                        'y0': 0,
                        'x1': arrow_end,
                        'y1': arrow_width
                    }
                )
                annotations.append(
                    {
                        'text': domain_name,
                        'xref': 'x',
                        'yref': 'y',
                        'x': domain_middle,
                        'y': arrow_width + (arrow_width/3),  # Adjust the vertical position as needed
                        'showarrow': False,
                        'font': {
                            'family': 'Helvetica',
                            'size': 15,
                            'color': 'black'
                        }
                    }
                )

    return {
        'data': [],
        'layout': {
            'shapes': shapes,
            'annotations': annotations,
            'xaxis': {
                'range': [arrow_start - x_padding, arrow_end + x_padding],
                'constrain': 'domain',
                'showticklabels': False
            },
            'yaxis': {
                'range': [-y_padding, arrow_width + y_padding],
                'constrain': 'domain',
                'showticklabels': False
            },
            'height': 400,
            'width': 800,
            'margin': {'t': 0, 'b': 0, 'l': 0, 'r': 0},
            'showlegend': False,
            'plot_bgcolor': transparent_background,
            'paper_bgcolor': transparent_background
        }
    }




create_fig(0, 10)