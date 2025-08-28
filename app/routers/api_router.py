import os
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/api",
    tags=["API"]
)

@router.get("/health")
def health():
    return {
    "status": "ok",
    "model": os.getenv("MODEL_PATH", "unknown"),
    "mode": os.getenv("MODEL_MODE", "unknown")
    }