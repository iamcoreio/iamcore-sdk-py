from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests
from iamcore.irn import IRN
from requests import Response

from iamcore.client.common import (
    IamEntitiesResponse,
    IamEntityResponse,
    SortOrder,
    generic_search_all,
)
from iamcore.client.config import config
from iamcore.client.exceptions import (
    IAMException,
    IAMPolicyException,
    IAMUnauthorizedException,
    err_chain,
    unwrap_delete,
    unwrap_get,
    unwrap_post,
)

from .dto import CreatePolicyRequest, Policy

if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger(__name__)


@err_chain(IAMPolicyException)
def create_policy(auth_headers: dict[str, str], payload: CreatePolicyRequest) -> Policy:
    url = config.IAMCORE_URL + "/api/v1/policies"
    payload_dict = payload.model_dump(by_alias=True, exclude_none=True)

    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "POST",
        url,
        json=payload_dict,
        headers=headers,
        timeout=config.TIMEOUT,
    )
    return IamEntityResponse(Policy, **unwrap_post(response)).data


@err_chain(IAMPolicyException)
def delete_policy(auth_headers: dict[str, str], policy_id: str) -> None:
    if not auth_headers:
        msg = "Missing authorization headers"
        raise IAMUnauthorizedException(msg)
    if not policy_id:
        msg = "Missing resource_id"
        raise IAMPolicyException(msg)

    url = config.IAMCORE_URL + "/api/v1/policies/" + IRN.of(policy_id).to_base64()
    headers = {"Content-Type": "application/json", **auth_headers}
    response: Response = requests.request(
        "DELETE",
        url,
        data="",
        headers=headers,
        timeout=config.TIMEOUT,
    )
    unwrap_delete(response)


@err_chain(IAMPolicyException)
def search_policy(
    headers: dict[str, str],
    *,
    irn: str | None = None,
    name: str | None = None,
    description: str | None = None,
    account_id: str | None = None,
    application: str | None = None,
    tenant_id: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> IamEntitiesResponse[Policy]:
    url = config.IAMCORE_URL + "/api/v1/policies"
    if not irn and account_id and tenant_id:
        application = application if application else "iamcore"
        irn = f"irn:{account_id}:{application}:{tenant_id}"

    querystring = {
        "irn": irn,
        "name": name,
        "description": description,
        "page": page,
        "pageSize": page_size,
        "sort": sort,
        "sortOrder": sort_order.name if sort_order else None,
    }
    querystring = {k: v for k, v in querystring.items() if v}

    response = requests.request(
        "GET",
        url,
        data="",
        headers=headers,
        params=querystring,
        timeout=config.TIMEOUT,
    )
    return IamEntitiesResponse(Policy, **unwrap_get(response))


@err_chain(IAMException)
def search_all_policies(
    auth_headers: dict[str, str],
    *,
    irn: str | None = None,
    name: str | None = None,
    description: str | None = None,
    account_id: str | None = None,
    application: str | None = None,
    tenant_id: str | None = None,
    sort: str | None = None,
    sort_order: SortOrder | None = None,
) -> Generator[Policy, None, None]:
    kwargs = {
        "irn": irn,
        "name": name,
        "description": description,
        "account_id": account_id,
        "application": application,
        "tenant_id": tenant_id,
        "sort": sort,
        "sort_order": sort_order,
    }
    kwargs = {k: v for k, v in kwargs.items() if v}
    return generic_search_all(auth_headers, search_policy, **kwargs)
