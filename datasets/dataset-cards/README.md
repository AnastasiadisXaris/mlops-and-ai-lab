# Dataset Cards

## Purpose

Dataset cards document datasets clearly and consistently — a single source of truth for every dataset in the ecosystem.

A good dataset card answers: *What is this data? Where did it come from? What can it be used for? What are its limitations?*

---

## Naming Convention

```text
<domain>-<description>-<version>.md

# Examples:
marketing-consumer-survey-v1.md
nlp-product-reviews-v2.md
recommendation-movielens-100k-v1.md
research-conjoint-analysis-v1.md
```

---

## Template

Copy this template for every new dataset:

```markdown
# Dataset Name

## Overview
- **Domain:** (e.g. marketing, nlp, recommendation)
- **Version:** 1.0
- **Created:** YYYY-MM-DD
- **Author:** 
- **License:** (e.g. MIT, CC BY 4.0, proprietary)

## Source
- **Origin:** (URL, survey, synthetic, internal)
- **Collection method:** (scraping, survey, API export, manual)
- **Date collected:** YYYY-MM-DD

## Purpose
What this dataset is intended for and what ML tasks it supports.

## Schema

| Column | Type | Description | Example |
|---|---|---|---|
| column_name | string/int/float | description | example value |

## Target Variable
- **Column:** target_column
- **Type:** binary / multiclass / continuous
- **Distribution:** (e.g. 60% class 0, 40% class 1)

## Size
- **Rows:** 
- **Columns:** 
- **File size:** 
- **Format:** CSV / Parquet / JSON

## Preprocessing Notes
Steps already applied to this dataset (cleaning, encoding, normalization).

## Known Limitations
Biases, missing values, coverage gaps, or caveats to be aware of.

## Usage Example
\`\`\`python
import pandas as pd
df = pd.read_parquet("path/to/dataset.parquet")
\`\`\`

## Related Files
- Raw: `datasets/raw/`
- Processed: `datasets/processed/`
- Schema: `datasets/schemas/`
```

---

## Completed Example

```markdown
# Consumer Preference Survey — v1

## Overview
- **Domain:** marketing
- **Version:** 1.0
- **Created:** 2026-01-15
- **Author:** Anastasiadis Xaris
- **License:** proprietary

## Source
- **Origin:** Google Forms survey
- **Collection method:** structured survey
- **Date collected:** 2026-01-10

## Purpose
Consumer conjoint analysis — estimating utility scores for product attributes
(price, brand, quality, delivery speed) for preference modeling.

## Schema

| Column | Type | Description | Example |
|---|---|---|---|
| respondent_id | string | unique ID | R0001 |
| age | integer | age in years | 34 |
| price_level | integer | 1–5 scale | 3 |
| brand_pref | string | preferred brand | BrandA |
| utility_score | float | estimated utility | 0.73 |
| purchase_intent | integer | 0 or 1 | 1 |

## Target Variable
- **Column:** purchase_intent
- **Type:** binary
- **Distribution:** 58% positive, 42% negative

## Size
- **Rows:** 1,200
- **Columns:** 14
- **File size:** 420 KB
- **Format:** Parquet

## Preprocessing Notes
- removed 23 incomplete responses
- encoded categorical variables (brand, region)
- normalized utility scores to [0, 1]

## Known Limitations
- convenience sample — not fully representative
- limited to Greek market respondents
- self-reported data subject to response bias

## Usage Example
\`\`\`python
import pandas as pd
df = pd.read_parquet("datasets/processed/consumer-preference-v1.parquet")
X = df.drop(columns=["purchase_intent"])
y = df["purchase_intent"]
\`\`\`

## Related Files
- Raw: `datasets/raw/consumer-preference-survey-raw.csv`
- Processed: `datasets/processed/consumer-preference-v1.parquet`
- Schema: `datasets/schemas/consumer-preference-schema.json`
```

---

## Why Dataset Cards Matter

| Benefit | Description |
|---|---|
| Transparency | everyone understands what the data contains |
| Reproducibility | preprocessing and assumptions are documented |
| Governance | ownership, license, and provenance are tracked |
| Collaboration | new contributors onboard without guesswork |
| Auditability | decisions can be traced back to data properties |

---

## Best Practices

- write the card **at ingestion time**, not after the fact
- update the card whenever preprocessing changes
- one card per dataset version
- store cards alongside schemas in `datasets/dataset-cards/`
