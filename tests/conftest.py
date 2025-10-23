import pytest
import responses

from tests.fixtures.mock_server import setup_mock_server


@pytest.fixture
def mock_iamcore_api():
    with responses.RequestsMock() as rsps:
        setup_mock_server()
        yield rsps
