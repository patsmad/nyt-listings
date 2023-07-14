from pytesseract import pytesseract
from src.util.config import Config

path_to_tesseract = Config().path_to_tesseract
pytesseract.tesseract_cmd = path_to_tesseract

def get_text(img):
    data =  pytesseract.image_to_string(img).strip().replace('\n', ' ')
    return data
