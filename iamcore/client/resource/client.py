from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.common import (
    SortOrder,
    generic_search_all,
)
from iamcore.client.config import config
from iamcore.client.exceptions import (
    IAMException,
    IAMResourceException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

from .dto import IamResourceResponse, IamResourcesResponse, Resource

if TYPE_CHECKING:
    from collections.abc import Generator


@err_chain(IAMResourceException)
def create_resource(
    auth_headers: dict[str, str],
    *,
    name: str,
    application: str,
    path: str,
    resource_type: str,
    display_name: str | None = None,
    tenant_id: str | None = None,
    description: str | None = None,
    metadata: dict[str, object] | None = None,
    enabled: bool = True,
) -> Resource:
    url = config.IAMCORE_URL + "/api/v1/resources"
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
    response: Response = requests.request(
        "POST",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamResourceResponse(**unwrap_post(response)).data


@err_chain(IAMResourceException)
def update_resource(
    auth_headers: dict[str, str],
    *,
    resource_id: str,
    display_name: str | None = None,
    enabled: bool = True,
    description: str | None = None,
    metadata: dict[str, object] | None = None,
) -> None:
    url = config.IAMCORE_URL + "/api/v1/resources/" + IRN.of(resource_id).to_base64()

    payload = {
        "displayName": display_name,
        "enabled": enabled,
        "description": description,
        "metadata": metadata,
    }
    payload = {k: v for k, v in payload.items() if v}

    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "PATCH",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_put(response)


@err_chain(IAMResourceException)
def delete_resource(auth_headers: dict[str, str], resource_id: str) -> None:
    url = config.IAMCORE_URL + "/api/v1/resources/" + IRN.of(resource_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "DELETE",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_delete(response)


@err_chain(IAMResourceException)
def delete_resources(auth_headers: dict[str, str], resources_irns: list[IRN]) -> None:
    url = config.IAMCORE_URL + "/api/v1/resources/delete"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"resourceIDs": [IRN.of(r).to_base64() for r in resources_irns if r]}
    response: Response = requests.request(
        "POST",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_delete(response)


@err_chain(IAMResourceException)
def search_resource(
    headers: dict[str, str],
    *,
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
) -> IamResourcesResponse:
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
        "sortOrder": sort_order.name if sort_order else None,
    }
    querystring = {k: v for k, v in querystring.items() if v}

    response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        params=querystring,
        timeout=config.TIMEOUT,
    )
    return IamResourcesResponse(**unwrap_get(response))


@err_chain(IAMException)
def search_all_resources(
    auth_headers: dict[str, str],
    *,
    irn: IRN | None = None,
    path: str | None = None,
    display_name: str | None = None,
    enabled: bool | None = None,
    tenant_id: str | None = None,
    application: str | None = None,
    resource_type: str | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> Generator[Resource, None, None]:
    kwargs = {
        "irn": str(irn) if irn else None,
        "path": path,
        "application": application,
        "enabled": enabled,
        "displayName": display_name,
        "resourceType": resource_type,
        "tenantID": tenant_id,
        "sort": sort,
        "sortOrder": sort_order,
    }
    kwargs = {k: v for k, v in kwargs.items() if v}
    return generic_search_all(auth_headers, search_resource, **kwargs)
