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
from iamcore.client.user.client import Client
from iamcore.client.user.dto import (
    CreateUser,
    IamUsersResponse,
    UpdateUser,
    User,
    UserSearchFilter,
)

BASE_URL = "http://localhost:8080"


class TestUserClient:
    """Class-based tests for User Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/"

    def test_user_client_initialization(self) -> None:
        """Test User Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_user_success(self) -> None:
        """Test successful user creation."""
        expected_url = f"{self.expected_base_url}users"
        user_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::user/johndoe",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
                "tenantID": "tenant123",
                "authID": "auth-uuid-123",
                "email": "john.doe@example.com",
                "enabled": True,
                "firstName": "John",
                "lastName": "Doe",
                "username": "johndoe",
                "path": "/users",
                "metadata": {"department": "engineering"},
                "requiredActions": ["VERIFY_EMAIL"],
                "poolIDs": ["pool1", "pool2"],
            }
        }
        responses.add(responses.POST, expected_url, json=user_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateUser(
            email="john.doe@example.com",
            username="johndoe",
            password="securepassword123",
            confirmPassword="securepassword123",
            firstName="John",
            lastName="Doe",
            path="/users",
            poolIDs=["pool1", "pool2"],
            requiredActions=["VERIFY_EMAIL"],
        )

        result = self.client.create_user(auth_headers, create_params)

        assert isinstance(result, User)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:::user/johndoe"
        assert result.email == "john.doe@example.com"
        assert result.username == "johndoe"
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.enabled is True
        assert result.path == "/users"
        assert result.metadata == {"department": "engineering"}
        assert result.required_actions == ["VERIFY_EMAIL"]
        assert result.pool_ids == ["pool1", "pool2"]
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
        assert request_data["email"] == "john.doe@example.com"
        assert request_data["username"] == "johndoe"
        assert request_data["password"] == "securepassword123"
        assert request_data["confirmPassword"] == "securepassword123"
        assert request_data["firstName"] == "John"
        assert request_data["lastName"] == "Doe"
        assert request_data["path"] == "/users"
        assert request_data["poolIDs"] == ["pool1", "pool2"]
        assert request_data["requiredActions"] == ["VERIFY_EMAIL"]

    @responses.activate
    def test_create_user_minimal_params(self) -> None:
        """Test user creation with minimal parameters."""
        expected_url = f"{self.expected_base_url}users"
        user_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::user/johndoe",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
                "tenantID": "tenant123",
                "authID": "auth-uuid-123",
                "email": "john.doe@example.com",
                "enabled": True,
                "firstName": None,
                "lastName": None,
                "username": "johndoe",
                "path": "/users",
                "metadata": None,
                "requiredActions": None,
                "poolIDs": None,
            }
        }
        responses.add(responses.POST, expected_url, json=user_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateUser(
            email="john.doe@example.com",
            username="johndoe",
            password="securepassword123",
            confirmPassword="securepassword123",
        )

        result = self.client.create_user(auth_headers, create_params)

        assert isinstance(result, User)
        assert result.username == "johndoe"
        assert result.first_name is None  # Optional field not provided
        assert result.last_name is None  # Optional field not provided

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["email"] == "john.doe@example.com"
        assert request_data["username"] == "johndoe"
        assert "firstName" not in request_data
        assert "lastName" not in request_data
        assert "path" not in request_data
        assert "poolIDs" not in request_data
        assert "requiredActions" not in request_data

    @responses.activate
    def test_get_user_me_success(self) -> None:
        """Test successful retrieval of current user."""
        expected_url = f"{self.expected_base_url}users/me"
        user_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::user/johndoe",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
                "tenantID": "tenant123",
                "authID": "auth-uuid-123",
                "email": "john.doe@example.com",
                "enabled": True,
                "firstName": "John",
                "lastName": "Doe",
                "username": "johndoe",
                "path": "/users",
                "metadata": {"department": "engineering"},
                "requiredActions": [],
                "poolIDs": ["pool1"],
            }
        }
        responses.add(responses.GET, expected_url, json=user_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.get_user_me(auth_headers)

        assert isinstance(result, User)
        assert result.username == "johndoe"
        assert result.email == "john.doe@example.com"
        assert result.first_name == "John"
        assert result.last_name == "Doe"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_get_irn_success(self) -> None:
        """Test successful retrieval of current user IRN."""
        expected_url = f"{self.expected_base_url}users/me/irn"
        irn_response = {"data": "irn:rc73dbh7q0:iamcore:::user/johndoe"}
        responses.add(responses.GET, expected_url, json=irn_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.get_irn(auth_headers)

        assert isinstance(result, IRN)
        assert str(result) == "irn:rc73dbh7q0:iamcore:::user/johndoe"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_update_user_success(self) -> None:
        """Test successful user update."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/johndoe")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}"
        responses.add(responses.PATCH, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdateUser(
            firstName="Johnny",
            lastName="Doe",
            email="johnny.doe@example.com",
            enabled=True,
        )

        # Should not raise an exception
        self.client.update_user(auth_headers, user_irn, update_params)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PATCH"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["firstName"] == "Johnny"
        assert request_data["lastName"] == "Doe"
        assert request_data["email"] == "johnny.doe@example.com"
        assert request_data["enabled"] is True

    @responses.activate
    def test_delete_user_success(self) -> None:
        """Test successful user deletion."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/johndoe")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}

        # Should not raise an exception
        self.client.delete_user(auth_headers, user_irn)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "DELETE"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_user_attach_policies_success(self) -> None:
        """Test successful policy attachment to user."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/johndoe")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}/policies/attach"
        responses.add(responses.PUT, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["policy1", "policy2"]

        # Should not raise an exception
        self.client.user_attach_policies(auth_headers, user_irn, policy_ids)

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
    def test_user_add_groups_success(self) -> None:
        """Test successful group addition to user."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/johndoe")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}/groups/add"
        responses.add(responses.POST, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        group_ids = ["group1", "group2"]

        # Should not raise an exception
        self.client.user_add_groups(auth_headers, user_irn, group_ids)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["groupIDs"] == group_ids

    @responses.activate
    def test_search_users_success(self) -> None:
        """Test successful user search."""
        expected_url = f"{self.expected_base_url}users"
        users_response: dict[str, Any] = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                    "irn": "irn:rc73dbh7q0:iamcore:::user/johndoe",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                    "tenantID": "tenant123",
                    "authID": "auth-uuid-123",
                    "email": "john.doe@example.com",
                    "enabled": True,
                    "firstName": "John",
                    "lastName": "Doe",
                    "username": "johndoe",
                    "path": "/users",
                    "metadata": None,
                    "requiredActions": None,
                    "poolIDs": None,
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=users_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = UserSearchFilter(email="john.doe@example.com", firstName="John", username="johndoe")

        result = self.client.search_users(auth_headers, search_filter)

        assert isinstance(result, IamUsersResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        user = result.data[0]
        assert isinstance(user, User)
        assert user.username == "johndoe"
        assert user.email == "john.doe@example.com"
        assert user.first_name == "John"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert (
            responses.calls[0].request.url
            == f"{expected_url}?email=john.doe%40example.com&firstName=John&username=johndoe"
        )
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_users_without_filter(self) -> None:
        """Test user search without filter parameters."""
        expected_url = f"{self.expected_base_url}users"
        users_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=users_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_users(auth_headers)

        assert isinstance(result, IamUsersResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_users_success(self) -> None:
        """Test successful search of all users with pagination."""
        expected_url = f"{self.expected_base_url}users"
        # First page response
        first_page_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                    "irn": "irn:rc73dbh7q0:iamcore:::user/johndoe",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                    "tenantID": "tenant123",
                    "authID": "auth-uuid-123",
                    "email": "john.doe@example.com",
                    "enabled": True,
                    "firstName": "John",
                    "lastName": "Doe",
                    "username": "johndoe",
                    "path": "/users",
                    "metadata": None,
                    "requiredActions": None,
                    "poolIDs": None,
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 1,
        }
        responses.add(responses.GET, expected_url, json=first_page_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        results = list(self.client.search_all_users(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], User)
        assert results[0].username == "johndoe"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_user_bad_request_error(self) -> None:
        """Test create_user raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid user data", "errors": ["email is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateUser(
            email="",  # Invalid: empty email
            username="johndoe",
            password="password",
            confirmPassword="password",
        )

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create_user(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid user data" in str(excinfo.value)

    @responses.activate
    def test_create_user_unauthorized_error(self) -> None:
        """Test create_user raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreateUser(
            email="john.doe@example.com",
            username="johndoe",
            password="password",
            confirmPassword="password",
        )

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create_user(auth_headers, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_user_forbidden_error(self) -> None:
        """Test create_user raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create users"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateUser(
            email="john.doe@example.com",
            username="johndoe",
            password="password",
            confirmPassword="password",
        )

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create_user(auth_headers, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_user_conflict_error(self) -> None:
        """Test create_user raises IAMConflictException for 409 Conflict."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(responses.POST, expected_url, json={"message": "User with this email already exists"}, status=409)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateUser(
            email="existing@example.com",
            username="johndoe",
            password="password",
            confirmPassword="password",
        )

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create_user(auth_headers, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_get_user_me_unauthorized_error(self) -> None:
        """Test get_user_me raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}users/me"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.get_user_me(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_update_user_not_found_error(self) -> None:
        """Test update_user raises IAMException for 404 Not Found."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/nonexistent")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}"
        responses.add(responses.PATCH, expected_url, json={"message": "User not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdateUser(firstName="Johnny")

        with pytest.raises(IAMException) as excinfo:
            self.client.update_user(auth_headers, user_irn, update_params)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_delete_user_not_found_error(self) -> None:
        """Test delete_user raises IAMException for 404 Not Found."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/nonexistent")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "User not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.delete_user(auth_headers, user_irn)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_user_attach_policies_bad_request_error(self) -> None:
        """Test user_attach_policies raises IAMBedRequestException for 400 Bad Request."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/johndoe")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}/policies/attach"
        responses.add(
            responses.PUT,
            expected_url,
            json={"message": "Invalid policy IDs provided", "errors": ["Policy ID format invalid"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        policy_ids = ["invalid@policy@id"]

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.user_attach_policies(auth_headers, user_irn, policy_ids)

        assert excinfo.value.status_code == 400
        assert "Invalid policy IDs" in str(excinfo.value)

    @responses.activate
    def test_user_add_groups_not_found_error(self) -> None:
        """Test user_add_groups raises IAMException for 404 Not Found."""
        user_irn = IRN.of("irn:rc73dbh7q0:iamcore:::user/nonexistent")
        expected_url = f"{self.expected_base_url}users/{user_irn.to_base64()}/groups/add"
        responses.add(responses.POST, expected_url, json={"message": "User not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        group_ids = ["group1", "group2"]

        with pytest.raises(IAMException) as excinfo:
            self.client.user_add_groups(auth_headers, user_irn, group_ids)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_search_users_unauthorized_error(self) -> None:
        """Test search_users raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search_users(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_users_forbidden_error(self) -> None:
        """Test search_users raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}users"
        responses.add(
            responses.GET, expected_url, json={"message": "Insufficient permissions to search users"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search_users(auth_headers)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)
