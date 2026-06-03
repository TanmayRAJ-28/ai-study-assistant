"""Embedding model access for the RAG pipeline.

The HuggingFace model is intentionally loaded lazily and cached so the
FastAPI process does not pay the model memory cost at startup. This keeps
the service much more stable on Render's 512 MB instances.
"""

import os
from importlib import import_module
from functools import lru_cache


# Smaller than all-MiniLM-L6-v2 and easier to fit inside a 512 MB instance.
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L3-v2"


@lru_cache(maxsize=1)
def get_embeddings():
    """Return a cached HuggingFace embedding model instance.

    `EMBEDDING_MODEL` can be overridden in the environment if you want to
    trade accuracy for speed or memory usage.
    """
    model_name = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)

    # Import lazily so the FastAPI process does not pay the import cost
    # until the first upload/query actually needs embeddings.
    HuggingFaceEmbeddings = import_module(
        "langchain_huggingface"
    ).HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )