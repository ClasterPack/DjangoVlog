import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Allow extra fields
    )
    title: str = Field(default="vlog", alias="PROJECT_NAME")
    """Postgres"""
    pg_name: str = Field(default="db", alias="POSTGRES_DB")
    pg_host: str = Field(default="postgres", alias="POSTGRES_HOST")
    pg_port: int = Field(default=5432, alias="POSTGRES_PORT")
    pg_user: str = Field(default="user", alias="POSTGRES_USER")
    pg_password: str = Field(default="password", alias="POSTGRES_PASSWORD")
    pg_max_age: int = Field(default=60, alias="PG_CONN_MAX_AGE")
    pg_echo: bool = Field(default=True, alias="POSTGRES_ECHO")
    """Django"""
    debug: bool = Field(default=False, alias="DEBUG")
    django_secret_key: str = Field(default="secret", alias="SECRET_KEY")
    allowed_hosts: List[str] = Field(default=["localhost"], alias="ALLOWED_HOSTS")
    page_size: int = Field(default=20, alias="PAGE_SIZE")
    max_page_size: int = Field(default=100, alias="MAX_PAGE_SIZE")
    django_language: str = Field(default="en", alias="LANGUAGE")
    static_url: str = Field(default="/static/", alias="STATIC_URL")
    """Celery"""
    celery_broker: str = Field(default="celery", alias="CELERY_BROKER")
    celery_result_backend: str = Field(default="celery", alias="CELERY_RESULT_BACKEND")
    celery_task_always_eager: bool = Field(default=False, alias="CELERY_TASK_ALWAYS_EAGER")
    """Cache"""
    cache_url: str = Field(default="redis://redis:6379/2", alias="CACHE_URL")
    page_detail_cache_ttl: int = Field(default=60, alias="PAGE_DETAIL_CACHE_TTL")


config = Settings()