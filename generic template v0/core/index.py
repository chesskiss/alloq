from dataclasses import dataclass
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

@dataclass
class SearchResult:
    text: str
    doc_path: str
    score: float

class SimpleIndex:
    def __init__(self):
        self.vectorizer = None
        self.matrix = None
        self.corpus = []
        self.meta = []

    def build(self, docs: List[dict]):
        texts = [d["text"] for d in docs]
        self.meta = [(d["doc_path"], d["chunk_id"]) for d in docs]
        self.vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform(texts)
        self.corpus = texts
        return self

    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        if not self.vectorizer or not self.matrix:
            return []
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.matrix)[0]
        order = sims.argsort()[::-1][:k]
        out = []
        for i in order:
            doc_path, chunk_id = self.meta[i]
            out.append(SearchResult(text=self.corpus[i], doc_path=doc_path, score=float(sims[i])))
        return out
