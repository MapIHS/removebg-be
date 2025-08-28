from io import BytesIO
import os
from PIL import Image, ImageOps
from transparent_background import Remover
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageOps

from app.utils.alpha import refine_alpha
from app.utils.quality import QUALITY_PROFILES


load_dotenv()

class RemoveBgService():
    def __init__(self):
        model_path = os.getenv("MODEL_PATH")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model checkpoint not found at: {model_path}")
        
        self.remover_base = Remover(mode="base", ckpt=model_path)
        self.remover_fast = Remover(mode="fast", ckpt=model_path)
        print("Background Remover model loaded successfully.")

    def _resize_long(self, im: Image.Image, max_side: int) -> Image.Image:
        w, h = im.size
        if max(w, h) <= max_side: return im
        if w >= h:
            return im.resize((max_side, int(h * (max_side / w))), Image.LANCZOS)
        return im.resize((int(w * (max_side / h)), max_side), Image.LANCZOS)

    def process_image(self, image_data: bytes, quality: str = "standard") -> Image.Image:
        prof = QUALITY_PROFILES.get(quality, QUALITY_PROFILES["standard"])
        try:
            img = Image.open(BytesIO(image_data))
            im = ImageOps.exif_transpose(img).convert("RGB")
            im = self._resize_long(im, prof["max_side"])
            if prof["mode"] == "fast":
                rgba = self.remover_fast.process(im)
            else:
                rgba = self.remover_base.process(im)
            rgba = refine_alpha(rgba, feather=prof["feather"], dilate=prof["dilate"])
            return rgba
        except Exception as e:
            raise ValueError(f"Failed to process image: {e}")
        