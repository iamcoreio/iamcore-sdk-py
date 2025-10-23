from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from iamcore.irn import IRN

from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, IAMPolicyException, err_chain

from .dto import CreatePolicy, IamPoliciesResponse, IamPolicyResponse, Policy, PolicySearchFilter, UpdatePolicy

if TYPE_CHECKING:
    from collections.abc import Generator

    from requests import Response


logger = logging.getLogger(__name__)


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Policy API."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMPolicyException)
    def create_policy(self, auth_headers: dict[str, str], params: CreatePolicy) -> Policy:
        payload_dict = params.model_dump_json(by_alias=True, exclude_none=True)

        response: Response = self.post("policies", data=payload_dict, headers=auth_headers)
        return IamPolicyResponse(**response.json()).data

    @err_chain(IAMPolicyException)
    def delete_policy(self, auth_headers: dict[str, str], policy_id: str) -> None:
        path = "policies/" + IRN.of(policy_id).to_base64()
        self.delete(path, headers=auth_headers)

    @err_chain(IAMPolicyException)
    def update_policy(self, auth_headers: dict[str, str], policy_id: str, params: UpdatePolicy) -> None:
        path = "policies/" + policy_id
        data = params.model_dump_json(by_alias=True, exclude_none=True)
        self.put(path, data=data, headers=auth_headers)

    @err_chain(IAMPolicyException)
    def search_policy(
        self,
        headers: dict[str, str],
        policy_filter: Optional[PolicySearchFilter] = None,
    ) -> IamPoliciesResponse:
        query = policy_filter.model_dump(by_alias=True, exclude_none=True) if policy_filter else None
        response = self.get("policies", headers=headers, params=query)
        return IamPoliciesResponse(**response.json())

    @err_chain(IAMException)
    def search_all_policies(
        self,
        auth_headers: dict[str, str],
        policy_filter: Optional[PolicySearchFilter] = None,
    ) -> Generator[Policy, None, None]:
        return generic_search_all(auth_headers, self.search_policy, policy_filter)
