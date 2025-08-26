from io import BytesIO
import os
from PIL import Image
from transparent_background import Remover
from dotenv import load_dotenv

load_dotenv()

class RemoveBgService():
    def __init__(self):
        model_path = os.getenv("MODEL_PATH", "./models/ckpt_fast.pth")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model checkpoint not found at: {model_path}")
        
        self.remover = Remover(mode="fast", ckpt=model_path)
        print("Background Remover model loaded successfully.")

    def process_image(self, image_data: bytes) -> Image.Image:
        try:
            img = Image.open(BytesIO(image_data)).convert("RGB")

            result_img = self.remover.process(img)
            return result_img
        except Exception as e:
            print(f"Error processing image: {e}")
            raise ValueError(f"Failed to process image: {e}")

