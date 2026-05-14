# RAG Pipeline — Example

Realistic end-to-end RAG (Retrieval-Augmented Generation) implementation using Sentence Transformers, FAISS, and a pluggable LLM backend.

## Pipeline

```text
Documents
    ↓
Chunking (overlapping windows)
    ↓
Embeddings (Sentence Transformers)
    ↓
FAISS Index (cosine similarity)
    ↓
Query → Top-K Retrieval
    ↓
Context Assembly
    ↓
LLM Response (Anthropic / OpenAI / stub)
```

## What It Demonstrates

- document chunking with configurable size and overlap
- embedding generation with `all-MiniLM-L6-v2`
- FAISS `IndexFlatIP` for cosine similarity search
- pluggable LLM backends (Anthropic, OpenAI, stub)
- structured retrieval results with scores and source attribution
- clean separation of retrieval and generation

## Usage

```bash
pip install -r requirements.txt

# Run with stub LLM (no API key needed)
python rag_pipeline.py

# Run with Anthropic
ANTHROPIC_API_KEY=sk-... python rag_pipeline.py --llm anthropic

# Run with OpenAI
OPENAI_API_KEY=sk-... python rag_pipeline.py --llm openai

# Adjust top-k retrieval
python rag_pipeline.py --top-k 5
```

## Example Output

```
==================================================================
  RAG PIPELINE DEMO
==================================================================

❓ What is MLOps and what are its key components?
📄 Sources: ['mlops-overview', 'rag-systems', 'drift-detection']
🔢 Scores:  [0.6821, 0.5234, 0.4812]

💬 Response:
MLOps combines Machine Learning, DevOps, and Data Engineering
to streamline deployment and maintenance of ML models...
------------------------------------------------------------------
```

## Run Tests

```bash
pytest test_rag_pipeline.py -v
```

## Key Design Decisions

- **FAISS `IndexFlatIP`** — exact search on normalized vectors = cosine similarity, no approximation
- **Overlapping chunks** — 50-char overlap prevents context loss at boundaries
- **Stub LLM** — runs without any API key for testing and CI/CD
- **Source attribution** — every response includes source doc IDs and retrieval scores
- **Pluggable backends** — swap LLM provider without changing retrieval logic
