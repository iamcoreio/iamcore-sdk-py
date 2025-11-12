from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.application.client import json
from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import IamIRNResponse, generic_search_all
from iamcore.client.exceptions import IAMException, IAMUserException, err_chain

from .dto import CreateUser, IamUserResponse, IamUsersResponse, UpdateUser, User, UserSearchFilter

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core User API."""

    BASE_PATH = "users"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMUserException)
    def create(self, auth_headers: dict[str, str], params: CreateUser) -> User:
        """Create a new user."""
        data = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self._post(data=data, headers=auth_headers)
        return IamUserResponse(**response.json()).data

    @err_chain(IAMUserException)
    def get_authenticated(self, auth_headers: dict[str, str]) -> User:
        response = self._get("me", headers=auth_headers)
        return IamUserResponse(**response.json()).data

    @err_chain(IAMUserException)
    def get_authenticated_irn(self, auth_headers: dict[str, str]) -> IRN:
        response = self._get("me/irn", headers=auth_headers)
        return IamIRNResponse(**response.json()).data

    @err_chain(IAMUserException)
    def update(self, auth_headers: dict[str, str], irn: IRN, params: UpdateUser) -> None:
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        self._patch(irn.to_base64(), data=payload, headers=auth_headers)

    @err_chain(IAMUserException)
    def delete(self, auth_headers: dict[str, str], user_irn: IRN) -> None:
        self._delete(user_irn.to_base64(), headers=auth_headers)

    @err_chain(IAMUserException)
    def policies_attach(self, auth_headers: dict[str, str], user_irn: IRN, policies_ids: list[str]) -> None:
        path = f"{user_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        self._put(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMUserException)
    def add_groups(self, auth_headers: dict[str, str], user_irn: IRN, group_ids: list[str]) -> None:
        path = f"{user_irn.to_base64()}/groups/add"
        payload = {"groupIDs": group_ids}
        self._post(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMUserException)
    def search(
        self,
        auth_headers: dict[str, str],
        user_filter: Optional[UserSearchFilter] = None,
    ) -> IamUsersResponse:
        query = user_filter.model_dump(by_alias=True, exclude_none=True) if user_filter else None
        response = self._get(headers=auth_headers, params=query)
        return IamUsersResponse(**response.json())

    @err_chain(IAMException)
    def search_all(
        self,
        auth_headers: dict[str, str],
        user_filter: Optional[UserSearchFilter] = None,
    ) -> Generator[User, None, None]:
        return generic_search_all(auth_headers, self.search, user_filter)
