"""
test_rag_pipeline.py — Tests for the RAG pipeline.

Covers:
    - Document chunking produces correct number of chunks
    - Chunks respect size limits
    - VectorStore build and search (stub — no FAISS needed for unit tests)
    - RAGPipeline.query returns expected keys
    - Stub LLM returns a response
"""

import pytest
from llms.examples.rag.rag_pipeline import (
    Document,
    Chunk,
    RAGPipeline,
    chunk_documents,
    generate_stub,
    SAMPLE_DOCUMENTS,
    CHUNK_SIZE,
)


# ─── Chunking ───
def test_chunking_produces_chunks():
    docs = [Document(doc_id="d1", text="A" * 600)]
    chunks = chunk_documents(docs, chunk_size=300, overlap=50)
    assert len(chunks) >= 2


def test_chunking_respects_size():
    docs = [Document(doc_id="d1", text="word " * 200)]
    chunks = chunk_documents(docs, chunk_size=100, overlap=0)
    for c in chunks:
        assert len(c.text) <= 110  # small buffer for strip


def test_chunking_assigns_doc_id():
    docs = [Document(doc_id="test-doc", text="Hello world " * 50)]
    chunks = chunk_documents(docs)
    assert all(c.doc_id == "test-doc" for c in chunks)


def test_chunking_unique_chunk_ids():
    docs = [Document(doc_id="d1", text="text " * 300)]
    chunks = chunk_documents(docs, chunk_size=100, overlap=0)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


# ─── Stub LLM ───
def test_stub_llm_returns_string():
    response = generate_stub("some context", "what is MLOps?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_stub_llm_contains_query():
    query = "unique_query_string_xyz"
    response = generate_stub("context", query)
    assert query in response


# ─── RAGPipeline (stub LLM, no FAISS) ───
class MockVectorStore:
    """Mock VectorStore that returns fixed chunks without FAISS."""
    def __init__(self):
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks

    def search(self, query, top_k=3):
        from llms.examples.rag.rag_pipeline import RetrievalResult
        return [
            RetrievalResult(chunk=c, score=0.9 - i * 0.1)
            for i, c in enumerate(self.chunks[:top_k])
        ]


@pytest.fixture
def pipeline_stub(monkeypatch):
    """RAGPipeline with mock VectorStore and stub LLM."""
    pipeline = RAGPipeline(llm="stub")
    pipeline.store = MockVectorStore()
    pipeline.ingest(SAMPLE_DOCUMENTS[:2])
    return pipeline


def test_pipeline_query_returns_expected_keys(pipeline_stub):
    result = pipeline_stub.query("What is MLOps?")
    assert "question"  in result
    assert "response"  in result
    assert "sources"   in result
    assert "scores"    in result
    assert "chunks"    in result


def test_pipeline_query_response_not_empty(pipeline_stub):
    result = pipeline_stub.query("What is drift detection?")
    assert len(result["response"]) > 0


def test_pipeline_query_returns_sources(pipeline_stub):
    result = pipeline_stub.query("Tell me about RAG")
    assert isinstance(result["sources"], list)
    assert len(result["sources"]) > 0


def test_pipeline_query_scores_between_0_and_1(pipeline_stub):
    result = pipeline_stub.query("What is TBCA?")
    assert all(0.0 <= s <= 1.0 for s in result["scores"])
