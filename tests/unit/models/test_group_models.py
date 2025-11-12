from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.group.dto import (
    CreateGroup,
    Group,
    IamGroupResponse,
    IamGroupsResponse,
    UpdateGroup,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_group_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a Group."""
    return {
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


@pytest.fixture
def sample_create_group_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating a Group."""
    return {
        "name": "java",
        "displayName": "Java",
        "parentID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXY=",
        "tenantID": "4atcicnisg",
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
    }


@pytest.fixture
def sample_update_group_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for updating a Group."""
    return {
        "displayName": "updated org1",
        "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
    }


# Test the Core Data Model in Isolation
class TestGroupModel:
    """Tests for the Group Pydantic model."""

    def test_successful_validation(self, sample_group_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a Group object.
        """
        # ACT
        group = Group.model_validate(sample_group_data)

        # ASSERT
        assert group.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ=="
        assert str(group.irn) == "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java"
        assert group.tenant_id == "4atcicnisg"
        assert group.name == "java"
        assert group.display_name == "Java"
        assert group.path == "/dev"
        assert group.metadata == {"location": "Kyiv"}
        assert group.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert group.created == "2021-10-18T11:08:09.4919Z"

    def test_serialization_to_dict_uses_aliases(self, sample_group_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        group = Group.model_validate(sample_group_data)

        # ACT
        group_dict = group.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert group_dict["tenantID"] == "4atcicnisg"
        assert group_dict["displayName"] == "Java"
        assert group_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert "tenant_id" not in group_dict  # The snake_case attribute name should not be a key

    def test_raises_validation_error_for_missing_required_field(self, sample_group_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_group_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            Group.model_validate(sample_group_data)

        assert "Field required" in str(excinfo.value)


class TestCreateGroupModel:
    """Tests for the CreateGroup Pydantic model."""

    def test_successful_validation(self, sample_create_group_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreateGroup object.
        """
        # ACT
        create_group = CreateGroup.model_validate(sample_create_group_data)

        # ASSERT
        assert create_group.name == "java"
        assert create_group.display_name == "Java"
        assert create_group.parent_id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXY="
        assert create_group.tenant_id == "4atcicnisg"
        assert create_group.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    def test_serialization_to_dict_uses_aliases(self, sample_create_group_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        create_group = CreateGroup.model_validate(sample_create_group_data)

        # ACT
        create_dict = create_group.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert create_dict["displayName"] == "Java"
        assert create_dict["parentID"] == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXY="
        assert create_dict["tenantID"] == "4atcicnisg"
        assert create_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert "display_name" not in create_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_create_group_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_create_group_data["displayName"]  # Remove the optional field

        # ACT
        create_group = CreateGroup.model_validate(sample_create_group_data)

        # ASSERT
        assert create_group.display_name is None

    def test_raises_validation_error_for_missing_required_field(self, sample_create_group_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_create_group_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreateGroup.model_validate(sample_create_group_data)

        assert "Field required" in str(excinfo.value)


class TestUpdateGroupModel:
    """Tests for the UpdateGroup Pydantic model."""

    def test_successful_validation(self, sample_update_group_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an UpdateGroup object.
        """
        # ACT
        update_group = UpdateGroup.model_validate(sample_update_group_data)

        # ASSERT
        assert update_group.display_name == "updated org1"
        assert update_group.pool_ids == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]

    def test_serialization_to_dict_uses_aliases(self, sample_update_group_data: dict[str, Any]) -> None:
        """
        Tests that the model_dump(by_alias=True) correctly uses camelCase aliases.
        """
        # ARRANGE
        update_group = UpdateGroup.model_validate(sample_update_group_data)

        # ACT
        update_dict = update_group.model_dump(by_alias=True)

        # ASSERT
        # The output dictionary should have camelCase keys
        assert update_dict["displayName"] == "updated org1"
        assert update_dict["poolIDs"] == ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="]
        assert "display_name" not in update_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_update_group_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_update_group_data["poolIDs"]  # Remove the optional field

        # ACT
        update_group = UpdateGroup.model_validate(sample_update_group_data)

        # ASSERT
        assert update_group.pool_ids is None

    def test_raises_validation_error_for_missing_required_field(self, sample_update_group_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_update_group_data["displayName"]  # 'displayName' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            UpdateGroup.model_validate(sample_update_group_data)

        assert "Field required" in str(excinfo.value)


# Test the Response Wrappers
class TestGroupResponseWrappers:
    """Tests for the IamGroupResponse and IamGroupsResponse wrappers."""

    def test_iam_group_response_single_item(self, sample_group_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamGroupResponse(**{"data": sample_group_data})

        # ASSERT
        assert isinstance(response.data, Group)
        assert response.data.name == "java"

    def test_iam_groups_response_multiple_items(self, sample_group_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second group for the list
        group_2_data = sample_group_data.copy()
        group_2_data["name"] = "python"
        group_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvcHl0aG9u"

        raw_list = [sample_group_data, group_2_data]

        # ACT
        response = IamGroupsResponse(
            data=[Group.model_validate(item) for item in raw_list], count=2, page=1, pageSize=10
        )

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated Group objects
        assert isinstance(response.data[0], Group)
        assert isinstance(response.data[1], Group)
        assert response.data[0].name == "java"
        assert response.data[1].name == "python"
