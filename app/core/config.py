from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: list

    API_HOST: str
    API_PORT: int

    UPLOAD_DIRECTORY: str
    OTHER_FILES_DIRECTORY_NAME: str

    FILE_CRYPT: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = Settings()
