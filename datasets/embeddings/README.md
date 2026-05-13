# Embeddings Datasets

## Purpose

This folder stores embedding datasets — dense vector representations generated from text, images, or structured data. Embeddings are the foundation of semantic search, RAG systems, recommendation engines, and clustering workflows.

---

## Naming Convention

```text
<source>-<model>-<dim>d-<version>.npy / .parquet

# Examples:
product-reviews-sentence-transformers-384d-v1.npy
marketing-surveys-bge-768d-v1.parquet
wiki-documents-openai-1536d-v1.parquet
```

---

## Generation Pipeline

```text
Raw Text / Documents
    ↓
Chunking (if needed)
    ↓
Embedding Model
    ↓
Vector Representations
    ↓
Storage (numpy / parquet / vector DB export)
```

---

## Recommended Models

| Model | Dimensions | Best For |
|---|---|---|
| `all-MiniLM-L6-v2` | 384 | fast, general purpose |
| `all-mpnet-base-v2` | 768 | higher quality, general |
| `bge-large-en-v1.5` | 1024 | retrieval tasks |
| `text-embedding-3-small` | 1536 | OpenAI API |
| `text-embedding-3-large` | 3072 | OpenAI, high quality |

---

## Storage Formats

| Format | Use Case |
|---|---|
| `.npy` | fast local numpy arrays |
| `.parquet` | analytics, with metadata columns |
| `.jsonl` | portability, id + vector + metadata |
| vector DB export | Qdrant, ChromaDB snapshots |

### Example Parquet Schema

```text
id          | string  — document / chunk identifier
text        | string  — original text (optional)
embedding   | list    — vector of floats
model       | string  — embedding model name
created_at  | string  — generation timestamp
```

---

## Usage Example

```python
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
texts = ["product review one", "product review two"]
embeddings = model.encode(texts, normalize_embeddings=True)

# Save as numpy
np.save("datasets/embeddings/reviews-minilm-384d-v1.npy", embeddings)

# Save as parquet with metadata
df = pd.DataFrame({
    "id": [f"doc_{i}" for i in range(len(texts))],
    "text": texts,
    "embedding": embeddings.tolist(),
    "model": "all-MiniLM-L6-v2",
})
df.to_parquet("datasets/embeddings/reviews-minilm-384d-v1.parquet", index=False)

# Load and use
vecs = np.load("datasets/embeddings/reviews-minilm-384d-v1.npy")
```

---

## Use Cases

| Use Case | Description |
|---|---|
| Semantic Search | find similar documents by meaning |
| RAG Systems | retrieve relevant chunks for LLM context |
| Recommendation | user/item similarity matching |
| Clustering | group semantically similar content |
| Classification | embedding features as model input |

---

## Best Practices

- store model name and dimensions in the filename
- normalize embeddings before storage (`normalize_embeddings=True`)
- regenerate embeddings when switching models — they are not compatible
- cache embeddings to avoid repeated API calls
- version embeddings alongside the model that generated them

**Common pitfalls:** mixing embeddings from different models · storing without metadata · not normalizing before cosine similarity · regenerating unnecessarily
