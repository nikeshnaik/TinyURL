from pydantic import BaseModel, BaseSettings, Field  # type: ignore


class AppSettings(BaseSettings):

    DB_URL: str = None
    TINY_URL_ENV: str = None
    LOG_CONFIG: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


Settings = AppSettings()
print(Settings.DB_URL)
