import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

# ساخت پوشه logs در صورت وجود نداشتن
os.makedirs(LOG_DIR, exist_ok=True)

# فرمت لاگ
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, LOG_FILE), maxBytes=5 * 1024 * 1024, backupCount=3  # 5 MB
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
