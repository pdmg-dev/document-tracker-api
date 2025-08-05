from fastapi import FastAPI

from .core.logger import get_logger

app = FastAPI()
logger = get_logger(__name__)


@app.get("/")
def root():
    logger.info("Root endpoint hit!")
    return {"message": "Document Tracking API is running!"}
