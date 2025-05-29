import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Path to the CAPTCHA directory
CAPTCHA_DIR = os.path.expanduser(os.getenv("CAPTCHA_DIR"))

# Create main directory if it doesn't exist
if not os.path.exists(CAPTCHA_DIR):
    os.makedirs(CAPTCHA_DIR)

# Logging configuration
LOG_DIR = os.getenv("LOG_DIR")
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME")
LOG_FILE = os.path.join(LOG_DIR, LOG_FILE_NAME)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Clear log file before starting
open(LOG_FILE, 'w').close()
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Website URL with CAPTCHA
BASE_URL = os.getenv("BASE_URL")
