from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://asset_mgmt:asset_mgmt@localhost:5432/asset_management"
    cors_origins: list[str] = ["http://localhost:4200"]  # Angular dev server


settings = Settings()
