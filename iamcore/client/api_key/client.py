from __future__ import annotations

from typing import TYPE_CHECKING

from iamcore.client.exceptions import IAMException, err_chain, unwrap_get
from iamcore.client.models.base import generic_search_all
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import ApiKey, IamApiKeyResponse, IamApiKeysResponse

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


class Client(HTTPClientWithTimeout):
    """Client for IAM Core API Keys."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMException)
    def create_application_api_key(
        self,
        auth_headers: dict[str, str],
        principal_id: str,
    ) -> IamApiKeyResponse:
        path = f"principals/{principal_id}/api-keys"
        headers = {"Content-Type": "application/json", **auth_headers}
        response = self.post(path, headers=headers)
        return IamApiKeyResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def get_application_api_keys(
        self,
        headers: dict[str, str],
        principal_id: str,
        page: int = 1,
    ) -> IamApiKeysResponse:
        path = f"principals/{principal_id}/api-keys?page={page}"
        response = self.get(path, headers=headers)
        return IamApiKeysResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def get_all_applications_api_keys(
        self,
        auth_headers: dict[str, str],
        irn: str | IRN,
    ) -> Generator[ApiKey, None, None]:
        return generic_search_all(auth_headers, self.get_application_api_keys, irn)
