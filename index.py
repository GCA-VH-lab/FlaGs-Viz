from dash import html, dcc
from dash.dependencies import Input, Output

import app as app
from pages import help, home

application = app

app.layout = html.Div([
        dcc.Location(id = 'url', refresh = False),
        html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/help':
        return help.layout
    else:
        return home.layout


if __name__ == '__main__':
    # hostname = socket.gethostname()
    # ip_address = socket.gethostbyname(hostname)
    # app.run_server(host=ip_address, port=5002, debug=True)
    app.run_server(host='0.0.0.0', port=8080, debug=True)
    
    # app.run_server(debug = True)