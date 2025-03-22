from pydantic import BaseModel
from typing import List
from datetime import datetime

class Token(BaseModel):
    id: int
    text: str
    pos: str
    head: int
    dep: str

class SentenceParse(BaseModel):
    text: str
    tokens: List[Token]

class AnnotationVersion(BaseModel):
    version_id: str
    sentence: SentenceParse
    created_at: datetime

class CreateAnnotationRequest(BaseModel):
    version: AnnotationVersion

class AnnotationResponse(BaseModel):
    version: AnnotationVersion

class ListAnnotationsResponse(BaseModel):
    annotations: List[AnnotationVersion] 