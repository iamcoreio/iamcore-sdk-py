from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
from iamcore.client.exceptions import (
    IAMException,
    IAMResourceException,
    IAMUnauthorizedException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)
from iamcore.client.models.base import IAMCoreBaseModel

if TYPE_CHECKING:
    from collections.abc import Generator


class Resource(IAMCoreBaseModel):
    """Resource model representing IAM Core resources."""

    id: str
    irn: IRN
    name: str
    display_name: str = Field(alias="displayName")
    description: str
    path: str
    tenant_id: str = Field(alias="tenantID")
    application: str
    resource_type: str = Field(alias="resourceType")
    enabled: bool
    metadata: dict[str, str]
    created: str
    updated: str

    @staticmethod
    def of(item: Resource | dict[str, Any]) -> Resource:
        """Create Resource instance from Resource object or dict."""
        if isinstance(item, Resource):
            return item
        if isinstance(item, dict):
            return Resource.model_validate(item)
        raise IAMResourceException("Unexpected response format")

    def delete(self, auth_headers: dict[str, str]) -> None:
        delete_resource(auth_headers, self.id)

    def update(self, auth_headers: dict[str, str]) -> None:
        update_resource(
            auth_headers,
            resource_id=self.id,
            display_name=self.display_name,
            enabled=self.enabled,
            description=self.description,
            metadata=self.metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


@err_chain(IAMResourceException)
def create_resource(
    auth_headers: dict[str, str],
    payload: dict[str, object] | None = None,
    name: str | None = None,
    display_name: str | None = None,
    tenant_id: str | None = None,
    application: str | None = None,
    path: str | None = None,
    resource_type: str | None = None,
    enabled: bool = True,
    description: str | None = None,
    metadata: dict[str, object] | None = None,
) -> Resource:
    url = config.IAMCORE_URL + "/api/v1/resources"
    if not payload:
        payload = {
            "name": name,
            "displayName": display_name,
            "tenantID": tenant_id,
            "application": application,
            "path": path,
            "resourceType": resource_type,
            "enabled": enabled,
            "description": description,
            "metadata": metadata,
        }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse(Resource, **unwrap_post(response)).data


@err_chain(IAMResourceException)
def update_resource(
    auth_headers: dict[str, str],
    payload: dict[str, object] | None = None,
    resource_id: str | None = None,
    display_name: str | None = None,
    enabled: bool = True,
    description: str | None = None,
    metadata: dict[str, object] | None = None,
) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not resource_id:
        msg = "Missing resource_id"
        raise IAMResourceException(msg)
    url = config.IAMCORE_URL + "/api/v1/resources/" + IRN.of(resource_id).to_base64()
    if not payload:
        payload = {
            "displayName": display_name,
            "enabled": enabled,
            "description": description,
            "metadata": metadata,
        }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("PATCH", url, json=payload, headers=headers)
    unwrap_put(response)


@err_chain(IAMResourceException)
def delete_resource(auth_headers: dict[str, str], resource_id: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not resource_id:
        msg = "Missing resource_id"
        raise IAMResourceException(msg)

    url = config.IAMCORE_URL + "/api/v1/resources/" + IRN.of(resource_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("DELETE", url, data="", headers=headers)
    unwrap_delete(response)


@err_chain(IAMResourceException)
def delete_resources(auth_headers: dict[str, str], resources_ids: list[IRN]) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not resources_ids:
        msg = "Missing resource_id"
        raise IAMResourceException(msg)

    url = config.IAMCORE_URL + "/api/v1/resources/delete"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"resourceIDs": [IRN.of(r).to_base64() for r in resources_ids if r]}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    unwrap_delete(response)


@err_chain(IAMResourceException)
def search_resource(
    headers: dict[str, str],
    irn: IRN | None = None,
    path: str | None = None,
    display_name: str | None = None,
    enabled: bool | None = None,
    tenant_id: str | None = None,
    application: str | None = None,
    resource_type: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[Resource]:
    url = config.IAMCORE_URL + "/api/v1/resources"

    querystring = {
        "irn": str(irn) if irn else None,
        "path": path,
        "application": application,
        "enabled": enabled,
        "displayName": display_name,
        "resourceType": resource_type,
        "tenantID": tenant_id,
        "page": page,
        "pageSize": page_size,
        "sort": sort,
        "sortOrder": sort_order,
    }

    querystring = {k: v for k, v in querystring.items() if v}

    response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(Resource, **unwrap_get(response))


@err_chain(IAMException)
def search_all_resources(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[Resource, None, None]:
    return generic_search_all(auth_headers, search_resource, *args, **kwargs)
