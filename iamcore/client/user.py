from __future__ import annotations

from typing import TYPE_CHECKING, Any, NoReturn

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
    IAMUnauthorizedException,
    IAMUserException,
    unwrap_patch,
)
from iamcore.client.models.base import IAMCoreBaseModel

from .exceptions import err_chain, unwrap_delete, unwrap_get, unwrap_post, unwrap_put

if TYPE_CHECKING:
    from collections.abc import Generator


class User(IAMCoreBaseModel):
    """User model representing an IAM Core user."""

    id: str
    irn: IRN
    created: str
    updated: str
    tenant_id: str = Field(alias="tenantId")
    auth_id: str  # UUID stored as string
    email: str
    enabled: bool  # API returns boolean, not string
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    username: str
    path: str

    @staticmethod
    def of(item: User | dict[str, Any]) -> User:
        """Create User instance from User object or dict."""
        if isinstance(item, User):
            return item
        if isinstance(item, dict):
            return User.model_validate(item)
        raise IAMUserException("Unexpected response format")

    def delete(self, auth_headers: dict[str, str]) -> None:
        """Delete this user."""
        delete_user(auth_headers, self.id)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class CreateUser(IAMCoreBaseModel):
    """Request model for creating a new user."""

    tenant_id: str | None = Field(None, alias="tenantId")
    email: str | None = None
    enabled: bool = True
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    username: str | None = None
    password: str | None = None
    confirm_password: str | None = Field(None, alias="confirmPassword")
    path: str | None = None

    def create(self, auth_headers: dict[str, str]) -> User:
        """Create the user via API call."""
        return create_user(auth_headers, **self.model_dump(by_alias=True, exclude_none=True))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)


@err_chain(IAMUserException)
def create_user(auth_headers: dict[str, str], **kwargs: Any) -> User:
    """Create a new user."""
    url = config.IAMCORE_URL + "/api/v1/users"
    payload = kwargs
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse(User, **unwrap_post(response)).data


@err_chain(IAMUserException)
def get_user_me(auth_headers: dict[str, str]) -> User:
    url = config.IAMCORE_URL + "/api/v1/users/me"
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("GET", url, data="", headers=headers)
    return IamEntityResponse(User, **unwrap_get(response)).data


@err_chain(IAMUserException)
def get_irn(auth_headers: dict[str, str]) -> IRN:
    url = config.IAMCORE_URL + "/api/v1/users/me/irn"
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("GET", url, data="", headers=headers)
    irn_str = IamEntityResponse(str, **unwrap_get(response)).data
    return IRN.of(irn_str)


@err_chain(IAMUserException)
def update_user(
    auth_headers: dict[str, str],
    user_id: str,
    payload: dict[str, str] | None = None,
    enabled: bool | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not user_id:
        msg = "Missing user_id"
        raise IAMUserException(msg)
    url = config.IAMCORE_URL + "/api/v1/users/" + IRN.of(user_id).to_base64()
    if not payload:
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "enabled": enabled,
        }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("PATCH", url, json=payload, headers=headers)
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
    response: Response = requests.request("DELETE", url, data="", headers=headers)
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
    if not policies_ids or not isinstance(policies_ids, list):
        msg = "Missing policies_ids or it's not a list"
        raise IAMUserException(msg)

    url = config.IAMCORE_URL + "/api/v1/users/" + user_id + "/policies/attach"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"policyIDs": policies_ids}

    response = requests.request("PUT", url, json=payload, headers=headers)
    return unwrap_put(response)


@err_chain(IAMUserException)
def user_add_groups(auth_headers: dict[str, str], user_id: str, group_ids: list[str]) -> NoReturn:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not user_id:
        msg = "Missing user_id"
        raise IAMUserException(msg)
    if not group_ids or not isinstance(group_ids, list):
        msg = "Missing policies_ids or it's not a list"
        raise IAMUserException(msg)

    url = config.IAMCORE_URL + "/api/v1/users/" + user_id + "/groups/add"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"groupIDs": group_ids}

    response = requests.request("POST", url, json=payload, headers=headers)
    raise unwrap_put(response)


@err_chain(IAMUserException)
def search_users(
    auth_headers: dict[str, str],
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
        "sortOrder": sort_order,
    }

    querystring = {k: v for k, v in querystring.items() if v}

    response = requests.request("GET", url, data="", headers=auth_headers, params=querystring)
    return IamEntitiesResponse(User, **unwrap_get(response))


@err_chain(IAMException)
def search_all_users(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[User, None, None]:
    return generic_search_all(auth_headers, search_users, *args, **kwargs)
