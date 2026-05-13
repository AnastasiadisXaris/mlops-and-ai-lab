# Dataset Notebooks

## Purpose

This folder stores notebooks for exploratory data analysis (EDA), preprocessing, feature engineering, visualization, and dataset experimentation. Notebooks here are the analytical workspace — where data is understood before it enters a pipeline.

---

## Naming Convention

```text
<type>-<dataset>-<description>.ipynb

# Examples:
eda-consumer-conjoint-v1.ipynb
preprocessing-product-reviews-cleaning.ipynb
features-rfm-engineering.ipynb
viz-marketing-segmentation.ipynb
experiment-absa-label-distribution.ipynb
```

---

## Folder Structure

```text
notebooks/
│
├── eda/                  # exploratory data analysis
├── preprocessing/        # cleaning, encoding, normalization
├── feature-engineering/  # feature creation and selection
├── visualization/        # plots, distributions, correlations
├── experiments/          # ad-hoc investigations
└── templates/            # reusable notebook templates
```

---

## Notebook Types

### EDA Notebooks

Goal: understand the dataset before modeling.

**Standard sections:**
1. Dataset overview (shape, dtypes, head)
2. Missing value analysis
3. Target distribution
4. Feature distributions
5. Correlation analysis
6. Outlier detection
7. Key findings summary

### Preprocessing Notebooks

Goal: document and validate every cleaning step.

**Standard sections:**
1. Raw data loading
2. Cleaning steps (with counts before/after)
3. Encoding
4. Normalization / scaling
5. Train / val / test split
6. Save processed dataset

### Feature Engineering Notebooks

Goal: create, validate, and select features.

**Standard sections:**
1. Feature definitions and rationale
2. Feature creation code
3. Feature importance analysis
4. Correlation with target
5. Final feature set selection

---

## EDA Template

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load
df = pd.read_parquet("datasets/processed/dataset-v1.parquet")

# 2. Overview
print(df.shape)
print(df.dtypes)
print(df.head())

# 3. Missing values
missing = df.isnull().sum()
print(missing[missing > 0])

# 4. Target distribution
df["target"].value_counts(normalize=True).plot(kind="bar")
plt.title("Target Distribution")
plt.tight_layout()
plt.savefig("viz/target-distribution.png", dpi=150)

# 5. Correlations
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig("viz/correlation-matrix.png", dpi=150)
```

---

## Recommended Tools

| Tool | Purpose |
|---|---|
| Jupyter | standard notebook environment |
| VS Code Notebooks | integrated editor |
| Google Colab | cloud, free GPU |
| Kaggle Notebooks | competition datasets |
| nbconvert | export to HTML / PDF |

---

## Best Practices

- one notebook per purpose — avoid combining EDA with preprocessing
- use markdown cells to explain findings, not just code
- save figures to a `viz/` subfolder alongside the notebook
- clear all outputs before committing to Git
- document key findings in a summary cell at the top
- link processed output paths explicitly

**Common pitfalls:** notebooks that run top-to-bottom only when cells are in order · committing large outputs to Git · mixing exploration with production logic · undocumented magic numbers
