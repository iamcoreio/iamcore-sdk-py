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
        self.auth = AuthClient(config.iamcore_issuer_url, config.iamcore_client_timeout)
        # Resource clients
        self.api_key = ApiKeyClient(config.iamcore_url, config.iamcore_client_timeout)
        self.application = AppClient(config.iamcore_url, config.iamcore_client_timeout)
        self.application_resource_type = AppResourceTypeClient(config.iamcore_url, config.iamcore_client_timeout)
        self.evaluate = EvaluateClient(config.iamcore_url, config.iamcore_client_timeout)
        self.group = GroupClient(config.iamcore_url, config.iamcore_client_timeout)
        self.policy = PolicyClient(config.iamcore_url, config.iamcore_client_timeout)
        self.resource = ResourceClient(config.iamcore_url, config.iamcore_client_timeout)
        self.tenant = TenantClient(config.iamcore_url, config.iamcore_client_timeout)
        self.user = UserClient(config.iamcore_url, config.iamcore_client_timeout)
