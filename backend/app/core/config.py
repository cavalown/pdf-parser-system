from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PDF Parser API"
    debug: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()
