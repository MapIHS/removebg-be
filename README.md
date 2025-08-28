# Remove BG Service — InSPyReNet (FastAPI)

Layanan **remove background** berbasis **InSPyReNet** via [`transparent-background`](https://pypi.org/project/transparent-background/) + FastAPI.  
Sudah ada opsi kualitas (“fast/standard/pro”), auto-resize, dan output PNG.

---

## 1) Prasyarat

- Ubuntu/Debian (atau Linux lain)
- Python ≥ 3.10 (3.12 juga ok)
- Git, venv
- (Jika error `libGL.so.1`) paket sistem: `libgl1`

```bash
sudo apt update
sudo apt install -y python3-venv git libgl1
```

## 2) Clone & Siapkan Env

```bash
git clone https://github.com/MapIHS/removebg-be
cd removebg-be
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Download model InSPyReNet

### Cara A
```bash
pip install -U huggingface_hub
huggingface-cli login  # bisa skip
mkdir -p models
huggingface-cli download plemeri/InSPyReNet ckpt_fast.pth --local-dir ./models
# (opsional) untuk kualitas lebih tinggi:
# huggingface-cli download plemeri/InSPyReNet ckpt_base.pth --local-dir ./models
```
### Cara B

```bash
mkdir -p models
wget -O models/ckpt_fast.pth https://huggingface.co/plemeri/InSPyReNet/resolve/main/ckpt_fast.pth
```


## 4) Jalankan

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 5) Coba API

```bash
curl -F image="@/path/foto.png" -F quality="standard" "http://127.0.0.1:8000/image/remove-bg"
```

### Contoh Respon

```json
{
  "message": "Background removed successfully.",
  "original_filename": "foto.jpg",
  "result_filename": "a1b2c3d4e5f6.png",
  "result_url": "/uploads/a1b2c3d4e5f6.png",
  "content_type": "image/png",
  "quality": "standard"
}
```