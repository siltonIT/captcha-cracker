import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Путь к папке с капчами
CAPTCHA_DIR = os.path.expanduser(os.getenv("CAPTCHA_DIR"))

# Создаём общую папку
if not os.path.exists(CAPTCHA_DIR):
    os.makedirs(CAPTCHA_DIR)

# Настройка логирования
LOG_DIR = os.getenv("LOG_DIR")
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME")
LOG_FILE = os.path.join(LOG_DIR, LOG_FILE_NAME)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Очищаем лог-файл перед запуском
open(LOG_FILE, 'w').close()
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# URL сайта с капчей
BASE_URL = os.getenv("BASE_URL")
