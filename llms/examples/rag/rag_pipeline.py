"""
rag_pipeline.py — Realistic RAG (Retrieval-Augmented Generation) pipeline.

Pipeline:
    1. Load documents
    2. Chunk text
    3. Generate embeddings (Sentence Transformers)
    4. Build FAISS index
    5. Retrieve relevant chunks for a query
    6. Generate response via LLM (Anthropic / OpenAI / local stub)

Usage:
    # Run with stub LLM (no API key needed):
    python llms/examples/rag/rag_pipeline.py

    # Run with Anthropic:
    ANTHROPIC_API_KEY=sk-... python llms/examples/rag/rag_pipeline.py --llm anthropic

    # Run with OpenAI:
    OPENAI_API_KEY=sk-... python llms/examples/rag/rag_pipeline.py --llm openai
"""

import argparse
import logging
import os
import textwrap
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

EMBED_MODEL  = "all-MiniLM-L6-v2"
CHUNK_SIZE   = 300     # characters
CHUNK_OVERLAP = 50
TOP_K        = 3


# ─────────────────────────────────────────
# Data Structures
# ─────────────────────────────────────────
@dataclass
class Document:
    doc_id: str
    text: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    metadata: dict = field(default_factory=dict)


@dataclass
class RetrievalResult:
    chunk: Chunk
    score: float


# ─────────────────────────────────────────
# Chunking
# ─────────────────────────────────────────
def chunk_documents(documents: List[Document],
                    chunk_size: int = CHUNK_SIZE,
                    overlap: int = CHUNK_OVERLAP) -> List[Chunk]:
    """Split documents into overlapping chunks."""
    chunks = []
    for doc in documents:
        text = doc.text
        start = 0
        idx = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(
                    chunk_id=f"{doc.doc_id}_chunk_{idx:03d}",
                    doc_id=doc.doc_id,
                    text=chunk_text,
                    metadata={**doc.metadata, "chunk_index": idx},
                ))
                idx += 1
            start += chunk_size - overlap
    log.info(f"Chunked {len(documents)} documents → {len(chunks)} chunks")
    return chunks


# ─────────────────────────────────────────
# Embeddings + FAISS Index
# ─────────────────────────────────────────
class VectorStore:
    """Simple FAISS-based vector store."""

    def __init__(self, model_name: str = EMBED_MODEL):
        log.info(f"Loading embedding model: {model_name}")
        self.model  = SentenceTransformer(model_name)
        self.chunks: List[Chunk] = []
        self.index  = None

    def build(self, chunks: List[Chunk]) -> None:
        """Embed all chunks and build FAISS index."""
        try:
            import faiss
        except ImportError:
            raise ImportError("Install faiss: pip install faiss-cpu")

        self.chunks = chunks
        texts = [c.text for c in chunks]

        log.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False
        )
        embeddings = np.array(embeddings, dtype=np.float32)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)   # Inner product = cosine on normalized vecs
        self.index.add(embeddings)
        log.info(f"Index built: {self.index.ntotal} vectors, dim={dim}")

    def search(self, query: str, top_k: int = TOP_K) -> List[RetrievalResult]:
        """Retrieve top-k most similar chunks for a query."""
        if self.index is None:
            raise RuntimeError("Call build() before search()")

        query_vec = self.model.encode(
            [query], normalize_embeddings=True
        ).astype(np.float32)

        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                results.append(RetrievalResult(
                    chunk=self.chunks[idx],
                    score=float(score),
                ))
        return results


# ─────────────────────────────────────────
# LLM Backends
# ─────────────────────────────────────────
def generate_anthropic(context: str, query: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=(
            "You are a helpful assistant. Answer the question using only the "
            "provided context. If the answer is not in the context, say so."
        ),
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }],
    )
    return message.content[0].text


def generate_openai(context: str, query: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": (
                "Answer the question using only the provided context. "
                "If the answer is not in the context, say so."
            )},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
        ],
        max_tokens=512,
    )
    return response.choices[0].message.content


def generate_stub(context: str, query: str) -> str:
    """Stub LLM — returns context summary without an API key."""
    return (
        f"[STUB RESPONSE — no LLM connected]\n\n"
        f"Query: {query}\n\n"
        f"Based on the retrieved context:\n"
        f"{textwrap.shorten(context, width=300, placeholder='...')}\n\n"
        f"To use a real LLM, set ANTHROPIC_API_KEY or OPENAI_API_KEY "
        f"and pass --llm anthropic|openai"
    )


LLM_BACKENDS = {
    "anthropic": generate_anthropic,
    "openai":    generate_openai,
    "stub":      generate_stub,
}


