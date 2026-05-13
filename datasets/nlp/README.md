# NLP Datasets

## Purpose

This folder stores datasets for Natural Language Processing tasks — sentiment analysis, text classification, named entity recognition, summarization, question answering, embeddings, and RAG pipelines.

---

## Naming Convention

```text
<task>-<description>-<version>.parquet / .jsonl / .csv

# Examples:
sentiment-product-reviews-v1.parquet
classification-news-ag-v1.parquet
ner-marketing-corpus-v1.jsonl
rag-knowledge-base-v1.jsonl
absa-aspect-opinions-v1.parquet
```

---

## Folder Structure

```text
nlp/
│
├── sentiment/            # sentiment analysis datasets
├── classification/       # text classification
├── ner/                  # named entity recognition
├── summarization/        # summarization corpora
├── qa/                   # question answering
├── absa/                 # aspect-based sentiment analysis
├── rag/                  # retrieval corpora
└── raw/                  # unprocessed text
```

---

## Common Public Datasets

| Dataset | Task | Size |
|---|---|---|
| IMDB Reviews | sentiment | 50K reviews |
| AG News | classification | 120K articles |
| CoNLL-2003 | NER | 14K sentences |
| SQuAD 2.0 | QA | 150K questions |
| CNN/DailyMail | summarization | 300K articles |
| Amazon Reviews | sentiment + ABSA | millions |
| Wikipedia | embeddings / RAG | multilingual |

---

## Preprocessing Pipeline

```text
Raw Text
    ↓
Cleaning (HTML, special chars, whitespace)
    ↓
Tokenization
    ↓
Lowercasing / Normalization
    ↓
Stopword Removal (optional — task-dependent)
    ↓
Train / Val / Test Split
    ↓
Encoding (token IDs for transformers)
```

---

## ABSA Schema

Aspect-Based Sentiment Analysis datasets are particularly relevant for the TBCA framework:

| Column | Type | Description | Example |
|---|---|---|---|
| review_id | string | unique review | R0042 |
| text | string | full review text | "Great battery life but slow charging" |
| aspect | string | aspect term | "battery life" |
| sentiment | string | positive/negative/neutral | positive |
| opinion | string | opinion word | "great" |
| category | string | aspect category | BATTERY |
| confidence | float | annotation confidence | 0.91 |

---

## Recommended Formats

| Format | Use Case |
|---|---|
| JSONL | one record per line, flexible schema |
| Parquet | fast analytics, columnar storage |
| CSV | portability, simple tasks |
| Arrow / Feather | in-memory processing |

---

## Usage Example

```python
import pandas as pd
from datasets import load_dataset

# Load from HuggingFace
dataset = load_dataset("imdb")
df_train = dataset["train"].to_pandas()

# Load local ABSA dataset
df = pd.read_parquet("datasets/nlp/absa/absa-product-reviews-v1.parquet")

# Basic stats
print(df["sentiment"].value_counts())
print(f"Rows: {len(df)}, Aspects: {df['aspect'].nunique()}")
```

---

## Tokenization Notes

- transformers operate on **token IDs**, not raw text — always tokenize with the correct model tokenizer
- `max_length` truncation can silently drop important context — log truncation rates
- multilingual datasets require language-aware tokenizers (e.g. `XLM-RoBERTa`)
- DeBERTa-v3 tokenizer handles subword tokenization — aspect spans may split across tokens

---

## Train / Val / Test Split Strategy

| Split | Ratio | Notes |
|---|---|---|
| Train | 70% | model learning |
| Validation | 15% | hyperparameter tuning |
| Test | 15% | final evaluation only |

- stratify splits by label to preserve class distribution
- for ABSA: stratify by aspect category, not just sentiment

---

## Best Practices

- clean text before tokenization, not after
- document language(s) and domain of the corpus
- preserve original text alongside cleaned version
- track label distribution — NLP datasets are often imbalanced
- store tokenized versions separately from raw text

**Common pitfalls:** data leakage via shared entities across splits · tokenizer mismatch between training and inference · missing language metadata · inconsistent label schemas across dataset versions
