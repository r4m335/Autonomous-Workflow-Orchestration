from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_name: str = "Digital Worker Platform"
    debug: bool = False
    
    # Database Settings
    db_path: str = os.getenv("DB_PATH", "digital_worker_state.db")
    legacy_db_path: str = os.getenv("LEGACY_DB_PATH", "digital_worker.db")
    
    # Agent Settings
    default_tenant: str = "tenant_a"
    validation_threshold: float = 0.8
    
    # Ingestion Settings
    gmail_user: str = "bot@bpo-firm.com"
    gmail_pass: str = "v3ry-s3cur3-p4ss"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
