# Hybrid AI MCP Orchestrator

This project demonstrates a hybrid AI framework using MCP for analysis and hardware recommendations with a CI/CD pipeline.


hybrid-ai-mcp-orchestrator/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                  # FastAPI app: HTTP API + simple UI
│  ├─ analyzer.py              # Analyzes code, detects algorithms
│  ├─ hardware_recommender.py  # RAG wrapper / stub for recommending hardware
│  ├─ mcp_server.py            # MCP server exposing tools (analyze, recommend)
│  └─ config.py                # Settings, paths, feature flags
│
├─ rag/
│  ├─ __init__.py
│  ├─ docs_index.py            # Scripts to build an index from scraped docs (stub ok)
│  └─ retriever.py             # Retrieval API (stub ok)
│
├─ tests/
│  ├─ __init__.py
│  └─ test_analyzer.py         # At least 1–2 tests to show CI working
│
├─ requirements.txt            # Python deps (FastAPI, uvicorn, etc.)
├─ Dockerfile                  # Container image for app
├─ .gitlab-ci.yml              # CI: test + build (and later deploy if you want)
├─ README.md                   # Description + how to run
└─ .gitignore
