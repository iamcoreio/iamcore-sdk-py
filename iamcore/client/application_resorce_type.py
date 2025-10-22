from __future__ import annotations

from collections.abc import Generator
from typing import Any

import requests
from iamcore.irn import IRN
from pydantic import Field
from requests import Response

from iamcore.client.common import (
    IamEntitiesResponse,
    IamEntityResponse,
    SortOrder,
    generic_search_all,
)
from iamcore.client.config import config
from iamcore.client.exceptions import IAMException, err_chain, unwrap_get, unwrap_post
from iamcore.client.models.base import IAMCoreBaseModel


class ApplicationResourceType(IAMCoreBaseModel):
    """Application resource type model representing IAM Core application resource types."""

    id: str
    irn: IRN
    type: str
    description: str
    action_prefix: str = Field(alias="actionPrefix")
    operations: list[str]
    created: str
    updated: str

    @staticmethod
    def of(item: ApplicationResourceType | dict[str, Any]) -> ApplicationResourceType:
        """Create ApplicationResourceType instance from ApplicationResourceType object or dict."""
        if isinstance(item, ApplicationResourceType):
            return item
        if isinstance(item, dict):
            return ApplicationResourceType.model_validate(item)
        raise IAMException("Unexpected response format")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


@err_chain(IAMException)
def create_resource_type(
    auth_headers: dict[str, str],
    application_irn: IRN,
    payload: dict[str, str] | None = None,
    type: str | None = None,
    description: str | None = None,
    action_prefix: str | None = None,
    operations: list[str] | None = None,
) -> ApplicationResourceType:
    url = (
        config.IAMCORE_URL
        + "/api/v1/applications/"
        + IRN.of(application_irn).to_base64()
        + "/resource-types"
    )
    if not payload:
        payload = {
            "type": type,
            "description": description,
            "actionPrefix": action_prefix,
            "operations": operations,
        }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse(ApplicationResourceType, **unwrap_post(response)).data


@err_chain(IAMException)
def get_resource_type(
    auth_headers: dict[str, str],
    application_irn: IRN,
    irn: IRN,
) -> ApplicationResourceType:
    url = (
        config.IAMCORE_URL
        + "/api/v1/applications/"
        + IRN.of(application_irn).to_base64()
        + "/resource-types/"
        + IRN.of(irn).to_base64()
    )
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("GET", url, headers=headers)
    return IamEntityResponse(ApplicationResourceType, **unwrap_get(response)).data


@err_chain(IAMException)
def search_application_resource_types(
    headers: dict[str, str],
    application_irn: IRN,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[ApplicationResourceType]:
    url = (
        config.IAMCORE_URL
        + "/api/v1/applications/"
        + IRN.of(application_irn).to_base64()
        + "/resource-types"
    )

    querystring = {"page": page, "pageSize": page_size, "sort": sort, "sortOrder": sort_order}

    querystring = {k: v for k, v in querystring.items() if v}

    response: Response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(ApplicationResourceType, **unwrap_get(response))


@err_chain(IAMException)
def search_all_application_resource_types(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[ApplicationResourceType, None, None]:
    return generic_search_all(auth_headers, search_application_resource_types, *args, **kwargs)
