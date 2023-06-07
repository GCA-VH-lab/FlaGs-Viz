import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import base64
import urllib

app = dash.Dash()

app.layout = html.Div(
    [
        dcc.Graph(
            id='arrow-graph',
            figure={
                'data': [],
                'layout': {
                    'shapes': [
                        {
                            'type': 'path',
                            'path': 'M0,0 L0.9,0 L1,0.5 L0.9,1 L0,1 Z',
                            'fillcolor': 'black',
                            'line': {
                                'width': 1,
                                'color': 'black'
                            },
                            'xref': 'paper',
                            'yref': 'paper',
                            'x0': 0.1,
                            'y0': 0.25,
                            'x1': 0.9,
                            'y1': 0.75
                        }
                    ],
                    'xaxis': {'range': [0, 1]},
                    'yaxis': {'range': [0, 1]},
                    'height': 400,
                    'width': 800
                }
            }
        ),
        html.A(
            html.Button('Download as SVG'),
            id='download',
            download="arrow.svg",
            href="",
            target="_blank",
            className="download-btn",
            style={"margin": "10px"}
        )
    ]
)

@app.callback(
    dash.dependencies.Output('download', 'href'),
    dash.dependencies.Input('download', 'n_clicks')
)
def download_svg(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return 'data:image/svg+xml;charset=utf-8,' + urllib.parse.quote(get_svg_data(), safe='')

def get_svg_data():
    # Generate the SVG data for the arrow shape
    svg_data = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' \
               '<path d="M0,0 L90,0 L100,50 L90,100 L0,100 Z" fill="black" stroke="black" stroke-width="1" />' \
               '</svg>'
    return svg_data

if __name__ == '__main__':
    app.run_server(debug=True)
