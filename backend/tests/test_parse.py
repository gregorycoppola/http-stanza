import pytest
from fastapi import status

def test_parse_text(client, sample_parse_request):
    response = client.post("/parse", json=sample_parse_request)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "svg" in data
    assert "<svg" in data["svg"]
    assert "fox" in data["svg"]  # Check if the word is in the visualization

def test_parse_empty_text(client):
    response = client.post("/parse", json={"text": ""})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "<svg" in data["svg"]

def test_parse_invalid_input(client):
    response = client.post("/parse", json={"invalid": "input"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_parse_long_text(client):
    long_text = "The quick brown fox jumps over the lazy dog. " * 5
    response = client.post("/parse", json={"text": long_text})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "<svg" in data["svg"] 