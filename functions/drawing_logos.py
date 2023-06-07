# TAKES IN THE USER INPUT AND CREATES THE LOGO

# Import packages
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import colorsys





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




def create_fig(length, logo_color, domains_list = None):
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
        if domains_list != '':
            for domain in domain_list:
                domain_start = domain['start']
                domain_end = domain['end']
                domain_name = domain['name']
                domain_middle = (domain_start + domain_end) / 2

                # Create a shape that matches the arrow shape
                arrow_shape = f'M{domain_start},0 L{arrow_minus_head},0 L{length},{arrow_point} L{arrow_minus_head},{arrow_width} L{domain_start},{arrow_width} Z'

                # Adjust the domain shape if it doesn't cover the full arrow head
                if domain_end < arrow_minus_head:
                    domain_shape = f'M{domain_start},0 L{domain_end},0 L{domain_end},{arrow_width} L{domain_start},{arrow_width} Z'
                else:
                    domain_shape = arrow_shape

                shapes.append(
                    {
                        'type': 'path',
                        'path': domain_shape,
                        'fillcolor': 'rgba(0, 0, 0, 0.2)',  # Customize the fill color for the highlighted area
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

                shapes.append(
                    {
                        'type': 'text',
                        'xref': 'x',
                        'yref': 'y',
                        'x': domain_middle,
                        'y': arrow_width + 10,  # Adjust the vertical position as needed
                        'text': domain_name,
                        'showarrow': False,
                        'font': {
                            'size': 12,
                            'color': 'black'
                        }
                    }
                )
    return {
        'data': [],
        'layout': {
            'shapes': shapes,
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
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white'
        }
    }




create_fig(0, 10)