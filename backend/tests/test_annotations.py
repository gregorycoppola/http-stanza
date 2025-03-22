import pytest
from fastapi import status

def test_create_annotation(client, redis_mock, sample_annotation):
    response = client.post("/annotations", json=sample_annotation)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "annotation_id" in data
    assert "latest_version" in data
    assert data["latest_version"]["sentence"]["text"] == sample_annotation["text"]
    
    # Check Redis keys
    annotation_id = data["annotation_id"]
    assert redis_mock.exists(f"http-stanza:annotations:{annotation_id}")
    assert redis_mock.exists(f"http-stanza:annotations:{annotation_id}:versions")
    assert redis_mock.sismember("http-stanza:annotations", annotation_id)

def test_get_annotation(client, redis_mock, sample_annotation):
    # First create an annotation
    create_response = client.post("/annotations", json=sample_annotation)
    annotation_id = create_response.json()["annotation_id"]
    
    # Then get it
    response = client.get(f"/annotations/{annotation_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["annotation_id"] == annotation_id
    assert data["latest_version"]["sentence"]["text"] == sample_annotation["text"]

def test_get_nonexistent_annotation(client):
    response = client.get("/annotations/nonexistent-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_annotation(client, redis_mock, sample_annotation):
    # First create an annotation
    create_response = client.post("/annotations", json=sample_annotation)
    annotation_id = create_response.json()["annotation_id"]
    
    # Update it with new text
    new_text = "A different sentence for testing."
    update_response = client.put(f"/annotations/{annotation_id}", json={"text": new_text})
    
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["latest_version"]["sentence"]["text"] == new_text
    
    # Check that versions were created
    versions = redis_mock.lrange(f"http-stanza:annotations:{annotation_id}:versions", 0, -1)
    assert len(versions) == 2  # Original + update

def test_update_nonexistent_annotation(client):
    response = client.put("/annotations/nonexistent-id", json={"text": "new text"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_annotation(client, redis_mock, sample_annotation):
    # First create an annotation
    create_response = client.post("/annotations", json=sample_annotation)
    annotation_id = create_response.json()["annotation_id"]
    
    # Delete it
    response = client.delete(f"/annotations/{annotation_id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"
    
    # Verify it's deleted
    get_response = client.get(f"/annotations/{annotation_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_list_annotations(client, redis_mock, sample_annotation):
    # Create multiple annotations
    annotation_ids = []
    for _ in range(3):
        response = client.post("/annotations", json=sample_annotation)
        annotation_ids.append(response.json()["annotation_id"])
    
    # List all annotations
    response = client.get("/annotations")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    assert all(id in data for id in annotation_ids)

def test_list_versions(client, redis_mock, sample_annotation):
    # Create an annotation
    create_response = client.post("/annotations", json=sample_annotation)
    annotation_id = create_response.json()["annotation_id"]
    
    # Update it multiple times
    for _ in range(2):
        client.put(f"/annotations/{annotation_id}", json={"text": "Updated text"})
    
    # List versions
    response = client.get(f"/annotations/{annotation_id}/versions")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["versions"]) == 3  # Original + 2 updates 