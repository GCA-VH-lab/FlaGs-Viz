from dash import html, dcc
from dash.dependencies import Input, Output

import app as app


from pages import *

application = app

app.layout = html.Div([
        dcc.Location(id = 'url', refresh = False),
        html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/find_submissions':
        return b_find_submission.layout
    elif pathname == '/upload_files':
        return c_upload_files.layout
    elif pathname == '/view_domains':
        return d_view_domains.layout
    elif pathname == '/create_logos':
        return e_create_logos.layout
    else:
        return a_cover_page.layout


if __name__ == '__main__':
    # Set the debug to False when deploying app 
    app.run_server(host='0.0.0.0', port=8080, debug=True)  
    