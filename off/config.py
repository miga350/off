import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOOKASSA_SECRET = os.getenv("YOOKASSA_SECRET")
SHOP_ID = os.getenv("SHOP_ID")
DB_URL = os.getenv("DB_URL", "postgresql+asyncpg://postgres:postgres@db:5432/pdfbot")
FILES_PATH = os.getenv("FILES_PATH", "files")
