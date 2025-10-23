import json

import pytest
import responses

from iamcore.client.base.client import APIVersion, HTTPClientWithTimeout, HTTPMethod
from iamcore.client.exceptions import IAMUnauthorizedException

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
            self.client.request(HTTPMethod.GET, "/test")

    @responses.activate
    def test_http_client_request_adds_content_type_header(self) -> None:
        """Test that request method adds Content-Type header if not present."""
        expected_url = f"{self.expected_base_url}test"
        responses.add(responses.GET, expected_url, json={"message": "success"}, status=200)

        headers = {"Authorization": "Bearer token"}
        self.client.request(HTTPMethod.GET, "/test", headers=headers)

        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_http_client_request_preserves_existing_content_type_header(self) -> None:
        """Test that request method preserves existing Content-Type header."""
        expected_url = f"{self.expected_base_url}test"
        responses.add(responses.GET, expected_url, json={"message": "success"}, status=200)

        headers = {"Authorization": "Bearer token", "Content-Type": "application/xml"}
        self.client.request(HTTPMethod.GET, "/test", headers=headers)

        assert responses.calls[0].request.headers["Content-Type"] == "application/xml"

    @responses.activate
    def test_http_client_get_request(self) -> None:
        """Test GET request method."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(responses.GET, expected_url, json={"users": []}, status=200)

        headers = {"Authorization": "Bearer token"}
        response = self.client.get("/users", headers=headers)

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
        response = self.client.post("/users", headers=headers, data=data)

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
        response = self.client.put("/users/123", headers=headers, data=data)

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
        response = self.client.patch("/users/123", headers=headers, data=data)

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
        response = self.client.delete("/users/123", headers=headers)

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
        response = self.client.get("/search", headers=headers, params=params)

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
        response = client.get("/long_request", headers=headers)

        assert response.status_code == 200
