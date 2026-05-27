# ocr.py

import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from model import classify

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_text_from_image(image_file):
    img = Image.open(image_file).convert("RGB")
    img = img.convert("L")
    img = img.resize((img.width * 2, img.height * 2))
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text.strip()


def analyze_image_abuse(image_file):
    text = get_text_from_image(image_file)

    if not text:
        return {
            "text": "",
            "label": "Non-Abusive",
            "score": 0.0,
            "category": "safe"
        }

    result = classify(text)

    return {
        "text": text,
        "label": result["label"],
        "score": result["score"],
        "category": result["category"]
    }