from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db: str = Field(...)
    mongo_host: str = Field(...)
    mongo_port: int = Field(...)
    mongo_username: str = Field(...)
    mongo_password: str = Field(...)
    mongo_auth_source: str = Field(...)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
