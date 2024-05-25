from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Blog App")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    SECRET: str = os.getenv("SECRET", "SECRET")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:admin@localhost:5432/blogs_app")

    class Config:
        env_file = ".env"


settings = Settings()