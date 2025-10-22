from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.config import config
from iamcore.client.exceptions import IAMException, err_chain, unwrap_get
from iamcore.client.models.base import generic_search_all

from .dto import ApiKey, IamApiKeyResponse, IamApiKeysResponse

if TYPE_CHECKING:
    from collections.abc import Generator


@err_chain(IAMException)
def create_application_api_key(
    auth_headers: dict[str, str],
    principal_id: str,
) -> IamApiKeyResponse:
    url = config.IAMCORE_URL + "/api/v1/principals/" + principal_id + "/api-keys"
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request("POST", url, headers=headers, timeout=config.TIMEOUT)
    return IamApiKeyResponse(**unwrap_get(response))


@err_chain(IAMException)
def get_application_api_keys(
    headers: dict[str, str],
    irn: str | IRN,
    page: int = 1,
) -> IamApiKeysResponse:
    irn = IRN.of(irn) if isinstance(irn, str) else irn

    url = f"{config.IAMCORE_URL}/api/v1/principals/{irn.to_base64()}/api-keys?page={page}"
    response: Response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamApiKeysResponse(**unwrap_get(response))


@err_chain(IAMException)
def get_all_applications_api_keys(
    auth_headers: dict[str, str],
    irn: str | IRN,
) -> Generator[ApiKey, None, None]:
    return generic_search_all(auth_headers, get_application_api_keys, irn)
