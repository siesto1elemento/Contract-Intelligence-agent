from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils import rag_embedding

router = APIRouter()


@router.post("/embed")
async def embed(file_location: str):
    try:
        await rag_embedding(file_location)

        return JSONResponse(
            content={"message": "Embedding completed successfully"}, status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
