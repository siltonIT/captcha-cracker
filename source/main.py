from utils.preprocess import preprocess_image
from utils.ocr import recognize_text
from session import get_session_id, download_captcha, verify_captcha
import logging
import os
from display import show_image

def main():
    random_image_path = None
    while True:
        # Получение session_id и скачивание капчи
        try:
            session_id, session = get_session_id()
            if session_id:
                image_path = download_captcha(session_id, session)
            
                # Предобработка изображения
                processed_image, processed_path = preprocess_image(image_path, session_id)
                logging.info(f"Обработанное изображение сохранено: {processed_path}")
            
                # Распознавание текста
                for psm in [10]:  # Используем PSM 10 для символов
                    recognized_text = recognize_text(processed_image, psm=psm)
                
                    # Ограничиваем до 6 символов
                    EXPECTED_LENGTH = 6
                    recognized_text = (recognized_text[:EXPECTED_LENGTH] + ' ' * EXPECTED_LENGTH)[:EXPECTED_LENGTH]
                    logging.info(f"Session ID: {session_id}, Recognized Text (PSM={psm}): {recognized_text}")
                
                    # Проверка распознанного текста
                    if recognized_text and any(c.isalnum() for c in recognized_text):
                        success, random_image_path = verify_captcha(session_id, recognized_text, session)
                        if success:
                            break
        except Exception as e:
            logging.error(f"Ошибка в основном цикле: {str(e)}")
        
        if random_image_path:
            break
        logging.error("Не удалось распознать или проверить капчу.")

    return random_image_path

if __name__ == "__main__":
    image_path = main()
    if image_path and os.path.exists(image_path):
        print(f"Случайное изображение скачано и сохранено: {image_path}")
        try:
            show_image(image_path)
            # Удаляем файл
            os.remove(image_path)
            print(f"Изображение удалено: {image_path}")
        except Exception as e:
            print(f"Ошибка при работе с изображением: {e}")
    else:
        print("Капча не была решена, изображение не скачано.")
