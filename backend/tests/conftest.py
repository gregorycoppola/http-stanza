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
        # Clear all keys after each test
        fake_redis.flushall()

@pytest.fixture(scope="function")
def sample_annotation():
    return {
        "version": {
            "version_id": "test-id",  # Will be overwritten by service
            "sentence": {
                "text": "The quick brown fox jumps over the lazy dog.",
                "tokens": [
                    {
                        "id": 0,
                        "text": "The",
                        "pos": "DET",
                        "head": 1,
                        "dep": "det"
                    }
                ]
            },
            "created_at": "2024-01-01T00:00:00"  # Will be overwritten by service
        }
    } 