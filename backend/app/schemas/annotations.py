from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.annotations import Token, SentenceParse, AnnotationVersion

class CreateAnnotationRequest(BaseModel):
    version: AnnotationVersion

class AnnotationResponse(BaseModel):
    annotation_id: str
    latest_version: AnnotationVersion

class UpdateAnnotationRequest(BaseModel):
    text: str

class AnnotationVersionResponse(BaseModel):
    version_id: str
    sentence: SentenceParse
    created_at: datetime

class ListVersionsResponse(BaseModel):
    versions: List[AnnotationVersion] 