from typing import Any

import pytest
import responses

from iamcore.client.api_key.client import Client
from iamcore.client.api_key.dto import ApiKey, IamApiKeysResponse
from iamcore.client.base.models import PaginatedSearchFilter
from iamcore.client.exceptions import (
    IAMBedRequestException,
    IAMException,
    IAMForbiddenException,
    IAMUnauthorizedException,
)

BASE_URL = "http://localhost:8080"


class TestApiKeyClient:
    """Class-based tests for API Key Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/principals"

    def test_api_key_client_initialization(self) -> None:
        """Test API Key Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_application_api_key_success(self) -> None:
        """Test successful API key creation."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(responses.POST, expected_url, status=201)

        auth_headers = {"Authorization": "Bearer token"}

        # Should not raise an exception
        self.client.create(auth_headers, principal_id)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_get_application_api_keys_success(self) -> None:
        """Test successful API keys retrieval."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        api_keys_response: dict[str, Any] = {
            "data": [
                {
                    "apiKey": "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14",
                    "state": "active",
                    "lastUsed": "2021-10-19T17:57:31.14492667Z",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                },
                {
                    "apiKey": "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga15",
                    "state": "inactive",
                    "lastUsed": None,
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                },
            ],
            "count": 2,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=api_keys_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search(auth_headers, principal_id)

        assert isinstance(result, IamApiKeysResponse)
        assert result.count == 2
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 2

        # Verify first API key
        api_key_1 = result.data[0]
        assert isinstance(api_key_1, ApiKey)
        assert api_key_1.api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14"
        assert api_key_1.state == "active"
        assert api_key_1.last_used == "2021-10-19T17:57:31.14492667Z"

        # Verify second API key
        api_key_2 = result.data[1]
        assert isinstance(api_key_2, ApiKey)
        assert api_key_2.api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga15"
        assert api_key_2.state == "inactive"
        assert api_key_2.last_used is None

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_get_application_api_keys_with_filter(self) -> None:
        """Test API keys retrieval with search filter."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        api_keys_response: dict[str, Any] = {
            "data": [
                {
                    "apiKey": "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14",
                    "state": "active",
                    "lastUsed": "2021-10-19T17:57:31.14492667Z",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=api_keys_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = PaginatedSearchFilter(page=1, pageSize=10)

        result = self.client.search(auth_headers, principal_id, search_filter)

        assert isinstance(result, IamApiKeysResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        # Verify the request includes query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=10"

    @responses.activate
    def test_get_application_api_keys_without_filter(self) -> None:
        """Test API keys retrieval without filter parameters."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        api_keys_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=api_keys_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search(auth_headers, principal_id)

        assert isinstance(result, IamApiKeysResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_get_all_applications_api_keys_success(self) -> None:
        """Test successful retrieval of all API keys with pagination."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        # First page response
        first_page_response = {
            "data": [
                {
                    "apiKey": "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14",
                    "state": "active",
                    "lastUsed": "2021-10-19T17:57:31.14492667Z",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 1,
        }
        responses.add(responses.GET, expected_url, json=first_page_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        results = list(self.client.search_all(auth_headers, principal_id))

        assert len(results) == 1
        assert isinstance(results[0], ApiKey)
        assert results[0].api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_application_api_key_bad_request_error(self) -> None:
        """Test create_application_api_key raises IAMBedRequestException for 400 Bad Request."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid principal ID", "errors": ["Principal ID format invalid"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create(auth_headers, principal_id)

        assert excinfo.value.status_code == 400
        assert "Invalid principal ID" in str(excinfo.value)

    @responses.activate
    def test_create_application_api_key_unauthorized_error(self) -> None:
        """Test create_application_api_key raises IAMUnauthorizedException for 401 Unauthorized."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create(auth_headers, principal_id)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_application_api_key_forbidden_error(self) -> None:
        """Test create_application_api_key raises IAMForbiddenException for 403 Forbidden."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create API keys"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create(auth_headers, principal_id)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_get_application_api_keys_not_found_error(self) -> None:
        """Test get_application_api_keys raises IAMException for 404 Not Found."""
        principal_id = "nonexistent"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(responses.GET, expected_url, json={"message": "Principal not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search(auth_headers, principal_id)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_get_application_api_keys_unauthorized_error(self) -> None:
        """Test get_application_api_keys raises IAMUnauthorizedException for 401 Unauthorized."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search(auth_headers, principal_id)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_get_application_api_keys_forbidden_error(self) -> None:
        """Test get_application_api_keys raises IAMForbiddenException for 403 Forbidden."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(
            responses.GET, expected_url, json={"message": "Access denied to this principal's API keys"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search(auth_headers, principal_id)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_get_application_api_keys_server_error(self) -> None:
        """Test get_application_api_keys raises IAMException for 500 Internal Server Error."""
        principal_id = "principal123"
        expected_url = f"{self.expected_base_url}/{principal_id}/api-keys"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search(auth_headers, principal_id)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
