# My_Scissors_Project/config.py

from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv
import os

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)
DB_URL = os.getenv('DB_URL')

class Settings(BaseSettings):
    env_name: str = "Development"
    base_url: str = "http://localhost:8000"
    db_url: str = DB_URL

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}; The db url is {settings.db_url}")
    return settings