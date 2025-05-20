from PIL import Image
import pytesseract

def recognize_text(image, psm=6):
    # Конвертация numpy array в PIL Image
    pil_image = Image.fromarray(image)
    
    # Ограничение символов: только a-z, A-Z, 0-9
    whitelist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    # Настройки Tesseract
    custom_config = f'--oem 3 --psm {psm} -c tessedit_char_whitelist={whitelist}'
    
    # Распознавание текста
    text = pytesseract.image_to_string(pil_image, config=custom_config)
    return text.strip()
