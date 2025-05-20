from utils.preprocess import preprocess_image
from utils.ocr import recognize_text
from session import get_session_id, download_captcha, verify_captcha
from display import show_images
import logging

def main():
    # Получение session_id и скачивание капчи
    session_id, session = get_session_id()
    if session_id:
        image_path = download_captcha(session_id, session)
        
        # Предобработка изображения
        processed_image, processed_path = preprocess_image(image_path, session_id)
        logging.info(f"Обработанное изображение сохранено: {processed_path}")
        
        # Отображение оригинального и обработанного изображений
        show_images(image_path, processed_path)
        
        # Распознавание текста
        for psm in [10]:  # Используем PSM 10 для символов
            recognized_text = recognize_text(processed_image, psm=psm)
            
            # Ограничиваем до 6 символов
            EXPECTED_LENGTH = 6
            recognized_text = (recognized_text[:EXPECTED_LENGTH] + ' ' * EXPECTED_LENGTH)[:EXPECTED_LENGTH]
            print(f"Распознанный текст (PSM={psm}): {recognized_text}")
            logging.info(f"Session ID: {session_id}, Recognized Text (PSM={psm}): {recognized_text}")
            
            # Проверка распознанного текста
            if recognized_text and any(c.isalnum() for c in recognized_text):
                if verify_captcha(session_id, recognized_text, session):
                    return
    
    print("Не удалось распознать или проверить капчу.")
    logging.error("Не удалось распознать или проверить капчу.")

if __name__ == "__main__":
    main()
