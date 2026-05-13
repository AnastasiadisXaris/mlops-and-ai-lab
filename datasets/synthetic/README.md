# Synthetic Datasets

## Purpose

This folder stores artificially generated datasets for privacy-safe testing, simulation, prototyping, model validation, and low-data ML environments. Synthetic data mimics the statistical properties of real data without exposing sensitive information.

---

## Naming Convention

```text
<domain>-synthetic-<description>-<version>.<ext>

# Examples:
marketing-synthetic-conjoint-v1.parquet
recommendation-synthetic-user-item-v1.parquet
nlp-synthetic-reviews-v1.jsonl
tabular-synthetic-classification-v1.parquet
```

---

## Folder Structure

```text
synthetic/
│
├── marketing/            # synthetic survey and preference data
├── recommendation/       # synthetic user-item interactions
├── nlp/                  # synthetic text and review data
├── tabular/              # synthetic classification / regression data
└── generators/           # reusable generation scripts
```

---

## Use Cases

| Use Case | Description |
|---|---|
| Privacy-safe testing | test pipelines without exposing real user data |
| Prototyping | build and validate ML pipelines before real data arrives |
| Class imbalance simulation | generate minority class samples |
| Edge case testing | create adversarial or rare scenarios |
| Data augmentation | expand small datasets |
| CI/CD pipelines | deterministic test data for automated tests |

---

## Generation Examples

### Tabular Classification Data

```python
from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification(
    n_samples=2000,
    n_features=15,
    n_informative=8,
    n_redundant=3,
    n_classes=2,
    weights=[0.6, 0.4],   # class imbalance
    random_state=42,
)

df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
df["target"] = y

df.to_parquet(
    "datasets/synthetic/tabular/tabular-synthetic-classification-v1.parquet",
    index=False
)
print(f"Generated: {df.shape} | Class distribution: {df['target'].value_counts().to_dict()}")
```

### Synthetic Conjoint Survey Data

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n = 1200

brands = ["BrandA", "BrandB", "BrandC"]
df = pd.DataFrame({
    "respondent_id": [f"R{i:04d}" for i in range(n)],
    "task_id":       np.random.randint(1, 9, n),
    "price_level":   np.random.randint(1, 6, n),
    "brand":         np.random.choice(brands, n),
    "quality":       np.random.randint(1, 6, n),
    "delivery_days": np.random.randint(1, 8, n),
    "utility_score": np.clip(np.random.normal(0.5, 0.2, n), 0, 1).round(4),
    "purchase_intent": np.random.binomial(1, 0.55, n),
})

df.to_parquet(
    "datasets/synthetic/marketing/marketing-synthetic-conjoint-v1.parquet",
    index=False
)
print(f"Generated conjoint dataset: {df.shape}")
```

### Synthetic User-Item Interactions

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n_users, n_items, n_interactions = 500, 200, 5000

df = pd.DataFrame({
    "user_id":   [f"U{np.random.randint(0, n_users):04d}" for _ in range(n_interactions)],
    "item_id":   [f"I{np.random.randint(0, n_items):04d}" for _ in range(n_interactions)],
    "rating":    np.random.choice([1.0, 2.0, 3.0, 4.0, 5.0], n_interactions,
                                   p=[0.05, 0.10, 0.20, 0.35, 0.30]),
    "timestamp": np.sort(np.random.randint(1700000000, 1710000000, n_interactions)),
})
df = df.drop_duplicates(subset=["user_id", "item_id"])

df.to_parquet(
    "datasets/synthetic/recommendation/recommendation-synthetic-user-item-v1.parquet",
    index=False
)
print(f"Generated interactions: {df.shape}")
```

---

## Quality Checks

Always validate synthetic data before using it in pipelines:

```python
import pandas as pd

df = pd.read_parquet("datasets/synthetic/tabular/tabular-synthetic-classification-v1.parquet")

print("Shape:          ", df.shape)
print("Missing values:\n", df.isnull().sum())
print("Target dist:\n",    df["target"].value_counts(normalize=True).round(3))
print("Feature stats:\n",  df.describe().round(3))
```

---

## Recommended Tools

| Tool | Purpose |
|---|---|
| `sklearn.datasets` | quick tabular and classification data |
| `Faker` | realistic names, emails, addresses |
| `SDV` (Synthetic Data Vault) | statistical distribution matching |
| `Gretel AI` | privacy-preserving generation |
| `numpy.random` | custom distributions |

---

## Risks & Limitations

| Risk | Description |
|---|---|
| Unrealistic distributions | synthetic data may not reflect real patterns |
| Hidden bias | generator assumptions can introduce bias |
| Poor generalization | models trained on synthetic data may fail on real data |
| Overfit to generator | pipeline tests may pass but real data fails |

---

## Best Practices

- use a fixed `random_seed` for reproducibility in tests
- document generation parameters alongside the dataset
- validate statistical properties match expected real-world distributions
- use synthetic data for pipeline testing — not for final model evaluation
- label synthetic datasets clearly to prevent accidental use in production

**Common pitfalls:** using synthetic data for final model evaluation · no random seed · missing generation parameter documentation · unrealistic feature correlations
