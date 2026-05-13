# Vector Data

## Purpose

This folder stores vectorized datasets for semantic retrieval systems — pre-computed embeddings indexed for fast similarity search, RAG pipelines, recommendation engines, and clustering workflows.

Vector data differs from raw embeddings: it is **indexed, structured, and ready for retrieval** — not just raw numpy arrays.

---

## Naming Convention

```text
<domain>-<model>-<dim>d-index-<version>.<ext>

# Examples:
marketing-minilm-384d-index-v1.parquet
rag-knowledge-base-bge-768d-index-v1.parquet
recommendation-items-mpnet-768d-index-v1.parquet
research-papers-openai-1536d-index-v1.parquet
```

---

## Folder Structure

```text
vector-data/
│
├── rag/                  # retrieval corpora for RAG pipelines
├── recommendation/       # item and user embedding indexes
├── marketing/            # product and consumer embeddings
├── research/             # academic document embeddings
└── exports/              # vector DB snapshots and exports
```

---

## Schema

Each vector data file should include metadata alongside the vector:

| Column | Type | Description | Example |
|---|---|---|---|
| id | string | unique chunk/document ID | doc_042_chunk_3 |
| text | string | original text (optional) | "Great battery life..." |
| embedding | list[float] | dense vector | [0.12, -0.45, ...] |
| model | string | embedding model name | all-MiniLM-L6-v2 |
| dimensions | integer | vector dimensions | 384 |
| source | string | origin document/file | reviews_v1.parquet |
| created_at | string | generation timestamp | 2026-01-15 |
| metadata | string | JSON string of extra fields | {"category": "battery"} |

---

## Generation Pipeline

```text
Documents / Chunks
    ↓
Embedding Model (Sentence Transformers / OpenAI)
    ↓
Normalized Vectors
    ↓
Parquet Storage + Vector DB Upsert
```

---

## Generation & Upsert Example

```python
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION = "marketing-reviews"
DIM = 384

# --- Generate embeddings ---
model = SentenceTransformer(MODEL_NAME)
texts = ["Great battery life", "Poor build quality", "Fast delivery"]
ids   = [f"doc_{i:04d}" for i in range(len(texts))]

embeddings = model.encode(texts, normalize_embeddings=True)

# --- Save to parquet ---
df = pd.DataFrame({
    "id":         ids,
    "text":       texts,
    "embedding":  embeddings.tolist(),
    "model":      MODEL_NAME,
    "dimensions": DIM,
    "created_at": "2026-01-15",
})
df.to_parquet(
    f"datasets/vector-data/marketing/marketing-minilm-{DIM}d-index-v1.parquet",
    index=False
)

# --- Upsert to Qdrant ---
client = QdrantClient(url="http://localhost:6333")

client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
)

points = [
    PointStruct(id=i, vector=emb.tolist(), payload={"text": txt})
    for i, (emb, txt) in enumerate(zip(embeddings, texts))
]
client.upsert(collection_name=COLLECTION, points=points)
print(f"Upserted {len(points)} vectors to '{COLLECTION}'")
```

---

## Similarity Search Example

```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333")
model  = SentenceTransformer("all-MiniLM-L6-v2")

query     = "battery performance issues"
query_vec = model.encode(query, normalize_embeddings=True).tolist()

results = client.search(
    collection_name="marketing-reviews",
    query_vector=query_vec,
    limit=5,
)

for r in results:
    print(f"Score: {r.score:.4f} | Text: {r.payload['text']}")
```

---

## Index Formats

| Format | Description | Use Case |
|---|---|---|
| Parquet | columnar storage with metadata | archiving, analytics |
| Qdrant snapshot | vector DB export | production backup |
| FAISS index | binary index file | local fast search |
| ChromaDB | embedded vector store | lightweight RAG |
| Pinecone export | cloud index backup | managed retrieval |

---

## Recommended Vector Databases

| Tool | Best For |
|---|---|
| Qdrant | production, filtering, hybrid search |
| ChromaDB | lightweight, local RAG |
| FAISS | fast local ANN search |
| Pinecone | managed cloud retrieval |
| pgvector | PostgreSQL-native vector search |

---

## Best Practices

- normalize embeddings before storage (`normalize_embeddings=True`)
- store model name and dimensions in filenames and metadata
- keep a parquet backup alongside the vector DB index
- regenerate indexes when switching embedding models — indexes are model-specific
- version indexes alongside the model and dataset they were generated from

**Common pitfalls:** mixing vectors from different models in the same index · no metadata stored alongside vectors · missing normalization before cosine similarity · no backup of vector DB collections · regenerating unnecessarily due to poor versioning
