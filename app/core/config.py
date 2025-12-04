from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MySQL
    MYSQL_HOST: str = "h192.252.187.219"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "package_admin"
    MYSQL_PASSWORD: str = "XbzdbXZnGxCYpBiC"
    MYSQL_DB: str = "package_system"

    # Redis
    REDIS_HOST: str = "h192.252.187.219"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = "redis_PPkznB"

    # Cloudflare R2
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_REGION: str = "auto"
    R2_ENDPOINT_URL: Optional[str] = None
    ORIGINAL_PACKAGE_PREFIX: str = "original/"
    PROCESSED_PACKAGE_PREFIX: str = "processed/"

    # Cloudflare CDN
    CDN_DOMAIN: str
    FIXED_TAG: str = "release"

    # System
    API_KEY: str
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str
    MAX_PACKAGE_SIZE: int = 21474836480
    SECRET_KEY: str
    DEBUG: bool = True

    # Alerts
    DINGTALK_WEBHOOK: Optional[str] = None
    EMAIL_SMTP_HOST: Optional[str] = None
    EMAIL_SMTP_PORT: int = 465
    EMAIL_USER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    @property
    def REDIS_URL(self) -> str:
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/0"


settings = Settings()
