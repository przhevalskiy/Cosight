from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    # Mistral (fallback)
    mistral_api_key: str = ""
    mistral_model: str = "mistral-large-latest"

    # Google APIs (GA4 + GSC share one service-account JSON)
    google_credentials_json: str = ""
    google_credentials_file: str = ""
    ga4_property_id: str = "288367390"
    gsc_site_url: str = "https://business.columbia.edu/"

    # Emma email marketing
    emma_public_key: str = ""
    emma_private_key: str = ""
    emma_account_id: str = ""

    # Sprout Social
    sprout_api_token: str = ""
    sprout_cbs_group_ids: str = "2415696,2468619,2551611"
    sprout_data_lag_days: int = 2

    # Event Registry (media mentions — optional)
    eventregistry_api_key: str = ""

    # Application
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    debug: bool = True
    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
