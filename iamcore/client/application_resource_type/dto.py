from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field
from typing_extensions import override

from iamcore.client.common import IamEntitiesResponse, IamEntityResponse, JSON_List
from iamcore.client.models.base import IAMCoreBaseModel

if TYPE_CHECKING:
    from iamcore.irn import IRN


class ApplicationResourceType(IAMCoreBaseModel):
    """Application resource type model representing IAM Core application resource types."""

    id: str
    irn: IRN
    type: str
    description: str
    action_prefix: str = Field(alias="actionPrefix")
    operations: list[str]
    created: str
    updated: str

    @staticmethod
    def of(item: ApplicationResourceType | dict[str, Any]) -> ApplicationResourceType:
        """Create ApplicationResourceType instance from ApplicationResourceType object or dict."""
        return ApplicationResourceType.model_validate(item) if isinstance(item, dict) else item

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class IamApplicationResourceTypeResponse(IamEntityResponse[ApplicationResourceType]):
    data: ApplicationResourceType

    @override
    def converter(self, item: dict[str, Any]) -> ApplicationResourceType:
        return ApplicationResourceType.model_validate(item)


class IamApplicationResourceTypesResponse(IamEntitiesResponse[ApplicationResourceType]):
    data: list[ApplicationResourceType]

    @override
    def converter(self, item: JSON_List) -> list[ApplicationResourceType]:
        return [ApplicationResourceType.model_validate(item) for item in item]
