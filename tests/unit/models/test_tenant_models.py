from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.tenant.dto import (
    CreateTenant,
    IamTenantIssuerResponse,
    IamTenantIssuersResponse,
    IamTenantResponse,
    IamTenantsResponse,
    Tenant,
    TenantIssuer,
    UpdateTenant,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_tenant_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a Tenant."""
    return {
        "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
        "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
        "tenantID": "47g5l2ijc0",
        "name": "my-tenant",
        "displayName": "My tenant",
        "loginTheme": "My theme",
        "userMetadataUiSchema": {"key": "val"},
        "groupMetadataUiSchema": {"key": "val"},
        "created": "2021-10-18T12:27:15.55267632Z",
        "updated": "2021-10-18T12:27:15.55267632Z",
    }


@pytest.fixture
def sample_tenant_issuer_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a TenantIssuer."""
    return {
        "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ==",
        "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::issuer/iamcore",
        "name": "iamcore",
        "type": "iamcore",
        "url": "https://iamcore.io/auth",
        "loginURL": "https://iamcore.io/login",
        "clientID": "a04583ab-cdc5-4991-ad1c-1e5555adea7e",
    }


@pytest.fixture
def sample_create_tenant_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating a Tenant."""
    return {
        "name": "my-tenant",
        "displayName": "My tenant",
        "loginTheme": "My theme",
        "userMetadataUiSchema": {"key": "val"},
        "groupMetadataUiSchema": {"key": "val"},
    }


@pytest.fixture
def sample_update_tenant_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for updating a Tenant."""
    return {
        "displayName": "New display name",
        "userMetadataUiSchema": {"key": "val"},
        "groupMetadataUiSchema": {"key": "val"},
    }


# Test the Core Data Model in Isolation
class TestTenantModel:
    """Tests for the Tenant Pydantic model."""

    def test_successful_validation(self, sample_tenant_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a Tenant object.
        """
        # ACT
        tenant = Tenant.model_validate(sample_tenant_data)

        # ASSERT
        assert tenant.resource_id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA=="
        assert str(tenant.irn) == "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0"
        assert tenant.tenant_id == "47g5l2ijc0"
        assert tenant.name == "my-tenant"
        assert tenant.display_name == "My tenant"
        assert tenant.login_theme == "My theme"
        assert tenant.user_metadata_ui_schema == {"key": "val"}
        assert tenant.group_metadata_ui_schema == {"key": "val"}
        assert tenant.created == "2021-10-18T12:27:15.55267632Z"

    def test_serialization_to_dict_uses_aliases(self, sample_tenant_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        tenant = Tenant.model_validate(sample_tenant_data)

        # ACT
        tenant_dict = tenant.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert tenant_dict["tenantID"] == "47g5l2ijc0"
        assert tenant_dict["displayName"] == "My tenant"
        assert tenant_dict["loginTheme"] == "My theme"
        assert tenant_dict["userMetadataUiSchema"] == {"key": "val"}
        assert tenant_dict["groupMetadataUiSchema"] == {"key": "val"}
        assert "tenant_id" not in tenant_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(self, sample_tenant_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_tenant_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            Tenant.model_validate(sample_tenant_data)

        assert "Field required" in str(excinfo.value)


class TestTenantIssuerModel:
    """Tests for the TenantIssuer Pydantic model."""

    def test_successful_validation(self, sample_tenant_issuer_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a TenantIssuer object.
        """
        # ACT
        tenant_issuer = TenantIssuer.model_validate(sample_tenant_issuer_data)

        # ASSERT
        assert tenant_issuer.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ=="
        assert str(tenant_issuer.irn) == "irn:rc73dbh7q0:iamcore:47g5l2ijc0::issuer/iamcore"
        assert tenant_issuer.name == "iamcore"
        assert tenant_issuer.type == "iamcore"
        assert tenant_issuer.url == "https://iamcore.io/auth"
        assert tenant_issuer.client_id == "a04583ab-cdc5-4991-ad1c-1e5555adea7e"
        assert tenant_issuer.login_url == "https://iamcore.io/login"

    def test_serialization_to_dict_uses_aliases(self, sample_tenant_issuer_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        tenant_issuer = TenantIssuer.model_validate(sample_tenant_issuer_data)

        # ACT
        tenant_issuer_dict = tenant_issuer.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert tenant_issuer_dict["clientID"] == "a04583ab-cdc5-4991-ad1c-1e5555adea7e"
        assert tenant_issuer_dict["loginURL"] == "https://iamcore.io/login"
        assert "client_id" not in tenant_issuer_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(self, sample_tenant_issuer_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_tenant_issuer_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            TenantIssuer.model_validate(sample_tenant_issuer_data)

        assert "Field required" in str(excinfo.value)


class TestCreateTenantModel:
    """Tests for the CreateTenant Pydantic model."""

    def test_successful_validation(self, sample_create_tenant_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreateTenant object.
        """
        # ACT
        create_tenant = CreateTenant.model_validate(sample_create_tenant_data)

        # ASSERT
        assert create_tenant.name == "my-tenant"
        assert create_tenant.display_name == "My tenant"
        assert create_tenant.login_theme == "My theme"
        assert create_tenant.user_metadata_ui_schema == {"key": "val"}
        assert create_tenant.group_metadata_ui_schema == {"key": "val"}

    def test_serialization_to_dict_uses_aliases(self, sample_create_tenant_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        create_tenant = CreateTenant.model_validate(sample_create_tenant_data)

        # ACT
        create_dict = create_tenant.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert create_dict["displayName"] == "My tenant"
        assert create_dict["loginTheme"] == "My theme"
        assert create_dict["userMetadataUiSchema"] == {"key": "val"}
        assert create_dict["groupMetadataUiSchema"] == {"key": "val"}
        assert "display_name" not in create_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_create_tenant_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_create_tenant_data["userMetadataUiSchema"]  # Remove the optional field

        # ACT
        create_tenant = CreateTenant.model_validate(sample_create_tenant_data)

        # ASSERT
        assert create_tenant.user_metadata_ui_schema is None

    def test_raises_validation_error_for_missing_required_field(self, sample_create_tenant_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_create_tenant_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreateTenant.model_validate(sample_create_tenant_data)

        assert "Field required" in str(excinfo.value)


class TestUpdateTenantModel:
    """Tests for the UpdateTenant Pydantic model."""

    def test_successful_validation(self, sample_update_tenant_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an UpdateTenant object.
        """
        # ACT
        update_tenant = UpdateTenant.model_validate(sample_update_tenant_data)

        # ASSERT
        assert update_tenant.display_name == "New display name"
        assert update_tenant.user_metadata_ui_schema == {"key": "val"}
        assert update_tenant.group_metadata_ui_schema == {"key": "val"}

    def test_serialization_to_dict_uses_aliases(self, sample_update_tenant_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        update_tenant = UpdateTenant.model_validate(sample_update_tenant_data)

        # ACT
        update_dict = update_tenant.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert update_dict["displayName"] == "New display name"
        assert update_dict["userMetadataUiSchema"] == {"key": "val"}
        assert update_dict["groupMetadataUiSchema"] == {"key": "val"}
        assert "display_name" not in update_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_update_tenant_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_update_tenant_data["userMetadataUiSchema"]  # Remove the optional field

        # ACT
        update_tenant = UpdateTenant.model_validate(sample_update_tenant_data)

        # ASSERT
        assert update_tenant.user_metadata_ui_schema is None

    def test_raises_validation_error_for_missing_required_field(self, sample_update_tenant_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_update_tenant_data["displayName"]  # 'displayName' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            UpdateTenant.model_validate(sample_update_tenant_data)

        assert "Field required" in str(excinfo.value)


# Test the Response Wrappers
class TestTenantResponseWrappers:
    """Tests for the IamTenantResponse, IamTenantsResponse, IamTenantIssuerResponse, and IamTenantIssuersResponse wrappers."""

    def test_iam_tenant_response_single_item(self, sample_tenant_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamTenantResponse(sample_tenant_data)

        # ASSERT
        assert isinstance(response.data, Tenant)
        assert response.data.name == "my-tenant"

    def test_iam_tenants_response_multiple_items(self, sample_tenant_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second tenant for the list
        tenant_2_data = sample_tenant_data.copy()
        tenant_2_data["name"] = "another-tenant"
        tenant_2_data["resourceID"] = "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvYW5vdGhlcg=="

        raw_list = [sample_tenant_data, tenant_2_data]

        # ACT
        response = IamTenantsResponse(item=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated Tenant objects
        assert isinstance(response.data[0], Tenant)
        assert isinstance(response.data[1], Tenant)
        assert response.data[0].name == "my-tenant"
        assert response.data[1].name == "another-tenant"

    def test_iam_tenant_issuer_response_single_item(self, sample_tenant_issuer_data: dict[str, Any]) -> None:
        """
        Tests that the single-item tenant issuer response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamTenantIssuerResponse(sample_tenant_issuer_data)

        # ASSERT
        assert isinstance(response.data, TenantIssuer)
        assert response.data.name == "iamcore"

    def test_iam_tenant_issuers_response_multiple_items(self, sample_tenant_issuer_data: dict[str, Any]) -> None:
        """
        Tests that the list tenant issuer response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second tenant issuer for the list
        issuer_2_data = sample_tenant_issuer_data.copy()
        issuer_2_data["name"] = "another-issuer"
        issuer_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvYW5vdGhlcg=="

        raw_list = [sample_tenant_issuer_data, issuer_2_data]

        # ACT
        response = IamTenantIssuersResponse(item=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated TenantIssuer objects
        assert isinstance(response.data[0], TenantIssuer)
        assert isinstance(response.data[1], TenantIssuer)
        assert response.data[0].name == "iamcore"
        assert response.data[1].name == "another-issuer"
