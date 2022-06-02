from base64 import b64decode, b64encode
from io import BytesIO

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
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
    # j comes first, so we get blocks row-by-row
    for i in range(image.height//BLOCK_SIZE):
        for j in range(image.width//BLOCK_SIZE):
            block = image.crop((
                j*BLOCK_SIZE,
                i*BLOCK_SIZE,
                (j + 1)*BLOCK_SIZE,
                (i + 1)*BLOCK_SIZE))

            yield b64encode(block.tobytes())


@app.get("/block.png")
async def block(s: str):
    image_bytes = b64decode(s)
    image = Image.frombytes("RGB", (8, 8), image_bytes)
    stream = BytesIO()
    image.save(stream, format="png")
    stream.seek(0)

    return StreamingResponse(stream, media_type="image/png")
