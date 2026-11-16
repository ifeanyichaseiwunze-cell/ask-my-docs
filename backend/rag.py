import math

from ingest import chunks, embed


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)


def find_relevant_chunks(question: str, top_k: int = 2) -> list[dict]:
    question_embedding = embed(question)
    all_chunks = list(chunks.find())
    scored = [
        (cosine_similarity(question_embedding, c["embedding"]), c)
        for c in all_chunks
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [c for score, c in scored[:top_k]]