from __future__ import annotations

import logging
from typing import Any

from iamcore.irn import IRN
from pydantic import Field
from typing_extensions import override

from iamcore.client.models.base import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
    JSON_obj,
)

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

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests."""
        return self.model_dump(by_alias=True, exclude_none=True)


class IamPolicyResponse(IamEntityResponse[Policy]):
    data: Policy

    @override
    def converter(self, item: JSON_obj) -> Policy:
        return Policy.model_validate(item)


class IamPoliciesResponse(IamEntitiesResponse[Policy]):
    data: list[Policy]

    @override
    def converter(self, item: JSON_List) -> list[Policy]:
        return [Policy.model_validate(item) for item in item]
