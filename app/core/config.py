from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Blog App")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    SECRET: str = os.getenv("SECRET", "SECRET")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:admin@localhost:5432/blogs_app")

    class Config:
        env_file = ".env"


settings = Settings()