# Datasets Knowledge Base

## Purpose

This folder contains datasets, dataset documentation, metadata, references, preprocessing notes, schemas, and data-related resources for AI, Machine Learning, MLOps, recommendation systems, NLP, marketing analytics, and research projects.

The goal is to build a structured and reusable data ecosystem — not merely a storage place for CSV files, but a **dataset intelligence layer** where datasets are documented, categorized, versioned, evaluated, and reusable.

---

## Folder Structure

```text
datasets/
│
├── public/
├── private/
├── processed/
├── raw/
├── schemas/
├── metadata/
├── notebooks/
├── dataset-cards/
├── synthetic/
├── embeddings/
├── vector-data/
├── recommendation/
├── marketing/
├── nlp/
├── time-series/
├── images/
├── research/
└── scripts/
```

| Folder | Purpose |
|---|---|
| public | open/public datasets |
| private | restricted/private datasets |
| processed | cleaned/transformed datasets |
| raw | untouched original datasets |
| schemas | dataset schemas and structure |
| metadata | dataset descriptions |
| notebooks | EDA and preprocessing notebooks |
| dataset-cards | documentation cards |
| synthetic | generated synthetic datasets |
| embeddings | embedding datasets |
| vector-data | vectorized content |
| recommendation | recommendation datasets |
| marketing | marketing analytics datasets |
| nlp | NLP datasets |
| time-series | sequential datasets |
| research | research-specific datasets |
| scripts | preprocessing scripts |

---

## Data Lifecycle

```text
Raw Data → Validation → Cleaning → Transformation → Feature Engineering → Processed Dataset → Training / Analytics
```

**Core rule:** never overwrite raw data — always preserve the original.

---

## Dataset Categories

### Recommendation System Datasets

Useful for collaborative filtering, ranking systems, personalization, and recommendation engines.

| Dataset | Purpose |
|---|---|
| MovieLens | recommendation systems |
| Amazon Reviews | product recommendations |
| Instacart | shopping behavior |
| Last.fm | music recommendations |

### Marketing Datasets

Useful for consumer analytics, preference modeling, segmentation, and conjoint analysis.

**Example data:** survey responses · purchase history · clickstream behavior · CRM exports · campaign analytics

**Key features:** demographics · conjoint utilities · purchase intent · behavioral segmentation · campaign engagement

### NLP Datasets

| Dataset | Purpose |
|---|---|
| IMDB Reviews | sentiment analysis |
| AG News | classification |
| Wikipedia | retrieval systems |
| Common Crawl | large-scale NLP |

### Time-Series Datasets

**Examples:** stock prices · sales data · IoT telemetry · web traffic

### Research Datasets

For academic experimentation, thesis work, and reproducibility.

---

## Raw vs Processed Data

Keeping raw and processed data separate ensures reproducibility, debugging, auditing, and rollback capability.

```text
raw/customer-survey.csv              # never touch
processed/customer-survey-cleaned.parquet   # transformed copy
```

---

## Storage & Versioning

### Recommended Formats

| Format | Use |
|---|---|
| CSV | portability |
| Parquet | analytics performance |
| JSON | APIs |
| Feather | fast local access |
| SQLite | lightweight databases |

### Storage Strategy

**Small datasets:** store directly in Git.

**Large datasets:** use DVC · S3 · MinIO · Google Cloud Storage

> ⚠️ Avoid committing multi-GB datasets directly into Git. Git tracks history permanently.

### Data Versioning

| Tool | Purpose |
|---|---|
| DVC | dataset versioning |
| Git LFS | large file storage |
| LakeFS | data lake versioning |

```text
Dataset Update → DVC Tracking → Remote Storage → Versioned Dataset
```

---

## Data Validation & EDA

### Validation

Before using datasets: validate schema · detect missing values · detect duplicates · check ranges · detect drift

| Tool | Purpose |
|---|---|
| Great Expectations | validation |
| Pandera | schema enforcement |
| Evidently | drift monitoring |

### EDA

**Common tasks:** distribution analysis · missing value analysis · correlation analysis · outlier detection · feature importance

**Tools:** Pandas · Polars · Matplotlib · Plotly

---

## Synthetic Data

Artificially generated datasets for privacy protection, testing, simulation, and low-data environments.

**Risks:** unrealistic distributions · hidden bias · poor generalization

---

## Embeddings

```text
Documents → Embedding Model → Vector Representations → Vector Storage
```

---

## Dataset Card Template

```markdown
# Dataset Name

## Source
## Purpose
## Features
## Target
## Size
## License
## Limitations
```

**Example metadata:**

```json
{
  "dataset": "consumer_preferences",
  "version": "1.0",
  "rows": 12000,
  "features": 28
}
```

---

## Privacy & Governance

**Protect:** personal identifiers · emails · phone numbers · behavioral logs · purchase histories

**Privacy practices:** anonymization · pseudonymization · encryption · access control · retention policies

**Governance includes:** ownership · versioning · validation · access rules · auditing

---

## Production Stack

| Layer | Technology |
|---|---|
| Storage | PostgreSQL |
| Large Files | S3 / MinIO |
| Versioning | DVC |
| Validation | Great Expectations |
| Processing | Pandas / Spark |
| Monitoring | Evidently |

---

## Best Practices

- never overwrite raw data
- version datasets alongside models
- document preprocessing steps
- validate continuously
- separate train/validation/test splits clearly
- monitor dataset drift in production
- store metadata for every dataset

**Common pitfalls:** data leakage · hidden bias · poor documentation · inconsistent preprocessing · missing versioning · privacy violations
