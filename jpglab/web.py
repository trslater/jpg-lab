from base64 import b64decode, b64encode
from io import BytesIO

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div((
    # Preamble
    html.H1("JPG Lab"),

    # Controls
    daq.BooleanSwitch(id="quantization-on", label="Quantization"),
    daq.BooleanSwitch(id="downsampling-on", label="Downsampling"),
    dcc.Upload(id="upload", children=(html.Div("Upload"),)),
    dbc.Row((
        dbc.Col((
            html.H2("Image"),
            dcc.Graph(id="image"),
            daq.BooleanSwitch(id="y-on", label="Y", on=True),
            daq.BooleanSwitch(id="cb-on", label="Cb", on=True),
            daq.BooleanSwitch(id="cr-on", label="Cr", on=True))),
        dbc.Col((
            html.H2("Spectrum"),
            dcc.Graph(id="spectrum"))))),

    # Browser storage
    dcc.Store(id="img-data"),

    # For throwing unwanted output
    html.Div(id="void", style={"display": "None"})))


@app.callback(Output("img-data", "data"),
              Input("upload", "contents"))
def process(contents):
    # DEBUG
    img = Image.open("test_data/Layia_glandulosa_white_layia_flower_bud.png")
    img_buf = BytesIO()
    img.save(img_buf, format="PNG")
    img_str = b64encode(img_buf.getvalue()).decode("ascii")

    return img_str


@app.callback(Output("image", "figure"),
              Input("y-on", "on"),
              Input("cb-on", "on"),
              Input("cr-on", "on"),
              Input("img-data", "data"))
def update_image(y_is_on, cb_is_on, cr_is_on, img_data):
    if not img_data:
        return go.Figure()

    y, cb, cr = Image.open(BytesIO(b64decode(img_data))).convert("YCbCr").split()
    grey = Image.new("L", (y.width, y.height), 127)

    channels = (
        y if y_is_on else grey,
        cb if cb_is_on else grey,
        cr if cr_is_on else grey)
    img = Image.merge("YCbCr", channels)
    
    return px.imshow(np.array(img.convert("RGB")))


def serve():
    app.run_server(debug=True)
