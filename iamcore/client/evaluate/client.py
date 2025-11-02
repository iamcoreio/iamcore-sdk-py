from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Optional

from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import IamIRNsResponse, PaginatedSearchFilter, generic_search_all

if TYPE_CHECKING:
    from collections.abc import Generator

    from iamcore.irn import IRN


logger = logging.getLogger(__name__)


class Client(HTTPClientWithTimeout):
    """IAMCore evaluation client."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    def evaluate(self, auth_headers: dict[str, str], action: str, resources: list[IRN]) -> None:
        payload = {"action": action, "resources": [str(r) for r in resources if r]}
        logger.debug("Going to evaluate resources: json=%s", payload)
        self._post("evaluate", data=json.dumps(payload), headers=auth_headers)

    def evaluate_actions(self, auth_headers: dict[str, str], actions: list[str], irns: list[IRN]) -> dict[str, Any]:
        payload = {"actions": actions, "irns": [str(r) for r in irns if r]}
        logger.debug("Going to evaluate resources: json=%s", payload)
        response = self._post("evaluate/actions", data=json.dumps(payload), headers=auth_headers)
        return response.json()

    def evaluate_resources(
        self,
        auth_headers: dict[str, str],
        *,
        application: str,
        action: str,
        resource_type: str,
        search_filter: Optional[PaginatedSearchFilter] = None,
    ) -> IamIRNsResponse:
        payload = {"application": application, "action": action, "resourceType": resource_type}
        logger.debug("Going to evaluate resource type: json=%s", payload)
        response = self._post(
            "evaluate/resources",
            data=json.dumps(payload),
            headers=auth_headers,
            params=search_filter.model_dump(by_alias=True, exclude_none=True) if search_filter else None,
        )
        return IamIRNsResponse(**response.json())

    def evaluate_all_resources(
        self,
        auth_headers: dict[str, str],
        *,
        application: str,
        action: str,
        resource_type: str,
    ) -> Generator[IRN, None, None]:
        def search_func(headers: dict[str, str], search_filter: PaginatedSearchFilter) -> IamIRNsResponse:
            return self.evaluate_resources(
                headers,
                application=application,
                action=action,
                resource_type=resource_type,
                search_filter=search_filter,
            )

        return generic_search_all(auth_headers, search_func, None)
