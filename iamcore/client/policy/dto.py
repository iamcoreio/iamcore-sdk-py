from __future__ import annotations

import logging
from typing import Any, Optional

from iamcore.irn import IRN
from pydantic import Field, field_validator
from typing_extensions import override

from iamcore.client.models.base import (
    IAMCoreBaseModel,
    IamEntitiesResponse,
    IamEntityResponse,
    JSON_List,
    JSON_obj,
    PaginatedSearchFilter,
)

logger = logging.getLogger(__name__)


class PolicyStatement(IAMCoreBaseModel):
    """Policy statement model representing IAM policy statements."""

    effect: str
    description: str
    resources: list[IRN]
    actions: list[str]


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

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class UpsertPolicy(IAMCoreBaseModel):
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
    ) -> UpsertPolicy:
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


class PolicySearchFilter(PaginatedSearchFilter):
    """Policy search filter."""

    irn: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    account_id: Optional[str] = Field(None, alias="accountID")
    application: Optional[str] = None
    tenant_id: Optional[str] = Field(None, alias="tenantID")

    @field_validator("irn", mode="after")
    @classmethod
    def validate_irn(cls, v: Optional[str]) -> Optional[str]:
        if not v and (cls.account_id and cls.tenant_id):
            return f"irn:{cls.account_id}:iamcore:{cls.tenant_id}"
        return v


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
