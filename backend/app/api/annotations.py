from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.annotations import (
    CreateAnnotationRequest,
    AnnotationResponse,
    UpdateAnnotationRequest,
    ListVersionsResponse
)
from ..services import annotations

router = APIRouter(prefix="/annotations", tags=["annotations"])

@router.post("/", response_model=AnnotationResponse)
async def create_new_annotation(request: CreateAnnotationRequest):
    annotation_id, version = annotations.create_annotation(request.text)
    return AnnotationResponse(
        annotation_id=annotation_id,
        latest_version=version
    )

@router.get("/{annotation_id}", response_model=AnnotationResponse)
async def get_annotation(annotation_id: str):
    version = annotations.get_annotation(annotation_id)
    if not version:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return AnnotationResponse(
        annotation_id=annotation_id,
        latest_version=version
    )

@router.put("/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(annotation_id: str, request: UpdateAnnotationRequest):
    version = annotations.update_annotation(annotation_id, request.text)
    if not version:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return AnnotationResponse(
        annotation_id=annotation_id,
        latest_version=version
    )

@router.delete("/{annotation_id}")
async def delete_annotation(annotation_id: str):
    if not annotations.delete_annotation(annotation_id):
        raise HTTPException(status_code=404, detail="Annotation not found")
    return {"status": "success"}

@router.get("/{annotation_id}/versions", response_model=ListVersionsResponse)
async def list_versions(annotation_id: str):
    versions = annotations.list_annotation_versions(annotation_id)
    if not versions:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return ListVersionsResponse(versions=versions)

@router.get("/", response_model=List[str])
async def list_annotations():
    return annotations.list_annotations() 