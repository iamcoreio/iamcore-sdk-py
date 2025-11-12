from __future__ import annotations

from typing import Optional
from urllib.parse import urljoin

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_IAMCORE_ISSUER_PATH = "auth/"


class BaseConfig(BaseSettings):
    """Configuration for IAM Core SDK."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    iamcore_url: HttpUrl = Field(description="IAM Core URL")
    iamcore_issuer_url: Optional[HttpUrl] = Field(default=None, description="IAMCore issuer URL")
    iamcore_client_timeout: int = Field(description="IAM Core Client Timeout", default=30, ge=1, le=300)

    @property
    def iamcore_url_str(self) -> str:
        """Get IAM Core URL as string."""
        return str(self.iamcore_url)

    @property
    def get_iamcore_issuer_url(self) -> str:
        """Get IAM Core Issuer URL as string."""
        if iamcore_issuer_url := self.iamcore_issuer_url:
            return str(iamcore_issuer_url)
        return urljoin(str(self.iamcore_url), DEFAULT_IAMCORE_ISSUER_PATH)
