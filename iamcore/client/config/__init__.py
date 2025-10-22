from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    iamcore_url: str
    iamcore_issuer_url: str
    system_backend_client_id: str
    iamcore_client_timeout: int = 30

    def set_iamcore_config(self, iamcore_url: str, iamcore_issuer_url: str, client_id: str) -> None:
        self.iamcore_url = iamcore_url
        self.iamcore_issuer_url = iamcore_issuer_url
        self.system_backend_client_id = client_id
