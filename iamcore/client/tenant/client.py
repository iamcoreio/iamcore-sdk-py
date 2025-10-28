from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.application.client import json
from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, IAMTenantException, err_chain

from .dto import (
    CreateTenant,
    GetTenantIssuer,
    GetTenantsFilter,
    IamTenantIssuersResponse,
    IamTenantResponse,
    IamTenantsResponse,
    Tenant,
    TenantIssuer,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Tenant API."""

    BASE_PATH = "tenants"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMTenantException)
    def create_tenant(self, auth_headers: dict[str, str], params: CreateTenant) -> Tenant:
        path = "issuer-types/iamcore"
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self._post(path, data=payload, headers=auth_headers)
        return IamTenantResponse(**response.json()).data

    @err_chain(IAMTenantException)
    def update_tenant(self, auth_headers: dict[str, str], irn: IRN, display_name: str) -> None:
        payload = {"displayName": display_name}
        self._put(irn.to_base64(), data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMTenantException)
    def delete_tenant(self, auth_headers: dict[str, str], irn: IRN) -> None:
        self._delete(irn.to_base64(), headers=auth_headers)

    @err_chain(IAMTenantException)
    def get_issuer(self, headers: dict[str, str], params: GetTenantIssuer) -> TenantIssuer:
        response = self._get("issuers", headers=headers, params=params.to_dict())
        return IamTenantIssuersResponse(**response.json()).data.pop()

    @err_chain(IAMTenantException)
    def search_tenants(
        self,
        headers: dict[str, str],
        tenant_filter: Optional[GetTenantsFilter] = None,
    ) -> IamTenantsResponse:
        query = tenant_filter.model_dump(by_alias=True, exclude_none=True) if tenant_filter else None
        response = self._get(headers=headers, params=query)
        return IamTenantsResponse(**response.json())

    @err_chain(IAMException)
    def search_all_tenants(
        self,
        auth_headers: dict[str, str],
        tenant_filter: Optional[GetTenantsFilter] = None,
    ) -> Generator[Tenant, None, None]:
        return generic_search_all(auth_headers, self.search_tenants, tenant_filter)
