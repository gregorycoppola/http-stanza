# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from spacy import load
from spacy import displacy

nlp = load("en_core_web_sm")

app = FastAPI()

# Allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParseRequest(BaseModel):
    text: str

@app.post("/parse")
async def parse_text(req: ParseRequest):
    doc = nlp(req.text)
    svg = displacy.render(doc, style="dep", options={"compact": True})
    return {"svg": svg}

