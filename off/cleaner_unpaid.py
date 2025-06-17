import os
import asyncio
from datetime import datetime, timedelta

FOLDER = "/app/files"
LIFETIME_MINUTES = 30

async def clean_unpaid_files():
    while True:
        now = datetime.utcnow()
        for filename in os.listdir(FOLDER):
            if filename.startswith("temp_"):
                full_path = os.path.join(FOLDER, filename)
                try:
                    stat = os.stat(full_path)
                    created = datetime.utcfromtimestamp(stat.st_ctime)
                    if now - created > timedelta(minutes=LIFETIME_MINUTES):
                        os.remove(full_path)
                        print(f"🧹 Удалён файл: {filename}")
                except Exception as e:
                    print(f"⚠️ Ошибка при удалении {filename}: {e}")
        await asyncio.sleep(300)  # Проверка каждые 5 минут
