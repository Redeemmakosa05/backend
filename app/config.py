from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_username: str
    admin_password: str
    resend_api_key: str
    email_from: str
    email_to: str
    frontend_url: str = "https://redeemmakosa05.github.io"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
