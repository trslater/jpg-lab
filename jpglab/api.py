from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.post("/upload")
async def upload():
    return StreamingResponse(iter(
        ("OSUDJCIQ", "BVUQODLK", "SUDHQBVY", "ZXOQPWOI", "IUWRVCBN")))
