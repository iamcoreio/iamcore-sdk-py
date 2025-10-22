from __future__ import annotations

import json
from typing import TYPE_CHECKING

from iamcore.client.exceptions import IAMException, err_chain, unwrap_get, unwrap_post
from iamcore.client.models.base import (
    SortOrder,
    generic_search_all,
)
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import (
    ApplicationResourceType,
    IamApplicationResourceTypeResponse,
    IamApplicationResourceTypesResponse,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN

    from iamcore.client.config import BaseConfig


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Application Resource Type API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.iamcore_url, timeout=config.iamcore_client_timeout)

    @err_chain(IAMException)
    def create_resource_type(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        *,
        type: str,
        description: str | None = None,
        action_prefix: str | None = None,
        operations: list[str] | None = None,
    ) -> ApplicationResourceType:
        path = f"applications/{application_irn.to_base64()}/resource-types"

        payload = {
            "type": type,
            "description": description,
            "actionPrefix": action_prefix,
            "operations": operations,
        }
        payload = {k: v for k, v in payload.items() if v}

        response = self.post(path, data=json.dumps(payload), headers=auth_headers)
        return IamApplicationResourceTypeResponse(**unwrap_post(response)).data

    @err_chain(IAMException)
    def get_resource_type(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        type_irn: IRN,
    ) -> ApplicationResourceType:
        path = f"applications/{application_irn.to_base64()}/resource-types/{type_irn.to_base64()}"
        response = self.get(path, headers=auth_headers)
        return IamApplicationResourceTypeResponse(**unwrap_get(response)).data

    @err_chain(IAMException)
    def search_application_resource_types(
        self,
        headers: dict[str, str],
        application_irn: IRN,
        *,
        page: int | None = None,
        page_size: int | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> IamApplicationResourceTypesResponse:
        path = f"applications/{application_irn.to_base64()}/resource-types"

        querystring = {
            "page": page,
            "pageSize": page_size,
            "sort": sort,
            "sortOrder": sort_order.name if sort_order else None,
        }
        querystring = {k: v for k, v in querystring.items() if v}

        response = self.get(path, headers=headers, params=querystring)
        return IamApplicationResourceTypesResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_application_resource_types(
        self,
        auth_headers: dict[str, str],
        *,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> Generator[ApplicationResourceType, None, None]:
        kwargs = {
            "sort": sort,
            "sort_order": sort_order,
        }
        kwargs = {k: v for k, v in kwargs.items() if v}
        return generic_search_all(auth_headers, self.search_application_resource_types, **kwargs)
