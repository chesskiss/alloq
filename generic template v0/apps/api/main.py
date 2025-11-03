from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from core.index import SimpleIndex
from core.ingest import load_text_files
from core.judge import judge
import os

app = FastAPI(title="AI Judge Starter", version="0.1.0")

@app.get("/")
def root():
    return _startup()

# Build a tiny in-memory index at startup from domains/default/domain_kb
INDEX = SimpleIndex()
DOCS = []

@app.on_event("startup")
def _startup():
    global DOCS, INDEX
    DOCS = load_text_files()
    if DOCS:
        INDEX.build(DOCS)

class AskRequest(BaseModel):
    question: str
    k: int = 4
    use_llm: bool = False  # placeholder for future

class AskResponse(BaseModel):
    answer: str
    sources: List[dict] = Field(default_factory=list)

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    results = INDEX.search(req.question, k=req.k) if INDEX else []
    # Placeholder answer: concatenate top snippet; swap with LLM later
    answer_parts = [r.text for r in results[:2]] or ["(No context found. Add docs in domains/default/domain_kb)"]
    answer = "\n\n".join(answer_parts)
    sources = [{"doc_path": r.doc_path, "score": r.score} for r in results]
    return AskResponse(answer=answer, sources=sources)

class JudgeRequest(BaseModel):
    question: str
    answer: str
    context_docs: Optional[List[str]] = Field(default=None)
    rubric_path: str = "domains/default/domain_rules/example_rubric.yaml"

@app.post("/judge")
def judge_endpoint(req: JudgeRequest):
    try:
        result = judge(req.question, req.answer, req.context_docs or [], req.rubric_path)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail=f"Rubric not found: {req.rubric_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


