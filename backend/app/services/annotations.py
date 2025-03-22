import uuid
import json
from datetime import datetime
from typing import List, Optional
from ..core.redis import redis_client
from ..models.annotations import AnnotationVersion, SentenceParse, Token
from spacy import load
from spacy import displacy

nlp = load("en_core_web_sm")
ANNOTATION_PREFIX = "http-stanza:annotations"

def parse_text(text: str) -> SentenceParse:
    doc = nlp(text)
    tokens = []
    for i, token in enumerate(doc):
        tokens.append(Token(
            id=i,
            text=token.text,
            pos=token.pos_,
            head=token.head.i,
            dep=token.dep_
        ))
    return SentenceParse(text=text, tokens=tokens)

def create_annotation(version: AnnotationVersion) -> tuple[str, AnnotationVersion]:
    annotation_id = str(uuid.uuid4())
    
    # Ensure the version has a unique ID and timestamp
    version.version_id = str(uuid.uuid4())
    version.created_at = datetime.utcnow()
    
    # Store the annotation
    key = f"{ANNOTATION_PREFIX}:{annotation_id}"
    redis_client.set(key, version.json())
    
    # Add to the set of all annotations
    redis_client.sadd(ANNOTATION_PREFIX, annotation_id)
    
    # Store version history
    versions_key = f"{key}:versions"
    redis_client.lpush(versions_key, version.json())
    
    return annotation_id, version

def get_annotation(annotation_id: str) -> Optional[AnnotationVersion]:
    key = f"{ANNOTATION_PREFIX}:{annotation_id}"
    data = redis_client.get(key)
    if data:
        return AnnotationVersion.parse_raw(data)
    return None

def update_annotation(annotation_id: str, text: str) -> Optional[AnnotationVersion]:
    if not get_annotation(annotation_id):
        return None
        
    version_id = str(uuid.uuid4())
    sentence = parse_text(text)
    annotation_version = AnnotationVersion(
        version_id=version_id,
        sentence=sentence,
        created_at=datetime.utcnow()
    )
    
    # Update the current version
    key = f"{ANNOTATION_PREFIX}:{annotation_id}"
    redis_client.set(key, annotation_version.json())
    
    # Add to version history
    versions_key = f"{key}:versions"
    redis_client.lpush(versions_key, annotation_version.json())
    
    return annotation_version

def delete_annotation(annotation_id: str) -> bool:
    key = f"{ANNOTATION_PREFIX}:{annotation_id}"
    if redis_client.exists(key):
        # Delete the annotation
        redis_client.delete(key)
        
        # Remove from the set of all annotations
        redis_client.srem(ANNOTATION_PREFIX, annotation_id)
        
        # Delete version history
        versions_key = f"{key}:versions"
        redis_client.delete(versions_key)
        
        return True
    return False

def list_annotation_versions(annotation_id: str) -> List[AnnotationVersion]:
    versions_key = f"{ANNOTATION_PREFIX}:{annotation_id}:versions"
    versions = redis_client.lrange(versions_key, 0, -1)
    return [AnnotationVersion.parse_raw(v) for v in versions]

def list_annotations() -> List[str]:
    return list(redis_client.smembers(ANNOTATION_PREFIX)) 