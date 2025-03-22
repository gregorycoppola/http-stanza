import pytest
from fastapi import status

def test_create_annotation(client, redis_mock, sample_annotation):
    # Create a proper annotation version
    version = {
        "version_id": "test-id",  # Will be overwritten by service
        "sentence": {
            "text": sample_annotation["text"],
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
    
    response = client.post("/api/annotations/create", json={"version": version})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "version" in data
    assert data["version"]["sentence"]["text"] == sample_annotation["text"]
    
    # Check Redis key
    key = f"http-stanza:sentence:{sample_annotation['text'].strip()}"
    assert redis_mock.exists(key)
    assert redis_mock.llen(key) == 1

def test_list_annotations(client, redis_mock, sample_annotation):
    # Create multiple annotations for the same sentence
    version = {
        "version_id": "test-id",
        "sentence": {
            "text": sample_annotation["text"],
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
        "created_at": "2024-01-01T00:00:00"
    }
    
    # Create 3 annotations
    for _ in range(3):
        client.post("/api/annotations/create", json={"version": version})
    
    # List annotations for the sentence
    response = client.get(f"/api/annotations/list?text={sample_annotation['text']}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["annotations"]) == 3
    assert all(a["sentence"]["text"] == sample_annotation["text"] for a in data["annotations"])

def test_list_annotations_empty(client):
    response = client.get("/api/annotations/list?text=nonexistent")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["annotations"]) == 0 