from base64 import b64encode

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

app = FastAPI()

BLOCK_SIZE = 8


@app.post("/upload")
async def upload(upload: UploadFile):
    image = Image.open(upload.file)
    # DEBUG: Shrink for now, so a predictable number of blocks are generated
    image = image.resize((64, 64))

    blocks = (
        b64encode(
            image.crop((
            j*BLOCK_SIZE,
            i*BLOCK_SIZE,
            (j + 1)*BLOCK_SIZE,
            (i + 1)*BLOCK_SIZE)).tobytes()).decode("ascii")
        for i in range(image.height//BLOCK_SIZE)
        for j in range(image.width//BLOCK_SIZE))

    return StreamingResponse(blocks)
