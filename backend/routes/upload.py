from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from utils import rag_embedding, summarize_whole
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            contents = await file.read()
            f.write(contents)

        summary = summarize_whole(file_location)
        embedding = rag_embedding(file_location)

        return JSONResponse(
            content={"filename": file.filename, "message": "Upload successful"},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
