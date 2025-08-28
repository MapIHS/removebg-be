import os
import uuid
from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from app.services.remove_bg_service import RemoveBgService

router = APIRouter(
    prefix="/image",
    tags=["Image Processing"]
)

UPLOAD_DIR = os.getenv("UPLOAD_DIRECTORY", "uploads")

_default_service = RemoveBgService()

@router.post("/remove-bg")
async def remove_background(
    image: UploadFile = File(...),
    quality: str = Form("standard"),   # fast | standard | pro
):

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa gambar.")

    image_data = await image.read()
    await image.close()

    if not image_data:
        raise HTTPException(status_code=400, detail="File gambar kosong atau gagal dibaca.")

    try:
        result_pil_image = await run_in_threadpool(_default_service.process_image, image_data, quality)


    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan internal: {e}")

    out_name = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(UPLOAD_DIR, out_name)

    await run_in_threadpool(result_pil_image.save, file_path, "PNG")

    return JSONResponse(
        content={
            "message": "Background removed successfully.",
            "original_filename": image.filename,
            "result_filename": out_name,
            "result_url": f"/{UPLOAD_DIR}/{out_name}",
            "content_type": "image/png",
            "quality": quality
        }
    )