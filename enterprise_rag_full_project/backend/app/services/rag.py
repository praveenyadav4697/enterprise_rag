from dataclasses import dataclass
from collections import Counter
import math
import re
from typing import List, Tuple
from app.db import models

WORD_RE = re.compile(r"[A-Za-z0-9']+")

@dataclass
class RetrievedSource:
    document_id: int
    filename: str
    chunk_index: int
    content: str
    score: float

def tokenize(text: str) -> List[str]:
    return [t.lower() for t in WORD_RE.findall(text or "")]

def vectorize(tokens: List[str]) -> Counter:
    return Counter(tokens)

def cosine_similarity(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b.get(k, 0) for k in a)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def retrieve(query: str, chunks: List[models.Chunk], documents: List[models.Document], top_k: int = 5) -> List[RetrievedSource]:
    q_vec = vectorize(tokenize(query))
    doc_map = {doc.id: doc.filename for doc in documents}
    ranked = []
    for ch in chunks:
        c_vec = vectorize(tokenize(ch.content))
        score = cosine_similarity(q_vec, c_vec)
        if score > 0:
            ranked.append(
                RetrievedSource(
                    document_id=ch.document_id,
                    filename=doc_map.get(ch.document_id, "document"),
                    chunk_index=ch.chunk_index,
                    content=ch.content,
                    score=score,
                )
            )
    ranked.sort(key=lambda x: x.score, reverse=True)
    return ranked[:top_k]

def generate_answer(query: str, sources: List[RetrievedSource]) -> str:
    if not sources:
        return (
            "I could not find a grounded answer in the uploaded documents. "
            "Please upload relevant files or ask a question that matches the available content."
        )

    bullets = []
    for src in sources[:3]:
        snippet = src.content.replace("\n", " ").strip()
        if len(snippet) > 240:
            snippet = snippet[:240].rsplit(" ", 1)[0] + "..."
        bullets.append(f"- {src.filename} [chunk {src.chunk_index}]: {snippet}")

    joined = "\n".join(bullets)
    return (
        "Grounded answer based on the uploaded documents:\n"
        f"{joined}\n\n"
        f"Question: {query}\n"
        "This project uses retrieval-first answering, so the response is anchored to the uploaded content."
    )
