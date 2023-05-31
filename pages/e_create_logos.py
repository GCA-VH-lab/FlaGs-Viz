# PAGE 4 - CREATING LOGOS

# Import packages
import dash 
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq
import matplotlib.pyplot as plt
import io
import base64

# Import pages
from pages import navigation

# Import layout specifics
from assets.color_scheme import *

# ---------------------------- INDEX PAGE ------------------------------

dash.register_page(__name__, path = '/create_logos')



# ----------------------------- LAYOUT ---------------------------------

layout = html.Div([
            navigation.navbar,
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(
                            html.H6('Gene Start:')
                        ),
                        dbc.Col(
                            dcc.Input(
                                id="input-start", 
                                type="number", 
                                value=1, 
                                min=1)
                        )
                    ], style = {'padding' : '20px'}),
                    dbc.Row([
                        dbc.Col(
                            html.H6('Gene End:')
                        ),
                        dbc.Col(
                            dcc.Input(
                                id="input-end", 
                                type="number", 
                                value=1, 
                                min=1)
                        )
                    ], style = {
                        'margin-left' : '20px',
                        'margin-right' : '20px'}),
                    dbc.Row([
                        html.Label("Arrow Color:"),
                        html.Br(),
                        daq.ColorPicker(
                            id="input-color", 
                            value={"hex": "#000000"}
                        ),
                    ], style = {'padding' : '20px'}),
                    dbc.Row(html.Button("Generate Arrow", id="button-generate"))
                ],  width={
                        'size': 4,
                        'offset': 0},  
                    style={
                        'height': '90vh', 
                        'background': container_background}),
                dbc.Col([], style={'width' : 1}),
                dbc.Col([
                    dcc.Graph(id="arrow-output")
                ],  width={
                            'size': 7,
                            'offset': 0},  
                        style={
                            'height': '90vh', 
                            'background': container_background})
            ], style = {'padding' : '60px'})
])




@callback(
    Output("arrow-output", "figure"),
    [Input("button-generate", "n_clicks")],
    [dash.dependencies.State("input-start", "value"),
     dash.dependencies.State("input-end", "value")]
)
def generate_arrow(n_clicks, start, end):
    if n_clicks is None:
        return {}

    # Create the arrow using Matplotlib
    fig, ax = plt.subplots()
    ax.arrow(start, 0, end - start, 2, head_width=0.05, head_length=0.1, fc="black", ec="black")
    ax.set_xlim(start - 1, end + 1)
    ax.set_ylim(-1, 1)
    ax.axis("off")

    # Convert the Matplotlib figure to HTML image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close(fig)
    img.seek(0)
    encoded_img = base64.b64encode(img.getvalue()).decode()

    # Return the figure as a dictionary for Dash graph
    return {
        "data": [],
        "layout": {
            "images": [
                {
                    "source": f"data:image/png;base64,{encoded_img}",
                    "xref": "x",
                    "yref": "y",
                    "x": start,
                    "y": 0,
                    "sizex": end - start,
                    "sizey": 1,
                    "sizing": "stretch",
                    "layer": "below",
                }
            ],
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "width": 800,
            "height": 200,
        },
    }

