from __future__ import annotations

import json
from typing import TYPE_CHECKING, Optional

from iamcore.irn import IRN

from iamcore.client.base.client import HTTPClientWithTimeout, append_path_to_url
from iamcore.client.base.models import generic_search_all
from iamcore.client.exceptions import IAMException, err_chain

from .dto import (
    Application,
    ApplicationSearchFilter,
    CreateApplication,
    IamApplicationResponse,
    IamApplicationsResponse,
)

if TYPE_CHECKING:
    from collections.abc import Generator


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Application API."""

    BASE_PATH = "applications"

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.base_url = append_path_to_url(self.base_url, self.BASE_PATH)

    @err_chain(IAMException)
    def create(self, auth_headers: dict[str, str], params: CreateApplication) -> str:
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        created_response = self._post(data=payload, headers=auth_headers)
        location = created_response.headers.get("Location")
        if not location:
            msg = "Location header is missing"
            raise IAMException(msg)

        return location.split("/")[-1]

    @err_chain(IAMException)
    def get(self, auth_headers: dict[str, str], irn: IRN) -> Application:
        response = self._get(irn.to_base64(), headers=auth_headers)
        return IamApplicationResponse(**response.json()).data

    @err_chain(IAMException)
    def policies_attach(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        policies_ids: list[str],
    ) -> None:
        path = f"{application_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        self._post(path, data=json.dumps(payload), headers=auth_headers)

    @err_chain(IAMException)
    def search(
        self,
        headers: dict[str, str],
        application_filter: Optional[ApplicationSearchFilter] = None,
    ) -> IamApplicationsResponse:
        query = application_filter.model_dump(by_alias=True, exclude_none=True) if application_filter else None
        response = self._get(headers=headers, params=query)
        return IamApplicationsResponse(**response.json())

    @err_chain(IAMException)
    def search_all(
        self,
        auth_headers: dict[str, str],
        application_filter: Optional[ApplicationSearchFilter] = None,
    ) -> Generator[Application, None, None]:
        return generic_search_all(auth_headers, self.search, application_filter)
