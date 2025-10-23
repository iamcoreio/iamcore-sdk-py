from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.user.dto import (
    CreateUser,
    IamUserResponse,
    IamUsersResponse,
    UpdateUser,
    User,
    UserSearchFilter,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_user_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a User."""
    return {
        "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
        "created": "2021-10-18T08:47:54.219531Z",
        "updated": "2021-10-18T08:47:54.219531Z",
        "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
        "tenantID": "4atcicnisg",
        "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
        "email": "tom@example.com",
        "enabled": True,
        "firstName": "Tom",
        "lastName": "Jasper",
        "username": "tom",
        "path": "/org1",
        "metadata": {"language": "uk", "age": 23},
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
        "requiredActions": ["VERIFY_EMAIL"],
    }


@pytest.fixture
def sample_create_user_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating a User."""
    return {
        "firstName": "Tom",
        "lastName": "Jasper",
        "email": "tom@example.com",
        "enabled": True,
        "username": "tom",
        "password": "YesYkYKpLd6n3dVZ",
        "confirmPassword": "YesYkYKpLd6n3dVZ",
        "path": "/org1",
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
        "requiredActions": ["VERIFY_EMAIL"],
    }


@pytest.fixture
def sample_update_user_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for updating a User."""
    return {
        "firstName": "MorganUpdated",
        "lastName": "JosephUpdated",
        "email": "josephm@gmail.com",
        "enabled": True,
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
        "requiredActions": ["UPDATE_PASSWORD"],
    }


# Test the Core Data Model in Isolation
class TestUserModel:
    """Tests for the User Pydantic model."""

    def test_successful_validation(self, sample_user_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a User object.
        """
        # ACT
        user = User.model_validate(sample_user_data)

        # ASSERT
        assert user.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t"
        assert str(user.irn) == "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom"
        assert user.created == "2021-10-18T08:47:54.219531Z"
        assert user.updated == "2021-10-18T08:47:54.219531Z"
        assert user.tenant_id == "4atcicnisg"
        assert user.auth_id == "68a8372d-cc0a-4a42-8a56-099ac466e0bd"
        assert user.email == "tom@example.com"
        assert user.enabled is True
        assert user.first_name == "Tom"
        assert user.last_name == "Jasper"
        assert user.username == "tom"
        assert user.path == "/org1"
        assert user.metadata == {"language": "uk", "age": 23}
        assert user.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert user.required_actions == ["VERIFY_EMAIL"]

    def test_serialization_to_dict_uses_aliases(self, sample_user_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        user = User.model_validate(sample_user_data)

        # ACT
        user_dict = user.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert user_dict["tenantID"] == "4atcicnisg"
        assert user_dict["authID"] == "68a8372d-cc0a-4a42-8a56-099ac466e0bd"
        assert user_dict["firstName"] == "Tom"
        assert user_dict["lastName"] == "Jasper"
        assert user_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert user_dict["requiredActions"] == ["VERIFY_EMAIL"]
        assert "tenant_id" not in user_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_user_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_user_data["metadata"]  # Remove the optional field
        del sample_user_data["poolIDs"]  # Remove the optional field
        del sample_user_data["requiredActions"]  # Remove the optional field

        # ACT
        user = User.model_validate(sample_user_data)

        # ASSERT
        assert user.metadata is None
        assert user.pool_ids is None
        assert user.required_actions is None

    def test_raises_validation_error_for_missing_required_field(self, sample_user_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_user_data["id"]  # 'id' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            User.model_validate(sample_user_data)

        assert "Field required" in str(excinfo.value)


class TestCreateUserModel:
    """Tests for the CreateUser Pydantic model."""

    def test_successful_validation(self, sample_create_user_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreateUser object.
        """
        # ACT
        create_user = CreateUser.model_validate(sample_create_user_data)

        # ASSERT
        assert create_user.email == "tom@example.com"
        assert create_user.username == "tom"
        assert create_user.password == "YesYkYKpLd6n3dVZ"
        assert create_user.confirm_password == "YesYkYKpLd6n3dVZ"
        assert create_user.enabled is True
        assert create_user.first_name == "Tom"
        assert create_user.last_name == "Jasper"
        assert create_user.path == "/org1"
        assert create_user.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert create_user.required_actions == ["VERIFY_EMAIL"]

    def test_serialization_to_dict_uses_aliases(self, sample_create_user_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        create_user = CreateUser.model_validate(sample_create_user_data)

        # ACT
        create_dict = create_user.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert create_dict["firstName"] == "Tom"
        assert create_dict["lastName"] == "Jasper"
        assert create_dict["confirmPassword"] == "YesYkYKpLd6n3dVZ"
        assert create_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert create_dict["requiredActions"] == ["VERIFY_EMAIL"]
        assert "first_name" not in create_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_create_user_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_create_user_data["firstName"]  # Remove the optional field
        del sample_create_user_data["poolIDs"]  # Remove the optional field
        del sample_create_user_data["requiredActions"]  # Remove the optional field

        # ACT
        create_user = CreateUser.model_validate(sample_create_user_data)

        # ASSERT
        assert create_user.first_name is None
        assert create_user.pool_ids is None
        assert create_user.required_actions is None

    def test_raises_validation_error_for_missing_required_field(self, sample_create_user_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_create_user_data["email"]  # 'email' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreateUser.model_validate(sample_create_user_data)

        assert "Field required" in str(excinfo.value)


class TestUpdateUserModel:
    """Tests for the UpdateUser Pydantic model."""

    def test_successful_validation(self, sample_update_user_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an UpdateUser object.
        """
        # ACT
        update_user = UpdateUser.model_validate(sample_update_user_data)

        # ASSERT
        assert update_user.first_name == "MorganUpdated"
        assert update_user.last_name == "JosephUpdated"
        assert update_user.email == "josephm@gmail.com"
        assert update_user.enabled is True
        assert update_user.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert update_user.required_actions == ["UPDATE_PASSWORD"]

    def test_serialization_to_dict_uses_aliases(self, sample_update_user_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        update_user = UpdateUser.model_validate(sample_update_user_data)

        # ACT
        update_dict = update_user.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert update_dict["firstName"] == "MorganUpdated"
        assert update_dict["lastName"] == "JosephUpdated"
        assert update_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert update_dict["requiredActions"] == ["UPDATE_PASSWORD"]
        assert "first_name" not in update_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_update_user_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_update_user_data["firstName"]  # Remove the optional field
        del sample_update_user_data["poolIDs"]  # Remove the optional field
        del sample_update_user_data["requiredActions"]  # Remove the optional field

        # ACT
        update_user = UpdateUser.model_validate(sample_update_user_data)

        # ASSERT
        assert update_user.first_name is None
        assert update_user.pool_ids is None
        assert update_user.required_actions is None

    def test_raises_validation_error_for_missing_required_field(self, sample_update_user_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        # UpdateUser has no required fields beyond the defaults, so we'll test that it can be empty
        empty_data = {}

        # ACT
        update_user = UpdateUser.model_validate(empty_data)

        # ASSERT
        assert update_user.first_name is None
        assert update_user.last_name is None
        assert update_user.email is None
        assert update_user.enabled is True  # Default value
        assert update_user.pool_ids is None
        assert update_user.required_actions is None


class TestUserSearchFilterModel:
    """Tests for the UserSearchFilter Pydantic model."""

    def test_successful_validation(self) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a UserSearchFilter object.
        """
        # ARRANGE
        filter_data = {
            "email": "test@example.com",
            "path": "/org1",
            "firstName": "John",
            "lastName": "Doe",
            "username": "johndoe",
            "tenantId": "tenant123",
            "search": "query",
        }

        # ACT
        search_filter = UserSearchFilter.model_validate(filter_data)

        # ASSERT
        assert search_filter.email == "test@example.com"
        assert search_filter.path == "/org1"
        assert search_filter.first_name == "John"
        assert search_filter.last_name == "Doe"
        assert search_filter.username == "johndoe"
        assert search_filter.tenant_id == "tenant123"
        assert search_filter.search == "query"

    def test_handles_missing_optional_fields(self) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        filter_data = {}

        # ACT
        search_filter = UserSearchFilter.model_validate(filter_data)

        # ASSERT
        assert search_filter.email is None
        assert search_filter.path is None
        assert search_filter.first_name is None
        assert search_filter.last_name is None
        assert search_filter.username is None
        assert search_filter.tenant_id is None
        assert search_filter.search is None


# Test the Response Wrappers
class TestUserResponseWrappers:
    """Tests for the IamUserResponse and IamUsersResponse wrappers."""

    def test_iam_user_response_single_item(self, sample_user_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamUserResponse(sample_user_data)

        # ASSERT
        assert isinstance(response.data, User)
        assert response.data.username == "tom"

    def test_iam_users_response_multiple_items(self, sample_user_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second user for the list
        user_2_data = sample_user_data.copy()
        user_2_data["username"] = "jane"
        user_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvamFuZQ=="
        user_2_data["email"] = "jane@example.com"
        user_2_data["firstName"] = "Jane"
        user_2_data["lastName"] = "Smith"

        raw_list = [sample_user_data, user_2_data]

        # ACT
        response = IamUsersResponse(data=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated User objects
        assert isinstance(response.data[0], User)
        assert isinstance(response.data[1], User)
        assert response.data[0].username == "tom"
        assert response.data[1].username == "jane"
