from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Obviously a very basic app config for the current example code. 
# It would be better to get your config from secret managers / feature flag solutions!

class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    LOGLEVEL: str = Field(default = "info")

config = Settings()
