import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from app.services.remove_bg_service import RemoveBgService

router = APIRouter(
    prefix="/image",
    tags=["Image Processing"]
)

UPLOAD_DIR = os.getenv("UPLOAD_DIRECTORY", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/remove-bg")
async def remove_background(
    image: UploadFile = File(...)
):

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa gambar.")

    image_data = await image.read()

    try:
        remover_service = RemoveBgService()
        result_pil_image = await run_in_threadpool(remover_service.process_image, image_data)

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
            "result_url": f"/uploads/{out_name}",
            "content_type": "image/png"
        }
    )