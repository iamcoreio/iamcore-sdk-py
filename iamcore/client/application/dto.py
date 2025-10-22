from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field
from typing_extensions import override

from iamcore.client.common import IamEntitiesResponse, IamEntityResponse, JSON_List
from iamcore.client.models.base import IAMCoreBaseModel

if TYPE_CHECKING:
    from iamcore.irn import IRN


class Application(IAMCoreBaseModel):
    """Application model representing IAM Core applications."""

    id: str
    irn: IRN
    name: str
    display_name: str = Field(alias="displayName")
    created: str
    updated: str

    @staticmethod
    def of(item: Application | dict[str, Any]) -> Application:
        """Create Application instance from Application object or dict."""
        return Application.model_validate(item) if isinstance(item, dict) else item

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(by_alias=True)


class IamApplicationResponse(IamEntityResponse[Application]):
    data: Application

    @override
    def converter(self, item: dict[str, Any]) -> Application:
        return Application.model_validate(item)


class IamApplicationsResponse(IamEntitiesResponse[Application]):
    data: list[Application]

    @override
    def converter(self, item: JSON_List) -> list[Application]:
        return [Application.model_validate(item) for item in item]
