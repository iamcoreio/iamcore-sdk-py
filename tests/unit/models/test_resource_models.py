from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.resource.dto import (
    CreateResource,
    IamResourceResponse,
    IamResourcesResponse,
    Resource,
    UpdateResource,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_resource_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a Resource."""
    return {
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


@pytest.fixture
def sample_create_resource_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating a Resource."""
    return {
        "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
        "displayName": "Thermostat",
        "tenantID": "4atcicnisg",
        "application": "myapp",
        "path": "/dev",
        "resourceType": "device",
        "enabled": True,
        "description": "Resource description",
        "metadata": {"temperature": "10", "city": "Kyiv"},
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
    }


@pytest.fixture
def sample_update_resource_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for updating a Resource."""
    return {
        "displayName": "Thermostat",
        "enabled": True,
        "description": "Resource description",
        "metadata": {"temperature": "10", "city": "Kyiv"},
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
    }


# Test the Core Data Model in Isolation
class TestResourceModel:
    """Tests for the Resource Pydantic model."""

    def test_successful_validation(self, sample_resource_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a Resource object.
        """
        # ACT
        resource = Resource.model_validate(sample_resource_data)

        # ASSERT
        assert (
            resource.id
            == "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk="
        )
        assert str(resource.irn) == "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert resource.tenant_id == "4atcicnisg"
        assert resource.application == "myapp"
        assert resource.name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert resource.display_name == "Thermostat"
        assert resource.path == "/dev"
        assert resource.resource_type == "device"
        assert resource.enabled is True
        assert resource.description == "Resource description"
        assert resource.metadata == {"temperature": "10", "city": "Kyiv"}
        assert resource.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert resource.created == "2022-10-25T22:22:17.390631+03:00"

    def test_serialization_to_dict_uses_aliases(self, sample_resource_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        resource = Resource.model_validate(sample_resource_data)

        # ACT
        resource_dict = resource.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert resource_dict["tenantID"] == "4atcicnisg"
        assert resource_dict["displayName"] == "Thermostat"
        assert resource_dict["resourceType"] == "device"
        assert resource_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert "tenant_id" not in resource_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(self, sample_resource_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_resource_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            Resource.model_validate(sample_resource_data)

        assert "Field required" in str(excinfo.value)


class TestCreateResourceModel:
    """Tests for the CreateResource Pydantic model."""

    def test_successful_validation(self, sample_create_resource_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreateResource object.
        """
        # ACT
        create_resource = CreateResource.model_validate(sample_create_resource_data)

        # ASSERT
        assert create_resource.name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert create_resource.display_name == "Thermostat"
        assert create_resource.tenant_id == "4atcicnisg"
        assert create_resource.application == "myapp"
        assert create_resource.path == "/dev"
        assert create_resource.resource_type == "device"
        assert create_resource.enabled is True
        assert create_resource.description == "Resource description"
        assert create_resource.metadata == {"temperature": "10", "city": "Kyiv"}
        assert create_resource.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    def test_serialization_to_dict_uses_aliases(self, sample_create_resource_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        create_resource = CreateResource.model_validate(sample_create_resource_data)

        # ACT
        create_dict = create_resource.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert create_dict["tenantID"] == "4atcicnisg"
        assert create_dict["displayName"] == "Thermostat"
        assert create_dict["resourceType"] == "device"
        assert create_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert "tenant_id" not in create_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_create_resource_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_create_resource_data["displayName"]  # Remove the optional field

        # ACT
        create_resource = CreateResource.model_validate(sample_create_resource_data)

        # ASSERT
        assert create_resource.display_name is None

    def test_raises_validation_error_for_missing_required_field(
        self, sample_create_resource_data: dict[str, Any]
    ) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_create_resource_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreateResource.model_validate(sample_create_resource_data)

        assert "Field required" in str(excinfo.value)


class TestUpdateResourceModel:
    """Tests for the UpdateResource Pydantic model."""

    def test_successful_validation(self, sample_update_resource_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an UpdateResource object.
        """
        # ACT
        update_resource = UpdateResource.model_validate(sample_update_resource_data)

        # ASSERT
        assert update_resource.display_name == "Thermostat"
        assert update_resource.enabled is True
        assert update_resource.description == "Resource description"
        assert update_resource.metadata == {"temperature": "10", "city": "Kyiv"}
        assert update_resource.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    def test_serialization_to_dict_uses_aliases(self, sample_update_resource_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        update_resource = UpdateResource.model_validate(sample_update_resource_data)

        # ACT
        update_dict = update_resource.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert update_dict["displayName"] == "Thermostat"
        assert update_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert "display_name" not in update_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_update_resource_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_update_resource_data["displayName"]  # Remove the optional field

        # ACT
        update_resource = UpdateResource.model_validate(sample_update_resource_data)

        # ASSERT
        assert update_resource.display_name is None

    def test_all_fields_optional(self, sample_update_resource_data: dict[str, Any]) -> None:
        """
        Tests that all fields in UpdateResource are optional.
        """
        # ARRANGE
        empty_data = {}

        # ACT
        update_resource = UpdateResource.model_validate(empty_data)

        # ASSERT
        assert update_resource.display_name is None
        assert update_resource.enabled is True  # Default value
        assert update_resource.description is None
        assert update_resource.metadata is None
        assert update_resource.pool_ids is None


# Test the Response Wrappers
class TestResourceResponseWrappers:
    """Tests for the IamResourceResponse and IamResourcesResponse wrappers."""

    def test_iam_resource_response_single_item(self, sample_resource_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamResourceResponse(sample_resource_data)

        # ASSERT
        assert isinstance(response.data, Resource)
        assert response.data.name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"

    def test_iam_resources_response_multiple_items(self, sample_resource_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second resource for the list
        resource_2_data = sample_resource_data.copy()
        resource_2_data["name"] = "another-device"
        resource_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi9hbm90aGVy"

        raw_list = [sample_resource_data, resource_2_data]

        # ACT
        response = IamResourcesResponse(data=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated Resource objects
        assert isinstance(response.data[0], Resource)
        assert isinstance(response.data[1], Resource)
        assert response.data[0].name == "7e1edad5-7841-4d38-bdf1-bdc575b0e989"
        assert response.data[1].name == "another-device"
