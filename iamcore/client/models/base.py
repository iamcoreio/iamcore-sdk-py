from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from iamcore.client.exceptions import IAMException


class IAMCoreBaseModel(BaseModel):
    """Base model for all IAM Core API models with camelCase field aliasing."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        alias_generator=lambda field_name: "".join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split("_"))
        ),
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IAMCoreBaseModel":
        """Create model instance from dictionary, handling validation errors."""
        try:
            return cls(**data)
        except ValidationError as e:
            msg = f"Validation error for {cls.__name__}: {e}"
            raise IAMException(msg) from e

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary with optional field aliasing."""
        return self.model_dump(by_alias=True)
