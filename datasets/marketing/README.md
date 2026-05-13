# Marketing Datasets

## Purpose

This folder stores datasets related to consumer behavior, conjoint analysis, customer segmentation, campaign analytics, preference modeling, and marketing intelligence systems.

---

## Naming Convention

```text
<type>-<description>-<version>.parquet / .csv

# Examples:
survey-consumer-conjoint-v1.parquet
crm-purchase-history-v2.parquet
campaign-email-engagement-v1.csv
segmentation-rfm-features-v1.parquet
```

---

## Folder Structure

```text
marketing/
│
├── surveys/              # conjoint, preference, satisfaction surveys
├── crm/                  # purchase history, customer profiles
├── campaigns/            # email, ad, social media analytics
├── segmentation/         # RFM, behavioral, psychographic
├── web-analytics/        # clickstream, sessions, funnels
└── synthetic/            # generated datasets for testing
```

---

## Key Dataset Types

### Conjoint Analysis Data

Used for utility estimation and consumer preference modeling.

| Column | Type | Description | Example |
|---|---|---|---|
| respondent_id | string | unique respondent | R0042 |
| task_id | integer | choice task number | 3 |
| profile_id | integer | product profile shown | 2 |
| price_level | integer | 1–5 scale | 4 |
| brand | string | brand name | BrandA |
| quality | integer | 1–5 scale | 3 |
| delivery_days | integer | delivery time | 2 |
| chosen | integer | 0 or 1 | 1 |
| utility_score | float | estimated utility | 0.68 |

### CRM / Purchase History Data

| Column | Type | Description |
|---|---|---|
| customer_id | string | unique customer |
| purchase_date | date | transaction date |
| product_id | string | purchased product |
| amount | float | transaction value |
| channel | string | web / mobile / store |
| recency | integer | days since last purchase |
| frequency | integer | total purchases |
| monetary | float | total spend |

### Campaign Analytics Data

| Column | Type | Description |
|---|---|---|
| campaign_id | string | campaign identifier |
| send_date | date | send timestamp |
| open_rate | float | % opened |
| ctr | float | click-through rate |
| conversion_rate | float | % converted |
| channel | string | email / social / paid |

---

## Preprocessing Pipeline

```text
Raw Survey / CRM Export
    ↓
Remove Incomplete Responses
    ↓
Encode Categoricals
    ↓
Normalize / Scale
    ↓
Feature Engineering (RFM, utility scores)
    ↓
Train / Test Split
    ↓
Processed Dataset
```

---

## Usage Example

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_parquet("datasets/marketing/surveys/consumer-conjoint-v1.parquet")

# Encode brand
le = LabelEncoder()
df["brand_encoded"] = le.fit_transform(df["brand"])

# Features and target
X = df[["price_level", "brand_encoded", "quality", "delivery_days"]]
y = df["chosen"]
```

---

## Conjoint Analysis Notes

Marketing datasets in this repo are closely tied to the TBCA framework:

- **Utility estimation:** part-worth utilities extracted via MNL / MAUT
- **Debiasing:** Prospect Theory corrections applied to utility scores
- **Choice modeling:** MNL probabilities computed per profile
- **Input to ML:** utility features fed into DeBERTa-v3 ABSA pipeline

---

## Best Practices

- document survey methodology alongside data
- preserve original response scales before encoding
- track class imbalance in binary targets (chosen / not chosen)
- version datasets when survey waves change
- anonymize respondent identifiers before storage

**Common pitfalls:** leaking future information into features · encoding before train/test split · missing response bias documentation · dropping incomplete responses without noting the count
