# app/main.py
from fastapi import FastAPI

from .core.database import Base, engine
from .core.logger import get_logger
from .routes import admin

logger = get_logger(__name__)
app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created.")


app.include_router(admin.router)


@app.get("/")
def root():
    logger.info("Root endpoint hit!")
    return {"message": "Document Tracking API is running!"}
