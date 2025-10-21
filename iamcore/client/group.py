from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.common import (
    IamEntitiesResponse,
    IamEntityResponse,
    SortOrder,
    generic_search_all,
    to_snake_case,
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

if TYPE_CHECKING:
    from collections.abc import Generator


class Group:
    id: str
    irn: IRN
    tenant_id: str
    name: str
    display_name: str
    path: str
    created: str
    updated: str

    @staticmethod
    def of(item: dict[str, Any] | Group) -> Group:
        if isinstance(item, Group):
            return item
        if isinstance(item, dict):
            return Group(**item)
        raise IAMGroupException("Unexpected response format")

    def __init__(self, irn: str, **kwargs: Any) -> None:
        self._irn = IRN.from_irn_str(irn)
        for k, v in kwargs.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)


@err_chain(IAMGroupException)
def create_group(
    auth_headers: dict[str, str],
    payload: dict[str, object] | None = None,
    name: str | None = None,
    display_name: str | None = None,
    tenant_id: str | None = None,
    parent_id: str | None = None,
) -> Group:
    url = config.IAMCORE_URL + "/api/v1/groups"
    if not payload:
        payload = {
            "name": name,
            "displayName": display_name,
            "parentID": parent_id,
            "tenantID": tenant_id,
        }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse[Group](Group, **unwrap_post(response)).data


@err_chain(IAMGroupException)
def delete_group(auth_headers: dict[str, str], group_id: str) -> None:
    if not auth_headers:
        raise IAMUnauthorizedException("Missing authorization headers")
    if not group_id:
        raise IAMGroupException("Missing group_id")

    url = config.IAMCORE_URL + "/api/v1/groups/" + IRN.of(group_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("DELETE", url, data="", headers=headers)
    unwrap_delete(response)


@err_chain(IAMGroupException)
def group_attach_policies(
    auth_headers: dict[str, str],
    group_id: str,
    policies_ids: list[str],
) -> None:
    if not auth_headers:
        raise IAMUnauthorizedException("Missing authorization headers")
    if not group_id:
        raise IAMGroupException("Missing group_id")
    if not policies_ids or not isinstance(policies_ids, list):
        raise IAMGroupException("Missing policies_ids or it's not a list")

    url = config.IAMCORE_URL + "/api/v1/groups/" + group_id + "/policies/attach"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"policyIDs": policies_ids}

    response = requests.request("PUT", url, json=payload, headers=headers)
    unwrap_put(response)


@err_chain(IAMGroupException)
def group_add_members(auth_headers: dict[str, str], group_id: str, members_ids: list[str]) -> None:
    if not auth_headers:
        raise IAMUnauthorizedException("Missing authorization headers")
    if not group_id:
        raise IAMGroupException("Missing group_id")
    if not members_ids or not isinstance(members_ids, list):
        raise IAMGroupException("Missing policies_ids or it's not a list")

    url = config.IAMCORE_URL + "/api/v1/groups/" + group_id + "/members/add"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"userIDs": members_ids}

    response = requests.request("POST", url, json=payload, headers=headers)
    unwrap_put(response)


@err_chain(IAMGroupException)
def search_group(
    headers: dict[str, str],
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
        "sortOrder": sort_order,
    }

    querystring = {k: v for k, v in querystring.items() if v}

    response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(Group, **unwrap_get(response))


@err_chain(IAMException)
def search_all_groups(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[Group, None, None]:
    return generic_search_all(auth_headers, search_group, *args, **kwargs)
