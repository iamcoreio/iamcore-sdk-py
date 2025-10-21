from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.config import config

from .common import (
    IamEntitiesResponse,
    IamEntityResponse,
    SortOrder,
    generic_search_all,
    to_dict,
    to_snake_case,
)
from .exceptions import (
    IAMException,
    IAMTenantException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

if TYPE_CHECKING:
    from collections.abc import Generator


class Tenant:
    resource_id: str
    irn: IRN
    tenant_id: str
    name: str
    display_name: str
    login_theme: str
    created: str
    updated: str

    def __init__(self, irn: str, **kwargs: Any) -> None:
        self.irn = IRN.from_irn_str(irn)
        for k, v in kwargs.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

    @staticmethod
    def of(item: dict[str, Any] | Tenant) -> Tenant:
        if isinstance(item, Tenant):
            return item
        if isinstance(item, dict):
            return Tenant(**item)
        raise IAMTenantException("Unexpected response format")

    def to_dict(self) -> dict[str, Any]:
        return to_dict(self)

    def update(self, auth_headers: dict[str, str]) -> None:
        return update_tenant(auth_headers, self.resource_id, self.display_name)

    def delete(self, auth_headers: dict[str, str]):
        return delete_tenant(auth_headers, self.resource_id)


class TenantIssuer:
    id: str
    irn: IRN
    name: str
    type: str
    url: str
    client_id: str
    login_url: str

    def __init__(self, irn: str, **kwargs: Any):
        self.irn = IRN.from_irn_str(irn)
        for k, v in kwargs.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

    @staticmethod
    def of(item: dict[str, Any] | TenantIssuer) -> TenantIssuer:
        if isinstance(item, TenantIssuer):
            return item
        if isinstance(item, dict):
            return TenantIssuer(**item)
        raise IAMTenantException("Unexpected response format")

    def to_dict(self) -> dict[str, Any]:
        return to_dict(self)

    def update(self, auth_headers: dict[str, str]) -> None:
        return update_tenant(auth_headers, self.resource_id, self.display_name)

    def delete(self, auth_headers: dict[str, str]):
        return delete_tenant(auth_headers, self.resource_id)


@err_chain(IAMTenantException)
def create_tenant(
    auth_headers: dict[str, str],
    payload: dict[str, str] | None = None,
    name: str | None = None,
    display_name: str | None = None,
    login_theme: str | None = None,
) -> Tenant:
    url = config.IAMCORE_URL + "/api/v1/tenants/issuer-types/iamcore"
    if not payload:
        payload = {
            "name": name,
            "displayName": display_name,
            "loginTheme": login_theme,
        }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, json=payload, headers=headers)
    return IamEntityResponse(Tenant, **unwrap_post(response)).data


@err_chain(IAMTenantException)
def update_tenant(auth_headers: dict[str, str], resource_id: str, display_name: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMTenantException(msg)
    if not resource_id or not display_name:
        msg = "Missing resource_id or display_name"
        raise IAMTenantException(msg)

    url = config.IAMCORE_URL + "/api/v1/tenants/" + IRN.of(resource_id).to_base64()
    payload = {"displayName": display_name}
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("PUT", url, json=payload, headers=headers)
    return unwrap_put(response)


@err_chain(IAMTenantException)
def delete_tenant(auth_headers: dict[str, str], resource_id: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMTenantException(msg)
    if not resource_id:
        msg = "Missing resource_id"
        raise IAMTenantException(msg)

    url = config.IAMCORE_URL + "/api/v1/tenants/" + IRN.of(resource_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("DELETE", url, data="", headers=headers)
    return unwrap_delete(response)


@err_chain(IAMTenantException)
def get_issuer(
    headers: dict[str, str],
    account: str | None = None,
    tenant_id: str | None = None,
) -> TenantIssuer:
    url = config.IAMCORE_URL + "/api/v1/tenants/issuers"

    querystring = {
        "account": account,
        "tenant": tenant_id,
    }

    response: Response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(TenantIssuer, **unwrap_get(response)).data.pop()


@err_chain(IAMTenantException)
def search_tenant(
    headers: dict[str, str],
    irn: str | None = None,
    tenant_id: str | None = None,
    name: str | None = None,
    display_name: str | None = None,
    issuer_type: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[Tenant]:
    url = config.IAMCORE_URL + "/api/v1/tenants"

    querystring = {
        "irn": str(irn) if irn else None,
        "name": name,
        "displayName": display_name,
        "tenantID": tenant_id,
        "issuerType": issuer_type,
        "page": page,
        "pageSize": page_size,
        "sort": sort,
        "sortOrder": sort_order,
    }

    querystring = {k: v for k, v in querystring.items() if v}

    response: Response = requests.request("GET", url, data="", headers=headers, params=querystring)
    return IamEntitiesResponse(Tenant, **unwrap_get(response))


@err_chain(IAMException)
def search_all_tenants(
    auth_headers: dict[str, str],
    *args: Any,
    **kwargs: Any,
) -> Generator[Tenant, None, None]:
    return generic_search_all(auth_headers, search_tenant, *args, **kwargs)
