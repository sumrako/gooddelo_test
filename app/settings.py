from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str
    ALLOWED_HOST: str
    ALLOWED_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
