from pathlib import Path

import ollama

from db import db

chunks = db["chunks"]
EMBED_MODEL = "nomic-embed-text"
DOCS_DIR = Path(__file__).parent / "docs"


def split_into_chunks(text: str) -> list[str]:
    sections = text.split("## ")
    return [s.strip() for s in sections if s.strip()]


def embed(text: str) -> list[float]:
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]


def ingest():
    chunks.delete_many({})
    for file in DOCS_DIR.glob("*.md"):
        text = file.read_text()
        for piece in split_into_chunks(text):
            chunks.insert_one({
                "source": file.name,
                "text": piece,
                "embedding": embed(piece),
            })
            print(f"Saved chunk from {file.name}: {piece[:40]}...")


if __name__ == "__main__":
    ingest()