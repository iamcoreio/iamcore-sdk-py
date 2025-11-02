import json
from typing import Any, cast

import pytest
import responses
from iamcore.irn import IRN

from iamcore.client.application.client import Client
from iamcore.client.application.dto import (
    Application,
    ApplicationSearchFilter,
    CreateApplication,
    IamApplicationsResponse,
)
from iamcore.client.exceptions import (
    IAMBedRequestException,
    IAMConflictException,
    IAMException,
    IAMForbiddenException,
    IAMUnauthorizedException,
)

BASE_URL = "http://localhost:8080"


class TestApplicationClient:
    """Class-based tests for Application Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/{cls.client.BASE_PATH}"

    def test_application_client_initialization(self) -> None:
        """Test Application Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_application_success(self) -> None:
        """Test successful application creation."""
        expected_url = f"{self.expected_base_url}"
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

        result = self.client.create(auth_headers, create_params)

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
        expected_url = f"{self.expected_base_url}"
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

        result = self.client.create(auth_headers, create_params)

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
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}"
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

        result = self.client.get(auth_headers, application_irn)

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
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/policies/attach"
        responses.add(responses.POST, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["policy1", "policy2"]

        # Should not raise an exception
        self.client.attach_policies(auth_headers, application_irn, policy_ids)

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
        expected_url = f"{self.expected_base_url}"
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

        result = self.client.search(auth_headers, search_filter)

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
        expected_url = f"{self.expected_base_url}"
        applications_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=applications_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search(auth_headers)

        assert isinstance(result, IamApplicationsResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_applications_success(self) -> None:
        """Test successful search of all applications with pagination."""
        expected_url = f"{self.expected_base_url}"
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

        results = list(self.client.search_all(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], Application)
        assert results[0].name == "myapp"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_application_bad_request_error(self) -> None:
        """Test create_application raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid application data", "errors": ["name is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplication(name="")  # Invalid: empty name

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid application data" in str(excinfo.value)

    @responses.activate
    def test_create_application_unauthorized_error(self) -> None:
        """Test create_application raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreateApplication(name="myapp")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create(auth_headers, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_application_forbidden_error(self) -> None:
        """Test create_application raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create applications"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplication(name="myapp")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create(auth_headers, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_application_conflict_error(self) -> None:
        """Test create_application raises IAMConflictException for 409 Conflict."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.POST, expected_url, json={"message": "Application with this name already exists"}, status=409
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplication(name="existing_app")

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create(auth_headers, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_create_application_validation_error(self) -> None:
        """Test create_application raises IAMException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Validation failed", "errors": ["Invalid application name format"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplication(name="invalid@name!")

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Validation failed" in str(excinfo.value)

    @responses.activate
    def test_get_application_not_found_error(self) -> None:
        """Test get_application raises IAMException for 404 Not Found."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/nonexistent")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}"
        responses.add(responses.GET, expected_url, json={"message": "Application not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.get(auth_headers, application_irn)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_get_application_unauthorized_error(self) -> None:
        """Test get_application raises IAMUnauthorizedException for 401 Unauthorized."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.get(auth_headers, application_irn)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_get_application_forbidden_error(self) -> None:
        """Test get_application raises IAMForbiddenException for 403 Forbidden."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/restricted")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}"
        responses.add(responses.GET, expected_url, json={"message": "Access denied to this application"}, status=403)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.get(auth_headers, application_irn)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_application_attach_policies_bad_request_error(self) -> None:
        """Test application_attach_policies raises IAMBedRequestException for 400 Bad Request."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/policies/attach"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid policy IDs provided", "errors": ["Policy ID format invalid"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["invalid@policy@id"]

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.attach_policies(auth_headers, application_irn, policy_ids)

        assert excinfo.value.status_code == 400
        assert "Invalid policy IDs" in str(excinfo.value)

    @responses.activate
    def test_application_attach_policies_not_found_error(self) -> None:
        """Test application_attach_policies raises IAMException for 404 Not Found."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/nonexistent")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/policies/attach"
        responses.add(responses.POST, expected_url, json={"message": "Application not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["policy1", "policy2"]

        with pytest.raises(IAMException) as excinfo:
            self.client.attach_policies(auth_headers, application_irn, policy_ids)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_search_application_unauthorized_error(self) -> None:
        """Test search_application raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_application_forbidden_error(self) -> None:
        """Test search_application raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.GET, expected_url, json={"message": "Insufficient permissions to search applications"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search(auth_headers)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_search_application_server_error(self) -> None:
        """Test search_application raises IAMException for 500 Internal Server Error."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search(auth_headers)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
