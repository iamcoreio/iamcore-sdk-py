from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.application.dto import (
    Application,
    CreateApplication,
    IamApplicationResponse,
    IamApplicationsResponse,
    UpdateApplication,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_application_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for an Application."""
    return {
        "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
        "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
        "name": "myapp",
        "displayName": "My app name",
        "created": "2021-10-18T12:27:15.55267632Z",
        "updated": "2021-10-18T12:27:15.55267632Z",
    }


@pytest.fixture
def sample_create_application_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating an Application."""
    return {
        "name": "myapp",
        "displayName": "My app name",
    }


@pytest.fixture
def sample_update_application_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for updating an Application."""
    return {
        "displayName": "New display name",
    }


# Test the Core Data Model in Isolation
class TestApplicationModel:
    """Tests for the Application Pydantic model."""

    def test_successful_validation(self, sample_application_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an Application object.
        """
        # ACT
        application = Application.model_validate(sample_application_data)

        # ASSERT
        assert application.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert str(application.irn) == "irn:rc73dbh7q0:iamcore:::application/myapp"
        assert application.name == "myapp"
        assert application.display_name == "My app name"
        assert application.created == "2021-10-18T12:27:15.55267632Z"
        assert application.updated == "2021-10-18T12:27:15.55267632Z"

    def test_serialization_to_dict_uses_aliases(self, sample_application_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        application = Application.model_validate(sample_application_data)

        # ACT
        app_dict = application.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert app_dict["id"] == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert str(app_dict["irn"]) == "irn:rc73dbh7q0:iamcore:::application/myapp"
        assert app_dict["name"] == "myapp"
        assert app_dict["displayName"] == "My app name"
        assert app_dict["created"] == "2021-10-18T12:27:15.55267632Z"
        assert app_dict["updated"] == "2021-10-18T12:27:15.55267632Z"
        assert "display_name" not in app_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(self, sample_application_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_application_data["id"]  # 'id' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            Application.model_validate(sample_application_data)

        assert "Field required" in str(excinfo.value)


class TestCreateApplicationModel:
    """Tests for the CreateApplication Pydantic model."""

    def test_successful_validation_with_all_fields(self, sample_create_application_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreateApplication object.
        """
        # ACT
        create_app = CreateApplication.model_validate(sample_create_application_data)

        # ASSERT
        assert create_app.name == "myapp"
        assert create_app.display_name == "My app name"

    def test_successful_validation_with_minimal_fields(self) -> None:
        """
        Tests that CreateApplication can be created with only required fields.
        """
        # ARRANGE
        minimal_data = {"name": "minimal-app"}

        # ACT
        create_app = CreateApplication.model_validate(minimal_data)

        # ASSERT
        assert create_app.name == "minimal-app"
        assert create_app.display_name is None

    def test_serialization_to_dict_uses_aliases(self, sample_create_application_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        create_app = CreateApplication.model_validate(sample_create_application_data)

        # ACT
        app_dict = create_app.to_dict()

        # ASSERT
        assert app_dict["name"] == "myapp"
        assert app_dict["displayName"] == "My app name"
        assert "display_name" not in app_dict

    def test_handles_missing_optional_fields(self) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        data_without_display_name = {"name": "app-without-display"}

        # ACT
        create_app = CreateApplication.model_validate(data_without_display_name)

        # ASSERT
        assert create_app.display_name is None

    def test_raises_validation_error_for_missing_required_field(self) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        data_without_name = {"displayName": "App without name"}

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreateApplication.model_validate(data_without_name)

        assert "Field required" in str(excinfo.value)


class TestUpdateApplicationModel:
    """Tests for the UpdateApplication Pydantic model."""

    def test_successful_validation(self, sample_update_application_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an UpdateApplication object.
        """
        # ACT
        update_app = UpdateApplication.model_validate(sample_update_application_data)

        # ASSERT
        assert update_app.display_name == "New display name"

    def test_serialization_to_dict_uses_aliases(self, sample_update_application_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        update_app = UpdateApplication.model_validate(sample_update_application_data)

        # ACT
        update_dict = update_app.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert update_dict["displayName"] == "New display name"
        assert "display_name" not in update_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(self) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        empty_data = {}

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            UpdateApplication.model_validate(empty_data)

        assert "Field required" in str(excinfo.value)


# Test the Response Wrappers
class TestApplicationResponseWrappers:
    """Tests for the IamApplicationResponse and IamApplicationsResponse wrappers."""

    def test_iam_application_response_single_item(self, sample_application_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamApplicationResponse(sample_application_data)

        # ASSERT
        assert isinstance(response.data, Application)
        assert response.data.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert response.data.name == "myapp"
        assert response.data.display_name == "My app name"

    def test_iam_applications_response_multiple_items(self, sample_application_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second application for the list
        app_2_data = sample_application_data.copy()
        app_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL2Fub3RoZXJhcHA="
        app_2_data["name"] = "anotherapp"
        app_2_data["displayName"] = "Another App"
        app_2_data["irn"] = "irn:rc73dbh7q0:iamcore:::application/anotherapp"

        raw_list = [sample_application_data, app_2_data]

        # ACT
        response = IamApplicationsResponse(data=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated Application objects
        assert isinstance(response.data[0], Application)
        assert isinstance(response.data[1], Application)
        assert response.data[0].id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw"
        assert response.data[0].name == "myapp"
        assert response.data[1].id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL2Fub3RoZXJhcHA="
        assert response.data[1].name == "anotherapp"
