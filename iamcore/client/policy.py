from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.config import config

from .common import IamEntitiesResponse, IamEntityResponse, SortOrder, generic_search_all, to_dict
from .exceptions import (
    IAMException,
    IAMPolicyException,
    IAMUnauthorizedException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger(__name__)


class PolicyStatement:
    effect: str
    description: str
    resources: list[IRN]
    actions: list[str]

    @staticmethod
    def of(item: dict[str, Any] | PolicyStatement) -> PolicyStatement:
        if isinstance(item, PolicyStatement):
            return item
        if isinstance(item, dict):
            return PolicyStatement(**item)
        raise IAMPolicyException("Unexpected response format")

    def __init__(
        self,
        effect: str | None = None,
        description: str | None = None,
        resources: list[str] | None = None,
        actions: list[str] | None = None,
    ):
        self.effect = effect
        self.description = description
        self.resources = [IRN.of(irn) for irn in resources]
        self.actions = actions


class Policy:
    id: str
    irn: IRN
    name: str
    description: str
    type: str
    origin: str
    version: str
    statements: list[PolicyStatement]

    def __init__(
        self,
        irn: str,
        statements: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        self.irn = IRN.of(irn)
        if isinstance(statements, list):
            self.statements = [PolicyStatement.of(item) for item in statements]
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def of(item: dict[str, Any] | Policy) -> Policy:
        if isinstance(item, Policy):
            return item
        if isinstance(item, dict):
            return Policy(**item)
        raise IAMPolicyException("Unexpected response format")

    @err_chain(IAMPolicyException)
    def update(self, auth_headers: dict[str, str]) -> None:
        if not auth_headers:
            msg = "Missing authorization headers"
            raise IAMUnauthorizedException(msg)
        if not self.id:
            msg = "Missing resource_id or display_name"
            raise IAMPolicyException(msg)

        url = config.IAMCORE_URL + "/api/v1/policies/" + self.id
        payload = to_dict(self)
        headers = {"Content-Type": "application/json", **auth_headers}
        response: Response = requests.request("PUT", url, json=payload, headers=headers)
        unwrap_put(response)

    def delete(self, auth_headers: dict[str, str]) -> None:
        delete_policy(auth_headers, policy_id=self.id)

    def to_dict(self) -> dict[str, Any]:
        return to_dict(self)


class CreatePolicyRequest:
    name: str
    level: str
    tenant_id: str
    description: str
    statements: list[PolicyStatement]

    def __init__(
        self,
        name: str,
        level: str,
        description: str,
        tenant_id: str | None = None,
    ) -> None:
        self.name = name
        self.level = level
        self.tenant_id = tenant_id
        self.description = description
        self.statements = []
        if level == "tenant" and not tenant_id:
            logger.warning("Missing tenant_id for tenant level policy")

    def with_statement(
        self,
        effect: str,
        description: str,
        resources: list[str],
        actions: list[str],
    ) -> CreatePolicyRequest:
        self.statements.append(
            PolicyStatement(
                effect=effect, description=description, resources=resources, actions=actions
            )
        )
        return self

    @err_chain(IAMPolicyException)
    def create(self, auth_headers: dict[str, str]) -> Policy:
        return create_policy(auth_headers, self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "level": self.level,
            "description": self.description,
            "tenantID": self.tenant_id,
            "statements": to_dict(self.statements),
        }


@err_chain(IAMPolicyException)
def create_policy(auth_headers: dict[str, str], payload: CreatePolicyRequest) -> Policy:
    url = config.IAMCORE_URL + "/api/v1/policies"
    payload = payload.to_dict()

    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse(Policy, **unwrap_post(response)).data


@err_chain(IAMPolicyException)
def delete_policy(auth_headers: dict[str, str], policy_id: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not policy_id:
        msg = "Missing resource_id"
        raise IAMPolicyException(msg)

    url = config.IAMCORE_URL + "/api/v1/policies/" + IRN.of(policy_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("DELETE", url, data="", headers=headers)
    unwrap_delete(response)


@err_chain(IAMPolicyException)
def search_policy(
    headers: dict[str, str],
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
) -> IamEntitiesResponse[Policy]:
    url = config.IAMCORE_URL + "/api/v1/policies"
    if not irn and account_id and tenant_id:
        application = application if application else "iamcore"
        irn = f"irn:{account_id}:{application}:{tenant_id}"
    querystring = {
        "irn": irn,
        "name": name,
        "description": description,
        "page": page,
        "pageSize": page_size,
        "sort": sort,
        "sortOrder": sort_order,
    }

    querystring = {k: v for k, v in querystring.items() if v}

    response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(Policy, **unwrap_get(response))


@err_chain(IAMException)
def search_all_policies(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[Policy, None, None]:
    return generic_search_all(auth_headers, search_policy, *args, **kwargs)
