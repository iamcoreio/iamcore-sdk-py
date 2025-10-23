from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import PaginatedSearchFilter, generic_search_all
from iamcore.client.exceptions import IAMException, err_chain

from .dto import (
    ApplicationResourceType,
    CreateApplicationResourceType,
    IamApplicationResourceTypeResponse,
    IamApplicationResourceTypesResponse,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Application Resource Type API."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMException)
    def create_resource_type(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        params: CreateApplicationResourceType,
    ) -> ApplicationResourceType:
        path = f"applications/{application_irn.to_base64()}/resource-types"
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post(path, data=payload, headers=auth_headers)
        return IamApplicationResourceTypeResponse(**response.json()).data

    @err_chain(IAMException)
    def get_resource_type(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        type_irn: IRN,
    ) -> ApplicationResourceType:
        path = f"applications/{application_irn.to_base64()}/resource-types/{type_irn.to_base64()}"
        response = self.get(path, headers=auth_headers)
        return IamApplicationResourceTypeResponse(**response.json()).data

    @err_chain(IAMException)
    def search_application_resource_types(
        self,
        headers: dict[str, str],
        application_irn: IRN,
        resource_type_filter: Optional[PaginatedSearchFilter] = None,
    ) -> IamApplicationResourceTypesResponse:
        path = f"applications/{application_irn.to_base64()}/resource-types"
        query = resource_type_filter.model_dump(by_alias=True, exclude_none=True) if resource_type_filter else None
        response = self.get(path, headers=headers, params=query)
        return IamApplicationResourceTypesResponse(**response.json())

    @err_chain(IAMException)
    def search_all_application_resource_types(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        resource_type_filter: Optional[PaginatedSearchFilter] = None,
    ) -> Generator[ApplicationResourceType, None, None]:
        return generic_search_all(
            auth_headers,
            lambda headers, search_filter: self.search_application_resource_types(
                headers,
                application_irn,
                search_filter,
            ),
            resource_type_filter,
        )