# ─────────────────────────────────────────
# RAG Pipeline
# ─────────────────────────────────────────
class RAGPipeline:

    def __init__(self, llm: str = "stub"):
        self.store    = VectorStore()
        self.generate = LLM_BACKENDS[llm]
        self.llm_name = llm

    def ingest(self, documents: List[Document]) -> None:
        chunks = chunk_documents(documents)
        self.store.build(chunks)

    def query(self, question: str, top_k: int = TOP_K) -> dict:
        log.info(f"Query: {question}")

        # Retrieve
        results = self.store.search(question, top_k=top_k)
        log.info(f"Retrieved {len(results)} chunks")

        # Build context
        context = "\n\n---\n\n".join([
            f"[Source: {r.chunk.doc_id} | Score: {r.score:.4f}]\n{r.chunk.text}"
            for r in results
        ])

        # Generate
        log.info(f"Generating response via: {self.llm_name}")
        response = self.generate(context, question)

        return {
            "question":  question,
            "response":  response,
            "sources":   [r.chunk.doc_id for r in results],
            "scores":    [round(r.score, 4) for r in results],
            "chunks":    [r.chunk.text[:100] + "..." for r in results],
        }


# ─────────────────────────────────────────
# Sample Knowledge Base
# ─────────────────────────────────────────
SAMPLE_DOCUMENTS = [
    Document(
        doc_id="mlops-overview",
        text="""
        MLOps (Machine Learning Operations) combines Machine Learning, DevOps, and Data Engineering
        to streamline the deployment and maintenance of ML models in production. Key components
        include experiment tracking, model registry, CI/CD pipelines, model serving, and monitoring.
        MLflow is a popular open-source platform for experiment tracking and model registry.
        Docker and Kubernetes are used for containerization and orchestration of ML services.
        """,
        metadata={"domain": "mlops", "topic": "overview"},
    ),
    Document(
        doc_id="drift-detection",
        text="""
        Data drift occurs when the statistical properties of model input features change over time.
        Model drift occurs when model performance degrades due to concept drift or data distribution shift.
        PSI (Population Stability Index) measures feature distribution drift: PSI < 0.10 is stable,
        PSI > 0.20 indicates significant drift. The KS test (Kolmogorov-Smirnov) detects distributional
        changes with a p-value threshold of 0.05. CUSUM (Cumulative Sum) tracks sustained performance
        degradation and triggers retraining alerts.
        """,
        metadata={"domain": "mlops", "topic": "monitoring"},
    ),
    Document(
        doc_id="conjoint-analysis",
        text="""
        Conjoint analysis is a statistical technique used to estimate consumer preferences and
        utility scores for product attributes. In the TBCA framework, text-based conjoint analysis
        extracts preference data from unstructured product reviews using NLP. DeBERTa-v3 is used
        for aspect-based sentiment analysis (ABSA) to identify product attributes and opinions.
        Prospect Theory debiasing corrects for cognitive biases in utility estimation.
        MNL (Multinomial Logit) models compute choice probabilities from utility scores.
        """,
        metadata={"domain": "marketing", "topic": "conjoint"},
    ),
    Document(
        doc_id="rag-systems",
        text="""
        RAG (Retrieval-Augmented Generation) systems combine vector retrieval with large language
        models to answer questions grounded in a knowledge base. The pipeline involves chunking
        documents, generating embeddings with models like Sentence Transformers, indexing vectors
        in a vector database (Qdrant, ChromaDB, FAISS), retrieving the top-k most relevant chunks
        for a query, and passing the context to an LLM for response generation. This reduces
        hallucinations and enables factual, up-to-date responses.
        """,
        metadata={"domain": "llms", "topic": "rag"},
    ),
]


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="Run RAG pipeline demo.")
    parser.add_argument("--llm", choices=["stub", "anthropic", "openai"],
                        default="stub", help="LLM backend to use")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    pipeline = RAGPipeline(llm=args.llm)
    pipeline.ingest(SAMPLE_DOCUMENTS)

    questions = [
        "What is MLOps and what are its key components?",
        "How does PSI detect data drift and what are the thresholds?",
        "What is conjoint analysis and how does TBCA use NLP?",
    ]

    print("\n" + "=" * 65)
    print("  RAG PIPELINE DEMO")
    print("=" * 65)

    for question in questions:
        result = pipeline.query(question, top_k=args.top_k)
        print(f"\n❓ {result['question']}")
        print(f"📄 Sources: {result['sources']}")
        print(f"🔢 Scores:  {result['scores']}")
        print(f"\n💬 Response:\n{textwrap.fill(result['response'], width=65)}")
        print("-" * 65)
