from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

app = FastAPI()


@app.post("/upload")
async def upload(upload: UploadFile):
    image = Image.open(upload.file)

    block_size = 400
    for i in range(image.height//block_size):
        for j in range(image.width//block_size):
            image.crop((
                j*block_size,
                i*block_size,
                (j + 1)*block_size,
                (i + 1)*block_size)).show()

    return StreamingResponse(iter(
        ("OSUDJCIQ", "BVUQODLK", "SUDHQBVY", "ZXOQPWOI", "IUWRVCBN")))
