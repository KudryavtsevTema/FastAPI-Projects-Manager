from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str

settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8',
)