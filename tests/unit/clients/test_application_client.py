import json
from typing import Any, cast

import responses
from iamcore.irn import IRN

from iamcore.client.application.client import Client
from iamcore.client.application.dto import (
    Application,
    ApplicationSearchFilter,
    CreateApplication,
    IamApplicationsResponse,
)

BASE_URL = "http://localhost:8080"


class TestApplicationClient:
    """Class-based tests for Application Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/"

    def test_application_client_initialization(self) -> None:
        """Test Application Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_application_success(self) -> None:
        """Test successful application creation."""
        expected_url = f"{self.expected_base_url}applications"
        application_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "name": "myapp",
                "displayName": "My app name",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.POST, expected_url, json=application_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplication(name="myapp", displayName="My app name")

        result = self.client.create_application(auth_headers, create_params)

        assert isinstance(result, Application)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:::application/myapp"
        assert result.name == "myapp"
        assert result.display_name == "My app name"
        assert result.created == "2021-10-18T12:27:15.55267632Z"
        assert result.updated == "2021-10-18T12:27:15.55267632Z"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["name"] == "myapp"
        assert request_data["displayName"] == "My app name"

    @responses.activate
    def test_create_application_minimal_params(self) -> None:
        """Test application creation with minimal parameters."""
        expected_url = f"{self.expected_base_url}applications"
        application_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "name": "myapp",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.POST, expected_url, json=application_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplication(name="myapp")  # Only required field

        result = self.client.create_application(auth_headers, create_params)

        assert isinstance(result, Application)
        assert result.name == "myapp"
        assert result.display_name is None  # Optional field not provided

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["name"] == "myapp"
        assert "displayName" not in request_data

    @responses.activate
    def test_get_application_success(self) -> None:
        """Test successful application retrieval."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}applications/{application_irn!s}"
        application_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "name": "myapp",
                "displayName": "My app name",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.GET, expected_url, json=application_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.get_application(auth_headers, application_irn)

        assert isinstance(result, Application)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:::application/myapp"
        assert result.name == "myapp"
        assert result.display_name == "My app name"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_application_attach_policies_success(self) -> None:
        """Test successful policy attachment to application."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}applications/{application_irn.to_base64()}/policies/attach"
        responses.add(responses.POST, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["policy1", "policy2"]

        # Should not raise an exception
        self.client.application_attach_policies(auth_headers, application_irn, policy_ids)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["policyIDs"] == policy_ids

    @responses.activate
    def test_search_application_success(self) -> None:
        """Test successful application search."""
        expected_url = f"{self.expected_base_url}applications"
        applications_response: dict[str, Any] = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                    "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                    "name": "myapp",
                    "displayName": "My app name",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=applications_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = ApplicationSearchFilter(name="myapp")

        result = self.client.search_application(auth_headers, search_filter)

        assert isinstance(result, IamApplicationsResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        application = result.data[0]
        assert isinstance(application, Application)
        assert application.name == "myapp"
        assert application.display_name == "My app name"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?name=myapp"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_application_without_filter(self) -> None:
        """Test application search without filter parameters."""
        expected_url = f"{self.expected_base_url}applications"
        applications_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=applications_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_application(auth_headers)

        assert isinstance(result, IamApplicationsResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_applications_success(self) -> None:
        """Test successful search of all applications with pagination."""
        expected_url = f"{self.expected_base_url}applications"
        # First page response
        first_page_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                    "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                    "name": "myapp",
                    "displayName": "My app name",
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

        results = list(self.client.search_all_applications(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], Application)
        assert results[0].name == "myapp"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"
