from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.application.client import json
from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import IamIRNResponse, generic_search_all
from iamcore.client.exceptions import IAMException, IAMUserException, err_chain

from .dto import CreateUser, IamUserResponse, IamUsersResponse, UpdateUser, User, UserSearchFilter

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core User API."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMUserException)
    def create_user(self, auth_headers: dict[str, str], params: CreateUser) -> User:
        """Create a new user."""
        data = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post("users", data=data, headers=auth_headers)
        return IamUserResponse(**response.json()).data

    @err_chain(IAMUserException)
    def get_user_me(self, auth_headers: dict[str, str]) -> User:
        response = self.get("users/me", headers=auth_headers)
        return IamUserResponse(**response.json()).data

    @err_chain(IAMUserException)
    def get_irn(self, auth_headers: dict[str, str]) -> IRN:
        response = self.get("users/me/irn", headers=auth_headers)
        return IamIRNResponse(**response.json()).data

    @err_chain(IAMUserException)
    def update_user(self, auth_headers: dict[str, str], irn: IRN, params: UpdateUser) -> None:
        path = f"users/{irn.to_base64()}"
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        self.patch(path, data=payload, headers=auth_headers)

    @err_chain(IAMUserException)
    def delete_user(self, auth_headers: dict[str, str], user_irn: IRN) -> None:
        path = f"users/{user_irn.to_base64()}"
        self.delete(path, headers=auth_headers)

    @err_chain(IAMUserException)
    def user_attach_policies(self, auth_headers: dict[str, str], user_irn: IRN, policies_ids: list[str]) -> None:
        path = f"users/{user_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        self.put(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMUserException)
    def user_add_groups(self, auth_headers: dict[str, str], user_irn: IRN, group_ids: list[str]) -> None:
        path = f"users/{user_irn.to_base64()}/groups/add"
        payload = {"groupIDs": group_ids}
        self.post(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMUserException)
    def search_users(
        self,
        auth_headers: dict[str, str],
        user_filter: Optional[UserSearchFilter] = None,
    ) -> IamUsersResponse:
        query = user_filter.model_dump(by_alias=True, exclude_none=True) if user_filter else None
        response = self.get("users", headers=auth_headers, params=query)
        return IamUsersResponse(**response.json())

    @err_chain(IAMException)
    def search_all_users(
        self,
        auth_headers: dict[str, str],
        user_filter: Optional[UserSearchFilter] = None,
    ) -> Generator[User, None, None]:
        return generic_search_all(auth_headers, self.search_users, user_filter)
