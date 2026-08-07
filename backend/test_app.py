from typing import Annotated

from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.post("/upload")
async def upload(
    files: Annotated[list[UploadFile], File()]
):
    return {
        "count": len(files)
    }