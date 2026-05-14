# LLM Examples

Realistic, runnable LLM examples demonstrating production patterns for RAG systems, agents, and LLM application development.

Each example is self-contained with its own `requirements.txt`, tests, and README.

---

## Examples

### [rag/](./rag/) — RAG Pipeline

End-to-end Retrieval-Augmented Generation pipeline using Sentence Transformers, FAISS, and a pluggable LLM backend (Anthropic, OpenAI, or stub).

```bash
cd llms/examples/rag
pip install -r requirements.txt

# Run with stub LLM (no API key needed)
python rag_pipeline.py

# Run with Anthropic
ANTHROPIC_API_KEY=sk-... python rag_pipeline.py --llm anthropic

# Run tests
pytest test_rag_pipeline.py -v
```

**Demonstrates:** document chunking · Sentence Transformers embeddings · FAISS index · top-k retrieval · pluggable LLM backends · source attribution · stub LLM for CI/CD

---

## How LLM Examples Connect to MLOps Examples

```text
mlops/examples/tracking/   →  model trained and tracked
mlops/examples/serving/    →  model served via FastAPI
llms/examples/rag/         →  knowledge base retrieval + LLM grounding
```

RAG can be combined with the MLOps serving layer: Django or FastAPI routes a user query to the RAG pipeline, retrieves relevant context, and calls the LLM — all observable via the Prometheus + Grafana stack in `devops/docker/`.

---

## Requirements

| Example | Key Dependencies |
|---|---|
| rag | `sentence-transformers` · `faiss-cpu` · `anthropic` · `openai` |