from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, TypeVar, Union

from iamcore.irn import IRN
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from typing_extensions import override

from iamcore.client.exceptions import IAMException

if TYPE_CHECKING:
    from collections.abc import Generator


class IAMCoreBaseModel(BaseModel):
    """Base model for all IAM Core API models with camelCase field aliasing."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IAMCoreBaseModel:
        """Create model instance from dictionary, handling validation errors."""
        try:
            return cls(**data)
        except ValidationError as e:
            msg = f"Validation error for {cls.__name__}: {e}"
            raise IAMException(msg) from e

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary with optional field aliasing."""
        return self.model_dump(by_alias=True)


class PaginatedSearchFilter(IAMCoreBaseModel):
    """Paginated search filter."""

    page: Optional[int] = None
    page_size: Optional[int] = Field(None, alias="pageSize")
    sort: Optional[str] = None
    sort_order: Optional[str] = Field(None, alias="sortOrder")


def to_snake_case(field_name: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", field_name).lower()


class SortOrder(Enum):
    asc = 1
    desc = 2


T = TypeVar("T")
JSON_obj = dict[str, Any]
JSON_List = Union[list[dict[str, Any]], list[str]]


class IamEntityResponse(ABC, Generic[T]):
    data: T

    def __init__(self, item: JSON_obj) -> None:
        self.data = self.converter(item)
        super().__init__()

    @abstractmethod
    def converter(self, item: JSON_obj) -> T:
        pass


class IamEntitiesResponse(ABC, Generic[T]):
    data: list[T]
    count: int
    page: int
    page_size: int

    def __init__(self, item: JSON_List, count: int, page: int, page_size: int) -> None:
        self.data = self.converter(item)
        self.count = count
        self.page = page
        self.page_size = page_size
        super().__init__()

    @abstractmethod
    def converter(self, item: JSON_List) -> list[T]:
        pass


class IamIRNResponse(IamEntityResponse[IRN]):
    data: IRN

    @override
    def converter(self, item: JSON_obj) -> IRN:
        return IRN.of(item)


class IamIRNsResponse(IamEntitiesResponse[IRN]):
    data: list[IRN]
    count: int
    page: int
    page_size: int

    @override
    def converter(self, item: JSON_List) -> list[IRN]:
        return [IRN.of(item) for item in item]


DEFAULT_PAGE_SIZE = 1_000


def generic_search_all(
    auth_headers: dict[str, str],
    func: Callable[[dict[str, str], PaginatedSearchFilter], IamEntitiesResponse[T]],
    search_filter: PaginatedSearchFilter | None = None,
) -> Generator[T, None, None]:
    new_results = True
    page = 1

    search_filter = search_filter or PaginatedSearchFilter()
    search_filter.page_size = search_filter.page_size or DEFAULT_PAGE_SIZE

    counter = 0
    while new_results:
        search_filter.page = page
        resp = func(auth_headers, search_filter)
        if not resp.data:
            break
        for d in resp.data:
            yield d
            counter += 1
        new_results = counter < resp.count
        page += 1
