import pytest
from fastapi.testclient import TestClient
from app.main import app
from fakeredis import FakeRedis
from unittest.mock import patch

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def redis_mock():
    fake_redis = FakeRedis(decode_responses=True)
    with patch('app.core.redis.redis_client', fake_redis):
        yield fake_redis

@pytest.fixture(scope="function")
def sample_annotation():
    return {
        "text": "The quick brown fox jumps over the lazy dog."
    }

@pytest.fixture(scope="function")
def sample_parse_request():
    return {
        "text": "The quick brown fox jumps over the lazy dog."
    } 