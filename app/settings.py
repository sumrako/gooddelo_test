from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DB: str
    ALLOWED_HOST: str
    ALLOWED_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB_NUM: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
