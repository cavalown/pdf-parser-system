from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PDF Parser API"
    debug: bool = False
    upload_dir: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
