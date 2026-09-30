"""RAG over the destination guides.

Uses ChromaDB's bundled default embedding function -- an ONNX runtime build
of sentence-transformers/all-MiniLM-L6-v2 -- so there's no separate PyTorch
dependency to install or deploy. It downloads its small ONNX weights once on
first run (needs internet the first time; cached after that).
"""
from __future__ import annotations

import chromadb
from chromadb.utils import embedding_functions

from data.guides import GUIDES

COLLECTION_NAME = "destination_guides"


def build_collection(persist_dir: str = "chroma_db"):
    client = chromadb.PersistentClient(path=persist_dir)
    ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(COLLECTION_NAME, embedding_function=ef)

    if collection.count() == 0:
        collection.add(
            ids=[g["destination"] for g in GUIDES],
            documents=[g["text"] for g in GUIDES],
            metadatas=[
                {
                    "destination": g["destination"],
                    "best_season": g["best_season"],
                    "budget_level": g["budget_level"],
                }
                for g in GUIDES
            ],
        )
    return collection


def retrieve(collection, query: str, k: int = 3) -> list[tuple[str, dict]]:
    """Return up to k (document_text, metadata) pairs for the query."""
    if not query:
        return []
    results = collection.query(query_texts=[query], n_results=k)
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    return list(zip(docs, metas))


def format_context(hits: list[tuple[str, dict]]) -> str:
    if not hits:
        return "(no destination guide retrieved for this request)"
    return "\n\n".join(f"[{meta.get('destination', 'unknown')}]\n{doc}" for doc, meta in hits)
