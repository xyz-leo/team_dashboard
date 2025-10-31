from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    BASE_DIR: Path = Path(__file__).resolve().parent.parent


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()


""" 
Debug
Example usage: python -m app.core.config
"""
if __name__ == "__main__":
    print("DATABASE_URL:", settings.DATABASE_URL)
    print("DEBUG:", settings.DEBUG)
    print("BASE_DIR:", settings.BASE_DIR)
