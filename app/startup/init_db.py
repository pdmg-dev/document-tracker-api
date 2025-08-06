from app.core.database import Base, engine
from app.core.logger import get_logger
from app.core.settings import settings
from app.models import Document, User
from app.utils.table_reset import reset_table

logger = get_logger(__name__)


def init_database():
    if settings.reset_table:
        logger.warning("Resetting dev tables...")
        reset_table(User)
        reset_table(Document)

    Base.metadata.create_all(bind=engine)
    logger.info("Database setup complete.")
