#!/usr/bin/env python
import argparse, json
from core.ingest import load_text_files
from core.index import SimpleIndex

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", default=None, help="Folder with .txt/.md files (defaults to domains/default/domain_kb)")
    ap.add_argument("-k", type=int, default=5, help="Top-K to preview after building index")
    args = ap.parse_args()

    docs = load_text_files(args.folder)
    print(f"Loaded chunks: {len(docs)}")
    idx = SimpleIndex().build(docs)
    res = idx.search("test", k=args.k)
    print(json.dumps([{"score": r.score, "doc": r.doc_path} for r in res], indent=2))

if __name__ == "__main__":
    main()
