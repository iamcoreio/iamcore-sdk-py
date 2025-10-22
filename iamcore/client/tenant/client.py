from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from requests import Response

from iamcore.client.common import (
    SortOrder,
    generic_search_all,
)
from iamcore.client.config import config
from iamcore.client.exceptions import (
    IAMException,
    IAMTenantException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

from .dto import (
    IamTenantIssuersResponse,
    IamTenantResponse,
    IamTenantsResponse,
    Tenant,
    TenantIssuer,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


DEFAULT_LOGIN_THEME = "iamcore"


@err_chain(IAMTenantException)
def create_tenant(
    auth_headers: dict[str, str],
    *,
    name: str,
    display_name: str,
    login_theme: str = DEFAULT_LOGIN_THEME,
) -> Tenant:
    url = config.IAMCORE_URL + "/api/v1/tenants/issuer-types/iamcore"
    payload = {
        "name": name,
        "displayName": display_name,
        "loginTheme": login_theme,
    }
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "POST",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamTenantResponse(**unwrap_post(response)).data


@err_chain(IAMTenantException)
def update_tenant(auth_headers: dict[str, str], irn: IRN, display_name: str) -> None:
    url = config.IAMCORE_URL + "/api/v1/tenants/" + irn.to_base64()
    payload = {"displayName": display_name}
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "PUT",
        url,
        json=payload,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return unwrap_put(response)


@err_chain(IAMTenantException)
def delete_tenant(auth_headers: dict[str, str], irn: IRN) -> None:
    url = config.IAMCORE_URL + "/api/v1/tenants/" + irn.to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "DELETE",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return unwrap_delete(response)


@err_chain(IAMTenantException)
def get_issuer(
    headers: dict[str, str],
    *,
    account: str,
    tenant_id: str,
) -> TenantIssuer:
    url = config.IAMCORE_URL + "/api/v1/tenants/issuers"

    querystring = {
        "account": account,
        "tenant": tenant_id,
    }

    response: Response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        params=querystring,
        timeout=config.TIMEOUT,
    )
    return IamTenantIssuersResponse(**unwrap_get(response)).data.pop()


@err_chain(IAMTenantException)
def search_tenant(
    headers: dict[str, str],
    *,
    irn: str | None = None,
    tenant_id: str | None = None,
    name: str | None = None,
    display_name: str | None = None,
    issuer_type: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamTenantsResponse:
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
        "sortOrder": sort_order.name if sort_order else None,
    }
    querystring = {k: v for k, v in querystring.items() if v}

    response: Response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        params=querystring,
        timeout=config.TIMEOUT,
    )
    return IamTenantsResponse(**unwrap_get(response))


@err_chain(IAMException)
def search_all_tenants(
    auth_headers: dict[str, str],
    *,
    irn: str | None = None,
    tenant_id: str | None = None,
    name: str | None = None,
    display_name: str | None = None,
    issuer_type: str | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> Generator[Tenant, None, None]:
    kwargs = {
        "irn": irn,
        "tenant_id": tenant_id,
        "name": name,
        "display_name": display_name,
        "issuer_type": issuer_type,
        "sort": sort,
        "sort_order": sort_order,
    }
    return generic_search_all(auth_headers, search_tenant, **kwargs)
