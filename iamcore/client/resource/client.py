from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.application.client import json
from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, IAMResourceException, err_chain

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


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Resource API."""

    BASE_PATH = "resources"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMResourceException)
    def create(self, auth_headers: dict[str, str], params: CreateResource) -> Resource:
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self._post(data=payload, headers=auth_headers)
        return IamResourceResponse(**response.json()).data

    @err_chain(IAMResourceException)
    def update(self, auth_headers: dict[str, str], irn: IRN, params: UpdateResource) -> None:
        payload = params.model_dump_json(by_alias=True, exclude_none=True, exclude_unset=True)
        self._patch(irn.to_base64(), data=payload, headers=auth_headers)

    @err_chain(IAMResourceException)
    def delete(self, auth_headers: dict[str, str], resource_irn: IRN) -> None:
        self._delete(resource_irn.to_base64(), headers=auth_headers)

    @err_chain(IAMResourceException)
    def delete_in_batch(self, auth_headers: dict[str, str], resources_irns: list[IRN]) -> None:
        payload = {"resourceIDs": [r.to_base64() for r in resources_irns if r]}
        self._post("delete", data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMResourceException)
    def search(
        self,
        auth_headers: dict[str, str],
        resource_filter: Optional[ResourceSearchFilter] = None,
    ) -> IamResourcesResponse:
        query = resource_filter.model_dump(by_alias=True, exclude_none=True) if resource_filter else None
        response = self._get(headers=auth_headers, params=query)
        return IamResourcesResponse(**response.json())

    @err_chain(IAMException)
    def search_all(
        self,
        auth_headers: dict[str, str],
        resource_filter: Optional[ResourceSearchFilter] = None,
    ) -> Generator[Resource, None, None]:
        return generic_search_all(auth_headers, self.search, resource_filter)
