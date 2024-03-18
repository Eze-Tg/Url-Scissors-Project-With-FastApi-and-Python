# My_Scissors_Project/config.py

from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env_name: str = "Development"
    base_url: str = "http://localhost:8000"
    db_url: str = 'postgresql://postgres:password@localhost/url_scissors_db'

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings