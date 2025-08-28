import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from app.routers import api_router, image_router

load_dotenv()

app = FastAPI(
    title="Image Processing",
    description="API untuk memproses gambar, seperti menghapus background.",
    version="1.0.0",
)

UPLOAD_DIR = os.getenv("UPLOAD_DIRECTORY", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount(f"/{UPLOAD_DIR}", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(image_router.router)
app.include_router(api_router.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
