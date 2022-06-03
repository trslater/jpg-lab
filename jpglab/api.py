from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import StreamingResponse
import numpy as np
from PIL import Image

app = FastAPI()

MAX_COLS = 32
BLOCK_SIZE = 8
NUM_RGB_CHANNELS = 3
NUM_ID_BITS = 2


@app.post("/upload")
async def upload(upload: UploadFile):
    image = Image.open(upload.file)
    if image.width//BLOCK_SIZE > MAX_COLS:
        # Shrink to manageable size
        image = image.resize((
            MAX_COLS*BLOCK_SIZE,
            int(MAX_COLS*BLOCK_SIZE*image.height/image.width)))
    # Crop to perfect multiples of BLOCK_SIZE
    image = image.crop((0, 0, BLOCK_SIZE*(image.width//BLOCK_SIZE),
                        BLOCK_SIZE*(image.height//BLOCK_SIZE)))

    return StreamingResponse(blocks(image))


def blocks(image):
    num_cols = image.width//BLOCK_SIZE
    num_rows = image.height//BLOCK_SIZE

    blocks = (
        np.frombuffer(image.tobytes(), "ubyte")
        .reshape(num_rows, BLOCK_SIZE, num_cols, BLOCK_SIZE*NUM_RGB_CHANNELS)
        .transpose(0, 2, 1, 3)
        .reshape(num_rows*num_cols, NUM_RGB_CHANNELS*BLOCK_SIZE**2))

    for i, block in enumerate(blocks):
        yield i.to_bytes(NUM_ID_BITS, byteorder="big") + block.tobytes()


@app.websocket("/block")
async def block(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        await websocket.send_bytes(data)
