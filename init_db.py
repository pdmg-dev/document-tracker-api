# init_db.py

import asyncio

from app.core.database import Base, async_engine
from app.core.logger import get_logger
from app.models import Document
from table_reset import reset_table

logger = get_logger(__name__)

async def init_database():
    logger.warning("Resetting only the Document table...")
    await reset_table(Document)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database setup complete.")

if __name__ == "__main__":
    asyncio.run(init_database())
