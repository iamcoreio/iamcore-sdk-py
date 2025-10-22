from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from iamcore.irn import IRN
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
    IAMGroupException,
    IAMUnauthorizedException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

from .dto import Group

if TYPE_CHECKING:
    from collections.abc import Generator


@err_chain(IAMGroupException)
def create_group(
    auth_headers: dict[str, str],
    *,
    name: str | None = None,
    display_name: str | None = None,
    tenant_id: str | None = None,
    parent_id: str | None = None,
) -> Group:
    url = config.IAMCORE_URL + "/api/v1/groups"
    payload = {
        "name": name,
        "displayName": display_name,
        "parentID": parent_id,
        "tenantID": tenant_id,
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
    return IamEntityResponse[Group](Group, **unwrap_post(response)).data


@err_chain(IAMGroupException)
def delete_group(auth_headers: dict[str, str], group_id: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not group_id:
        msg = "Missing group_id"
        raise IAMGroupException(msg)

    url = config.IAMCORE_URL + "/api/v1/groups/" + IRN.of(group_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "DELETE",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_delete(response)


@err_chain(IAMGroupException)
def group_attach_policies(
    auth_headers: dict[str, str],
    group_id: str,
    policies_ids: list[str],
) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not group_id:
        msg = "Missing group_id"
        raise IAMGroupException(msg)
    if not policies_ids:
        msg = "Missing policies_ids or it's not a list"
        raise IAMGroupException(msg)

    url = config.IAMCORE_URL + "/api/v1/groups/" + group_id + "/policies/attach"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"policyIDs": policies_ids}

    response = requests.request(
        "PUT",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_put(response)


@err_chain(IAMGroupException)
def group_add_members(auth_headers: dict[str, str], group_id: str, members_ids: list[str]) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not group_id:
        msg = "Missing group_id"
        raise IAMGroupException(msg)
    if not members_ids:
        msg = "Missing policies_ids or it's not a list"
        raise IAMGroupException(msg)

    url = config.IAMCORE_URL + "/api/v1/groups/" + group_id + "/members/add"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"userIDs": members_ids}

    response = requests.request(
        "POST",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_put(response)


@err_chain(IAMGroupException)
def search_group(
    headers: dict[str, str],
    *,
    irn: IRN | None = None,
    path: str | None = None,
    name: str | None = None,
    display_name: str | None = None,
    tenant_id: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[Group]:
    url = config.IAMCORE_URL + "/api/v1/groups"

    querystring = {
        "irn": str(irn) if irn else None,
        "path": path,
        "name": name,
        "displayName": display_name,
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
    return IamEntitiesResponse(Group, **unwrap_get(response))


@err_chain(IAMException)
def search_all_groups(
    auth_headers: dict[str, str],
    *,
    irn: IRN | None = None,
    path: str | None = None,
    name: str | None = None,
    display_name: str | None = None,
    tenant_id: str | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> Generator[Group, None, None]:
    kwargs = {
        "headers": auth_headers,
        "irn": irn,
        "path": path,
        "name": name,
        "display_name": display_name,
        "tenant_id": tenant_id,
        "sort": sort,
        "sort_order": sort_order,
    }
    return generic_search_all(auth_headers, search_group, **kwargs)
