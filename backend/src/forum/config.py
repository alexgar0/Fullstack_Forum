from functools import lru_cache
from typing import Tuple
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7     # 7 Days
    
    username_length_bounds: Tuple[int, int] = (4, 15)
    branch_name_length_bounds: Tuple[int, int] = (2, 30)
    topic_title_length_bounds: Tuple[int, int] =  (5, 60)
    topic_edition_timeframe_minutes: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Gets the application settings.

    This function returns a cached instance of the Settings class, ensuring that the settings
    are loaded only once.

    Returns:
        The application settings.
    """
    return Settings()  # type: ignore[call-arg]


settings = get_settings()