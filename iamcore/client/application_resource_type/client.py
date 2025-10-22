from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.config import config
from iamcore.client.exceptions import IAMException, err_chain, unwrap_get, unwrap_post
from iamcore.client.models.base import (
    SortOrder,
    generic_search_all,
)

from .dto import (
    ApplicationResourceType,
    IamApplicationResourceTypeResponse,
    IamApplicationResourceTypesResponse,
)

if TYPE_CHECKING:
    from collections.abc import Generator


@err_chain(IAMException)
def create_resource_type(
    auth_headers: dict[str, str],
    application_irn: IRN,
    *,
    type: str,
    description: str | None = None,
    action_prefix: str | None = None,
    operations: list[str] | None = None,
) -> ApplicationResourceType:
    url = (
        config.IAMCORE_URL
        + "/api/v1/applications/"
        + application_irn.to_base64()
        + "/resource-types"
    )
    payload = {
        "type": type,
        "description": description,
        "actionPrefix": action_prefix,
        "operations": operations,
    }
    payload = {k: v for k, v in payload.items() if v}

    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "POST",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamApplicationResourceTypeResponse(**unwrap_post(response)).data


@err_chain(IAMException)
def get_resource_type(
    auth_headers: dict[str, str],
    application_irn: IRN,
    type_irn: IRN,
) -> ApplicationResourceType:
    url = (
        config.IAMCORE_URL
        + "/api/v1/applications/"
        + application_irn.to_base64()
        + "/resource-types/"
        + type_irn.to_base64()
    )
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("GET", url, headers=headers, timeout=config.TIMEOUT)
    return IamApplicationResourceTypeResponse(**unwrap_get(response)).data


@err_chain(IAMException)
def search_application_resource_types(
    headers: dict[str, str],
    application_irn: IRN,
    *,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamApplicationResourceTypesResponse:
    url = (
        config.IAMCORE_URL
        + "/api/v1/applications/"
        + IRN.of(application_irn).to_base64()
        + "/resource-types"
    )

    querystring = {
        "page": page,
        "pageSize": page_size,
        "sort": sort,
        "sortOrder": sort_order.name if sort_order else None,
    }
    querystring = {k: v for k, v in querystring.items() if v}

    response: Response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        params=querystring,
        timeout=config.TIMEOUT,
    )
    return IamApplicationResourceTypesResponse(**unwrap_get(response))


@err_chain(IAMException)
def search_all_application_resource_types(
    auth_headers: dict[str, str],
    *,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> Generator[ApplicationResourceType, None, None]:
    kwargs = {
        "sort": sort,
        "sort_order": sort_order,
    }
    kwargs = {k: v for k, v in kwargs.items() if v}
    return generic_search_all(auth_headers, search_application_resource_types, **kwargs)
