from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.policy.dto import (
    CreatePolicy,
    IamPoliciesResponse,
    IamPolicyResponse,
    Policy,
    PolicyStatement,
    UpdatePolicy,
)


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_policy_statement_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a PolicyStatement."""
    return {
        "effect": "allow",
        "description": "Allow all actions on Jerry",
        "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
        "actions": ["iamcore:user:*"],
    }


@pytest.fixture
def sample_policy_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for a Policy."""
    return {
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


@pytest.fixture
def sample_create_policy_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for creating a Policy."""
    return {
        "name": "allow-all-actions-on-jerry",
        "level": "tenant",
        "description": "Allow all actions on Jerry",
        "statements": [
            {
                "effect": "allow",
                "description": "Allow all actions on Jerry",
                "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                "actions": ["iamcore:user:*"],
            }
        ],
    }


@pytest.fixture
def sample_update_policy_data() -> dict[str, Any]:
    """Provides a sample raw API request dictionary for updating a Policy."""
    return {
        "description": "Allow all actions on Jerry",
        "statements": [
            {
                "effect": "allow",
                "description": "Allow all actions on Jerry",
                "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                "actions": ["iamcore:user:*"],
            }
        ],
    }


# Test the Core Data Model in Isolation
class TestPolicyStatementModel:
    """Tests for the PolicyStatement Pydantic model."""

    def test_successful_validation(self, sample_policy_statement_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a PolicyStatement object.
        """
        # ACT
        statement = PolicyStatement.model_validate(sample_policy_statement_data)

        # ASSERT
        assert statement.effect == "allow"
        assert statement.description == "Allow all actions on Jerry"
        assert len(statement.resources) == 1
        assert str(statement.resources[0]) == "irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"
        assert statement.actions == ["iamcore:user:*"]

    def test_raises_validation_error_for_missing_required_field(
        self, sample_policy_statement_data: dict[str, Any]
    ) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_policy_statement_data["effect"]  # 'effect' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            PolicyStatement.model_validate(sample_policy_statement_data)

        assert "Field required" in str(excinfo.value)


class TestPolicyModel:
    """Tests for the Policy Pydantic model."""

    def test_successful_validation(self, sample_policy_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a Policy object.
        """
        # ACT
        policy = Policy.model_validate(sample_policy_data)

        # ASSERT
        assert (
            policy.id == "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk="
        )
        assert str(policy.irn) == "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry"
        assert policy.name == "allow-all-actions-on-jerry"
        assert policy.description == "Allow all actions on Jerry"
        assert policy.type == "identity"
        assert policy.origin == "api"
        assert policy.version == "1.0.0"
        assert len(policy.statements) == 1
        assert policy.statements[0].effect == "allow"

    def test_serialization_to_dict_uses_aliases(self, sample_policy_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        policy = Policy.model_validate(sample_policy_data)

        # ACT
        policy_dict = policy.to_dict()

        # ASSERT
        # Policy doesn't have aliases, but statements might
        assert policy_dict["name"] == "allow-all-actions-on-jerry"
        assert "statements" in policy_dict

    def test_raises_validation_error_for_missing_required_field(self, sample_policy_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_policy_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            Policy.model_validate(sample_policy_data)

        assert "Field required" in str(excinfo.value)


class TestCreatePolicyModel:
    """Tests for the CreatePolicy Pydantic model."""

    def test_successful_validation(self, sample_create_policy_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into a CreatePolicy object.
        """
        # ACT
        create_policy = CreatePolicy.model_validate(sample_create_policy_data)

        # ASSERT
        assert create_policy.name == "allow-all-actions-on-jerry"
        assert create_policy.level == "tenant"
        assert create_policy.description == "Allow all actions on Jerry"
        assert len(create_policy.statements) == 1
        assert create_policy.statements[0].effect == "allow"

    def test_serialization_to_dict_uses_aliases(self, sample_create_policy_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        sample_create_policy_data["tenantID"] = "4atcicnisg"  # Add tenantID to test alias
        create_policy = CreatePolicy.model_validate(sample_create_policy_data)

        # ACT
        create_dict = create_policy.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert create_dict["tenantID"] == "4atcicnisg"
        assert "tenant_id" not in create_dict  # The snake_case attribute name should not be a key
        assert "name" in create_dict

    def test_handles_missing_optional_fields(self, sample_create_policy_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        # tenantID is not in the fixture, so it's None by default

        # ACT
        create_policy = CreatePolicy.model_validate(sample_create_policy_data)

        # ASSERT
        assert create_policy.tenant_id is None

    def test_with_statement_method(self, sample_create_policy_data: dict[str, Any]) -> None:
        """
        Tests the with_statement method for adding statements.
        """
        # ARRANGE
        create_policy = CreatePolicy.model_validate(sample_create_policy_data)
        initial_statements = len(create_policy.statements)

        # ACT
        create_policy.with_statement(
            effect="deny",
            description="Deny some action",
            resources=["irn:rc73dbh7q0:iamcore:4atcicnisg::user/bob"],
            actions=["iamcore:user:read"],
        )

        # ASSERT
        assert len(create_policy.statements) == initial_statements + 1
        new_statement = create_policy.statements[-1]
        assert new_statement.effect == "deny"
        assert new_statement.description == "Deny some action"
        assert len(new_statement.resources) == 1
        assert str(new_statement.resources[0]) == "irn:rc73dbh7q0:iamcore:4atcicnisg::user/bob"
        assert new_statement.actions == ["iamcore:user:read"]

    def test_raises_validation_error_for_missing_required_field(
        self, sample_create_policy_data: dict[str, Any]
    ) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_create_policy_data["name"]  # 'name' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            CreatePolicy.model_validate(sample_create_policy_data)

        assert "Field required" in str(excinfo.value)


class TestUpdatePolicyModel:
    """Tests for the UpdatePolicy Pydantic model."""

    def test_successful_validation(self, sample_update_policy_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an UpdatePolicy object.
        """
        # ACT
        update_policy = UpdatePolicy.model_validate(sample_update_policy_data)

        # ASSERT
        assert update_policy.description == "Allow all actions on Jerry"
        assert len(update_policy.statements) == 1
        assert update_policy.statements[0].effect == "allow"

    def test_serialization_to_dict_uses_aliases(self, sample_update_policy_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        sample_update_policy_data["poolIDs"] = ["pool1"]  # Add poolIDs to test alias
        update_policy = UpdatePolicy.model_validate(sample_update_policy_data)

        # ACT
        update_dict = update_policy.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert update_dict["poolIDs"] == ["pool1"]
        assert "pool_ids" not in update_dict  # The snake_case attribute name should not be a key
        assert "description" in update_dict

    def test_handles_missing_optional_fields(self, sample_update_policy_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        # poolIDs is not in the fixture, so it's None by default

        # ACT
        update_policy = UpdatePolicy.model_validate(sample_update_policy_data)

        # ASSERT
        assert update_policy.pool_ids is None

    def test_with_statement_method(self, sample_update_policy_data: dict[str, Any]) -> None:
        """
        Tests the with_statement method for adding statements.
        """
        # ARRANGE
        update_policy = UpdatePolicy.model_validate(sample_update_policy_data)
        initial_statements = len(update_policy.statements)

        # ACT
        update_policy.with_statement(
            effect="deny",
            description="Deny some action",
            resources=["irn:rc73dbh7q0:iamcore:4atcicnisg::user/bob"],
            actions=["iamcore:user:read"],
        )

        # ASSERT
        assert len(update_policy.statements) == initial_statements + 1
        new_statement = update_policy.statements[-1]
        assert new_statement.effect == "deny"
        assert new_statement.description == "Deny some action"
        assert len(new_statement.resources) == 1
        assert str(new_statement.resources[0]) == "irn:rc73dbh7q0:iamcore:4atcicnisg::user/bob"
        assert new_statement.actions == ["iamcore:user:read"]

    def test_raises_validation_error_for_missing_required_field(
        self, sample_update_policy_data: dict[str, Any]
    ) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_update_policy_data["description"]  # 'description' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            UpdatePolicy.model_validate(sample_update_policy_data)

        assert "Field required" in str(excinfo.value)


# Test the Response Wrappers
class TestPolicyResponseWrappers:
    """Tests for the IamPolicyResponse and IamPoliciesResponse wrappers."""

    def test_iam_policy_response_single_item(self, sample_policy_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamPolicyResponse(sample_policy_data)

        # ASSERT
        assert isinstance(response.data, Policy)
        assert response.data.name == "allow-all-actions-on-jerry"

    def test_iam_policies_response_multiple_items(self, sample_policy_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second policy for the list
        policy_2_data = sample_policy_data.copy()
        policy_2_data["name"] = "deny-all-actions"
        policy_2_data["id"] = "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvZGVueS1hbGwtYWN0aW9ucw=="

        raw_list = [sample_policy_data, policy_2_data]

        # ACT
        response = IamPoliciesResponse(item=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated Policy objects
        assert isinstance(response.data[0], Policy)
        assert isinstance(response.data[1], Policy)
        assert response.data[0].name == "allow-all-actions-on-jerry"
        assert response.data[1].name == "deny-all-actions"
