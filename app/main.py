# app/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import admin_route, auth_route, documents, statuses
from app.core.database import Base, async_engine
from app.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (if not exist)")

    yield  # <-- App is running here

    # Shutdown
    await async_engine.dispose()
    logger.info("Database connection closed")


# Create app with lifespan
app = FastAPI(
    title="Document Tracking API",
    lifespan=lifespan,
)


# Register routers
app.include_router(documents.router)
app.include_router(statuses.router)
app.include_router(admin_route.router)
app.include_router(auth_route.router)


@app.get("/")
async def root():
    logger.info("Root endpoint hit!")
    return {"message": "Document Tracking API is running!"}
