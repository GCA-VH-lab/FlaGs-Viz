# TAKES IN THE USER INPUT AND CREATES THE LOGO

# Import packages
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import colorsys

# Import layout specifics
from assets.color_scheme import *


def rgba_to_hex(rgba_color):
    r = rgba_color['r']
    g = rgba_color['g']
    b = rgba_color['b']
    a = int(rgba_color['a'] * 255)
    hex_string = f'#{r:02x}{g:02x}{b:02x}{a:02x}'
    return hex_string


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




def create_fig(length, logo_color, domains_list=None, mutations_list=None):
    '''
    Creating a protein logo figure including the domain inside it.
    Args:
        length: Length of the protein arrow
        logo_color: Color of the protein arrow
        domain_list: contains any domains specified by user
    Returns:
        Returns a figure (graph) with protein and its domains
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
                domain_middle = domain_start + ((domain_end - domain_start) / 2)
                domain_end_head = (arrow_end * arrow_point) / domain_end

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
                    # Domain ends within the arrow head
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
                        'y': arrow_width + (arrow_width / 3),  
                        'showarrow': False,
                        'font': {
                            'family': 'Helvetica',
                            'size': 15,
                            'color': 'black'
                        }
                    }
                )

        if len(mutations_list) > 0:
            for index, row in mutations_list.iterrows():
                mutation_name = row['Name']
                mutation_position = row['Position']

                annotations.append(
                    {
                        'text': '*',
                        'xref': 'x',
                        'yref': 'y',
                        'x': mutation_position,
                        'y': arrow_width / 3, 
                        'showarrow': False,
                        'font': {
                            'family': 'Helvetica',
                            'size': 40,
                            'color': 'black'
                        }
                    }
                )
                annotations.append(
                    {
                        'text': mutation_name,
                        'xref': 'x',
                        'yref': 'y',
                        'x': mutation_position,
                        'y': -1.5,  
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
                'showticklabels': False,
                'visible': False
            },
            'yaxis': {
                'range': [-y_padding, arrow_width + y_padding],
                'constrain': 'domain',
                'showticklabels': False,
                'visible': False
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




import plotly.graph_objects as go

def placeholder_graph():
    fig_none = go.Figure()
    fig_none.add_annotation(
        x=0.5,
        y=0.5,
        text='waiting for your creation... :)',
        font=dict(size=20),
        showarrow=False,
        xanchor='center',
        yanchor='middle',
        align='center',
        xref='paper',
        yref='paper'
    )
    fig_none.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        )
    )
    return fig_none






