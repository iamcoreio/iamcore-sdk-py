from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

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
    IAMUnauthorizedException,
    IAMUserException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_patch,
    unwrap_post,
    unwrap_put,
)

from .dto import CreateUser, User

if TYPE_CHECKING:
    from collections.abc import Generator


@err_chain(IAMUserException)
def create_user(auth_headers: dict[str, str], create_user: CreateUser) -> User:
    """Create a new user."""
    url = config.IAMCORE_URL + "/api/v1/users"
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "POST",
        url,
        json=create_user.model_dump_json(by_alias=True, exclude_none=True),
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamEntityResponse(User, **unwrap_post(response)).data


@err_chain(IAMUserException)
def get_user_me(auth_headers: dict[str, str]) -> User:
    url = config.IAMCORE_URL + "/api/v1/users/me"
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamEntityResponse(User, **unwrap_get(response)).data


@err_chain(IAMUserException)
def get_irn(auth_headers: dict[str, str]) -> IRN:
    url = config.IAMCORE_URL + "/api/v1/users/me/irn"
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    irn_str = IamEntityResponse(str, **unwrap_get(response)).data
    return IRN.of(irn_str)


@err_chain(IAMUserException)
def update_user(
    auth_headers: dict[str, str],
    *,
    irn: IRN,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    enabled: bool | None = None,
) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)

    url = config.IAMCORE_URL + "/api/v1/users/" + irn.to_base64()
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "enabled": enabled,
    }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "PATCH",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return unwrap_patch(response)


@err_chain(IAMUserException)
def delete_user(auth_headers: dict[str, str], user_id: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not user_id:
        msg = "Missing user_id"
        raise IAMUserException(msg)

    url = config.IAMCORE_URL + "/api/v1/users/" + IRN.of(user_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "DELETE",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return unwrap_delete(response)


@err_chain(IAMUserException)
def user_attach_policies(
    auth_headers: dict[str, str],
    user_id: str,
    policies_ids: list[str],
) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not user_id:
        msg = "Missing user_id"
        raise IAMUserException(msg)
    if not policies_ids:
        msg = "Missing policies_ids"
        raise IAMUserException(msg)

    url = config.IAMCORE_URL + "/api/v1/users/" + user_id + "/policies/attach"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"policyIDs": policies_ids}

    response = requests.request(
        "PUT",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return unwrap_put(response)


@err_chain(IAMUserException)
def user_add_groups(auth_headers: dict[str, str], user_id: str, group_ids: list[str]) -> NoReturn:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not user_id:
        msg = "Missing user_id"
        raise IAMUserException(msg)
    if not group_ids:
        msg = "Missing policies_ids"
        raise IAMUserException(msg)

    url = config.IAMCORE_URL + "/api/v1/users/" + user_id + "/groups/add"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"groupIDs": group_ids}

    response = requests.request(
        "POST",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    raise unwrap_put(response)


@err_chain(IAMUserException)
def search_users(
    auth_headers: dict[str, str],
    *,
    email: str | None = None,
    path: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    username: str | None = None,
    tenant_id: str | None = None,
    search: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[User]:
    url = config.IAMCORE_URL + "/api/v1/users"

    querystring = {
        "email": email,
        "path": path,
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "tenantID": tenant_id,
        "search": search,
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
        headers=auth_headers,
        params=querystring,
        timeout=config.TIMEOUT,
    )
    return IamEntitiesResponse(User, **unwrap_get(response))


@err_chain(IAMException)
def search_all_users(
    auth_headers: dict[str, str],
    *,
    email: str | None = None,
    path: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    username: str | None = None,
    tenant_id: str | None = None,
    search: str | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> Generator[User, None, None]:
    kwargs = {
        "email": email,
        "path": path,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "tenant_id": tenant_id,
        "search": search,
        "sort": sort,
        "sort_order": sort_order,
    }
    return generic_search_all(auth_headers, search_users, **kwargs)
