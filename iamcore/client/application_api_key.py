from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests
from iamcore.irn import IRN
from pydantic import Field
from requests import Response

from iamcore.client.common import IamEntitiesResponse, generic_search_all
from iamcore.client.config import config
from iamcore.client.exceptions import IAMException, err_chain, unwrap_get
from iamcore.client.models.base import IAMCoreBaseModel

if TYPE_CHECKING:
    from collections.abc import Generator


class ApplicationApiKey(IAMCoreBaseModel):
    """Application API key model representing IAM Core application API keys."""

    api_key: str = Field(alias="apiKey")
    state: str
    last_used: str = Field(alias="lastUsed")
    created: str
    updated: str

    @staticmethod
    def of(item: ApplicationApiKey | dict[str, Any]) -> ApplicationApiKey:
        """Create ApplicationApiKey instance from ApplicationApiKey object or dict."""
        if isinstance(item, ApplicationApiKey):
            return item
        if isinstance(item, dict):
            return ApplicationApiKey.model_validate(item)
        raise IAMException("Unexpected response format")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


@err_chain(IAMException)
def create_application_api_key(
    auth_headers: dict[str, str],
    application_irn: IRN,
) -> IamEntitiesResponse[ApplicationApiKey]:
    url = (
        config.IAMCORE_URL
        + "/api/v1/principals/"
        + IRN.of(application_irn).to_base64()
        + "/api-keys"
    )
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, headers=headers)
    return IamEntitiesResponse(ApplicationApiKey, **unwrap_get(response))


@err_chain(IAMException)
def get_application_api_keys(
    headers: dict[str, str],
    irn: str | IRN,
    page: int = 1,
) -> IamEntitiesResponse[ApplicationApiKey]:
    if isinstance(irn, IRN):
        irn = irn.to_base64()
    if isinstance(irn, str):
        irn = IRN.of(irn).to_base64()

    url = f"{config.IAMCORE_URL}/api/v1/principals/{irn}/api-keys?page={page}"
    response: Response = requests.request("GET", url, data="", headers=headers)
    return IamEntitiesResponse(ApplicationApiKey, **unwrap_get(response))


@err_chain(IAMException)
def get_all_applications_api_keys(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[ApplicationApiKey, None, None]:
    return generic_search_all(auth_headers, get_application_api_keys, *args, **kwargs)
