from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from iamcore.irn import IRN

from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, IAMPolicyException, err_chain

from .dto import CreatePolicy, IamPoliciesResponse, IamPolicyResponse, Policy, PolicySearchFilter, UpdatePolicy

if TYPE_CHECKING:
    from collections.abc import Generator

    from requests import Response


logger = logging.getLogger(__name__)


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Policy API."""

    BASE_PATH = "policies"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMPolicyException)
    def create(self, auth_headers: dict[str, str], params: CreatePolicy) -> Policy:
        payload_dict = params.model_dump_json(by_alias=True, exclude_none=True)

        response: Response = self._post(data=payload_dict, headers=auth_headers)
        return IamPolicyResponse(**response.json()).data

    @err_chain(IAMPolicyException)
    def delete(self, auth_headers: dict[str, str], policy_id: str) -> None:
        self._delete(IRN.of(policy_id).to_base64(), headers=auth_headers)

    @err_chain(IAMPolicyException)
    def update(self, auth_headers: dict[str, str], policy_id: str, params: UpdatePolicy) -> None:
        data = params.model_dump_json(by_alias=True, exclude_none=True)
        self._put(policy_id, data=data, headers=auth_headers)

    @err_chain(IAMPolicyException)
    def search(
        self,
        headers: dict[str, str],
        policy_filter: Optional[PolicySearchFilter] = None,
    ) -> IamPoliciesResponse:
        query = policy_filter.model_dump(by_alias=True, exclude_none=True) if policy_filter else None
        response = self._get(headers=headers, params=query)
        return IamPoliciesResponse(**response.json())

    @err_chain(IAMException)
    def search_all(
        self,
        auth_headers: dict[str, str],
        policy_filter: Optional[PolicySearchFilter] = None,
    ) -> Generator[Policy, None, None]:
        return generic_search_all(auth_headers, self.search, policy_filter)
