# app/main.py

from fastapi import FastAPI

from .core.logger import get_logger
from .routes import admin, auth, user
from .startup.init_db import init_database

logger = get_logger(__name__)
app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_database()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def root():
    logger.info("Root endpoint hit!")
    return {"message": "Document Tracking API is running!"}
