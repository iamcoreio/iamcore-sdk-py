from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from iamcore.irn import IRN

from iamcore.client.exceptions import (
    EVALUATE_MAPPING,
    IAMException,
    unwrap_return_empty,
    unwrap_return_json,
)
from iamcore.client.models.base import IamIRNsResponse, generic_search_all
from iamcore.client.models.client import HTTPClientWithTimeout

if TYPE_CHECKING:
    from collections.abc import Generator


logger = logging.getLogger(__name__)


class Client(HTTPClientWithTimeout):
    """IAMCore evaluation client."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)

    def authorize(
        self,
        authorization_headers: dict[str, str],
        principal_irn: IRN,
        account_id: str,
        application: str,
        tenant_id: str,
        resource_type: str,
        resource_path: str,
        action: str,
        resource_ids: list[str] | None = None,
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
                authorization_headers,
                action,
                resources_irn_list,
            )
            self.evaluate(authorization_headers, action, resources_irn_list)
            return resources_irn_list
        logger.debug("Going to evaluate by type")
        return list(
            self.evaluate_all_resources(authorization_headers, application, action, resource_type)
        )

    def evaluate(self, auth_headers: dict[str, str], action: str, resources: list[IRN]) -> None:
        payload = {"action": action, "resources": [str(r) for r in resources if r]}
        logger.debug("Going to evaluate resources: json=%s", payload)
        response = self.post("evaluate", data=json.dumps(payload), headers=auth_headers)
        return unwrap_return_empty(response, EVALUATE_MAPPING)

    def evaluate_actions(
        self,
        auth_headers: dict[str, str],
        actions: list[str],
        irns: list[IRN],
    ) -> dict[str, Any]:
        payload = {"actions": actions, "irns": [str(r) for r in irns if r]}
        logger.debug("Going to evaluate resources: json=%s", payload)
        response = self.post("evaluate/actions", data=json.dumps(payload), headers=auth_headers)
        return unwrap_return_json(response, EVALUATE_MAPPING)

    def evaluate_resources(
        self,
        auth_headers: dict[str, str],
        application: str,
        action: str,
        resource_type: str,
        page: int = 1,
        page_size: int = 100,
    ) -> IamIRNsResponse:
        payload = {"application": application, "action": action, "resourceType": resource_type}
        logger.debug("Going to evaluate resource type: json=%s", payload)
        response = self.post(
            "evaluate/resources",
            data=json.dumps(payload),
            headers=auth_headers,
            params={"page": page, "pageSize": page_size},
        )
        return IamIRNsResponse(**unwrap_return_json(response, EVALUATE_MAPPING))

    def evaluate_all_resources(
        self,
        auth_headers: dict[str, str],
        *args: Any,
        **kwargs: Any,
    ) -> Generator[IRN, None, None]:
        return generic_search_all(auth_headers, self.evaluate_resources, *args, **kwargs)
