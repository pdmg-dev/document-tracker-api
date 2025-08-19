# app/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI

import init_db
from app.api.routes.admin import custom_fields, document_types, statuses, users
from app.api.routes.document import documents
from app.api.routes.user import auth
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


app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/admin", tags=["Admin - Users"])
app.include_router(statuses.router, prefix="/admin", tags=["Admin - Statuses"])
app.include_router(document_types.router, prefix="/admin", tags=["Admin - Document Types"])
app.include_router(custom_fields.router, prefix="/admin", tags=["Admin -  Custom Fields"])



@app.get("/")
async def root():
    logger.info("Root endpoint hit!")
    return {"message": "Document Tracking API is running!"}
