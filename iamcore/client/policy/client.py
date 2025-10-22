from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from iamcore.irn import IRN

from iamcore.client.exceptions import (
    IAMException,
    IAMPolicyException,
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

from .dto import CreatePolicyRequest, IamPoliciesResponse, IamPolicyResponse, Policy

if TYPE_CHECKING:
    from collections.abc import Generator

    from requests import Response

    from iamcore.client.config import BaseConfig

logger = logging.getLogger(__name__)


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Policy API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.iamcore_url, timeout=config.iamcore_client_timeout)

    @err_chain(IAMPolicyException)
    def create_policy(self, auth_headers: dict[str, str], payload: CreatePolicyRequest) -> Policy:
        payload_dict = payload.model_dump_json(by_alias=True, exclude_none=True)

        response: Response = self.post("policies", data=payload_dict, headers=auth_headers)
        return IamPolicyResponse(**unwrap_post(response)).data

    @err_chain(IAMPolicyException)
    def delete_policy(self, auth_headers: dict[str, str], policy_id: str) -> None:
        path = "policies/" + IRN.of(policy_id).to_base64()
        response: Response = self.delete(path, headers=auth_headers)
        unwrap_delete(response)

    @err_chain(IAMPolicyException)
    def update_policy(
        self,
        auth_headers: dict[str, str],
        policy_id: str,
        payload: CreatePolicyRequest,
    ) -> None:
        path = "policies/" + policy_id
        data = payload.model_dump_json(by_alias=True, exclude_none=True)
        response: Response = self.put(path, data=data, headers=auth_headers)
        unwrap_put(response)

    @err_chain(IAMPolicyException)
    def search_policy(
        self,
        headers: dict[str, str],
        *,
        irn: str | None = None,
        name: str | None = None,
        description: str | None = None,
        account_id: str | None = None,
        application: str | None = None,
        tenant_id: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> IamPoliciesResponse:
        if not irn and account_id and tenant_id:
            application = application if application else "iamcore"
            irn = f"irn:{account_id}:{application}:{tenant_id}"

        query = {
            "irn": irn,
            "name": name,
            "description": description,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
            "sortOrder": sort_order.name if sort_order else None,
        }
        query = {k: v for k, v in query.items() if v}

        response = self.get("policies", headers=headers, params=query)
        return IamPoliciesResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_policies(
        self,
        auth_headers: dict[str, str],
        *,
        irn: str | None = None,
        name: str | None = None,
        description: str | None = None,
        account_id: str | None = None,
        application: str | None = None,
        tenant_id: str | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> Generator[Policy, None, None]:
        kwargs = {
            "irn": irn,
            "name": name,
            "description": description,
            "account_id": account_id,
            "application": application,
            "tenant_id": tenant_id,
            "sort": sort,
            "sort_order": sort_order,
        }
        kwargs = {k: v for k, v in kwargs.items() if v}
        return generic_search_all(auth_headers, self.search_policy, **kwargs)
