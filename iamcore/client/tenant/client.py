from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.application.client import json
from iamcore.client.base.client import HTTPClientWithTimeout
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

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMTenantException)
    def create_tenant(self, auth_headers: dict[str, str], params: CreateTenant) -> Tenant:
        path = "tenants/issuer-types/iamcore"
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post(path, data=payload, headers=auth_headers)
        return IamTenantResponse(response.json()["data"]).data

    @err_chain(IAMTenantException)
    def update_tenant(self, auth_headers: dict[str, str], irn: IRN, display_name: str) -> None:
        path = f"tenants/{irn.to_base64()}"
        payload = {"displayName": display_name}
        self.put(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMTenantException)
    def delete_tenant(self, auth_headers: dict[str, str], irn: IRN) -> None:
        path = f"tenants/{irn.to_base64()}"
        self.delete(path, headers=auth_headers)

    @err_chain(IAMTenantException)
    def get_issuer(self, headers: dict[str, str], params: GetTenantIssuer) -> TenantIssuer:
        response = self.get(
            "tenants/issuers",
            headers=headers,
            params=params.model_dump(by_alias=True),
        )
        resp_data = response.json()
        return IamTenantIssuersResponse(
            data=resp_data["data"], count=resp_data["count"], page=resp_data["page"], page_size=resp_data["pageSize"]
        ).data.pop()

    @err_chain(IAMTenantException)
    def search_tenant(
        self,
        headers: dict[str, str],
        tenant_filter: Optional[GetTenantsFilter] = None,
    ) -> IamTenantsResponse:
        query = tenant_filter.model_dump(by_alias=True, exclude_none=True) if tenant_filter else None
        response = self.get("tenants", headers=headers, params=query)
        resp_data = response.json()
        return IamTenantsResponse(
            data=resp_data["data"], count=resp_data["count"], page=resp_data["page"], page_size=resp_data["pageSize"]
        )

    @err_chain(IAMException)
    def search_all_tenants(
        self,
        auth_headers: dict[str, str],
        tenant_filter: Optional[GetTenantsFilter] = None,
    ) -> Generator[Tenant, None, None]:
        return generic_search_all(auth_headers, self.search_tenant, tenant_filter)
