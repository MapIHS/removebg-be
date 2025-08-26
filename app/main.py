from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import image_router

load_dotenv()

app = FastAPI(
    title="Image Processing",
    description="API untuk memproses gambar, seperti menghapus background.",
    version="1.0.0",
)

app.include_router(image_router.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
