# app/main.py
from fastapi import FastAPI

from .core.database import Base, engine
from .core.logger import get_logger
from .routes import admin
from .core.settings import settings
from .models.user import User

logger = get_logger(__name__)
app = FastAPI()


@app.on_event("startup")
def on_startup():
    if settings.reset_table:
        logger.info(f"Dropping and recreating '{User.__tablename__}' table...")
        User.__table__.drop(engine)
        User.__table__.create(engine)

    Base.metadata.create_all(bind=engine)
    logger.info("Database setup complete.")


app.include_router(admin.router)


@app.get("/")
def root():
    logger.info("Root endpoint hit!")
    return {"message": "Document Tracking API is running!"}
