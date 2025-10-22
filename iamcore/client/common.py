from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

from iamcore.irn import IRN

from iamcore.client.exceptions import IAMException
from iamcore.client.models.base import IAMCoreBaseModel

if TYPE_CHECKING:
    from collections.abc import Generator


def to_snake_case(field_name: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", field_name).lower()


def to_dict(obj: Any) -> dict[str, Any]:
    """Convert object to dict."""

    def _to_dict_recursive(obj: Any) -> dict[str, Any] | Any:
        if isinstance(obj, dict):
            data = {}
            for k, v in obj.items():  # pyright: ignore[reportUnknownVariableType]
                data[k] = _to_dict_recursive(v)
            return data  # pyright: ignore[reportUnknownVariableType]

        if isinstance(obj, IRN):
            return str(obj)
        if hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [_to_dict_recursive(v) for v in obj]
        if hasattr(obj, "__dict__"):
            return {
                key: _to_dict_recursive(value)
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith("_")
            }
        return obj

    res = _to_dict_recursive(obj)
    if not isinstance(res, dict):
        msg = "Unexpected result format"
        raise IAMException(msg)

    return res  # pyright: ignore[reportUnknownVariableType]


class SortOrder(Enum):
    asc = 1
    desc = 2


T = TypeVar("T", bound=IAMCoreBaseModel)


class IamEntityResponse(Generic[T]):
    def __init__(self, base_class: type[T], data: dict[str, Any] | T) -> None:
        self.data: T = base_class.model_validate(data) if isinstance(data, dict) else data


class IamEntitiesResponse(Generic[T]):
    data: list[T]
    count: int
    page: int
    page_size: int

    def __init__(self, base_class: type[T], data: list[dict[str, Any]], **kwargs: Any) -> None:
        if not isinstance(data, list):  # pyright: ignore[reportUnnecessaryIsInstance]
            msg = "Unexpected response format"  # pyright: ignore[reportUnreachable]
            raise IAMException(msg)

        self.data = [base_class.model_validate(item) for item in data]

        for k, v in kwargs.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)


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
