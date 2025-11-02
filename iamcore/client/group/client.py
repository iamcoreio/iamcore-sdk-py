from __future__ import annotations

import json
from typing import TYPE_CHECKING, Optional

from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, IAMGroupException, err_chain

from .dto import CreateGroup, Group, GroupSearchFilter, IamGroupResponse, IamGroupsResponse

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Group API."""

    BASE_PATH = "groups"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMGroupException)
    def create(self, auth_headers: dict[str, str], create_group: CreateGroup) -> Group:
        payload = create_group.model_dump_json(by_alias=True, exclude_none=True)
        response = self._post(data=payload, headers=auth_headers)
        return IamGroupResponse(**response.json()).data

    @err_chain(IAMGroupException)
    def delete(self, auth_headers: dict[str, str], group_irn: IRN) -> None:
        self._delete(group_irn.to_base64(), headers=auth_headers)

    @err_chain(IAMGroupException)
    def attach_policies(self, auth_headers: dict[str, str], group_irn: IRN, policies_ids: list[str]) -> None:
        path = f"{group_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        self._put(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMGroupException)
    def add_members(self, auth_headers: dict[str, str], group_irn: IRN, members_ids: list[str]) -> None:
        path = f"{group_irn.to_base64()}/members/add"
        payload = {"userIDs": members_ids}
        self._post(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMGroupException)
    def search(
        self,
        headers: dict[str, str],
        group_filter: Optional[GroupSearchFilter] = None,
    ) -> IamGroupsResponse:
        querystring = group_filter.model_dump(by_alias=True, exclude_none=True) if group_filter else None
        response = self._get(headers=headers, params=querystring)
        return IamGroupsResponse(**response.json())

    @err_chain(IAMException)
    def search_all(
        self,
        auth_headers: dict[str, str],
        group_filter: Optional[GroupSearchFilter] = None,
    ) -> Generator[Group, None, None]:
        return generic_search_all(auth_headers, self.search, group_filter)
