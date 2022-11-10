import dash
from dash import html

import dash_bootstrap_components as dbc



# --------------------------- CREATE APP -------------------------------

app = dash.Dash(__name__, 
                external_stylesheets = [dbc.themes.SANDSTONE, 
                                        dbc.icons.BOOTSTRAP], 
                suppress_callback_exceptions = True,
                use_pages = True)

app.title = ('./assets/favicon.ico')
server = app.server


app.layout = html.Div(children=[
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(host = '127.0.0.1', port = '8050',debug=True)
