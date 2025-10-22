from __future__ import annotations

from typing import TYPE_CHECKING

from iamcore.client.application.client import json
from iamcore.client.exceptions import (
    IAMException,
    IAMUserException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_patch,
    unwrap_post,
    unwrap_put,
)
from iamcore.client.models.base import (
    IamIRNResponse,
    SortOrder,
    generic_search_all,
)
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import CreateUser, IamUserResponse, IamUsersResponse, User

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN

    from iamcore.client.config import BaseConfig


class Client(HTTPClientWithTimeout):
    """Client for IAM Core User API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.iamcore_url, timeout=config.iamcore_client_timeout)

    @err_chain(IAMUserException)
    def create_user(self, auth_headers: dict[str, str], create_user: CreateUser) -> User:
        """Create a new user."""
        data = create_user.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post("users", data=data, headers=auth_headers)
        return IamUserResponse(**unwrap_post(response)).data

    @err_chain(IAMUserException)
    def get_user_me(self, auth_headers: dict[str, str]) -> User:
        response = self.get("users/me", headers=auth_headers)
        return IamUserResponse(**unwrap_get(response)).data

    @err_chain(IAMUserException)
    def get_irn(self, auth_headers: dict[str, str]) -> IRN:
        response = self.get("users/me/irn", headers=auth_headers)
        return IamIRNResponse(**unwrap_get(response)).data

    @err_chain(IAMUserException)
    def update_user(
        self,
        auth_headers: dict[str, str],
        *,
        irn: IRN,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        enabled: bool | None = None,
    ) -> None:
        path = f"users/{irn.to_base64()}"
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "enabled": enabled,
        }
        response = self.patch(path, data=json.dumps(payload), headers=auth_headers)
        unwrap_patch(response)

    @err_chain(IAMUserException)
    def delete_user(self, auth_headers: dict[str, str], user_irn: IRN) -> None:
        path = f"users/{user_irn.to_base64()}"
        response = self.delete(path, headers=auth_headers)
        unwrap_delete(response)

    @err_chain(IAMUserException)
    def user_attach_policies(
        self,
        auth_headers: dict[str, str],
        user_irn: IRN,
        policies_ids: list[str],
    ) -> None:
        path = f"users/{user_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        response = self.put(path, data=json.dumps(payload), headers=auth_headers)
        unwrap_put(response)

    @err_chain(IAMUserException)
    def user_add_groups(
        self, auth_headers: dict[str, str], user_irn: IRN, group_ids: list[str]
    ) -> None:
        path = f"users/{user_irn.to_base64()}/groups/add"
        payload = {"groupIDs": group_ids}
        response = self.post(path, data=json.dumps(payload), headers=auth_headers)
        unwrap_put(response)

    @err_chain(IAMUserException)
    def search_users(
        self,
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
    ) -> IamUsersResponse:
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

        response = self.get("users", headers=auth_headers, params=querystring)
        return IamUsersResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_users(
        self,
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
        return generic_search_all(auth_headers, self.search_users, **kwargs)
