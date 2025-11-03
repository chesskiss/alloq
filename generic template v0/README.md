# AI Judge

Since it's quite hard for me to commit to a specifc project without proper validation on need, I love building generic tools that could be resued in many projects. Like this one...

A minimal, extensible scaffold for a rubric‑driven AI judging engine with RAG hooks.
Use this as a base to build vertical "judge" SaaS products
by adding domain rule packs and tools in `domains/<name>/`.

## Use case example
### See quantum-tech domain
The AI-judge scans the input, i.e. the code, checks its validity, breaks it down to sub-sections (sub-algorithms), and allocate the proper resource for each section (GPU, CPU, or QPU) depeding on the budget, efficiency, and performance needs of the customer.

## Features (MVP)
- FastAPI with two endpoints:
  - `POST /ask` → Hybrid retrieval (TF‑IDF baseline) + answer + citations (LLM optional)
  - `POST /judge` → Rubric‑driven scoring with rationale (LLM optional)
- Ingestion + indexing pipeline (simple TF‑IDF baseline; swap for vector DB later)
- Rubric YAML schema with rule weights, severities, and auto/LLM checks
- Config via env vars (`configs/settings.py`), multi‑tenant‑ready structure
- Tiny eval harness placeholder + tests to grow into CI quality gates

## Quickstart
```bash
# 1) Create a venv (optional but I recommend it)
python -m venv .venv && source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) (Optional) Set your OpenAI key to enable LLM answers/judging
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o-mini"   # or any chat model you prefer

# 4) Start the API
uvicorn apps.api.main:app --reload --port 8000
```

## Example requests
```bash
# Ask (retrieval + (optional) LLM answer with citations)
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{
  "question": "What is error mitigation in NISQ devices?",
  "k": 4
}'

# Judge (rubric-driven)
curl -X POST http://localhost:8000/judge -H "Content-Type: application/json" -d '{
  "question": "Does this claim demonstrate quantum advantage?",
  "answer": "We achieve exponential speedup on generic ML tasks.",
  "context_docs": [],
  "rubric_path": "domains/default/domain_rules/example_rubric.yaml"
}'
```

## Repo layout
```
ai-judge/
  apps/api/main.py             # FastAPI endpoints
  core/ingest.py               # Load/clean/chunk documents
  core/index.py                # Simple TF‑IDF index + search
  core/judge.py                # Rubric‑driven scoring (LLM or rules)
  core/rubric_schema.py        # Pydantic schema for rubric YAML
  configs/settings.py          # Env-config + model routing
  domains/
    default/
      domain_rules/example_rubric.yaml
      domain_tools/            # (add callable tools here)
      domain_kb/               # (drop seed docs here)
      domain_evals/            # (goldens for evals)
  scripts/ingest.py            # CLI to ingest and (re)build index
  tests/test_judge.py          # Minimal sanity test
  requirements.txt
  README.md
```

## Next steps
- Swap TF‑IDF for hybrid: BM25 + vector embeddings (FAISS, Qdrant, Weaviate, pgvector)
- Add re-ranking (e.g., cross-encoder) and freshness/recency filters
- Add tool registry and traces (e.g., for circuit analyzers in quantum domain)
- Build eval harness (pairwise + pointwise) and wire to CI
- Add multi-tenant auth, metering, and audit logs for SaaS
