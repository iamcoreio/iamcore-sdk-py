from __future__ import annotations

import json
from typing import TYPE_CHECKING

from iamcore.client.exceptions import (
    IAMException,
    IAMGroupException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)
from iamcore.client.models.base import (
    SortOrder,
    generic_search_all,
)
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import Group, IamGroupResponse, IamGroupsResponse

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN
    from requests import Response

    from iamcore.client.config import BaseConfig


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Group API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.iamcore_url, timeout=config.iamcore_client_timeout)

    @err_chain(IAMGroupException)
    def create_group(
        self,
        auth_headers: dict[str, str],
        *,
        name: str | None = None,
        display_name: str | None = None,
        tenant_id: str | None = None,
        parent_id: str | None = None,
    ) -> Group:
        payload = {
            "name": name,
            "displayName": display_name,
            "parentID": parent_id,
            "tenantID": tenant_id,
        }
        payload = {k: v for k, v in payload.items() if v}

        response = self.post("groups", data=json.dumps(payload), headers=auth_headers)
        return IamGroupResponse(**unwrap_post(response)).data

    @err_chain(IAMGroupException)
    def delete_group(self, auth_headers: dict[str, str], group_irn: IRN) -> None:
        path = f"groups/{group_irn.to_base64()}"
        response: Response = self.delete(path, headers=auth_headers)
        unwrap_delete(response)

    @err_chain(IAMGroupException)
    def group_attach_policies(
        self,
        auth_headers: dict[str, str],
        group_id: str,
        policies_ids: list[str],
    ) -> None:
        path = f"groups/{group_id}/policies/attach"
        payload = {"policyIDs": policies_ids}

        response = self.put(path, data=json.dumps(payload), headers=auth_headers)
        unwrap_put(response)

    @err_chain(IAMGroupException)
    def group_add_members(
        self,
        auth_headers: dict[str, str],
        group_id: str,
        members_ids: list[str],
    ) -> None:
        path = f"groups/{group_id}/members/add"
        payload = {"userIDs": members_ids}

        response = self.post(path, data=json.dumps(payload), headers=auth_headers)
        unwrap_put(response)

    @err_chain(IAMGroupException)
    def search_group(
        self,
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
    ) -> IamGroupsResponse:
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

        response = self.get("groups", headers=headers, params=querystring)
        return IamGroupsResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_groups(
        self,
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
        return generic_search_all(auth_headers, self.search_group, **kwargs)
