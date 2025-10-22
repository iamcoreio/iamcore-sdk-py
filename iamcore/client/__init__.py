from iamcore.client import (
    api_key,
    application,
    application_resource_type,
    group,
    policy,
    resource,
    tenant,
    user,
)
from iamcore.client.config import BaseConfig


class Client:
    """Iamcore client."""

    api_key: api_key.Client
    application: application.Client
    application_resource_type: application_resource_type.Client
    group: group.Client
    policy: policy.Client
    resource: resource.Client
    tenant: tenant.Client
    user: user.Client

    def __init__(self, config: BaseConfig) -> None:
        self.config = config
