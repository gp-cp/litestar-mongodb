from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = True
    # Redis stuff
    REDIS_URL: str = "redis://localhost:6379"
    # Mongo stuff
    MONGO_URL: str = "mongodb://localhost"
    MONGO_DB: str = "app"
    TEMPLATE_DIR: str = "src/templates"
    STATIC_DIR: str = "src/static"
    MAX_CONNECTIONS: int = 100
    MIN_CONNECTIONS: int = 10

    # Secret key for cookie
    SECRET_KEY: str = "CHANGE_ME"
    ADMIN_PASSWORD: str = "CHANGE_ME"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
