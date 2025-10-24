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
from iamcore.client.tenant.client import Client
from iamcore.client.tenant.dto import (
    CreateTenant,
    GetTenantIssuer,
    GetTenantsFilter,
    IamTenantsResponse,
    Tenant,
    TenantIssuer,
)

BASE_URL = "http://localhost:8080"


class TestTenantClient:
    """Class-based tests for Tenant Client."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up the test class with a client instance."""
        cls.client = Client(base_url=BASE_URL)
        cls.expected_base_url: str = f"{BASE_URL}/api/v1/"

    def test_tenant_client_initialization(self) -> None:
        """Test Tenant Client initialization."""
        client = Client(base_url=BASE_URL, timeout=60)
        assert client.base_url == self.expected_base_url
        assert client.timeout == 60

    @responses.activate
    def test_create_tenant_success(self) -> None:
        """Test successful tenant creation."""
        expected_url = f"{self.expected_base_url}tenants/issuer-types/iamcore"
        tenant_response = {
            "data": {
                "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                "tenantID": "47g5l2ijc0",
                "name": "my-tenant",
                "displayName": "My tenant",
                "loginTheme": "iamcore",
                "userMetadataUiSchema": {"key": "val"},
                "groupMetadataUiSchema": {"key": "val"},
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.POST, expected_url, json=tenant_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateTenant(
            name="my-tenant",
            displayName="My tenant",
            loginTheme="iamcore",
            userMetadataUiSchema={"key": "val"},
            groupMetadataUiSchema={"key": "val"},
        )

        result = self.client.create_tenant(auth_headers, create_params)

        assert isinstance(result, Tenant)
        assert result.resource_id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA=="
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0"
        assert result.tenant_id == "47g5l2ijc0"
        assert result.name == "my-tenant"
        assert result.display_name == "My tenant"
        assert result.login_theme == "iamcore"
        assert result.user_metadata_ui_schema == {"key": "val"}
        assert result.group_metadata_ui_schema == {"key": "val"}
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
        assert request_data["name"] == "my-tenant"
        assert request_data["displayName"] == "My tenant"
        assert request_data["loginTheme"] == "iamcore"
        assert request_data["userMetadataUiSchema"] == {"key": "val"}
        assert request_data["groupMetadataUiSchema"] == {"key": "val"}

    @responses.activate
    def test_create_tenant_minimal_params(self) -> None:
        """Test tenant creation with minimal parameters."""
        expected_url = f"{self.expected_base_url}tenants/issuer-types/iamcore"
        tenant_response = {
            "data": {
                "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                "tenantID": "47g5l2ijc0",
                "name": "my-tenant",
                "displayName": "my-tenant",
                "loginTheme": "iamcore",
                "userMetadataUiSchema": None,
                "groupMetadataUiSchema": None,
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        }
        responses.add(responses.POST, expected_url, json=tenant_response, status=201)

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateTenant(name="my-tenant", displayName="my-tenant")  # Only required fields

        result = self.client.create_tenant(auth_headers, create_params)

        assert isinstance(result, Tenant)
        assert result.name == "my-tenant"
        assert result.display_name == "my-tenant"
        assert result.user_metadata_ui_schema is None
        assert result.group_metadata_ui_schema is None

        # Verify the request payload excludes None values
        assert responses.calls[0].request.body is not None
        request_data = json.loads(str(responses.calls[0].request.body))
        assert request_data["name"] == "my-tenant"
        assert request_data["displayName"] == "my-tenant"
        assert request_data["loginTheme"] == "iamcore"
        assert "userMetadataUiSchema" not in request_data
        assert "groupMetadataUiSchema" not in request_data

    @responses.activate
    def test_update_tenant_success(self) -> None:
        """Test successful tenant update."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.PUT, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}
        display_name = "Updated tenant name"

        # Should not raise an exception
        self.client.update_tenant(auth_headers, tenant_irn, display_name)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PUT"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

        # Verify the request payload
        assert responses.calls[0].request.body is not None
        request_data = json.loads(cast("str", responses.calls[0].request.body))
        assert request_data["displayName"] == "Updated tenant name"

    @responses.activate
    def test_delete_tenant_success(self) -> None:
        """Test successful tenant deletion."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, status=204)

        auth_headers = {"Authorization": "Bearer token"}

        # Should not raise an exception
        self.client.delete_tenant(auth_headers, tenant_irn)

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "DELETE"
        assert responses.calls[0].request.url == expected_url
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_get_issuer_success(self) -> None:
        """Test successful tenant issuer retrieval."""
        expected_url = f"{self.expected_base_url}tenants/issuers"
        issuer_response = {
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::issuer/iamcore",
                    "name": "iamcore",
                    "type": "iamcore",
                    "url": "https://iamcore.io/auth",
                    "loginURL": "https://iamcore.io/login",
                    "clientID": "a04583ab-cdc5-4991-ad1c-1e5555adea7e",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=issuer_response, status=200)

        headers = {"Authorization": "Bearer token"}
        params = GetTenantIssuer(account="test-account", tenant_id="47g5l2ijc0")

        result = self.client.get_issuer(headers, params)

        assert isinstance(result, TenantIssuer)
        assert result.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ=="
        assert str(result.irn) == "irn:rc73dbh7q0:iamcore:47g5l2ijc0::issuer/iamcore"
        assert result.name == "iamcore"
        assert result.type == "iamcore"
        assert result.url == "https://iamcore.io/auth"
        assert result.client_id == "a04583ab-cdc5-4991-ad1c-1e5555adea7e"
        assert result.login_url == "https://iamcore.io/login"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?account=test-account&tenantID=47g5l2ijc0"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_tenant_success(self) -> None:
        """Test successful tenant search."""
        expected_url = f"{self.expected_base_url}tenants"
        tenants_response: dict[str, Any] = {
            "data": [
                {
                    "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                    "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                    "tenantID": "47g5l2ijc0",
                    "name": "my-tenant",
                    "displayName": "My tenant",
                    "loginTheme": "iamcore",
                    "userMetadataUiSchema": {"key": "val"},
                    "groupMetadataUiSchema": {"key": "val"},
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        }
        responses.add(responses.GET, expected_url, json=tenants_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}
        search_filter = GetTenantsFilter(name="my-tenant")

        result = self.client.search_tenant(auth_headers, search_filter)

        assert isinstance(result, IamTenantsResponse)
        assert result.count == 1
        assert result.page == 1
        assert result.page_size == 10
        assert len(result.data) == 1

        tenant = result.data[0]
        assert isinstance(tenant, Tenant)
        assert tenant.name == "my-tenant"
        assert tenant.display_name == "My tenant"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?name=my-tenant"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer token"

    @responses.activate
    def test_search_tenant_without_filter(self) -> None:
        """Test tenant search without filter parameters."""
        expected_url = f"{self.expected_base_url}tenants"
        tenants_response: dict[str, Any] = {"data": [], "count": 0, "page": 1, "pageSize": 10}
        responses.add(responses.GET, expected_url, json=tenants_response, status=200)

        auth_headers = {"Authorization": "Bearer token"}

        result = self.client.search_tenant(auth_headers)

        assert isinstance(result, IamTenantsResponse)
        assert result.count == 0
        assert len(result.data) == 0

        # Verify the request has no query parameters
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_search_all_tenants_success(self) -> None:
        """Test successful search of all tenants with pagination."""
        expected_url = f"{self.expected_base_url}tenants"
        # First page response
        first_page_response = {
            "data": [
                {
                    "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                    "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                    "tenantID": "47g5l2ijc0",
                    "name": "my-tenant",
                    "displayName": "My tenant",
                    "loginTheme": "iamcore",
                    "userMetadataUiSchema": {"key": "val"},
                    "groupMetadataUiSchema": {"key": "val"},
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

        results = list(self.client.search_all_tenants(auth_headers))

        assert len(results) == 1
        assert isinstance(results[0], Tenant)
        assert results[0].name == "my-tenant"

        # Verify the request
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{expected_url}?page=1&pageSize=1000"

    @responses.activate
    def test_create_tenant_bad_request_error(self) -> None:
        """Test create_tenant raises IAMBedRequestException for 400 Bad Request."""
        expected_url = f"{self.expected_base_url}tenants/issuer-types/iamcore"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Invalid tenant data", "errors": ["name is required"]},
            status=400,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateTenant(name="", displayName="My tenant")  # Invalid: empty name

        with pytest.raises(IAMBedRequestException) as excinfo:
            self.client.create_tenant(auth_headers, create_params)

        assert excinfo.value.status_code == 400
        assert "Invalid tenant data" in str(excinfo.value)

    @responses.activate
    def test_create_tenant_unauthorized_error(self) -> None:
        """Test create_tenant raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}tenants/issuer-types/iamcore"
        responses.add(responses.POST, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        create_params = CreateTenant(name="my-tenant", displayName="My tenant")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.create_tenant(auth_headers, create_params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_create_tenant_forbidden_error(self) -> None:
        """Test create_tenant raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}tenants/issuer-types/iamcore"
        responses.add(
            responses.POST,
            expected_url,
            json={"message": "Insufficient permissions to create tenants"},
            status=403,
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateTenant(name="my-tenant", displayName="My tenant")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.create_tenant(auth_headers, create_params)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_create_tenant_conflict_error(self) -> None:
        """Test create_tenant raises IAMConflictException for 409 Conflict."""
        expected_url = f"{self.expected_base_url}tenants/issuer-types/iamcore"
        responses.add(
            responses.POST, expected_url, json={"message": "Tenant with this name already exists"}, status=409
        )

        auth_headers = {"Authorization": "Bearer token"}
        create_params = CreateTenant(name="existing-tenant", displayName="Existing tenant")

        with pytest.raises(IAMConflictException) as excinfo:
            self.client.create_tenant(auth_headers, create_params)

        assert excinfo.value.status_code == 409
        assert "already exists" in str(excinfo.value)

    @responses.activate
    def test_update_tenant_not_found_error(self) -> None:
        """Test update_tenant raises IAMException for 404 Not Found."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/nonexistent")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.PUT, expected_url, json={"message": "Tenant not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}
        display_name = "Updated name"

        with pytest.raises(IAMException) as excinfo:
            self.client.update_tenant(auth_headers, tenant_irn, display_name)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_update_tenant_unauthorized_error(self) -> None:
        """Test update_tenant raises IAMUnauthorizedException for 401 Unauthorized."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.PUT, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}
        display_name = "Updated name"

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.update_tenant(auth_headers, tenant_irn, display_name)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_update_tenant_forbidden_error(self) -> None:
        """Test update_tenant raises IAMForbiddenException for 403 Forbidden."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/restricted")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.PUT, expected_url, json={"message": "Access denied to update this tenant"}, status=403)

        auth_headers = {"Authorization": "Bearer token"}
        display_name = "Updated name"

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.update_tenant(auth_headers, tenant_irn, display_name)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_delete_tenant_not_found_error(self) -> None:
        """Test delete_tenant raises IAMException for 404 Not Found."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/nonexistent")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Tenant not found"}, status=404)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.delete_tenant(auth_headers, tenant_irn)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_delete_tenant_unauthorized_error(self) -> None:
        """Test delete_tenant raises IAMUnauthorizedException for 401 Unauthorized."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(responses.DELETE, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.delete_tenant(auth_headers, tenant_irn)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_delete_tenant_forbidden_error(self) -> None:
        """Test delete_tenant raises IAMForbiddenException for 403 Forbidden."""
        tenant_irn = IRN.of("irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/restricted")
        expected_url = f"{self.expected_base_url}tenants/{tenant_irn.to_base64()}"
        responses.add(
            responses.DELETE, expected_url, json={"message": "Access denied to delete this tenant"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.delete_tenant(auth_headers, tenant_irn)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_get_issuer_not_found_error(self) -> None:
        """Test get_issuer raises IAMException for 404 Not Found."""
        expected_url = f"{self.expected_base_url}tenants/issuers"
        responses.add(responses.GET, expected_url, json={"message": "Issuer not found"}, status=404)

        headers = {"Authorization": "Bearer token"}
        params = GetTenantIssuer(account="nonexistent", tenant_id="47g5l2ijc0")

        with pytest.raises(IAMException) as excinfo:
            self.client.get_issuer(headers, params)

        assert excinfo.value.status_code == 404
        assert "not found" in str(excinfo.value)

    @responses.activate
    def test_get_issuer_unauthorized_error(self) -> None:
        """Test get_issuer raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}tenants/issuers"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        headers = {"Authorization": "Bearer invalid_token"}
        params = GetTenantIssuer(account="test-account", tenant_id="47g5l2ijc0")

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.get_issuer(headers, params)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_get_issuer_forbidden_error(self) -> None:
        """Test get_issuer raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}tenants/issuers"
        responses.add(responses.GET, expected_url, json={"message": "Access denied to issuer information"}, status=403)

        headers = {"Authorization": "Bearer token"}
        params = GetTenantIssuer(account="test-account", tenant_id="47g5l2ijc0")

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.get_issuer(headers, params)

        assert excinfo.value.status_code == 403
        assert "Access denied" in str(excinfo.value)

    @responses.activate
    def test_search_tenant_unauthorized_error(self) -> None:
        """Test search_tenant raises IAMUnauthorizedException for 401 Unauthorized."""
        expected_url = f"{self.expected_base_url}tenants"
        responses.add(responses.GET, expected_url, json={"message": "Authentication required"}, status=401)

        auth_headers = {"Authorization": "Bearer invalid_token"}

        with pytest.raises(IAMUnauthorizedException) as excinfo:
            self.client.search_tenant(auth_headers)

        assert excinfo.value.status_code == 401
        assert "Authentication required" in str(excinfo.value)

    @responses.activate
    def test_search_tenant_forbidden_error(self) -> None:
        """Test search_tenant raises IAMForbiddenException for 403 Forbidden."""
        expected_url = f"{self.expected_base_url}tenants"
        responses.add(
            responses.GET, expected_url, json={"message": "Insufficient permissions to search tenants"}, status=403
        )

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMForbiddenException) as excinfo:
            self.client.search_tenant(auth_headers)

        assert excinfo.value.status_code == 403
        assert "Insufficient permissions" in str(excinfo.value)

    @responses.activate
    def test_search_tenant_server_error(self) -> None:
        """Test search_tenant raises IAMException for 500 Internal Server Error."""
        expected_url = f"{self.expected_base_url}tenants"
        responses.add(responses.GET, expected_url, json={"message": "Internal server error occurred"}, status=500)

        auth_headers = {"Authorization": "Bearer token"}

        with pytest.raises(IAMException) as excinfo:
            self.client.search_tenant(auth_headers)

        assert excinfo.value.status_code == 500
        assert "Internal server error" in str(excinfo.value)
