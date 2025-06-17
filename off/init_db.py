import asyncio
from database.models import Base
from database.db import engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы успешно созданы.")

if __name__ == "__main__":
    asyncio.run(create_tables())
