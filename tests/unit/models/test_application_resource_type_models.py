from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.application_resource_type.dto import (
    ApplicationResourceType,
    CreateApplicationResourceType,
    IamApplicationResourceTypeResponse,
    IamApplicationResourceTypesResponse,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_application_resource_type_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for an ApplicationResourceType."""
    return {
        "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
        "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
        "type": "document",
        "description": "Representation of the 'document' resource type",
        "actionPrefix": "document",
        "created": "2021-10-18T12:27:15.55267632Z",
        "updated": "2021-10-18T12:27:15.55267632Z",
        "operations": ["sign", "export"],
    }


@pytest.fixture
def sample_create_application_resource_type_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating an ApplicationResourceType."""
    return {
        "type": "document",
        "description": "Representation of the 'document' resource type",
        "actionPrefix": "document",
        "operations": ["sign", "export"],
    }


# Test the Core Data Model in Isolation
class TestApplicationResourceTypeModel:
    """Tests for the ApplicationResourceType Pydantic model."""

    def test_successful_validation(self, sample_application_resource_type_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an ApplicationResourceType object.
        """
        # ACT
        resource_type = ApplicationResourceType.model_validate(sample_application_resource_type_data)

        # ASSERT
        assert resource_type.id == "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50"
        assert str(resource_type.irn) == "irn:rc73dbh7q0:myapp:::resource-type/document"
        assert resource_type.type == "document"
        assert resource_type.description == "Representation of the 'document' resource type"
        assert resource_type.action_prefix == "document"
        assert resource_type.operations == ["sign", "export"]
        assert resource_type.created == "2021-10-18T12:27:15.55267632Z"

    def test_serialization_to_dict_uses_aliases(self, sample_application_resource_type_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        resource_type = ApplicationResourceType.model_validate(sample_application_resource_type_data)

        # ACT
        resource_dict = resource_type.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert resource_dict["actionPrefix"] == "document"
        assert "action_prefix" not in resource_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(
        self, sample_application_resource_type_data: dict[str, Any]
    ) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_application_resource_type_data["type"]  # 'type' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            ApplicationResourceType.model_validate(sample_application_resource_type_data)

        assert "Field required" in str(excinfo.value)


class TestCreateApplicationResourceTypeModel:
    """Tests for the CreateApplicationResourceType Pydantic model."""

    def test_successful_validation(self, sample_create_application_resource_type_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreateApplicationResourceType object.
        """
        # ACT
        create_resource_type = CreateApplicationResourceType.model_validate(
            sample_create_application_resource_type_data
        )

        # ASSERT
        assert create_resource_type.type == "document"
        assert create_resource_type.description == "Representation of the 'document' resource type"
        assert create_resource_type.action_prefix == "document"
        assert create_resource_type.operations == ["sign", "export"]

    def test_serialization_to_dict_uses_aliases(
        self, sample_create_application_resource_type_data: dict[str, Any]
    ) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        create_resource_type = CreateApplicationResourceType.model_validate(
            sample_create_application_resource_type_data
        )

        # ACT
        create_dict = create_resource_type.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert create_dict["actionPrefix"] == "document"
        assert "action_prefix" not in create_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(
        self, sample_create_application_resource_type_data: dict[str, Any]
    ) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_create_application_resource_type_data["description"]  # Remove the optional field

        # ACT
        create_resource_type = CreateApplicationResourceType.model_validate(
            sample_create_application_resource_type_data
        )

        # ASSERT
        assert create_resource_type.description is None

    def test_raises_validation_error_for_missing_required_field(
        self, sample_create_application_resource_type_data: dict[str, Any]
    ) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_create_application_resource_type_data["type"]  # 'type' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreateApplicationResourceType.model_validate(sample_create_application_resource_type_data)

        assert "Field required" in str(excinfo.value)


# Test the Response Wrappers
class TestApplicationResourceTypeResponseWrappers:
    """Tests for the IamApplicationResourceTypeResponse and IamApplicationResourceTypesResponse wrappers."""

    def test_iam_application_resource_type_response_single_item(
        self, sample_application_resource_type_data: dict[str, Any]
    ) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamApplicationResourceTypeResponse(sample_application_resource_type_data)

        # ASSERT
        assert isinstance(response.data, ApplicationResourceType)
        assert response.data.type == "document"

    def test_iam_application_resource_types_response_multiple_items(
        self, sample_application_resource_type_data: dict[str, Any]
    ) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second resource type for the list
        resource_type_2_data = sample_application_resource_type_data.copy()
        resource_type_2_data["type"] = "image"
        resource_type_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2ltYWdl"

        raw_list = [sample_application_resource_type_data, resource_type_2_data]

        # ACT
        response = IamApplicationResourceTypesResponse(data=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated ApplicationResourceType objects
        assert isinstance(response.data[0], ApplicationResourceType)
        assert isinstance(response.data[1], ApplicationResourceType)
        assert response.data[0].type == "document"
        assert response.data[1].type == "image"
