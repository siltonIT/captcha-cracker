import requests
import logging
from config import CAPTCHA_DIR, BASE_URL, logging

def get_session_id():
    session = requests.Session()  # Создаём сессию для сохранения куки
    response = session.get(f"{BASE_URL}/captcha")
    if response.status_code == 200:
        data = response.json()
        session_id = data.get("session_id")
        logging.info(f"Получен session_id: {session_id}")
        return session_id, session
    else:
        raise Exception(f"Ошибка получения session_id: {response.status_code}, Ответ: {response.text}")

def download_captcha(session_id, session):
    url = f"{BASE_URL}/captcha-image?session_id={session_id}"
    response = session.get(url, stream=True)
    if response.status_code == 200:
        filename = f"{CAPTCHA_DIR}/captcha_{session_id}.png"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        logging.info(f"Изображение сохранено как: {filename}")
        return filename
    else:
        raise Exception(f"Ошибка скачивания изображения: {response.status_code}, Ответ: {response.text}")

def verify_captcha(session_id, captcha_text, session):
    url = f"{BASE_URL}/captcha"
    payload = {'captcha': captcha_text}
    params = {'session_id': session_id}  # Передаём session_id как параметр
    cookies = {'session_id': session_id}  # Передаём session_id в куки
    try:
        response = session.post(url, data=payload, params=params, headers={'Content-Type': 'application/x-www-form-urlencoded'}, cookies=cookies)
        logging.info(f"Отправлен POST-запрос: URL={url}, Payload={payload}, Params={params}, Cookies={cookies}")
        logging.info(f"Ответ сервера (сырой): {response.text}")
        
        if response.status_code == 200:
            if response.text.strip():  # Проверяем, не пустой ли ответ
                data = response.json()
                if data.get("success"):
                    logging.info(f"Капча успешно проверена. Session ID: {session_id}, Текст: {captcha_text}")
                    print(f"Капча успешно проверена! Текст: {captcha_text}")
                    return True
                else:
                    logging.warning(f"Неверный текст капчи. Session ID: {session_id}, Текст: {captcha_text}, Сообщение: {data.get('message')}")
                    print(f"Неверный текст: {captcha_text}.")
                    return False
            else:
                logging.error(f"Пустой ответ сервера при статусе 200 для session_id: {session_id}")
                raise Exception("Пустой ответ сервера при статусе 200")
        else:
            logging.error(f"Ошибка проверки капчи: {response.status_code}, Ответ сервера: {response.text}")
            raise Exception(f"Ошибка проверки капчи: {response.status_code}, Ответ сервера: {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Сетевая ошибка при проверке капчи: {str(e)}")
        raise Exception(f"Сетевая ошибка при проверке капчи: {str(e)}")
