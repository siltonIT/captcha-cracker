import requests
import logging
from config import CAPTCHA_DIR, BASE_URL, logging
import os

def get_session_id():
    session = requests.Session()  # Создаём сессию для сохранения куки
    try:
        response = session.get(f"{BASE_URL}")  # Убран timeout
        if response.status_code == 200:
            # Извлекаем session_id из куки
            session_id = session.cookies.get("session_id")
            if not session_id:
                logging.error("Кука session_id не найдена в ответе сервера")
                raise Exception("Кука session_id не найдена в ответе сервера")
            logging.info(f"Получен session_id из куки: {session_id}")
            return session_id, session
        else:
            logging.error(f"Ошибка получения session_id: {response.status_code}, Тело ответа: {response.text[:500]}")
            raise Exception(f"Ошибка получения session_id: {response.status_code}, Тело ответа: {response.text[:500]}")
    except requests.RequestException as e:
        logging.error(f"Сетевая ошибка при получении session_id: {str(e)}")
        raise Exception(f"Сетевая ошибка при получении session_id: {str(e)}")

def download_captcha(session_id, session):
    url = f"{BASE_URL}/captcha-image?session_id={session_id}"
    try:
        response = session.get(url, stream=True)  # Убран timeout
        response.raise_for_status()  # Вызывает исключение при ошибке HTTP
        filename = f"{CAPTCHA_DIR}/captcha_{session_id}.png"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:  # Фильтруем пустые чанки
                    f.write(chunk)
        logging.info(f"Изображение капчи сохранено как: {filename}")
        return filename
    except requests.RequestException as e:
        logging.error(f"Ошибка при скачивании капчи с {url}: {str(e)}, Тело ответа: {getattr(e.response, 'text', 'Нет данных')[:500]}")
        raise Exception(f"Ошибка при скачивании капчи: {str(e)}")

def download_random_image(session_id, session):
    url = f"{BASE_URL}/random-image?session_id={session_id}"
    try:
        response = session.get(url, stream=True)  # Убран timeout
        response.raise_for_status()  # Вызывает исключение при ошибке HTTP
        filename = f"{CAPTCHA_DIR}/random_{session_id}.png"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:  # Фильтруем пустые чанки
                    f.write(chunk)
        logging.info(f"Случайное изображение сохранено как: {filename}")
        return filename
    except requests.RequestException as e:
        logging.error(f"Ошибка при скачивании случайного изображения с {url}: {str(e)}, Тело ответа: {getattr(e.response, 'text', 'Нет данных')[:500]}")
        return None

def verify_captcha(session_id, captcha_text, session):
    url = f"{BASE_URL}/captcha"  # Указываем правильный endpoint для POST-запроса
    payload = {'captcha': captcha_text, 'attempts': '0'}  # Добавляем attempts
    cookies = {'session_id': session_id}  # Передаём session_id в куки
    try:
        # Отправляем запрос, разрешаем перенаправления
        response = session.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'}, cookies=cookies, allow_redirects=True)  # Убран timeout
        logging.info(f"Отправлен POST-запрос: URL={url}, Payload={payload}, Cookies={cookies}")
        logging.info(f"Ответ сервера (сырой): {response.text[:500]}")
        
        # Проверяем конечный URL после перенаправлений
        final_url = response.url
        logging.info(f"Конечный URL после перенаправлений: {final_url}")
        
        # Проверяем, является ли конечный URL страницей успеха
        if "/success" in final_url and response.status_code == 200:
            # Скачиваем случайное изображение
            random_image_path = download_random_image(session_id, session)
            if random_image_path:
                logging.info(f"Случайное изображение скачано: {random_image_path}")
            else:
                logging.warning("Не удалось скачать случайное изображение")
            
            logging.info(f"Капча успешно проверена. Session ID: {session_id}, Текст: {captcha_text}")
            return True, random_image_path
        elif response.status_code == 200:
            if response.text.strip():  # Проверяем, не пустой ли ответ
                try:
                    data = response.json()
                    if data.get("success"):
                        logging.info(f"Капча успешно проверена. Session ID: {session_id}, Текст: {captcha_text}")
                        return True, None  # Нет изображения, так как не было перенаправления
                    else:
                        logging.warning(f"Неверный текст капчи. Session ID: {session_id}, Текст: {captcha_text}, Сообщение: {data.get('message')}")
                        return False, None
                except ValueError:
                    logging.error(f"Не удалось разобрать JSON в ответе: {response.text[:500]}")
                    raise Exception(f"Не удалось разобрать JSON в ответе: {response.text[:500]}")
            else:
                logging.error(f"Пустой ответ сервера при статусе 200 для session_id: {session_id}")
                raise Exception("Пустой ответ сервера при статусе 200")
        else:
            logging.error(f"Ошибка проверки капчи: {response.status_code}, Тело ответа: {response.text[:500]}")
            raise Exception(f"Ошибка проверки капчи: {response.status_code}, Тело ответа: {response.text[:500]}")
    except requests.RequestException as e:
        logging.error(f"Сетевая ошибка при проверке капчи: {str(e)}, Тело ответа: {getattr(e.response, 'text', 'Нет данных')[:500]}")
        raise Exception(f"Сетевая ошибка при проверке капчи: {str(e)}")
