from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import StreamingResponse
import numpy as np
from PIL import Image

app = FastAPI()

MAX_COLS = 32
BLOCK_SIZE = 8


@app.post("/upload")
async def upload(upload: UploadFile):
    image = Image.open(upload.file)
    if image.width//8 > MAX_COLS:
        # Shrink to manageable size
        image = image.resize((
            MAX_COLS*BLOCK_SIZE,
            int(MAX_COLS*BLOCK_SIZE*image.height/image.width)))
    # Crop to perfect multiples of 8
    image = image.crop((0, 0, 8*(image.width//8), 8*(image.height//8)))

    return StreamingResponse(blocks(image))


def blocks(image):
    num_cols = image.width//BLOCK_SIZE
    num_rows = image.height//BLOCK_SIZE

    blocks = (
        np.frombuffer(image.tobytes(), "ubyte")
        .reshape(num_rows, BLOCK_SIZE, num_cols, BLOCK_SIZE*3)
        .transpose(0, 2, 1, 3)
        .reshape(num_rows*num_cols, 3*BLOCK_SIZE**2))

    for i, block in enumerate(blocks):
        yield i.to_bytes(2, byteorder="big") + block.tobytes()


@app.websocket("/block")
async def block(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        await websocket.send_bytes(data)
