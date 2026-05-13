# Recommendation Datasets

## Purpose

This folder stores datasets for recommendation systems and personalization engines — user-item interactions, ratings, purchase histories, clickstream data, and implicit feedback signals.

---

## Naming Convention

```text
<source>-<description>-<version>.<ext>

# Examples:
movielens-100k-ratings-v1.parquet
amazon-electronics-reviews-v1.parquet
instacart-orders-features-v1.parquet
lastfm-listening-history-v1.parquet
internal-user-item-interactions-v1.parquet
```

---

## Folder Structure

```text
recommendation/
│
├── explicit/             # ratings, reviews, scores
├── implicit/             # clicks, views, purchases, dwell time
├── features/             # user and item feature matrices
├── splits/               # train / val / test splits
└── synthetic/            # generated interaction data for testing
```

---

## Interaction Matrix Schema

The core data structure for collaborative filtering:

| Column | Type | Description | Example |
|---|---|---|---|
| user_id | string | unique user identifier | U0042 |
| item_id | string | unique item identifier | I0187 |
| rating | float | explicit rating (1–5) | 4.0 |
| timestamp | integer | Unix timestamp | 1706745600 |
| interaction_type | string | click / view / purchase | purchase |
| weight | float | implicit feedback weight | 1.0 |

### Explicit Feedback

User-provided scores — ratings, reviews, likes. High signal quality, low volume.

### Implicit Feedback

Behavioral signals — clicks, views, purchases, dwell time. High volume, noisy signal.

---

## Common Public Datasets

| Dataset | Users | Items | Interactions | Type |
|---|---|---|---|---|
| MovieLens 100K | 943 | 1,682 | 100K | explicit ratings |
| MovieLens 1M | 6,040 | 3,706 | 1M | explicit ratings |
| Amazon Electronics | 192K | 63K | 1.7M | explicit reviews |
| Last.fm 360K | 360K | 294K | 17.5M | implicit (plays) |
| Instacart 2017 | 206K | 49K | 3.4M | implicit (orders) |

---

## Train / Val / Test Split Strategy

Recommendation splits must respect temporal ordering to avoid data leakage:

```text
Temporal Split (preferred):
─────────────────────────────────────────
Train          │ Validation  │ Test
(oldest 70%)   │ (next 15%)  │ (newest 15%)
─────────────────────────────────────────
```

```python
import pandas as pd

df = pd.read_parquet("datasets/recommendation/explicit/movielens-100k-v1.parquet")
df = df.sort_values("timestamp")

n = len(df)
train = df.iloc[:int(n * 0.70)]
val   = df.iloc[int(n * 0.70):int(n * 0.85)]
test  = df.iloc[int(n * 0.85):]

train.to_parquet("datasets/recommendation/splits/movielens-train-v1.parquet", index=False)
val.to_parquet("datasets/recommendation/splits/movielens-val-v1.parquet", index=False)
test.to_parquet("datasets/recommendation/splits/movielens-test-v1.parquet", index=False)

print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
```

**Never use random splits** — they leak future interactions into training.

---

## User-Item Matrix Construction

```python
import pandas as pd
import scipy.sparse as sp

df = pd.read_parquet("datasets/recommendation/splits/movielens-train-v1.parquet")

# Map IDs to indices
user_idx = {u: i for i, u in enumerate(df["user_id"].unique())}
item_idx = {it: i for i, it in enumerate(df["item_id"].unique())}

rows = df["user_id"].map(user_idx)
cols = df["item_id"].map(item_idx)
vals = df["rating"].values

matrix = sp.csr_matrix((vals, (rows, cols)),
                        shape=(len(user_idx), len(item_idx)))

print(f"Matrix shape: {matrix.shape}")
print(f"Sparsity: {1 - matrix.nnz / (matrix.shape[0] * matrix.shape[1]):.4f}")
```

---

## Evaluation Metrics

| Metric | Description | Use Case |
|---|---|---|
| Precision@K | relevant items in top-K | explicit feedback |
| Recall@K | coverage of relevant items | explicit feedback |
| NDCG@K | ranked relevance quality | both |
| Hit Rate@K | at least one relevant in top-K | implicit feedback |
| MRR | mean reciprocal rank | ranking tasks |

---

## Best Practices

- use temporal splits — never random splits
- log sparsity of the interaction matrix (typically > 99%)
- handle cold-start users/items explicitly
- normalize implicit signals (log1p transformation for play counts)
- document the definition of "interaction" — clicks ≠ purchases ≠ ratings

**Common pitfalls:** random splits leaking future data · treating implicit and explicit feedback identically · ignoring cold-start in evaluation · missing timestamp information
