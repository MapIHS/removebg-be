from PIL import ImageFilter, Image

def refine_alpha(rgba: Image.Image, feather=1, dilate=0) -> Image.Image:
    r,g,b,a = rgba.split()
    if dilate > 0:
        k = max(3, dilate if dilate % 2 else dilate+1)
        a = a.filter(ImageFilter.MaxFilter(size=k))
    if feather > 0:
        a = a.filter(ImageFilter.GaussianBlur(radius=feather))
    return Image.merge("RGBA", (r,g,b,a))
