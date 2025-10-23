from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, TypeVar, Union

from iamcore.irn import IRN
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from typing_extensions import Self, override

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
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create model instance from dictionary, handling validation errors."""
        try:
            return cls.model_validate(data)
        except ValidationError as e:
            msg = f"Validation error for {cls.__name__}: {e}"
            raise IAMException(msg) from e

    @classmethod
    def from_json(cls, data: Union[str, bytes, bytearray]) -> Self:
        """Create model instance from JSON, handling validation errors."""
        try:
            return cls.model_validate_json(data)
        except ValidationError as e:
            msg = f"Validation error for {cls.__name__}: {e}"
            raise IAMException(msg) from e

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary with optional field aliasing."""
        return self.model_dump(by_alias=True)


class PaginatedSearchFilter(IAMCoreBaseModel):
    """Paginated search filter."""

    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")
    sort: Optional[str] = None
    sort_order: Optional[str] = Field(default=None, alias="sortOrder")


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
        return IRN.of(item["irn"])


class IamIRNsResponse(IamEntitiesResponse[IRN]):
    data: list[IRN]
    count: int
    page: int
    page_size: int

    @override
    def converter(self, item: JSON_List) -> list[IRN]:
        return [IRN.of(item) for item in item]


SEARCH_ALL_PAGE_SIZE = 1_000


# Use TypeAlias for a more explicit and readable type definition
_SearchFunc = Callable[[dict[str, str], PaginatedSearchFilter], IamEntitiesResponse[T]]


def generic_search_all(
    auth_headers: dict[str, str],
    func: _SearchFunc[T],
    search_filter: Optional[PaginatedSearchFilter] = None,
) -> Generator[T, None, None]:
    """
    Generic generator to handle paginated search requests and yield all results.

    Args:
        auth_headers: Authentication headers for the API call.
        func: The specific search function to call for each page.
        search_filter: An optional filter. A copy will be used to avoid side effects.

    Yields:
        All entities of type T from the paginated search.
    """
    # Create a deep copy to avoid mutating the original object.
    # If no filter is provided, create a new one.
    paginator_filter = search_filter.model_copy(deep=True) if search_filter else PaginatedSearchFilter()

    # Set our internal page size for this operation.
    paginator_filter.page_size = SEARCH_ALL_PAGE_SIZE

    page = 1
    items_yielded = 0
    total_items = -1  # Initialize to a sentinel value

    while True:
        paginator_filter.page = page
        resp = func(auth_headers, paginator_filter)

        # On the first response, set the total number of items we expect.
        if total_items == -1:
            total_items = resp.count

        if not resp.data:
            break  # Stop if the API returns an empty list, a safe fallback.

        yield from resp.data
        items_yielded += len(resp.data)

        # Stop as soon as we have all items.
        # This saves an extra API call if total_items is a multiple of page_size.
        if items_yielded >= total_items:
            break

        page += 1
