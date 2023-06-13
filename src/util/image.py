import io
from PIL import Image

def open_image(fname: str) -> Image:
    return Image.open(fname)

def crop_image(image: Image, left: int, top: int, width: int, height: int) -> Image:
    return image.crop((left, top, left + width, top + height))

def image_to_buf(image: Image) -> io.BytesIO:
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return buf
