from pydantic_settings import BaseSettings, SettingsConfigDict
import os

DOTENV = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    # DB
    postgres_hostname: str
    postgres_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    # email
    email_host: str

    secret_key: str

    # JWT
    access_token_expire_minutes: int

    debug: bool

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
