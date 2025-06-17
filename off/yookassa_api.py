import aiohttp
import os
import base64

YOOKASSA_SECRET = os.getenv("YOOKASSA_SECRET")
SHOP_ID = os.getenv("SHOP_ID")

async def get_receipt_url(payment_id: str) -> str:
    url = f"https://api.yookassa.ru/v3/payments/{payment_id}"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{SHOP_ID}:{YOOKASSA_SECRET}".encode()).decode(),
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("receipt", {}).get("url", None)
            return None
