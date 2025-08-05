# app/core/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    debug: bool

    log_level: str
    log_dir: str
    log_file: str
    log_format: str
    log_datefmt: str

    host: str
    port: int
    reload: bool

    database_url: str

    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = {"env_file": ".env"}

settings = Settings()
