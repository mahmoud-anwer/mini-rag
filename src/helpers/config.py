from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Setting some validation
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    # Reading the environment variables
    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
