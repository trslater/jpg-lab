from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

app = FastAPI()


@app.post("/upload")
async def upload(upload: UploadFile):
    image = Image.open(upload.file)

    image.show()

    return StreamingResponse(iter(
        ("OSUDJCIQ", "BVUQODLK", "SUDHQBVY", "ZXOQPWOI", "IUWRVCBN")))
