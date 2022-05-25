from dash import Dash, html


def serve():
    app = Dash(__name__)

    app.layout = html.Div(children=(
        html.H1(children="Test App"),
        html.P(children="Hello, world!")
    ))

    app.run_server(debug=True)
