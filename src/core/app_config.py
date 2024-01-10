from pydantic import Field
from pydantic import ValidationError, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.enums import DBEngine
from functools import cached_property
from urllib.parse import urlparse, urlunparse

DEFAULT_DATABASE_NAME = "app_db"

# Obviously a very basic app config, not recommended for production use.
# It would be better to get your config from secret managers / feature flag solutions!


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    LOGLEVEL: str = Field(default="info")
    DB_ENGINE: str = Field(default=DBEngine.SQLITE.name)
    SQLITE_DATA_PATH: str = Field(default="/./database.db")
    POSTGRES_URI: str = Field(default="postgres://test:test@postgres/database")
    CORS_ALLOWED_ORIGINS: list = Field(default=["*"])
    CORS_ALLOWED_METHODS: list = Field(default=["*"])
    CORS_ALLOWED_HEADERS: list = Field(default=["*"])
    CORS_ALLOW_CREDENTIALS: bool = Field(default=False)

    @field_validator("DB_ENGINE")
    def validate_db_engine(cls, value: str):
        if value.upper() not in DBEngine.keys:
            raise ValidationError(
                f"invalid or unsupported engine. please use one of {DBEngine.keys}"
            )
        return value

    @computed_field(return_type=str)
    @cached_property
    def DATABASE_URI(self):
        engine = getattr(DBEngine, self.DB_ENGINE.upper()).value
        if engine == DBEngine.SQLITE.value:
            conn = f"{engine}://{self.SQLITE_DATA_PATH}"
        elif engine == DBEngine.POSTGRES.value:
            # just to make sure we are using the correct engine for connection
            parsed_uri = urlparse(self.POSTGRES_URI)
            db = parsed_uri.path[1:] or DEFAULT_DATABASE_NAME
            conn = urlunparse(
                parsed_uri._replace(scheme=DBEngine.POSTGRES.value, path=f"/{db}")
            )
        return conn

config = Settings()
