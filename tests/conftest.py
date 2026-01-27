import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_dynamo_resource(mocker):
    """Mock DynamoDB resource"""
    mock = mocker.patch("boto3.resource")
    return mock

@pytest.fixture
def mock_dynamo_table(mocker):
    """Mock generic DynamoDB table"""
    mock_table = MagicMock()
    mocker.patch("app.db.dynamo.get_table", return_value=mock_table)
    return mock_table
