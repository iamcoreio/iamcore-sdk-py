from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Callable, Optional

from iamcore.irn import IRN

from iamcore.client.base.client import HTTPClientWithTimeout
from iamcore.client.base.models import IamIRNsResponse, PaginatedSearchFilter, generic_search_all
from iamcore.client.exceptions import IAMException

if TYPE_CHECKING:
    from collections.abc import Generator


logger = logging.getLogger(__name__)


class Client(HTTPClientWithTimeout):
    """IAMCore evaluation client."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    def authorize(
        self,
        auth_headers: dict[str, str],
        *,
        principal_irn: IRN,
        account_id: str,
        application: str,
        tenant_id: str,
        resource_type: str,
        resource_path: str,
        action: str,
        resource_ids: Optional[list[str]] = None,
    ) -> list[IRN]:
        if not action:
            msg = "Action must be defined"
            raise IAMException(msg)

        tenant_id = tenant_id or principal_irn.tenant_id
        account_id = account_id or principal_irn.account_id
        if resource_ids:
            resources_irn_list = [
                IRN.create(
                    account_id=account_id,
                    application=application,
                    tenant_id=tenant_id,
                    resource_type=resource_type,
                    resource_path=resource_path,
                    resource_id=resource_id,
                )
                for resource_id in resource_ids
            ]
            logger.debug(
                "Going to evaluate %s %s %s",
                auth_headers,
                action,
                resources_irn_list,
            )
            self.evaluate(auth_headers, action, resources_irn_list)
            return resources_irn_list
        logger.debug("Going to evaluate by type")
        return list(
            self.evaluate_all_resources(
                auth_headers,
                application=application,
                action=action,
                resource_type=resource_type,
            )
        )

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
