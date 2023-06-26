import dash
from dash import html

import dash_bootstrap_components as dbc



# --------------------------- CREATE APP -------------------------------

app = dash.Dash(__name__, 
                external_stylesheets = [dbc.themes.SANDSTONE, 
                                        dbc.icons.BOOTSTRAP],
                suppress_callback_exceptions = True,
                use_pages = True)



server = app.server



app.layout = html.Div(children=[
    dash.page_container
])
app.title = ('Flags Viz')

if __name__ == '__main__':
    # Set debug to True when working on app
    app.run_server(host = '0.0.0.0', port = '8080', debug = False)