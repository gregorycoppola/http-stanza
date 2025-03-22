from fastapi import APIRouter
from pydantic import BaseModel
from ..services import annotations

router = APIRouter(prefix="/parse", tags=["parse"])

class ParseRequest(BaseModel):
    text: str

class ParseResponse(BaseModel):
    svg: str

@router.post("/", response_model=ParseResponse)
async def parse_text(request: ParseRequest):
    sentence = annotations.parse_text(request.text)
    doc = annotations.nlp(request.text)
    svg = annotations.displacy.render(doc, style="dep", options={"compact": True})
    return ParseResponse(svg=svg) 