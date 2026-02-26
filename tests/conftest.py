import pytest

@pytest.fixture
def mock_httpx_client(mocker):
    """Fixture to mock httpx.Client"""
    mock_client = mocker.patch('httpx.Client')
    return mock_client
