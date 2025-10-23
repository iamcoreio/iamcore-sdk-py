from __future__ import annotations

import json
from typing import TYPE_CHECKING, Optional

from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, IAMGroupException, err_chain

from .dto import CreateGroup, Group, GroupSearchFilter, IamGroupResponse, IamGroupsResponse

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Group API."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMGroupException)
    def create_group(self, auth_headers: dict[str, str], create_group: CreateGroup) -> Group:
        payload = create_group.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post("groups", data=payload, headers=auth_headers)
        return IamGroupResponse(**response.json()).data

    @err_chain(IAMGroupException)
    def delete_group(self, auth_headers: dict[str, str], group_irn: IRN) -> None:
        path = f"groups/{group_irn.to_base64()}"
        self.delete(path, headers=auth_headers)

    @err_chain(IAMGroupException)
    def group_attach_policies(self, auth_headers: dict[str, str], group_irn: IRN, policies_ids: list[str]) -> None:
        path = f"groups/{group_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        self.put(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMGroupException)
    def group_add_members(self, auth_headers: dict[str, str], group_irn: IRN, members_ids: list[str]) -> None:
        path = f"groups/{group_irn.to_base64()}/members/add"
        payload = {"userIDs": members_ids}
        self.post(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMGroupException)
    def search_group(
        self,
        headers: dict[str, str],
        group_filter: Optional[GroupSearchFilter] = None,
    ) -> IamGroupsResponse:
        querystring = group_filter.model_dump(by_alias=True, exclude_none=True) if group_filter else None
        response = self.get("groups", headers=headers, params=querystring)
        return IamGroupsResponse(**response.json())

    @err_chain(IAMException)
    def search_all_groups(
        self,
        auth_headers: dict[str, str],
        group_filter: Optional[GroupSearchFilter] = None,
    ) -> Generator[Group, None, None]:
        return generic_search_all(auth_headers, self.search_group, group_filter)
