# TAKES IN THE USER INPUT AND CREATES THE LOGO

# Import packages
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import io
import base64
from PIL import Image


def fig2img(fig):
    # Convert Matplotlib figure to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    return img


def image_to_base64(img):
    # Convert image to base64 encoding
    buf = io.BytesIO()
    img.save(buf, format='png')
    encoded_img = base64.b64encode(buf.getvalue()).decode()
    return encoded_img


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

    # Set up the figure
    fig, ax = plt.subplots(figsize=(10, 3))

    # Define arrow parameters
    arrow_start = start
    arrow_size = end - start
    arrow_height = 0.4

    # Create the protein arrow
    ax.arrow(
        arrow_start, # protein start
        0, # y_level
        arrow_size, # protein size
        0, # y_level upper
        head_width=0.2, 
        head_length=0.2, 
        fc="gray", 
        ec="black"
    )

    # Create the domain arrows
    if domain_list:
        for domain in domain_list:
            domain_start = domain[0] - start
            domain_end = domain[1] - start

            # Draw the domain arrow
            ax.arrow(
                domain_start,
                0,
                domain_end - domain_start,
                arrow_height,
                head_width=0.2,
                head_length=0.2,
                fc="red",
                ec="black",
            )

            # Annotate the domain name
            text_x = domain_start + (domain_end - domain_start) / 2
            ax.annotate(
                domain[2],
                xy=(text_x, arrow_height),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="black",
            )

    # Set the x-axis limits
    ax.set_xlim(arrow_start - 1, arrow_size + 1)

    # Remove y-axis ticks and labels
    ax.yaxis.set_ticks([])

    # Set the figure background color
    fig.patch.set_facecolor("white")

    # Remove plot frame
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Set plot size and margins
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

    # Convert the Matplotlib figure to Plotly Figure object
    fig_plotly = go.Figure()

    # Convert the Matplotlib figure to an image
    img = fig2img(fig)
    encoded_img = image_to_base64(img)

    # Add the image to Plotly Figure
    fig_plotly.add_layout_image(
        dict(
            source=f"data:image/png;base64,{encoded_img}",
            xref="x",
            yref="y",
            x=arrow_start,
            y=0,
            sizex=arrow_size,
            sizey=arrow_height,
            sizing="stretch",
            layer="below",
        )
    )

    # Set the layout of Plotly Figure
    fig_plotly.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        width=800,
        height=800,
    )

    return fig_plotly



create_fig(0, 10)