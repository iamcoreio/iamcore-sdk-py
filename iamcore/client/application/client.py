from __future__ import annotations

import json
from typing import TYPE_CHECKING

from iamcore.client.exceptions import (
    IAMException,
    err_chain,
    unwrap_get,
    unwrap_post,
    unwrap_put,
)
from iamcore.client.models.base import (
    SortOrder,
    generic_search_all,
)
from iamcore.client.models.client import HTTPClientWithTimeout

from .dto import Application, IamApplicationResponse, IamApplicationsResponse

if TYPE_CHECKING:
    from collections.abc import Generator

    from requests import Response

    from iamcore.client.config import BaseConfig


class Client(HTTPClientWithTimeout):
    """Client for IAM Core Application API."""

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(base_url=config.IAMCORE_URL, timeout=config.TIMEOUT)

    @err_chain(IAMException)
    def create_application(
        self,
        auth_headers: dict[str, str],
        *,
        name: str,
        display_name: str | None = None,
    ) -> Application:
        payload = {"name": name, "displayName": display_name}
        payload = {k: v for k, v in payload.items() if v}

        response = self.post("applications", data=json.dumps(payload), headers=auth_headers)
        return IamApplicationResponse(**unwrap_post(response)).data

    @err_chain(IAMException)
    def get_application(self, auth_headers: dict[str, str], *, irn: str) -> Application:
        path = f"applications/{irn!s}"
        response: Response = self.get(path, headers=auth_headers)
        return IamApplicationResponse(**unwrap_get(response)).data

    @err_chain(IAMException)
    def application_attach_policies(
        self,
        auth_headers: dict[str, str],
        *,
        application_id: str,
        policies_ids: list[str],
    ) -> None:
        path = f"applications/{application_id}/policies/attach"
        payload = {"policyIDs": policies_ids}

        response = self.post(path, data=json.dumps(payload), headers=auth_headers)
        return unwrap_put(response)

    @err_chain(IAMException)
    def search_application(
        self,
        headers: dict[str, str],
        *,
        irn: str | None = None,
        name: str | None = None,
        display_name: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> IamApplicationsResponse:
        query = {
            "irn": str(irn) if irn else None,
            "name": name,
            "displayName": display_name,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
            "sortOrder": sort_order.name if sort_order else None,
        }
        query = {k: v for k, v in query.items() if v}

        response = self.get("applications", headers=headers, params=query)
        return IamApplicationsResponse(**unwrap_get(response))

    @err_chain(IAMException)
    def search_all_applications(
        self,
        auth_headers: dict[str, str],
        *,
        irn: str | None = None,
        name: str | None = None,
        display_name: str | None = None,
        sort: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> Generator[Application, None, None]:
        kwargs = {
            "irn": irn,
            "name": name,
            "display_name": display_name,
            "sort": sort,
            "sort_order": sort_order,
        }
        kwargs = {k: v for k, v in kwargs.items() if v}
        return generic_search_all(auth_headers, self.search_application, **kwargs)
