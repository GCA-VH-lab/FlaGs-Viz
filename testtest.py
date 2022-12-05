import dash
from dash import html, dcc, Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "New York City", "value": "NYC"},
                {"label": "Montréal", "value": "MTL"},
                {"label": "San Francisco", "value": "SF"},
            ],
            value="MTL",
        ),
        dcc.Textarea(id="text"),
        html.Button("Submit", id="submit"),
        dcc.Store(id="store", data={}),
    ],
)


@app.callback(
    Output("store", "data"),
    Output("text", "value"),
    Input("dropdown", "value"),
    Input("submit", "n_clicks"),
    State("text", "value"),
    State("store", "data"),
)
def update(val, n_clicks, text, data):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id == "submit":
        data[val] = text
        return data, dash.no_update
    else:
        return dash.no_update, data.get(val, "")


if __name__ == "__main__":
    app.run_server(debug=True)