from pydantic_settings import BaseSettings


class AiogramSettings(BaseSettings):
    token: str


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: str = 'INFO'
