from base64 import b64decode, b64encode
from io import BytesIO

from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

from . import cli


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
    dcc.Store(id="y-data"),
    dcc.Store(id="cb-data"),
    dcc.Store(id="cr-data"),
    dcc.Store(id="spectrum-data"),

    # For throwing unwanted output
    html.Div(id="void", style={"display": "None"})))


@app.callback(Output("y-data", "data"),
              Output("cb-data", "data"),
              Output("cr-data", "data"),
              Output("spectrum-data", "data"),
              Input("upload", "contents"))
def store_image_data(img_data):
    if not img_data:
        raise PreventUpdate()

    img_data = img_data.replace("data:image/png;base64,", "")

    y, cb, cr = Image.open(BytesIO(b64decode(img_data))).convert("YCbCr").split()
    
    spectrum_arr = np.array(y, dtype="float")
    for block in cli.blockized(spectrum_arr):
        block[:] = cli.spectrum(block)
        # Normalize
        block[:] *= 255.0/block.max()
    spectrum = Image.fromarray(spectrum_arr.astype("byte"), "L")

    y_buf = BytesIO()
    cb_buf = BytesIO()
    cr_buf = BytesIO()
    spectrum_buf = BytesIO()

    y.save(y_buf, format="PNG")
    cb.save(cb_buf, format="PNG")
    cr.save(cr_buf, format="PNG")
    spectrum.save(spectrum_buf, format="PNG")

    y_data = b64encode(y_buf.getvalue()).decode("ascii")
    cb_data = b64encode(cb_buf.getvalue()).decode("ascii")
    cr_data = b64encode(cr_buf.getvalue()).decode("ascii")
    spectrum_data = b64encode(spectrum_buf.getvalue()).decode("ascii")

    return y_data, cb_data, cr_data, spectrum_data


@app.callback(Output("image", "figure"),
              Output("spectrum", "figure"),
              Input("y-on", "on"),
              Input("cb-on", "on"),
              Input("cr-on", "on"),
              Input("y-data", "data"),
              Input("cb-data", "data"),
              Input("cr-data", "data"),
              Input("spectrum-data", "data"))
def update_image(y_is_on, cb_is_on, cr_is_on, y_data, cb_data, cr_data, spectrum_data):
    if not (y_data and cb_data and cr_data):
        raise PreventUpdate()

    y = Image.open(BytesIO(b64decode(y_data)))
    cb = Image.open(BytesIO(b64decode(cb_data)))
    cr = Image.open(BytesIO(b64decode(cr_data)))
    spectrum = Image.open(BytesIO(b64decode(spectrum_data)))
    grey = Image.new("L", (y.width, y.height), 127)

    channels = (
        y if y_is_on else grey,
        cb if cb_is_on else grey,
        cr if cr_is_on else grey)
    img = Image.merge("YCbCr", channels)
    
    image_fig = px.imshow(np.array(img.convert("RGB")))
    spectrum_fig = px.imshow(np.array(spectrum))

    return image_fig, spectrum_fig


# @app.callback(Output("spectrum", "figure"),
#               Input("image", "relayoutData"))
# def sync(relayout_data):
#     return go.Figure()


def serve():
    app.run_server(debug=True)
