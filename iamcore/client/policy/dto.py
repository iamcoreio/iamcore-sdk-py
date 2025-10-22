from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import requests
from pydantic import Field
from requests import Response

from iamcore.client.config import config
from iamcore.client.exceptions import (
    IAMPolicyException,
    IAMUnauthorizedException,
    err_chain,
    unwrap_put,
)
from iamcore.client.models.base import IAMCoreBaseModel
from iamcore.client.policy.client import create_policy, delete_policy

if TYPE_CHECKING:
    from iamcore.irn import IRN

logger = logging.getLogger(__name__)


class PolicyStatement(IAMCoreBaseModel):
    """Policy statement model representing IAM policy statements."""

    effect: str
    description: str
    resources: list[IRN]
    actions: list[str]

    @staticmethod
    def of(item: PolicyStatement | dict[str, Any]) -> PolicyStatement:
        """Create PolicyStatement instance from PolicyStatement object or dict."""
        return PolicyStatement.model_validate(item) if isinstance(item, dict) else item


class Policy(IAMCoreBaseModel):
    """Policy model representing IAM Core policies."""

    id: str
    irn: IRN
    name: str
    description: str
    type: str
    origin: str
    version: str
    statements: list[PolicyStatement]

    @staticmethod
    def of(item: Policy | dict[str, Any]) -> Policy:
        """Create Policy instance from Policy object or dict."""
        return Policy.model_validate(item) if isinstance(item, dict) else item

    @err_chain(IAMPolicyException)
    def update(self, auth_headers: dict[str, str]) -> None:
        if not auth_headers:
            msg = "Missing authorization headers"
            raise IAMUnauthorizedException(msg)
        if not self.id:
            msg = "Missing resource_id or display_name"
            raise IAMPolicyException(msg)

        url = config.IAMCORE_URL + "/api/v1/policies/" + self.id
        payload = self.model_dump(by_alias=True)
        headers = {"Content-Type": "application/json", **auth_headers}
        response: Response = requests.request(
            "PUT",
            url,
            json=payload,
            headers=headers,
            timeout=config.TIMEOUT,
        )
        unwrap_put(response)

    def delete(self, auth_headers: dict[str, str]) -> None:
        delete_policy(auth_headers, policy_id=self.id)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class CreatePolicyRequest(IAMCoreBaseModel):
    """Request model for creating a new policy."""

    name: str
    level: str
    tenant_id: str | None = Field(None, alias="tenantID")
    description: str
    statements: list[PolicyStatement] = Field(default_factory=list)

    def with_statement(
        self,
        effect: str,
        description: str,
        resources: list[str],
        actions: list[str],
    ) -> CreatePolicyRequest:
        self.statements.append(
            PolicyStatement(
                effect=effect,
                description=description,
                resources=[IRN.of(r) for r in resources],
                actions=actions,
            )
        )
        return self

    @err_chain(IAMPolicyException)
    def create(self, auth_headers: dict[str, str]) -> Policy:
        return create_policy(auth_headers, self)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)
