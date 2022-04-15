from typing import Any, Dict, Optional

from pydantic import (
    AnyUrl,
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    HttpUrl,
    RedisDsn,
    validator,
)

from app.core.environment import Environment


class AmqpDsn(AnyUrl):
    allowed_schemes = {"amqp"}
    user_required = False


class Settings(BaseSettings):
    API_V0_STR: str = "/api/v0"

    SERVER_HOST: Optional[AnyHttpUrl]
    PROJECT_NAME: str = "Eligibility-Service"
    ENVIRONMENT: Environment = Environment("development")

    ENABLE_RATE_LIMITING: bool

    SENTRY_DSN: Optional[HttpUrl] = None

    HTTP_BASIC_AUTH_USERNAME: str
    HTTP_BASIC_AUTH_PASSWORD: str

    REDIS_SERVER: str
    REDIS_USER: Optional[str]
    REDIS_PASSWORD: str
    REDIS_DB: Optional[str]
    REDIS_URI: Optional[RedisDsn] = None

    @validator("REDIS_URI", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            user=values.get("REDIS_USER") or "",
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_SERVER"),
            path=f"/{values.get('REDIS_DB') or '0'}",
        )

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_SCHEMA: str = "public"
    APP_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_POOL_SIZE: int = 10

    @validator("APP_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    RABBITMQ_DEFAULT_USER: Optional[str]
    RABBITMQ_DEFAULT_PASS: Optional[str]
    RABBITMQ_SERVER: Optional[str]
    RABBITMQ_NODE_PORT: Optional[int]
    RABBITMQ_DEFAULT_VHOST: Optional[str]

    AMQP_URI: Optional[AmqpDsn] = None

    @validator("AMQP_URI", pre=True)
    def assemble_amqp_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            user=values.get("RABBITMQ_DEFAULT_USER") or "",
            password=values.get("RABBITMQ_DEFAULT_PASS") or "",
            host=values.get("RABBITMQ_SERVER") or "",
            port=str(values.get("RABBITMQ_NODE_PORT") or 5679),
            path=""
            if values.get("RABBITMQ_DEFAULT_VHOST") is None
            else f"/{values.get('RABBITMQ_DEFAULT_VHOST')}",
        )

    EXAMPLE_API_ENDPOINT: AnyHttpUrl

    class Config:
        case_sensitive = True


settings = Settings()
