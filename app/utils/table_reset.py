# app/utils/table_reset.py

import importlib
import sys

from sqlalchemy.orm import DeclarativeMeta

from app.core.database import engine
from app.core.logger import get_logger

logger = get_logger(__name__)


def reset_table(model: DeclarativeMeta):
    table = model.__table__
    logger.info(f"Resetting table '{table.name}'...")
    table.drop(engine, checkfirst=True)
    table.create(engine)
    logger.info(f"Table '{table.name}' reset complete.")


def get_model(model_name: str) -> DeclarativeMeta | None:
    try:
        module = importlib.import_module(f"app.models.{model_name.lower()}")
        model_class = getattr(module, model_name)
        return model_class
    except (ModuleNotFoundError, AttributeError) as e:
        logger.error(f"Model '{model_name}' not found: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reset_table.py <ModelName>")
        sys.exit(1)

    model_name = sys.argv[1]
    model = get_model(model_name)

    if model:
        reset_table(model)
    else:
        print(
            f"❌ Could not find model '{model_name}' in app.models.{model_name.lower()}"
        )
