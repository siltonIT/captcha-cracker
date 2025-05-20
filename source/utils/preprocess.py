import cv2
from config import CAPTCHA_DIR

def preprocess_image(image_path, session_id):
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Не удалось загрузить изображение для предобработки: {image_path}")

    # Преобразование в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Простая бинаризация для нахождения текста
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Усиление контура 
    edges = cv2.Canny(binary, 100, 200) 
    result = cv2.bitwise_or(binary, edges)

    # Сохранение обработанного изображения
    processed_path = f"{CAPTCHA_DIR}/processed_{session_id}.png"
    cv2.imwrite(processed_path, result)

    return result, processed_path
