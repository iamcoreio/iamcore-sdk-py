from __future__ import annotations

import json
from typing import Optional
from unittest.mock import Mock

import pytest
from iamcore.irn import IRN
from pydantic import Field

from iamcore.client.models.base import (
    SEARCH_ALL_PAGE_SIZE,
    IAMCoreBaseModel,
    IAMException,
    IamIRNResponse,
    IamIRNsResponse,
    PaginatedSearchFilter,
    generic_search_all,
    to_snake_case,
)

# --- Testing IAMCoreBaseModel ---


class TestIAMCoreBaseModel:
    """Tests for the IAMCoreBaseModel."""

    class SimpleModel(IAMCoreBaseModel):
        """A concrete implementation for testing."""

        my_field: str = Field(..., alias="myField")
        optional_field: Optional[int] = Field(alias="optionalField", default=None)

    def test_from_dict(self) -> None:
        """Test model creation from a dict with camelCase keys."""
        data = {"my_field": "test_value", "optional_field": 123}
        model = self.SimpleModel.from_dict(data)
        assert model.my_field == "test_value"
        assert model.optional_field == 123

    def test_from_dict_with_aliasing(self) -> None:
        """Test model creation from a dict with camelCase keys."""
        data = {"myField": "test_value", "optionalField": 123}
        model = self.SimpleModel.from_dict(data)
        assert model.my_field == "test_value"
        assert model.optional_field == 123

    def test_from_json_with_aliasing(self) -> None:
        """Test model creation from JSON with camelCase keys."""
        data = {"myField": "test_value", "optionalField": 123}
        model = self.SimpleModel.from_json(json.dumps(data))
        assert model.my_field == "test_value"
        assert model.optional_field == 123

    def test_to_dict_with_aliasing(self) -> None:
        """Test model conversion to a dict uses camelCase aliases."""
        kwargs = {"my_field": "test", "optional_field": 456}
        model = self.SimpleModel(**kwargs)  # type: ignore
        expected_dict = {"myField": "test", "optionalField": 456}
        assert model.to_dict() == expected_dict

    def test_from_dict_handles_validation_error(self) -> None:
        """Test that from_dict raises IAMException on validation failure."""
        # 'myField' is missing
        data = {"optional_field": 123}
        with pytest.raises(IAMException, match="Validation error for SimpleModel"):
            self.SimpleModel.from_dict(data)

        # 'optionalField' has the wrong type
        data = {"my_field": "value", "optional_field": "not-an-int"}
        with pytest.raises(IAMException, match="Validation error for SimpleModel"):
            self.SimpleModel.from_dict(data)

    def test_from_dict_optional_field_with_default(self) -> None:
        data = {"my_field": "value"}
        model = self.SimpleModel.from_dict(data)
        assert model.my_field == "value"
        assert not model.optional_field

    def test_constructor_optional_field_with_default(self) -> None:
        model = self.SimpleModel(myField="value")
        assert model.my_field == "value"
        assert not model.optional_field


# --- Testing Utility Functions ---


@pytest.mark.parametrize(
    ("input_str", "expected_output"),
    [
        ("camelCase", "camel_case"),
        ("AnotherCamelCase", "another_camel_case"),
        ("already_snake_case", "already_snake_case"),
        ("PascalCase", "pascal_case"),
        ("field", "field"),
    ],
)
def test_to_snake_case(input_str: str, expected_output: str) -> None:
    """Test the to_snake_case utility function."""
    assert to_snake_case(input_str) == expected_output


# --- Testing Response Wrappers ---


class TestIamResponseModels:
    """Tests for the IamEntityResponse and IamEntitiesResponse wrappers."""

    def test_iam_irn_response(self) -> None:
        """Test the single IRN response wrapper."""

        irn_str = "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom"
        json_obj = {"irn": irn_str}
        response = IamIRNResponse(json_obj)

        assert isinstance(response.data, IRN)
        assert response.data.__str__() == irn_str

    def test_iam_irns_response(self) -> None:
        """Test the multiple IRNs response wrapper."""

        irn1_str = "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom"
        irn2_str = "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/jerry"
        json_list = [irn1_str, irn2_str]
        response = IamIRNsResponse(item=json_list, count=2, page=1, page_size=10)

        assert response.count == 2
        assert response.page == 1
        assert response.page_size == 10
        assert len(response.data) == 2
        assert all(isinstance(irn, IRN) for irn in response.data)
        assert response.data[0].__str__() == irn1_str
        assert response.data[1].__str__() == irn2_str


# --- Testing generic_search_all ---


class TestGenericSearchAll:
    """Tests for the generic_search_all pagination generator."""

    @pytest.mark.parametrize(
        "search_filter",
        [
            PaginatedSearchFilter(),
            PaginatedSearchFilter(pageSize=10),
        ],
    )
    def test_pagination_logic(self, search_filter: PaginatedSearchFilter) -> None:
        """Test that the generator pages through all results correctly."""
        # Setup
        mock_search_func = Mock()

        total_items = 2 * SEARCH_ALL_PAGE_SIZE
        irns = [f"irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/{i}" for i in range(1, total_items + 1)]

        # Define the responses for each page
        page1_response = IamIRNsResponse(
            item=irns[:SEARCH_ALL_PAGE_SIZE], count=total_items, page=1, page_size=SEARCH_ALL_PAGE_SIZE
        )
        page2_response = IamIRNsResponse(
            item=irns[SEARCH_ALL_PAGE_SIZE:], count=total_items, page=2, page_size=SEARCH_ALL_PAGE_SIZE
        )

        mock_search_func.side_effect = [page1_response, page2_response]

        # Execute
        results_generator = generic_search_all({}, mock_search_func, search_filter)
        results_list = list(results_generator)

        # Assert
        assert len(results_list) == total_items
        assert all(isinstance(irn, IRN) for irn in results_list)
        assert irns == [irn.__str__() for irn in results_list]
        assert mock_search_func.call_count == 2

    def test_with_no_initial_filter(self) -> None:
        """Test that a default filter is created and used."""
        mock_search_func = Mock()
        irn1_str = "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom"
        # Simulate a single page of results
        response = IamIRNsResponse(item=[irn1_str], count=1, page=1, page_size=SEARCH_ALL_PAGE_SIZE)
        mock_search_func.side_effect = [response]

        # Call with search_filter=None
        results_list = list(generic_search_all({}, mock_search_func, None))

        assert len(results_list) == 1
        assert mock_search_func.call_count == 1

        # Check that the first call used a default filter
        first_call_args = mock_search_func.call_args_list[0]
        called_filter = first_call_args[0][1]  # arg[1] of call(auth, filter)
        assert isinstance(called_filter, PaginatedSearchFilter)
        assert called_filter.page == 1
        assert called_filter.page_size == SEARCH_ALL_PAGE_SIZE
