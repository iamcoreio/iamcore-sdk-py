import json
from typing import Any, cast

import pytest
import responses
from iamcore.irn import IRN

from iamcore.client.application_resource_type.client import Client
from iamcore.client.application_resource_type.dto import (
    ApplicationResourceType,
    CreateApplicationResourceType,
    IamApplicationResourceTypesResponse,
)
from iamcore.client.base.models import PaginatedSearchFilter
from iamcore.client.exceptions import (
    IAMBedRequestException,
    IAMConflictException,
    IAMException,
    IAMForbiddenException,
    IAMUnauthorizedException,
)

BASE_URL = "http://localhost:8080"


class TestApplicationResourceTypeClient:
    """Class-based tests for Application Resource Type Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/{cls.client.BASE_PATH}"

    def test_application_resource_type_client_initialization(self) -> None:
        """Test Application Resource Type Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_resource_type_success(self) -> None:
        """Test successful resource type creation."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        resource_type_response: dict[str, Any] = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                "type": "document",
                "description": "Representation of the 'document' resource type",
                "actionPrefix": "document",
                "operations": ["sign", "export"],
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.POST, expected_url, json=resource_type_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplicationResourceType(
            type="document",
            description="Representation of the 'document' resource type",
            actionPrefix="document",
            operations=["sign", "export"],
        )

        result = self.client.create_resource_type(auth_headers, application_irn, create_params)

        assert isinstance(result, ApplicationResourceType)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50"
        assert str(result.irn) == "irn:rc73dbh7q0:myapp:::resource-type/document"
        assert result.type == "document"
        assert result.description == "Representation of the 'document' resource type"
        assert result.action_prefix == "document"
        assert result.operations == ["sign", "export"]

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["type"] == "document"
        assert request_data["description"] == "Representation of the 'document' resource type"
        assert request_data["actionPrefix"] == "document"
        assert request_data["operations"] == ["sign", "export"]

    @responses.activate
    def test_create_resource_type_minimal_params(self) -> None:
        """Test resource type creation with minimal parameters."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        resource_type_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                "type": "document",
                "operations": [],
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.POST, expected_url, json=resource_type_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplicationResourceType(type="document")  # Only required field

        result = self.client.create_resource_type(auth_headers, application_irn, create_params)

        assert isinstance(result, ApplicationResourceType)
        assert result.type == "document"
        assert result.description is None  # Optional field not provided
        assert result.action_prefix is None  # Optional field not provided
        assert result.operations == []  # Optional field not provided

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["type"] == "document"
        assert "description" not in request_data
        assert "actionPrefix" not in request_data
        assert "operations" not in request_data

    @responses.activate
    def test_get_resource_type_success(self) -> None:
        """Test successful resource type retrieval."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        type_irn = IRN.of("irn:rc73dbh7q0:myapp:::resource-type/document")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types/{type_irn.to_base64()}"
        resource_type_response: dict[str, Any] = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                "type": "document",
                "description": "Representation of the 'document' resource type",
                "actionPrefix": "document",
                "operations": ["sign", "export"],
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.GET, expected_url, json=resource_type_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.get_resource_type(auth_headers, application_irn, type_irn)

        assert isinstance(result, ApplicationResourceType)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50"
        assert str(result.irn) == "irn:rc73dbh7q0:myapp:::resource-type/document"
        assert result.type == "document"
        assert result.description == "Representation of the 'document' resource type"
        assert result.action_prefix == "document"
        assert result.operations == ["sign", "export"]

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_application_resource_types_success(self) -> None:
        """Test successful application resource types search."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        resource_types_response: dict[str, Any] = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                    "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                    "type": "document",
                    "description": "Representation of the 'document' resource type",
                    "actionPrefix": "document",
                    "operations": ["sign", "export"],
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=resource_types_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_application_resource_types(auth_headers, application_irn)

        assert isinstance(result, IamApplicationResourceTypesResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        resource_type = result.data[0]
        assert isinstance(resource_type, ApplicationResourceType)
        assert resource_type.type == "document"
        assert resource_type.description == "Representation of the 'document' resource type"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_application_resource_types_with_filter(self) -> None:
        """Test application resource types search with pagination filter."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        resource_types_response: dict[str, Any] = {"data": [], "count": 0, "page": 2, "pageSize": 5}
        responses.add(responses.GET, expected_url, json=resource_types_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = PaginatedSearchFilter(page=2, pageSize=5)

        result = self.client.search_application_resource_types(auth_headers, application_irn, search_filter)

        assert isinstance(result, IamApplicationResourceTypesResponse)
        assert result.count == 0
        assert result.page == 2
        assert result.page_size == 5
        assert len(result.data) == 0

        # Verify the request includes query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == f"{expected_url}?page=2&pageSize=5"

    @responses.activate
    def test_search_all_application_resource_types_success(self) -> None:
        """Test successful search of all application resource types with pagination."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        # First page response
        first_page_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                    "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                    "type": "document",
                    "description": "Representation of the 'document' resource type",
                    "actionPrefix": "document",
                    "operations": ["sign", "export"],
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

        results = list(self.client.search_all_application_resource_types(auth_headers, application_irn))

        assert len(results) == 1
        assert isinstance(results[0], ApplicationResourceType)
        assert results[0].type == "document"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_resource_type_bad_request_error(self) -> None:
        """Test create_resource_type raises IAMBedRequestException for 400 Bad Request."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid resource type data", "errors": ["type is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplicationResourceType(type="")  # Invalid: empty type

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create_resource_type(auth_headers, application_irn, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid resource type data" in str(excinfo.value)

    @responses.activate
    def test_create_resource_type_unauthorized_error(self) -> None:
        """Test create_resource_type raises IAMUnauthorizedException for 401 Unauthorized."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreateApplicationResourceType(type="document")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create_resource_type(auth_headers, application_irn, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_resource_type_forbidden_error(self) -> None:
        """Test create_resource_type raises IAMForbiddenException for 403 Forbidden."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create resource types"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplicationResourceType(type="document")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create_resource_type(auth_headers, application_irn, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_resource_type_conflict_error(self) -> None:
        """Test create_resource_type raises IAMConflictException for 409 Conflict."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(
            responses.POST, expected_url, json={"message": "Resource type with this name already exists"}, status=409
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateApplicationResourceType(type="existing_type")

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create_resource_type(auth_headers, application_irn, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_get_resource_type_not_found_error(self) -> None:
        """Test get_resource_type raises IAMException for 404 Not Found."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        type_irn = IRN.of("irn:rc73dbh7q0:myapp:::resource-type/nonexistent")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types/{type_irn.to_base64()}"
        responses.add(responses.GET, expected_url, json={"message": "Resource type not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.get_resource_type(auth_headers, application_irn, type_irn)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_get_resource_type_unauthorized_error(self) -> None:
        """Test get_resource_type raises IAMUnauthorizedException for 401 Unauthorized."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        type_irn = IRN.of("irn:rc73dbh7q0:myapp:::resource-type/document")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types/{type_irn.to_base64()}"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.get_resource_type(auth_headers, application_irn, type_irn)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_get_resource_type_forbidden_error(self) -> None:
        """Test get_resource_type raises IAMForbiddenException for 403 Forbidden."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        type_irn = IRN.of("irn:rc73dbh7q0:myapp:::resource-type/restricted")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types/{type_irn.to_base64()}"
        responses.add(responses.GET, expected_url, json={"message": "Access denied to this resource type"}, status=403)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.get_resource_type(auth_headers, application_irn, type_irn)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_search_application_resource_types_unauthorized_error(self) -> None:
        """Test search_application_resource_types raises IAMUnauthorizedException for 401 Unauthorized."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search_application_resource_types(auth_headers, application_irn)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_application_resource_types_forbidden_error(self) -> None:
        """Test search_application_resource_types raises IAMForbiddenException for 403 Forbidden."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(
            responses.GET,
            expected_url,
            json={"message": "Insufficient permissions to search resource types"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search_application_resource_types(auth_headers, application_irn)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_search_application_resource_types_server_error(self) -> None:
        """Test search_application_resource_types raises IAMException for 500 Internal Server Error."""
        application_irn = IRN.of("irn:rc73dbh7q0:iamcore:::application/myapp")
        expected_url = f"{self.expected_base_url}/{application_irn.to_base64()}/resource-types"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search_application_resource_types(auth_headers, application_irn)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
