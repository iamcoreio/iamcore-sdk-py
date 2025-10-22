from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar, Union

from iamcore.irn import IRN
from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Generator


def to_snake_case(field_name: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", field_name).lower()


class SortOrder(Enum):
    asc = 1
    desc = 2


T = TypeVar("T")
JSON = dict[str, Any]
JSON_List = Union[list[dict[str, Any]], list[str]]


class IamEntityResponse(ABC, Generic[T]):
    data: T

    def __init__(self, item: JSON) -> None:
        self.data = self.converter(item)
        super().__init__()

    @abstractmethod
    def converter(self, item: JSON) -> T:
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
    def converter(self, item: JSON) -> IRN:
        return IRN.of(item)


class IamIRNsResponse(IamEntitiesResponse[IRN]):
    data: list[IRN]
    count: int
    page: int
    page_size: int

    @override
    def converter(self, item: JSON_List) -> list[IRN]:
        return [IRN.of(item) for item in item]


def generic_search_all(
    auth_headers: dict[str, str],
    func: Callable[..., IamEntitiesResponse[T]],
    *args: Any,
    **kwargs: Any,
) -> Generator[T, None, None]:
    if "page" in kwargs:
        kwargs.pop("page")

    new_results = True
    page = 1

    counter = 0
    while new_results:
        resp = func(auth_headers, *args, page=page, **kwargs)
        if not resp.data:
            break
        for d in resp.data:
            yield d
            counter += 1
        new_results = counter < resp.count
        page += 1
