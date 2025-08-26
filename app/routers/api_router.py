from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
    tags=["API"]
)

@router.get("/health")
def health():
    return {
    "status": "ok",
    }