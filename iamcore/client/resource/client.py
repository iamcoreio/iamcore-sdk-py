from __future__ import annotations

from typing import TYPE_CHECKING

from iamcore.client.application.client import json
from iamcore.client.exceptions import (
    IAMException,
    IAMResourceException,
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

from .dto import IamResourceResponse, IamResourcesResponse, Resource

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN
    from requests import Response

    from iamcore.client.config import BaseConfig


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Resource API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.iamcore_url, timeout=config.iamcore_client_timeout)

    @err_chain(IAMResourceException)
    def create_resource(
        self,
        auth_headers: dict[str, str],
        *,
        name: str,
        application: str,
        path: str,
        resource_type: str,
        display_name: str | None = None,
        tenant_id: str | None = None,
        description: str | None = None,
        metadata: dict[str, object] | None = None,
        enabled: bool = True,
    ) -> Resource:
        payload = {
            "name": name,
            "displayName": display_name,
            "tenantID": tenant_id,
            "application": application,
            "path": path,
            "resourceType": resource_type,
            "enabled": enabled,
            "description": description,
            "metadata": metadata,
        }
        response = self.post("resources", data=json.dumps(payload), headers=auth_headers)
        return IamResourceResponse(**unwrap_post(response)).data

    @err_chain(IAMResourceException)
    def update_resource(
        self,
        auth_headers: dict[str, str],
        *,
        resource_irn: IRN,
        display_name: str | None = None,
        enabled: bool = True,
        description: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        path = f"resources/{resource_irn.to_base64()}"

        payload = {
            "displayName": display_name,
            "enabled": enabled,
            "description": description,
            "metadata": metadata,
        }
        payload = {k: v for k, v in payload.items() if v}

        response = self.patch(path, data=json.dumps(payload), headers=auth_headers)
        unwrap_put(response)

    @err_chain(IAMResourceException)
    def delete_resource(self, auth_headers: dict[str, str], resource_irn: IRN) -> None:
        url = f"/api/v1/resources/{resource_irn.to_base64()}"
        response: Response = self.delete(url, headers=auth_headers)
        unwrap_delete(response)

    @err_chain(IAMResourceException)
    def delete_resources(self, auth_headers: dict[str, str], resources_irns: list[IRN]) -> None:
        payload = {"resourceIDs": [r.to_base64() for r in resources_irns if r]}
        response = self.post("resources/delete", data=json.dumps(payload), headers=auth_headers)
        unwrap_delete(response)

    @err_chain(IAMResourceException)
    def search_resource(
        self,
        auth_headers: dict[str, str],
        *,
        irn: IRN | None = None,
        path: str | None = None,
        display_name: str | None = None,
        enabled: bool | None = None,
        tenant_id: str | None = None,
        application: str | None = None,
        resource_type: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> IamResourcesResponse:
        querystring = {
            "irn": str(irn) if irn else None,
            "path": path,
            "application": application,
            "enabled": enabled,
            "displayName": display_name,
            "resourceType": resource_type,
            "tenantID": tenant_id,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
            "sortOrder": sort_order.name if sort_order else None,
        }
        querystring = {k: v for k, v in querystring.items() if v}

        response = self.get("resources", headers=auth_headers, params=querystring)
        return IamResourcesResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_resources(
        self,
        auth_headers: dict[str, str],
        *,
        irn: IRN | None = None,
        path: str | None = None,
        display_name: str | None = None,
        enabled: bool | None = None,
        tenant_id: str | None = None,
        application: str | None = None,
        resource_type: str | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> Generator[Resource, None, None]:
        kwargs = {
            "irn": str(irn) if irn else None,
            "path": path,
            "application": application,
            "enabled": enabled,
            "displayName": display_name,
            "resourceType": resource_type,
            "tenantID": tenant_id,
            "sort": sort,
            "sortOrder": sort_order,
        }
        kwargs = {k: v for k, v in kwargs.items() if v}
        return generic_search_all(auth_headers, self.search_resource, **kwargs)
