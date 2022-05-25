from dash import Dash, dcc, html, Input, Output, State


app = Dash(__name__)

app.layout = html.Div(children=(
    html.H1("Test App"),
    html.P("Hello, world!"),
    dcc.Upload(id="upload", children=html.Div("Upload")),
    html.Div(id="image")))


@app.callback(Output("image", "children"),
              Input("upload", "contents"))
def upload(contents):
    return [html.Img(src=contents)]
    

def serve():
    app.run_server(debug=True)
