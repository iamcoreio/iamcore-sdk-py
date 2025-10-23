from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    iamcore_url: str = Field(description="IAM Core URL")
    iamcore_issuer_url: str = Field(description="IAM Core Issuer URL")
    system_backend_client_id: str = Field(description="System Backend Client ID")
    iamcore_client_timeout: int = Field(description="IAM Core Client Timeout", default=30)

    def set_iamcore_config(self, iamcore_url: str, iamcore_issuer_url: str, client_id: str) -> None:
        self.iamcore_url = iamcore_url
        self.iamcore_issuer_url = iamcore_issuer_url
        self.system_backend_client_id = client_id
