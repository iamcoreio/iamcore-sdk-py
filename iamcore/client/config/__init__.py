from pydantic import Field, HttpUrl, TypeAdapter
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Configuration for IAM Core SDK."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    iamcore_url: HttpUrl = Field(description="IAM Core URL")
    iamcore_issuer_url: HttpUrl = Field(description="IAM Core Issuer URL")
    system_backend_client_id: str = Field(description="System Backend Client ID")
    iamcore_client_timeout: int = Field(description="IAM Core Client Timeout", default=30, ge=1, le=300)

    def set_iamcore_config(self, iamcore_url: str, iamcore_issuer_url: str, client_id: str) -> None:
        """Manually set configuration values."""
        url_adapter = TypeAdapter(HttpUrl)
        # Create a new instance with updated values
        object.__setattr__(self, "iamcore_url", url_adapter.validate_python(iamcore_url))
        object.__setattr__(self, "iamcore_issuer_url", url_adapter.validate_python(iamcore_issuer_url))
        object.__setattr__(self, "system_backend_client_id", client_id)

    @property
    def iamcore_url_str(self) -> str:
        """Get IAM Core URL as string."""
        return str(self.iamcore_url)

    @property
    def iamcore_issuer_url_str(self) -> str:
        """Get IAM Core Issuer URL as string."""
        return str(self.iamcore_issuer_url)
