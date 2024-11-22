from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings that are loaded from environment variables.

    Attributes:
        APP_NAME (str): The name of the application.
        APP_VERSION (str): The version of the application.
        OPENAI_API_KEY (str): The API key for accessing OpenAI services.
        FILE_ALLOWED_TYPES (list): The list of allowed file types.
        FILE_MAX_SIZE (int): The maximum size allowed for uploaded files.
        FILE_DEFAULT_CHUNK_SIZE (int): The default chunk size for file uploads.

    Config:
        env_file (str): The path to the environment file that contains the settings.
    """

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGODB_URL: str
    MONGODB_DATABASE: str
    MINIO_URL: str
    MINIO_BUCKET_NAME: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str

    class Config:
        env_file = ".env"

def get_settings():
    """
    Retrieves the application settings.

    This function reads the settings from the environment variables
    defined in the `.env` file and returns an instance of the `Settings` class.

    Returns:
        Settings: An instance of the `Settings` class populated with the
        application settings.
    """
    return Settings()
