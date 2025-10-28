from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import PaginatedSearchFilter, generic_search_all
from iamcore.client.exceptions import IAMException, err_chain

from .dto import ApiKey, IamApiKeysResponse

if TYPE_CHECKING:
    from collections.abc import Generator


class Client(HTTPClientWithTimeout):
    """Client for IAM Core API Keys."""

    BASE_PATH = "principals"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMException)
    def create_application_api_key(self, auth_headers: dict[str, str], principal_id: str) -> None:
        path = f"{principal_id}/api-keys"
        headers = {"Content-Type": "application/json", **auth_headers}
        self._post(path, headers=headers)

    @err_chain(IAMException)
    def get_application_api_keys(
        self,
        headers: dict[str, str],
        principal_id: str,
        search_filter: Optional[PaginatedSearchFilter] = None,
    ) -> IamApiKeysResponse:
        query = search_filter.model_dump(by_alias=True, exclude_none=True) if search_filter else None
        path = f"{principal_id}/api-keys"
        response = self._get(path, headers=headers, params=query)
        return IamApiKeysResponse(**response.json())

    @err_chain(IAMException)
    def get_all_applications_api_keys(
        self,
        auth_headers: dict[str, str],
        principal_id: str,
    ) -> Generator[ApiKey, None, None]:
        return generic_search_all(
            auth_headers,
            lambda headers, search_filter: self.get_application_api_keys(
                headers,
                principal_id,
                search_filter=search_filter,
            ),
            None,
        )
