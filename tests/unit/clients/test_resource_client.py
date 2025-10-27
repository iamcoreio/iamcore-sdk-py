import json
from typing import Any, cast

import pytest
import responses
from iamcore.irn import IRN

from iamcore.client.exceptions import (
    IAMBedRequestException,
    IAMConflictException,
    IAMException,
    IAMForbiddenException,
    IAMUnauthorizedException,
)
from iamcore.client.resource.client import Client
from iamcore.client.resource.dto import (
    CreateResource,
    IamResourcesResponse,
    Resource,
    ResourceSearchFilter,
    UpdateResource,
)

BASE_URL = "http://localhost:8080"


class TestResourceClient:
    """Class-based tests for Resource Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/"

    def test_resource_client_initialization(self) -> None:
        """Test Resource Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_resource_success(self) -> None:
        """Test successful resource creation."""
        expected_url = f"{self.expected_base_url}resources"
        resource_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "created": "2022-10-25T22:22:17.390631+03:00",
                "updated": "2022-10-25T22:22:17.390631+03:00",
                "tenantID": "4atcicnisg",
                "application": "myapp",
                "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "displayName": "Thermostat",
                "path": "/dev",
                "resourceType": "device",
                "enabled": True,
                "description": "Resource description",
                "metadata": {"temperature": "10", "city": "Kyiv"},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        }
        responses.add(responses.POST, expected_url, json=resource_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateResource(
            name="7e1edad5-7841-4d38-bdf1-bdc575b0e989",
            application="myapp",
            path="/dev",
            resourceType="device",
            displayName="Thermostat",
            tenantID="4atcicnisg",
            enabled=True,
            description="Resource description",
            metadata={"temperature": "10", "city": "Kyiv"},
            poolIDs=["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
        )

        result = self.client.create_resource(auth_headers, create_params)

        assert isinstance(result, Resource)
        assert (
            result.id
            == "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk="
        )
        assert str(result.irn) == "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert result.name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert result.display_name == "Thermostat"
        assert result.tenant_id == "4atcicnisg"
        assert result.application == "myapp"
        assert result.path == "/dev"
        assert result.resource_type == "device"
        assert result.enabled is True
        assert result.description == "Resource description"
        assert result.metadata == {"temperature": "10", "city": "Kyiv"}
        assert result.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert result.created == "2022-10-25T22:22:17.390631+03:00"
        assert result.updated == "2022-10-25T22:22:17.390631+03:00"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["name"] == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert request_data["displayName"] == "Thermostat"
        assert request_data["tenantID"] == "4atcicnisg"
        assert request_data["application"] == "myapp"
        assert request_data["path"] == "/dev"
        assert request_data["resourceType"] == "device"
        assert request_data["enabled"] is True
        assert request_data["description"] == "Resource description"
        assert request_data["metadata"] == {"temperature": "10", "city": "Kyiv"}
        assert request_data["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    @responses.activate
    def test_create_resource_minimal_params(self) -> None:
        """Test resource creation with minimal parameters."""
        expected_url = f"{self.expected_base_url}resources"
        resource_response: dict[str, Any] = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "created": "2022-10-25T22:22:17.390631+03:00",
                "updated": "2022-10-25T22:22:17.390631+03:00",
                "tenantID": "4atcicnisg",
                "application": "myapp",
                "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "displayName": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "path": "/dev",
                "resourceType": "device",
                "enabled": True,
                "description": "",
                "metadata": {},
                "poolIDs": None,
            }
        }
        responses.add(responses.POST, expected_url, json=resource_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateResource(
            name="7e1edad5-7841-4d38-bdf1-bdc575b0e989",
            application="myapp",
            path="/dev",
            resourceType="device",
        )  # Only required fields

        result = self.client.create_resource(auth_headers, create_params)

        assert isinstance(result, Resource)
        assert result.name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert result.display_name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"  # Should match the response
        assert result.pool_ids is None

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["name"] == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert request_data["application"] == "myapp"
        assert request_data["path"] == "/dev"
        assert request_data["resourceType"] == "device"
        assert "displayName" not in request_data
        assert "poolIDs" not in request_data

    @responses.activate
    def test_update_resource_success(self) -> None:
        """Test successful resource update."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.PATCH, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdateResource(
            displayName="Updated Thermostat",
            enabled=False,
            description="Updated resource description",
            metadata={"temperature": "15", "city": "Kyiv"},
            poolIDs=["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
        )

        # Should not raise an exception
        self.client.update_resource(auth_headers, resource_irn, update_params)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PATCH"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["displayName"] == "Updated Thermostat"
        assert request_data["enabled"] is False
        assert request_data["description"] == "Updated resource description"
        assert request_data["metadata"] == {"temperature": "15", "city": "Kyiv"}
        assert request_data["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    @responses.activate
    def test_update_resource_minimal_params(self) -> None:
        """Test resource update with minimal parameters."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.PATCH, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdateResource(displayName="Updated Name")  # Only one field

        # Should not raise an exception
        self.client.update_resource(auth_headers, resource_irn, update_params)

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["displayName"] == "Updated Name"
        assert "enabled" not in request_data
        assert "description" not in request_data
        assert "metadata" not in request_data
        assert "poolIDs" not in request_data

    @responses.activate
    def test_delete_resource_success(self) -> None:
        """Test successful resource deletion."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}

        # Should not raise an exception
        self.client.delete_resource(auth_headers, resource_irn)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "DELETE"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_delete_resources_success(self) -> None:
        """Test successful bulk resource deletion."""
        expected_url = f"{self.expected_base_url}resources/delete"
        responses.add(responses.POST, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        resource_irns = [
            IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/resource1"),
            IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/resource2"),
        ]

        # Should not raise an exception
        self.client.delete_resources(auth_headers, resource_irns)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert "resourceIDs" in request_data
        assert len(request_data["resourceIDs"]) == 2

    @responses.activate
    def test_search_resource_success(self) -> None:
        """Test successful resource search."""
        expected_url = f"{self.expected_base_url}resources"
        resources_response: dict[str, Any] = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                    "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                    "created": "2022-10-25T22:22:17.390631+03:00",
                    "updated": "2022-10-25T22:22:17.390631+03:00",
                    "tenantID": "4atcicnisg",
                    "application": "myapp",
                    "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                    "displayName": "Thermostat",
                    "path": "/dev",
                    "resourceType": "device",
                    "enabled": True,
                    "description": "Resource description",
                    "metadata": {"temperature": "10", "city": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=resources_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = ResourceSearchFilter(resourceType="device")

        result = self.client.search_resources(auth_headers, search_filter)

        assert isinstance(result, IamResourcesResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        resource = result.data[0]
        assert isinstance(resource, Resource)
        assert resource.name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert resource.display_name == "Thermostat"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?resourceType=device"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_resource_without_filter(self) -> None:
        """Test resource search without filter parameters."""
        expected_url = f"{self.expected_base_url}resources"
        resources_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=resources_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_resources(auth_headers)

        assert isinstance(result, IamResourcesResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_resources_success(self) -> None:
        """Test successful search of all resources with pagination."""
        expected_url = f"{self.expected_base_url}resources"
        # First page response
        first_page_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                    "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                    "created": "2022-10-25T22:22:17.390631+03:00",
                    "updated": "2022-10-25T22:22:17.390631+03:00",
                    "tenantID": "4atcicnisg",
                    "application": "myapp",
                    "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                    "displayName": "Thermostat",
                    "path": "/dev",
                    "resourceType": "device",
                    "enabled": True,
                    "description": "Resource description",
                    "metadata": {"temperature": "10", "city": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 1,
        }
        responses.add(responses.GET, expected_url, json=first_page_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        results = list(self.client.search_all_resources(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], Resource)
        assert results[0].name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_resource_bad_request_error(self) -> None:
        """Test create_resource raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid resource data", "errors": ["name is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateResource(
            name="", application="myapp", path="/dev", resourceType="device"
        )  # Invalid: empty name

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create_resource(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid resource data" in str(excinfo.value)

    @responses.activate
    def test_create_resource_unauthorized_error(self) -> None:
        """Test create_resource raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreateResource(name="test", application="myapp", path="/dev", resourceType="device")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create_resource(auth_headers, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_resource_forbidden_error(self) -> None:
        """Test create_resource raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create resources"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateResource(name="test", application="myapp", path="/dev", resourceType="device")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create_resource(auth_headers, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_resource_conflict_error(self) -> None:
        """Test create_resource raises IAMConflictException for 409 Conflict."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(
            responses.POST, expected_url, json={"message": "Resource with this name already exists"}, status=409
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateResource(
            name="existing_resource", application="myapp", path="/dev", resourceType="device"
        )

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create_resource(auth_headers, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_update_resource_not_found_error(self) -> None:
        """Test update_resource raises IAMException for 404 Not Found."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/nonexistent")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.PATCH, expected_url, json={"message": "Resource not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdateResource(displayName="Updated Name")

        with pytest.raises(IAMException) as excinfo:
            self.client.update_resource(auth_headers, resource_irn, update_params)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_update_resource_unauthorized_error(self) -> None:
        """Test update_resource raises IAMUnauthorizedException for 401 Unauthorized."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/test")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.PATCH, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        update_params = UpdateResource(displayName="Updated Name")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.update_resource(auth_headers, resource_irn, update_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_update_resource_forbidden_error(self) -> None:
        """Test update_resource raises IAMForbiddenException for 403 Forbidden."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/restricted")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(
            responses.PATCH, expected_url, json={"message": "Access denied to update this resource"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdateResource(displayName="Updated Name")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.update_resource(auth_headers, resource_irn, update_params)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_delete_resource_not_found_error(self) -> None:
        """Test delete_resource raises IAMException for 404 Not Found."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/nonexistent")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Resource not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.delete_resource(auth_headers, resource_irn)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_delete_resource_unauthorized_error(self) -> None:
        """Test delete_resource raises IAMUnauthorizedException for 401 Unauthorized."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/test")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.delete_resource(auth_headers, resource_irn)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_delete_resource_forbidden_error(self) -> None:
        """Test delete_resource raises IAMForbiddenException for 403 Forbidden."""
        resource_irn = IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/restricted")
        expected_url = f"{self.expected_base_url}resources/{resource_irn.to_base64()}"
        responses.add(
            responses.DELETE, expected_url, json={"message": "Access denied to delete this resource"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.delete_resource(auth_headers, resource_irn)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_delete_resources_bad_request_error(self) -> None:
        """Test delete_resources raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}resources/delete"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid request data", "errors": ["Request validation failed"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        resource_irns = [IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/resource1")]

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.delete_resources(auth_headers, resource_irns)

        assert excinfo.value.status_code == 400
        assert "Invalid request data" in str(excinfo.value)

    @responses.activate
    def test_delete_resources_not_found_error(self) -> None:
        """Test delete_resources raises IAMException for 404 Not Found."""
        expected_url = f"{self.expected_base_url}resources/delete"
        responses.add(responses.POST, expected_url, json={"message": "Some resources not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        resource_irns = [IRN.of("irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/nonexistent")]

        with pytest.raises(IAMException) as excinfo:
            self.client.delete_resources(auth_headers, resource_irns)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_search_resource_unauthorized_error(self) -> None:
        """Test search_resource raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search_resources(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_resource_forbidden_error(self) -> None:
        """Test search_resource raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(
            responses.GET, expected_url, json={"message": "Insufficient permissions to search resources"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search_resources(auth_headers)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_search_resource_server_error(self) -> None:
        """Test search_resource raises IAMException for 500 Internal Server Error."""
        expected_url = f"{self.expected_base_url}resources"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search_resources(auth_headers)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
