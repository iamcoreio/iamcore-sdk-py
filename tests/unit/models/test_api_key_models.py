from typing import Any

import pytest
from pydantic import ValidationError

# Import the models you want to test
from iamcore.client.api_key import ApiKey, IamApiKeyResponse, IamApiKeysResponse


# Use a fixture to provide clean, reusable test data
@pytest.fixture
def sample_api_key_data() -> dict[str, Any]:
    """Provides a sample raw API response dictionary for an ApiKey."""
    return {
        "apiKey": "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14",
        "state": "active",
        "lastUsed": "2021-10-19T17:57:31.14492667Z",
        "created": "2021-10-18T12:27:15.55267632Z",
        "updated": "2021-10-18T12:27:15.55267632Z",
    }


# Test the Core Data Model in Isolation
class TestApiKeyModel:
    """Tests for the ApiKey Pydantic model."""

    def test_successful_validation(self, sample_api_key_data: dict[str, Any]) -> None:
        """
        Tests that a valid dictionary is correctly parsed into an ApiKey object.
        """
        # ACT
        api_key = ApiKey.model_validate(sample_api_key_data)

        # ASSERT
        assert api_key.api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14"
        assert api_key.state == "active"
        assert api_key.last_used == "2021-10-19T17:57:31.14492667Z"
        assert api_key.created == "2021-10-18T12:27:15.55267632Z"

    def test_serialization_to_dict_uses_aliases(self, sample_api_key_data: dict[str, Any]) -> None:
        """
        Tests that the to_dict() method correctly uses camelCase aliases.
        """
        # ARRANGE
        api_key = ApiKey.model_validate(sample_api_key_data)

        # ACT
        key_dict = api_key.to_dict()

        # ASSERT
        # The output dictionary should have camelCase keys
        assert key_dict["apiKey"] == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14"
        assert key_dict["lastUsed"] == "2021-10-19T17:57:31.14492667Z"
        assert "api_key" not in key_dict  # The snake_case attribute name should not be a key

    def test_handles_missing_optional_fields(self, sample_api_key_data: dict[str, Any]) -> None:
        """
        Tests that optional fields can be omitted from the input data.
        """
        # ARRANGE
        del sample_api_key_data["lastUsed"]  # Remove the optional field

        # ACT
        api_key = ApiKey.model_validate(sample_api_key_data)

        # ASSERT
        assert api_key.last_used is None

    def test_raises_validation_error_for_missing_required_field(self, sample_api_key_data: dict[str, Any]) -> None:
        """
        Tests that Pydantic raises a ValidationError if a required field is missing.
        """
        # ARRANGE
        del sample_api_key_data["apiKey"]  # 'apiKey' is a required field

        # ACT & ASSERT
        with pytest.raises(ValidationError) as excinfo:
            ApiKey.model_validate(sample_api_key_data)

        assert "Field required" in str(excinfo.value)


# Test the Response Wrappers
class TestApiResponseWrappers:
    """Tests for the IamApiKeyResponse and IamApiKeysResponse wrappers."""

    def test_iam_api_key_response_single_item(self, sample_api_key_data: dict[str, Any]) -> None:
        """
        Tests that the single-item response wrapper correctly converts a raw dict.
        """
        # ACT
        response = IamApiKeyResponse(sample_api_key_data)

        # ASSERT
        assert isinstance(response.data, ApiKey)
        assert response.data.api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14"

    def test_iam_api_keys_response_multiple_items(self, sample_api_key_data: dict[str, Any]) -> None:
        """
        Tests that the list response wrapper correctly converts a list of raw dicts.
        """
        # ARRANGE
        # Create a second API key for the list
        api_key_2_data = sample_api_key_data.copy()
        api_key_2_data["apiKey"] = "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga15"

        raw_list = [sample_api_key_data, api_key_2_data]

        # ACT
        response = IamApiKeysResponse(item=raw_list, count=2, page=1, page_size=10)

        # ASSERT
        assert response.count == 2
        assert response.page == 1
        assert len(response.data) == 2

        # Verify that the list contains fully validated ApiKey objects
        assert isinstance(response.data[0], ApiKey)
        assert isinstance(response.data[1], ApiKey)
        assert response.data[0].api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14"
        assert response.data[1].api_key == "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga15"
