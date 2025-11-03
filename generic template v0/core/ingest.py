import re, os, pathlib, glob
from typing import Iterable, List
from configs.settings import settings

def _split_into_chunks(text: str, min_chars: int, max_chars: int) -> List[str]:
    # basic paragraph/sentence chunker
    paras = re.split(r"\n\s*\n", text.strip())
    chunks, cur = [], ""
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if len(cur) + len(p) + 1 <= max_chars:
            cur = (cur + "\n" + p).strip()
        else:
            if len(cur) >= min_chars:
                chunks.append(cur)
            cur = p
    if cur and len(cur) >= min_chars:
        chunks.append(cur)
    return chunks

def load_text_files(folder: str | None = None) -> list[dict]:
    base = pathlib.Path(folder or settings.index_path)
    docs = []
    for path in glob.glob(str(base / "**/*"), recursive=True):
        p = pathlib.Path(path)
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".txt", ".md"}:
            continue
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        for idx, chunk in enumerate(_split_into_chunks(raw, settings.min_chunk_chars, settings.max_chunk_chars)):
            docs.append({
                "doc_path": str(p),
                "chunk_id": f"{p.name}#${idx}",
                "text": chunk
            })
    return docs
