from __future__ import annotations

from http.client import BAD_REQUEST, CONFLICT, FORBIDDEN, UNAUTHORIZED
from typing import TYPE_CHECKING, Optional

from iamcore.client.exceptions import (
    IAMBedRequestException,
    IAMConflictException,
    IAMException,
    IAMForbiddenException,
    IAMUnauthorizedException,
)

if TYPE_CHECKING:
    from requests import Response


class ResponseHandler:
    """
    A centralized handler for processing API responses and exceptions.
    """

    DEFAULT_ERROR_MAPPING: dict[int, type[IAMException]] = {
        UNAUTHORIZED: IAMUnauthorizedException,
        FORBIDDEN: IAMForbiddenException,
        BAD_REQUEST: IAMBedRequestException,
        CONFLICT: IAMConflictException,
    }

    @staticmethod
    def _handle_response(
        resp: Response,
        success_code_range: range,
        custom_mappings: Optional[dict[int, type[IAMException]]] = None,
    ) -> Response:
        """The core private handler logic."""
        # Check for success first.
        if resp.status_code in success_code_range:
            return resp

        # Combine default and custom error mappings. Custom mappings take precedence.
        mappings = ResponseHandler.DEFAULT_ERROR_MAPPING
        if custom_mappings:
            mappings = mappings | custom_mappings  # Python 3.9+ dictionary union

        # Find the appropriate exception for the error status code.
        exception_class = mappings.get(resp.status_code)

        # Raise the specific exception, or a generic one if the code is unknown.
        if exception_class:
            raise exception_class.from_response(resp)
        # Fallback for unexpected error codes
        raise IAMException.from_response(resp)

    @staticmethod
    def handle_response(
        resp: Response,
        custom_mappings: Optional[dict[int, type[IAMException]]] = None,
    ) -> Response:
        """
        Handles a response, returning its JSON body on success.
        Raises an appropriate IAMException on failure.
        """
        return ResponseHandler._handle_response(resp, range(200, 299), custom_mappings)
