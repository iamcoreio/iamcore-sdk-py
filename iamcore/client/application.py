from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.common import (
    IamEntitiesResponse,
    IamEntityResponse,
    SortOrder,
    generic_search_all,
    to_dict,
    to_snake_case,
)
from iamcore.client.config import config
from iamcore.client.exceptions import (
    IAMException,
    IAMUnauthorizedException,
    err_chain,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

if TYPE_CHECKING:
    from collections.abc import Generator


class IAMEntityBase:
    def __int__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @staticmethod
    def of(item: Any) -> IAMEntityBase:
        pass


class Application(IAMEntityBase):
    id: str
    irn: IRN
    name: str
    display_name: str
    created: str
    updated: str

    def __init__(self, irn: str, **kwargs: Any) -> None:
        self.irn = IRN.from_irn_str(irn)
        for k, v in kwargs.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

    @staticmethod
    def of(item: dict[str, Any] | Application) -> Application:
        if isinstance(item, Application):
            return item
        if isinstance(item, dict):
            return Application(**item)
        raise IAMException("Unexpected response format")

    def to_dict(self):
        return to_dict(self)


@err_chain(IAMException)
def create_application(
    auth_headers: dict[str, str],
    payload: dict[str, str] | None = None,
    name: str | None = None,
    display_name: str | None = None,
) -> Application:
    url = config.IAMCORE_URL + "/api/v1/applications"
    if not payload:
        payload = {"name": name, "displayName": display_name}
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse(Application, **unwrap_post(response)).data


@err_chain(IAMException)
def get_application(headers: dict[str, str], irn: str) -> Application:
    url = config.IAMCORE_URL + "/api/v1/applications/" + str(irn)
    response: Response = requests.request("GET", url, data="", headers=headers)
    return IamEntityResponse(Application, **unwrap_get(response)).data


@err_chain(IAMException)
def application_attach_policies(
    auth_headers: dict[str, str],
    application_id: str,
    policies_ids: list[str],
) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not application_id:
        msg = "Missing user_id"
        raise IAMException(msg)
    if not policies_ids or not isinstance(policies_ids, list):
        msg = "Missing policies_ids or it's not a list"
        raise IAMException(msg)

    url = config.IAMCORE_URL + "/api/v1/applications/" + application_id + "/policies/attach"
    headers = {"Content-Type": "application/json", **auth_headers}
    payload = {"policyIDs": policies_ids}

    response = requests.request("PUT", url, json=payload, headers=headers)
    return unwrap_put(response)


@err_chain(IAMException)
def search_application(
    headers: dict[str, str],
    irn: str | None = None,
    name: str | None = None,
    display_name: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[Application]:
    url = config.IAMCORE_URL + "/api/v1/applications"

    querystring = {
        "irn": str(irn) if irn else None,
        "name": name,
        "displayName": display_name,
        "page": page,
        "pageSize": page_size,
        "sort": sort,
        "sortOrder": sort_order,
    }

    querystring = {k: v for k, v in querystring.items() if v}

    response: Response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(Application, **unwrap_get(response))


@err_chain(IAMException)
def search_all_applications(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[Application, None, None]:
    return generic_search_all(auth_headers, search_application, *args, **kwargs)
