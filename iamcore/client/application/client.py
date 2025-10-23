from __future__ import annotations

import json
from typing import TYPE_CHECKING, Optional

from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import (
    generic_search_all,
)
from iamcore.client.exceptions import (
    IAMException,
    err_chain,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)

from .dto import (
    Application,
    ApplicationSearchFilter,
    CreateApplication,
    IamApplicationResponse,
    IamApplicationsResponse,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN
    from requests import Response


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Application API."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    @err_chain(IAMException)
    def create_application(
        self,
        auth_headers: dict[str, str],
        params: CreateApplication,
    ) -> Application:
        payload = params.model_dump_json(by_alias=True, exclude_none=True)
        response = self.post("applications", data=payload, headers=auth_headers)
        return IamApplicationResponse(**unwrap_post(response)).data

    @err_chain(IAMException)
    def get_application(self, auth_headers: dict[str, str], irn: IRN) -> Application:
        path = f"applications/{irn!s}"
        response: Response = self.get(path, headers=auth_headers)
        return IamApplicationResponse(**unwrap_get(response)).data

    @err_chain(IAMException)
    def application_attach_policies(
        self,
        auth_headers: dict[str, str],
        application_irn: IRN,
        policies_ids: list[str],
    ) -> None:
        path = f"applications/{application_irn.to_base64()}/policies/attach"
        payload = {"policyIDs": policies_ids}
        response = self.post(path, data=json.dumps(payload), headers=auth_headers)
        return unwrap_put(response)

    @err_chain(IAMException)
    def search_application(
        self,
        headers: dict[str, str],
        application_filter: Optional[ApplicationSearchFilter] = None,
    ) -> IamApplicationsResponse:
        query = application_filter.model_dump(by_alias=True, exclude_none=True) if application_filter else None
        response = self.get("applications", headers=headers, params=query)
        return IamApplicationsResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_applications(
        self,
        auth_headers: dict[str, str],
        application_filter: Optional[ApplicationSearchFilter] = None,
    ) -> Generator[Application, None, None]:
        return generic_search_all(auth_headers, self.search_application, application_filter)
