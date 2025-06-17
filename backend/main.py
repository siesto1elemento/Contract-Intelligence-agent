from backend.routes import upload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5174",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload.router)
