from __future__ import annotations

from http.client import BAD_REQUEST, CONFLICT, CREATED, FORBIDDEN, NO_CONTENT, OK, UNAUTHORIZED
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from requests import Response


class IAMException(Exception):
    msg: str

    def __init__(self, msg: str) -> None:
        self.msg = msg


class IAMUnauthorizedException(IAMException):
    pass


class IAMForbiddenException(IAMException):
    pass


class IAMBedRequestException(IAMException):
    pass


class IAMConflictException(IAMException):
    pass


class IAMTenantException(IAMException):
    pass


class IAMTenantExistsException(IAMTenantException):
    pass


class IAMPolicyException(IAMException):
    pass


class IAMPolicyExistsException(IAMPolicyException):
    pass


class IAMUserException(IAMException):
    pass


class IAMUserExistsException(IAMUserException):
    pass


class IAMGroupException(IAMException):
    pass


class IAMGroupExistsException(IAMGroupException):
    pass


class IAMResourceException(IAMException):
    pass


class IAMResourceExistsException(IAMResourceException):
    pass


GET_MAPPING = {OK: None, UNAUTHORIZED: IAMUnauthorizedException, FORBIDDEN: IAMForbiddenException}

POST_MAPPING = {
    CREATED: None,
    BAD_REQUEST: IAMBedRequestException,
    CONFLICT: IAMConflictException,
    UNAUTHORIZED: IAMUnauthorizedException,
    FORBIDDEN: IAMForbiddenException,
}

PUT_MAPPING = {
    NO_CONTENT: None,
    BAD_REQUEST: IAMBedRequestException,
    UNAUTHORIZED: IAMUnauthorizedException,
    FORBIDDEN: IAMForbiddenException,
}

DELETE_MAPPING = {
    NO_CONTENT: None,
    UNAUTHORIZED: IAMUnauthorizedException,
    FORBIDDEN: IAMForbiddenException,
}

EVALUATE_MAPPING = {
    OK: None,
    BAD_REQUEST: IAMBedRequestException,
    UNAUTHORIZED: IAMUnauthorizedException,
    FORBIDDEN: IAMForbiddenException,
}


def unwrap_return_empty(resp: Response, mapping: dict[int, Any]) -> None:
    if resp.status_code not in mapping:
        msg = f"Unexpected error code: {resp.status_code}"
        raise IAMTenantException(msg)
    mapped_exception = mapping.get(resp.status_code)
    if mapped_exception is None:
        return
    raise mapped_exception(resp.json()["message"])


def unwrap_return_json(resp: Response, mapping: dict[int, Any]) -> dict[str, Any]:
    if resp.status_code not in mapping:
        msg = f"Unexpected error code: {resp.status_code}"
        raise IAMTenantException(msg)
    mapped_exception = mapping.get(resp.status_code)
    if mapped_exception is None:
        return resp.json()
    raise mapped_exception(resp.json()["message"])


def unwrap_get(resp: Response, mapping: dict[int, Any] | None = None) -> dict[str, Any]:
    if mapping is None:
        mapping = GET_MAPPING
    return unwrap_return_json(resp, mapping)


def unwrap_post(resp: Response, mapping: dict[int, Any] | None = None) -> dict[str, Any]:
    if mapping is None:
        mapping = POST_MAPPING
    return unwrap_return_json(resp, mapping)


def unwrap_put(resp: Response, mapping: dict[int, Any] | None = None) -> None:
    if mapping is None:
        mapping = PUT_MAPPING
    return unwrap_return_empty(resp, mapping)


def unwrap_patch(resp: Response, mapping: dict[int, Any] | None = None) -> None:
    if mapping is None:
        mapping = PUT_MAPPING
    return unwrap_return_empty(resp, mapping)


def unwrap_delete(resp: Response, mapping: dict[int, Any] | None = None) -> None:
    if mapping is None:
        mapping = DELETE_MAPPING
    return unwrap_return_empty(resp, mapping)


def err_chain(error: type[IAMException] = IAMException) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def new_func(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except IAMException:
                raise
            except Exception as e:
                raise error(str(e)) from e

        return new_func

    return decorator
