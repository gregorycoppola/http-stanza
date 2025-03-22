from fastapi import APIRouter
from typing import List
from ..schemas.annotations import (
    CreateAnnotationRequest,
    AnnotationResponse,
    ListAnnotationsResponse
)
from ..services import annotations

router = APIRouter(prefix="/api/annotations", tags=["annotations"])

@router.post("/create", response_model=AnnotationResponse)
async def create_annotation(request: CreateAnnotationRequest):
    version = annotations.create_annotation(request.version)
    return AnnotationResponse(version=version)

@router.get("/list", response_model=ListAnnotationsResponse)
async def list_annotations(text: str):
    versions = annotations.get_annotations_by_sentence(text)
    return ListAnnotationsResponse(annotations=versions) 