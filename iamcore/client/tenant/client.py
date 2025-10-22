from __future__ import annotations

from typing import TYPE_CHECKING

from iamcore.client.application.client import json
from iamcore.client.exceptions import (
    IAMException,
    IAMTenantException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)
from iamcore.client.models.base import (
    SortOrder,
    generic_search_all,
)
from iamcore.client.models.client import HTTPClientWithTimeout

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
    from requests import Response

    from iamcore.client.config import BaseConfig


DEFAULT_LOGIN_THEME = "iamcore"


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Tenant API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.IAMCORE_URL, timeout=config.TIMEOUT)

    @err_chain(IAMTenantException)
    def create_tenant(
        self,
        auth_headers: dict[str, str],
        *,
        name: str,
        display_name: str,
        login_theme: str = DEFAULT_LOGIN_THEME,
    ) -> Tenant:
        path = "tenants/issuer-types/iamcore"
        payload = {
            "name": name,
            "displayName": display_name,
            "loginTheme": login_theme,
        }
        response = self.post(path, data=json.dumps(payload), headers=auth_headers)
        return IamTenantResponse(**unwrap_post(response)).data

    @err_chain(IAMTenantException)
    def update_tenant(self, auth_headers: dict[str, str], irn: IRN, display_name: str) -> None:
        path = f"tenants/{irn.to_base64()}"
        payload = {"displayName": display_name}
        response: Response = self.put(path, data=json.dumps(payload), headers=auth_headers)
        return unwrap_put(response)

    @err_chain(IAMTenantException)
    def delete_tenant(self, auth_headers: dict[str, str], irn: IRN) -> None:
        path = f"tenants/{irn.to_base64()}"
        response = self.delete(path, headers=auth_headers)
        unwrap_delete(response)

    @err_chain(IAMTenantException)
    def get_issuer(
        self,
        headers: dict[str, str],
        *,
        account: str,
        tenant_id: str,
    ) -> TenantIssuer:
        response = self.get(
            "tenants/issuers",
            headers=headers,
            params={"account": account, "tenant": tenant_id},
        )
        return IamTenantIssuersResponse(**unwrap_get(response)).data.pop()

    @err_chain(IAMTenantException)
    def search_tenant(
        self,
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

        response = self.get("tenants", headers=headers, params=querystring)
        return IamTenantsResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_tenants(
        self,
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
        return generic_search_all(auth_headers, self.search_tenant, **kwargs)
