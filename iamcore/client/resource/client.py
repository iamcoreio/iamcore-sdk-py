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
    generic_search_all,
)
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import (
    CreateResource,
    IamResourceResponse,
    IamResourcesResponse,
    Resource,
    ResourceSearchFilter,
    UpdateResource,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN
    from requests import Response


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Resource API."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMResourceException)
    def create_resource(
        self,
        auth_headers: dict[str, str],
        params: CreateResource,
    ) -> Resource:
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post("resources", data=payload, headers=auth_headers)
        return IamResourceResponse(**unwrap_post(response)).data

    @err_chain(IAMResourceException)
    def update_resource(
        self,
        auth_headers: dict[str, str],
        irn: IRN,
        params: UpdateResource,
    ) -> None:
        path = f"resources/{irn.to_base64()}"
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self.patch(path, data=payload, headers=auth_headers)
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
        resource_filter: ResourceSearchFilter | None = None,
    ) -> IamResourcesResponse:
        query = resource_filter.model_dump(by_alias=True, exclude_none=True) if resource_filter else None
        response = self.get("resources", headers=auth_headers, params=query)
        return IamResourcesResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_resources(
        self,
        auth_headers: dict[str, str],
        resource_filter: ResourceSearchFilter | None = None,
    ) -> Generator[Resource, None, None]:
        return generic_search_all(auth_headers, self.search_resource, resource_filter)
