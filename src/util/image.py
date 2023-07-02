import io
from skimage.transform import resize
import numpy as np
from PIL import Image
import imageio

def open_image(fname: str) -> Image:
    return Image.open(fname)

def crop_image(image: Image, left: int, top: int, width: int, height: int) -> Image:
    return image.crop((left, top, left + width, top + height))

def image_to_buf(image: Image) -> io.BytesIO:
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return buf

def getImage(url: str) -> np.ndarray:
    return imageio.imread_v2(url)

def resizeImage(image: np.ndarray, new_size: tuple):
    return resize(image, new_size, anti_aliasing=True)

def writeImage(image: np.ndarray, file_path: str):
    im = Image.fromarray((image * 255).astype(np.uint8))
    imageio.imwrite(file_path, im)
