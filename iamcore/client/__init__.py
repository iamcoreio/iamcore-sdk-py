from __future__ import annotations

from iamcore.client.api_key import Client as ApiKeyClient
from iamcore.client.application import Client as AppClient
from iamcore.client.application_resource_type import Client as AppResourceTypeClient
from iamcore.client.auth import Client as AuthClient
from iamcore.client.config import BaseConfig
from iamcore.client.evaluate import Client as EvaluateClient
from iamcore.client.group import Client as GroupClient
from iamcore.client.policy import Client as PolicyClient
from iamcore.client.resource import Client as ResourceClient
from iamcore.client.tenant import Client as TenantClient
from iamcore.client.user import Client as UserClient


class Client:
    """Iamcore client."""

    def __init__(self, config: BaseConfig) -> None:
        # Client configuration
        self.config = config
        # Authentication client
        self.auth = AuthClient(self.config.get_iamcore_issuer_url, self.config.iamcore_client_timeout)
        # Resource clients
        self.api_key = ApiKeyClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.application = AppClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.application_resource_type = AppResourceTypeClient(
            self.config.iamcore_url_str, self.config.iamcore_client_timeout
        )
        self.evaluate = EvaluateClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.group = GroupClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.policy = PolicyClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.resource = ResourceClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.tenant = TenantClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)
        self.user = UserClient(self.config.iamcore_url_str, self.config.iamcore_client_timeout)


__all__ = [
    "ApiKeyClient",
    "AppClient",
    "AppResourceTypeClient",
    "AuthClient",
    "BaseConfig",
    "Client",
    "EvaluateClient",
    "GroupClient",
    "PolicyClient",
    "ResourceClient",
    "TenantClient",
    "UserClient",
]
