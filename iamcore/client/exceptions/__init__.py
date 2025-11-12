from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from requests import Response


class IAMException(Exception):
    msg: str

    def __init__(self, msg: str, status_code: int | None = None) -> None:
        self.msg = msg
        self.status_code = status_code
        super().__init__(msg)

    @classmethod
    def from_response(cls, resp: Response) -> IAMException:
        """Create an exception instance from a requests.Response object."""
        try:
            data = resp.json()
            message = data.get("message") or data.get("detail") or data.get("error", "An unknown error occurred.")
        except Exception:
            message = resp.text or "An unknown error occurred."

        return cls(message, status_code=resp.status_code)


class IAMUnauthorizedException(IAMException): ...


class IAMForbiddenException(IAMException): ...


class IAMBedRequestException(IAMException): ...


class IAMConflictException(IAMException): ...


class IAMTenantException(IAMException): ...


class IAMTenantExistsException(IAMTenantException): ...


class IAMPolicyException(IAMException): ...


class IAMPolicyExistsException(IAMPolicyException): ...


class IAMUserException(IAMException): ...


class IAMUserExistsException(IAMUserException): ...


class IAMGroupException(IAMException): ...


class IAMGroupExistsException(IAMGroupException): ...


class IAMResourceException(IAMException): ...


class IAMResourceExistsException(IAMResourceException): ...


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
