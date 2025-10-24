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
from iamcore.client.policy.client import Client
from iamcore.client.policy.dto import (
    CreatePolicy,
    IamPoliciesResponse,
    Policy,
    PolicySearchFilter,
    PolicyStatement,
    UpdatePolicy,
)

BASE_URL = "http://localhost:8080"


class TestPolicyClient:
    """Class-based tests for Policy Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/"

    def test_policy_client_initialization(self) -> None:
        """Test Policy Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_policy_success(self) -> None:
        """Test successful policy creation."""
        expected_url = f"{self.expected_base_url}policies"
        policy_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                "name": "allow-all-actions-on-jerry",
                "description": "Allow all actions on Jerry",
                "type": "identity",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "effect": "allow",
                        "description": "Allow all actions on Jerry",
                        "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                        "actions": ["iamcore:user:*"],
                    }
                ],
            }
        }
        responses.add(responses.POST, expected_url, json=policy_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreatePolicy(
            name="allow-all-actions-on-jerry",
            level="tenant",
            description="Allow all actions on Jerry",
            statements=[
                PolicyStatement(
                    effect="allow",
                    description="Allow all actions on Jerry",
                    resources=["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                    actions=["iamcore:user:*"],
                )
            ],
        )

        result = self.client.create_policy(auth_headers, create_params)

        assert isinstance(result, Policy)
        assert (
            result.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk="
        )
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry"
        assert result.name == "allow-all-actions-on-jerry"
        assert result.description == "Allow all actions on Jerry"
        assert result.type == "identity"
        assert result.origin == "api"
        assert result.version == "1.0.0"
        assert len(result.statements) == 1
        assert result.statements[0].effect == "allow"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["name"] == "allow-all-actions-on-jerry"
        assert request_data["level"] == "tenant"
        assert request_data["description"] == "Allow all actions on Jerry"
        assert len(request_data["statements"]) == 1

    @responses.activate
    def test_create_policy_minimal_params(self) -> None:
        """Test policy creation with minimal parameters."""
        expected_url = f"{self.expected_base_url}policies"
        policy_response = {
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                "name": "allow-all-actions-on-jerry",
                "description": "Allow all actions on Jerry",
                "type": "identity",
                "origin": "api",
                "version": "1.0.0",
                "statements": [],
            }
        }
        responses.add(responses.POST, expected_url, json=policy_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreatePolicy(name="allow-all-actions-on-jerry", level="tenant")  # Only required fields

        result = self.client.create_policy(auth_headers, create_params)

        assert isinstance(result, Policy)
        assert result.name == "allow-all-actions-on-jerry"
        assert result.statements == []  # Empty statements list

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["name"] == "allow-all-actions-on-jerry"
        assert request_data["level"] == "tenant"
        assert "description" not in request_data or request_data["description"] is None

    @responses.activate
    def test_delete_policy_success(self) -> None:
        """Test successful policy deletion."""
        policy_id = "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry"
        expected_url = f"{self.expected_base_url}policies/{IRN.of(policy_id).to_base64()}"
        responses.add(responses.DELETE, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}

        # Should not raise an exception
        self.client.delete_policy(auth_headers, policy_id)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "DELETE"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_update_policy_success(self) -> None:
        """Test successful policy update."""
        policy_id = "allow-all-actions-on-jerry"
        expected_url = f"{self.expected_base_url}policies/{policy_id}"
        responses.add(responses.PUT, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdatePolicy(
            description="Updated description",
            statements=[
                PolicyStatement(
                    effect="allow",
                    description="Allow all actions on Jerry",
                    resources=["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                    actions=["iamcore:user:*"],
                )
            ],
        )

        # Should not raise an exception
        self.client.update_policy(auth_headers, policy_id, update_params)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PUT"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["description"] == "Updated description"
        assert len(request_data["statements"]) == 1

    @responses.activate
    def test_search_policy_success(self) -> None:
        """Test successful policy search."""
        expected_url = f"{self.expected_base_url}policies"
        policies_response: dict[str, Any] = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "effect": "allow",
                            "description": "Allow all actions on Jerry",
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "actions": ["iamcore:user:*"],
                        }
                    ],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=policies_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = PolicySearchFilter(name="allow-all-actions-on-jerry")

        result = self.client.search_policy(auth_headers, search_filter)

        assert isinstance(result, IamPoliciesResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        policy = result.data[0]
        assert isinstance(policy, Policy)
        assert policy.name == "allow-all-actions-on-jerry"
        assert policy.description == "Allow all actions on Jerry"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?name=allow-all-actions-on-jerry"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_policy_without_filter(self) -> None:
        """Test policy search without filter parameters."""
        expected_url = f"{self.expected_base_url}policies"
        policies_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=policies_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_policy(auth_headers)

        assert isinstance(result, IamPoliciesResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_policies_success(self) -> None:
        """Test successful search of all policies with pagination."""
        expected_url = f"{self.expected_base_url}policies"
        # First page response
        first_page_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "effect": "allow",
                            "description": "Allow all actions on Jerry",
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "actions": ["iamcore:user:*"],
                        }
                    ],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 1,
        }
        responses.add(responses.GET, expected_url, json=first_page_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        results = list(self.client.search_all_policies(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], Policy)
        assert results[0].name == "allow-all-actions-on-jerry"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_policy_bad_request_error(self) -> None:
        """Test create_policy raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid policy data", "errors": ["name is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreatePolicy(name="", level="tenant")  # Invalid: empty name

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create_policy(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid policy data" in str(excinfo.value)

    @responses.activate
    def test_create_policy_unauthorized_error(self) -> None:
        """Test create_policy raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreatePolicy(name="test-policy", level="tenant")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create_policy(auth_headers, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_policy_forbidden_error(self) -> None:
        """Test create_policy raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create policies"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreatePolicy(name="test-policy", level="tenant")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create_policy(auth_headers, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_policy_conflict_error(self) -> None:
        """Test create_policy raises IAMConflictException for 409 Conflict."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(
            responses.POST, expected_url, json={"message": "Policy with this name already exists"}, status=409
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreatePolicy(name="existing-policy", level="tenant")

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create_policy(auth_headers, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_delete_policy_not_found_error(self) -> None:
        """Test delete_policy raises IAMException for 404 Not Found."""
        policy_id = "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/nonexistent"
        expected_url = f"{self.expected_base_url}policies/{IRN.of(policy_id).to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Policy not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.delete_policy(auth_headers, policy_id)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_delete_policy_unauthorized_error(self) -> None:
        """Test delete_policy raises IAMUnauthorizedException for 401 Unauthorized."""
        policy_id = "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/test-policy"
        expected_url = f"{self.expected_base_url}policies/{IRN.of(policy_id).to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.delete_policy(auth_headers, policy_id)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_delete_policy_forbidden_error(self) -> None:
        """Test delete_policy raises IAMForbiddenException for 403 Forbidden."""
        policy_id = "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/restricted"
        expected_url = f"{self.expected_base_url}policies/{IRN.of(policy_id).to_base64()}"
        responses.add(
            responses.DELETE, expected_url, json={"message": "Access denied to delete this policy"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.delete_policy(auth_headers, policy_id)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_update_policy_bad_request_error(self) -> None:
        """Test update_policy raises IAMBedRequestException for 400 Bad Request."""
        policy_id = "test-policy"
        expected_url = f"{self.expected_base_url}policies/{policy_id}"
        responses.add(
            responses.PUT,
            expected_url,
            json={"message": "Invalid policy update data", "errors": ["description is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdatePolicy(description="", statements=[])  # Invalid: empty description

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.update_policy(auth_headers, policy_id, update_params)

        assert excinfo.value.status_code == 400
        assert "Invalid policy update data" in str(excinfo.value)

    @responses.activate
    def test_update_policy_not_found_error(self) -> None:
        """Test update_policy raises IAMException for 404 Not Found."""
        policy_id = "nonexistent-policy"
        expected_url = f"{self.expected_base_url}policies/{policy_id}"
        responses.add(responses.PUT, expected_url, json={"message": "Policy not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        update_params = UpdatePolicy(description="Updated description", statements=[])

        with pytest.raises(IAMException) as excinfo:
            self.client.update_policy(auth_headers, policy_id, update_params)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_search_policy_unauthorized_error(self) -> None:
        """Test search_policy raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search_policy(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_policy_forbidden_error(self) -> None:
        """Test search_policy raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(
            responses.GET, expected_url, json={"message": "Insufficient permissions to search policies"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search_policy(auth_headers)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_search_policy_server_error(self) -> None:
        """Test search_policy raises IAMException for 500 Internal Server Error."""
        expected_url = f"{self.expected_base_url}policies"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search_policy(auth_headers)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
