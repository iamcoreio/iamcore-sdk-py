import json

import pytest
import responses

from iamcore.client.base.client import APIVersion, HTTPClientWithTimeout, HTTPMethod
from iamcore.client.exceptions import (
    IAMBedRequestException,
    IAMConflictException,
    IAMException,
    IAMForbiddenException,
    IAMUnauthorizedException,
)

BASE_URL = "http://localhost:8080"


class TestHTTPClient:
    """Class-based tests for HTTPClientWithTimeout."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = HTTPClientWithTimeout(base_url=BASE_URL, api_version=APIVersion.V1)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/"

    def test_http_client_initialization(self) -> None:
        """Test HTTPClientWithTimeout initialization."""
        client = HTTPClientWithTimeout(base_url=BASE_URL, timeout=60, api_version=APIVersion.V1)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    def test_http_client_initialization_without_trailing_slash(self) -> None:
        """Test HTTPClientWithTimeout initialization when base_url has no trailing slash."""
        client = HTTPClientWithTimeout(base_url="http://localhost:8080", api_version=APIVersion.V1)
        assert client.base_url == self.expected_base_url

    def test_http_client_request_missing_headers_raises_exception(self) -> None:
        """Test that request method raises IAMUnauthorizedException if headers are missing."""
        with pytest.raises(IAMUnauthorizedException, match="Missing authorization headers"):
            self.client._request(HTTPMethod.GET, "/test")

    @responses.activate
    def test_http_client_request_adds_content_type_header(self) -> None:
        """Test that request method adds Content-Type header if not present."""
        expected_url = f"{self.expected_base_url}test"
        responses.add(responses.GET, expected_url, json={"message": "success"}, status=200)

        headers = {"Authorization": "Bearer token"}
        self.client._request(HTTPMethod.GET, "/test", headers=headers)

        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_http_client_request_preserves_existing_content_type_header(self) -> None:
        """Test that request method preserves existing Content-Type header."""
        expected_url = f"{self.expected_base_url}test"
        responses.add(responses.GET, expected_url, json={"message": "success"}, status=200)

        headers = {"Authorization": "Bearer token", "Content-Type": "application/xml"}
        self.client._request(HTTPMethod.GET, "/test", headers=headers)

        assert responses.calls[0].request.headers["Content-Type"] == "application/xml"

    @responses.activate
    def test_http_client_get_request(self) -> None:
        """Test GET request method."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(responses.GET, expected_url, json={"users": []}, status=200)

        headers = {"Authorization": "Bearer token"}
        response = self.client._get("/users", headers=headers)

        assert response.status_code == 200
        assert response.json() == {"users": []}
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_http_client_post_request(self) -> None:
        """Test POST request method."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(responses.POST, expected_url, json={"id": "123"}, status=201)

        headers = {"Authorization": "Bearer token"}
        data = json.dumps({"name": "test"})
        response = self.client._post("/users", headers=headers, data=data)

        assert response.status_code == 201
        assert response.json() == {"id": "123"}
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.body == data

    @responses.activate
    def test_http_client_put_request(self) -> None:
        """Test PUT request method."""
        expected_url = f"{self.expected_base_url}users/123"
        responses.add(responses.PUT, expected_url, json={"message": "updated"}, status=200)

        headers = {"Authorization": "Bearer token"}
        data = json.dumps({"name": "updated_test"})
        response = self.client._put("/users/123", headers=headers, data=data)

        assert response.status_code == 200
        assert response.json() == {"message": "updated"}
        assert responses.calls[0].request.method == "PUT"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.body == data

    @responses.activate
    def test_http_client_patch_request(self) -> None:
        """Test PATCH request method."""
        expected_url = f"{self.expected_base_url}users/123"
        responses.add(responses.PATCH, expected_url, json={"message": "patched"}, status=200)

        headers = {"Authorization": "Bearer token"}
        data = json.dumps({"name": "patched_test"})
        response = self.client._patch("/users/123", headers=headers, data=data)

        assert response.status_code == 200
        assert response.json() == {"message": "patched"}
        assert responses.calls[0].request.method == "PATCH"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.body == data

    @responses.activate
    def test_http_client_delete_request(self) -> None:
        """Test DELETE request method."""
        expected_url = f"{self.expected_base_url}users/123"
        responses.add(responses.DELETE, expected_url, status=204)

        headers = {"Authorization": "Bearer token"}
        response = self.client._delete("/users/123", headers=headers)

        assert response.status_code == 204
        assert responses.calls[0].request.method == "DELETE"
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_http_client_request_with_params(self) -> None:
        """Test request method with query parameters."""
        expected_url = f"{self.expected_base_url}search?query=test&limit=10"
        responses.add(responses.GET, expected_url, json={"results": []}, status=200)

        headers = {"Authorization": "Bearer token"}
        params = {"query": "test", "limit": 10}
        response = self.client._get("/search", headers=headers, params=params)

        assert response.status_code == 200
        assert response.json() == {"results": []}
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_http_client_request_timeout(self) -> None:
        """Test request method with timeout configuration."""
        client = HTTPClientWithTimeout(base_url=BASE_URL, timeout=1, api_version=APIVersion.V1)
        expected_url = f"{self.expected_base_url}long_request"
        responses.add(responses.GET, expected_url, json={"message": "success"}, status=200)

        headers = {"Authorization": "Bearer token"}
        response = client._get("/long_request", headers=headers)

        assert response.status_code == 200

    @responses.activate
    def test_http_client_request_raises_bad_request_exception_for_400_status(self) -> None:
        """Test that request method raises IAMBedRequestException for 400 Bad Request status."""
        expected_url = f"{self.expected_base_url}bad_request"
        responses.add(responses.POST, expected_url, json={"message": "Bad request error"}, status=400)

        headers = {"Authorization": "Bearer token"}
        data = json.dumps({"invalid": "data"})

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client._post("/bad_request", headers=headers, data=data)

        assert excinfo.value.status_code == 400
        assert "Bad request error" in str(excinfo.value)

    @responses.activate
    def test_http_client_request_raises_unauthorized_exception_for_401_status(self) -> None:
        """Test that request method raises IAMUnauthorizedException for 401 Unauthorized status."""
        expected_url = f"{self.expected_base_url}unauthorized"
        responses.add(responses.GET, expected_url, json={"message": "Unauthorized access"}, status=401)

        headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client._get("/unauthorized", headers=headers)

        assert excinfo.value.status_code == 401
        assert "Unauthorized access" in str(excinfo.value)

    @responses.activate
    def test_http_client_request_raises_forbidden_exception_for_403_status(self) -> None:
        """Test that request method raises IAMForbiddenException for 403 Forbidden status."""
        expected_url = f"{self.expected_base_url}forbidden"
        responses.add(responses.GET, expected_url, json={"message": "Access forbidden"}, status=403)

        headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client._get("/forbidden", headers=headers)

        assert excinfo.value.status_code == 403
        assert "Access forbidden" in str(excinfo.value)

    @responses.activate
    def test_http_client_request_raises_conflict_exception_for_409_status(self) -> None:
        """Test that request method raises IAMConflictException for 409 Conflict status."""
        expected_url = f"{self.expected_base_url}conflict"
        responses.add(responses.POST, expected_url, json={"message": "Resource already exists"}, status=409)

        headers = {"Authorization": "Bearer token"}
        data = json.dumps({"name": "duplicate"})

        with pytest.raises(IAMConflictException) as excinfo:
            self.client._post("/conflict", headers=headers, data=data)

        assert excinfo.value.status_code == 409
        assert "Resource already exists" in str(excinfo.value)

    @responses.activate
    def test_http_client_request_raises_generic_exception_for_404_status(self) -> None:
        """Test that request method raises generic IAMException for 404 Not Found status."""
        expected_url = f"{self.expected_base_url}not_found"
        responses.add(responses.GET, expected_url, json={"message": "Resource not found"}, status=404)

        headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client._get("/not_found", headers=headers)

        assert excinfo.value.status_code == 404
        assert "Resource not found" in str(excinfo.value)

    @responses.activate
    def test_http_client_request_raises_generic_exception_for_422_status(self) -> None:
        """Test that request method raises generic IAMException for 422 Unprocessable Entity status."""
        expected_url = f"{self.expected_base_url}unprocessable"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Validation failed", "errors": ["Invalid format"]},
            status=422,
        )

        headers = {"Authorization": "Bearer token"}
        data = json.dumps({"invalid_field": "value"})

        with pytest.raises(IAMException) as excinfo:
            self.client._post("/unprocessable", headers=headers, data=data)

        assert excinfo.value.status_code == 422
        assert "Validation failed" in str(excinfo.value)

    @responses.activate
    def test_http_client_request_raises_generic_exception_for_unmapped_4xx_status(self) -> None:
        """Test that request method raises generic IAMException for unmapped 4xx status codes."""
        expected_url = f"{self.expected_base_url}teapot"
        responses.add(responses.GET, expected_url, json={"message": "I'm a teapot"}, status=418)

        headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client._get("/teapot", headers=headers)

        assert excinfo.value.status_code == 418
        assert "I'm a teapot" in str(excinfo.value)
