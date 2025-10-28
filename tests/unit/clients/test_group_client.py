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
from iamcore.client.group.client import Client
from iamcore.client.group.dto import (
    CreateGroup,
    Group,
    GroupSearchFilter,
    IamGroupsResponse,
)

BASE_URL = "http://localhost:8080"


class TestGroupClient:
    """Class-based tests for Group Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/groups"

    def test_group_client_initialization(self) -> None:
        """Test Group Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_group_success(self) -> None:
        """Test successful group creation."""
        expected_url = f"{self.expected_base_url}"
        group_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                "tenantID": "4atcicnisg",
                "name": "java",
                "displayName": "Java",
                "path": "/dev",
                "metadata": {"location": "Kyiv"},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                "created": "2021-10-18T11:08:09.4919Z",
                "updated": "2021-10-18T11:08:09.4919Z",
            }
        }
        responses.add(responses.POST, expected_url, json=group_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateGroup(
            name="java",
            displayName="Java",
            parentID="aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXY=",
            tenantID="4atcicnisg",
            poolIDs=["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
        )

        result = self.client.create_group(auth_headers, create_params)

        assert isinstance(result, Group)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ=="
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java"
        assert result.name == "java"
        assert result.display_name == "Java"
        assert result.tenant_id == "4atcicnisg"
        assert result.path == "/dev"
        assert result.metadata == {"location": "Kyiv"}
        assert result.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert result.created == "2021-10-18T11:08:09.4919Z"
        assert result.updated == "2021-10-18T11:08:09.4919Z"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["name"] == "java"
        assert request_data["displayName"] == "Java"
        assert request_data["parentID"] == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXY="
        assert request_data["tenantID"] == "4atcicnisg"
        assert request_data["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    @responses.activate
    def test_create_group_minimal_params(self) -> None:
        """Test group creation with minimal parameters."""
        expected_url = f"{self.expected_base_url}"
        group_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                "tenantID": "4atcicnisg",
                "name": "java",
                "displayName": "java",
                "path": "/dev",
                "metadata": None,
                "poolIDs": None,
                "created": "2021-10-18T11:08:09.4919Z",
                "updated": "2021-10-18T11:08:09.4919Z",
            }
        }
        responses.add(responses.POST, expected_url, json=group_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateGroup(name="java")  # Only required field

        result = self.client.create_group(auth_headers, create_params)

        assert isinstance(result, Group)
        assert result.name == "java"
        assert result.display_name == "java"  # Should match the response
        assert result.pool_ids is None

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["name"] == "java"
        assert "displayName" not in request_data
        assert "poolIDs" not in request_data

    @responses.activate
    def test_delete_group_success(self) -> None:
        """Test successful group deletion."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}

        # Should not raise an exception
        self.client.delete_group(auth_headers, group_irn)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "DELETE"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_group_attach_policies_success(self) -> None:
        """Test successful policy attachment to group."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}/policies/attach"
        responses.add(responses.PUT, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["policy1", "policy2"]

        # Should not raise an exception
        self.client.group_attach_policies(auth_headers, group_irn, policy_ids)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PUT"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["policyIDs"] == policy_ids

    @responses.activate
    def test_group_add_members_success(self) -> None:
        """Test successful member addition to group."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}/members/add"
        responses.add(responses.POST, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        member_ids = ["user1", "user2"]

        # Should not raise an exception
        self.client.group_add_members(auth_headers, group_irn, member_ids)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["userIDs"] == member_ids

    @responses.activate
    def test_search_group_success(self) -> None:
        """Test successful group search."""
        expected_url = f"{self.expected_base_url}"
        groups_response: dict[str, Any] = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "tenantID": "4atcicnisg",
                    "name": "java",
                    "displayName": "Java",
                    "path": "/dev",
                    "metadata": {"location": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                    "created": "2021-10-18T11:08:09.4919Z",
                    "updated": "2021-10-18T11:08:09.4919Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=groups_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = GroupSearchFilter(name="java")

        result = self.client.search_groups(auth_headers, search_filter)

        assert isinstance(result, IamGroupsResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        group = result.data[0]
        assert isinstance(group, Group)
        assert group.name == "java"
        assert group.display_name == "Java"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?name=java"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_group_without_filter(self) -> None:
        """Test group search without filter parameters."""
        expected_url = f"{self.expected_base_url}"
        groups_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=groups_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_groups(auth_headers)

        assert isinstance(result, IamGroupsResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_groups_success(self) -> None:
        """Test successful search of all groups with pagination."""
        expected_url = f"{self.expected_base_url}"
        # First page response
        first_page_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "tenantID": "4atcicnisg",
                    "name": "java",
                    "displayName": "Java",
                    "path": "/dev",
                    "metadata": {"location": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                    "created": "2021-10-18T11:08:09.4919Z",
                    "updated": "2021-10-18T11:08:09.4919Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 1,
        }
        responses.add(responses.GET, expected_url, json=first_page_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        results = list(self.client.search_all_groups(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], Group)
        assert results[0].name == "java"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_group_bad_request_error(self) -> None:
        """Test create_group raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid group data", "errors": ["name is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateGroup(name="")  # Invalid: empty name

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create_group(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid group data" in str(excinfo.value)

    @responses.activate
    def test_create_group_unauthorized_error(self) -> None:
        """Test create_group raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreateGroup(name="java")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create_group(auth_headers, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_group_forbidden_error(self) -> None:
        """Test create_group raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create groups"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateGroup(name="java")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create_group(auth_headers, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_group_conflict_error(self) -> None:
        """Test create_group raises IAMConflictException for 409 Conflict."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.POST, expected_url, json={"message": "Group with this name already exists"}, status=409)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateGroup(name="existing_group")

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create_group(auth_headers, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_delete_group_not_found_error(self) -> None:
        """Test delete_group raises IAMException for 404 Not Found."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/nonexistent")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Group not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.delete_group(auth_headers, group_irn)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_delete_group_unauthorized_error(self) -> None:
        """Test delete_group raises IAMUnauthorizedException for 401 Unauthorized."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.delete_group(auth_headers, group_irn)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_delete_group_forbidden_error(self) -> None:
        """Test delete_group raises IAMForbiddenException for 403 Forbidden."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/restricted")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}"
        responses.add(
            responses.DELETE, expected_url, json={"message": "Access denied to delete this group"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.delete_group(auth_headers, group_irn)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_group_attach_policies_bad_request_error(self) -> None:
        """Test group_attach_policies raises IAMBedRequestException for 400 Bad Request."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}/policies/attach"
        responses.add(
            responses.PUT,
            expected_url,
            json={"message": "Invalid policy IDs provided", "errors": ["Policy ID format invalid"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["invalid@policy@id"]

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.group_attach_policies(auth_headers, group_irn, policy_ids)

        assert excinfo.value.status_code == 400
        assert "Invalid policy IDs" in str(excinfo.value)

    @responses.activate
    def test_group_attach_policies_not_found_error(self) -> None:
        """Test group_attach_policies raises IAMException for 404 Not Found."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/nonexistent")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}/policies/attach"
        responses.add(responses.PUT, expected_url, json={"message": "Group not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["policy1", "policy2"]

        with pytest.raises(IAMException) as excinfo:
            self.client.group_attach_policies(auth_headers, group_irn, policy_ids)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_group_add_members_bad_request_error(self) -> None:
        """Test group_add_members raises IAMBedRequestException for 400 Bad Request."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}/members/add"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid user IDs provided", "errors": ["User ID format invalid"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        member_ids = ["invalid@user@id"]

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.group_add_members(auth_headers, group_irn, member_ids)

        assert excinfo.value.status_code == 400
        assert "Invalid user IDs" in str(excinfo.value)

    @responses.activate
    def test_group_add_members_not_found_error(self) -> None:
        """Test group_add_members raises IAMException for 404 Not Found."""
        group_irn = IRN.of("irn:rc73dbh7q0:iamcore:4atcicnisg::group/nonexistent")
        expected_url = f"{self.expected_base_url}/{group_irn.to_base64()}/members/add"
        responses.add(responses.POST, expected_url, json={"message": "Group not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        member_ids = ["user1", "user2"]

        with pytest.raises(IAMException) as excinfo:
            self.client.group_add_members(auth_headers, group_irn, member_ids)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_search_group_unauthorized_error(self) -> None:
        """Test search_group raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search_groups(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_group_forbidden_error(self) -> None:
        """Test search_group raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}"
        responses.add(
            responses.GET, expected_url, json={"message": "Insufficient permissions to search groups"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search_groups(auth_headers)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_search_group_server_error(self) -> None:
        """Test search_group raises IAMException for 500 Internal Server Error."""
        expected_url = f"{self.expected_base_url}"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search_groups(auth_headers)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
