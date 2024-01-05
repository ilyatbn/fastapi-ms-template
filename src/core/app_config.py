from pydantic import Field
from pydantic import ValidationError, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.enums import DBEngine
from functools import cached_property
from urllib.parse import urlparse, urlunparse

# Obviously a very basic app config, not recommended for production use.
# It would be better to get your config from secret managers / feature flag solutions!
class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    LOGLEVEL: str = Field(default = "info")
    DB_ENGINE: str = Field(default = DBEngine.SQLITE.value)
    SQLITE_DATA_PATH: str = Field(default = '/./database.db')
    POSTGRES_URI: str = Field(default = 'postgres://test:test@postgres/database')

    @field_validator("DB_ENGINE")
    def validate_db_engine(cls, value):
        if value not in DBEngine.values:
            raise ValidationError(f"invalid or unsupported engine. please use one of {DBEngine.values}")

    @computed_field(return_type=str)
    @cached_property
    def DATABASE_URI(self):
        engine=self.DB_ENGINE
        if engine == DBEngine.SQLITE.value:
            conn = f"{engine}://{self.SQLITE_DATA_PATH}"
        elif engine == DBEngine.POSTGRES.value:
            # just to make sure we are using the correct engine for connection
            conn = urlunparse(urlparse(self.POSTGRES_URI)._replace(scheme=DBEngine.POSTGRES.value))
        return conn

config = Settings()
