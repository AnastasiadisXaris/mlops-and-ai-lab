# Research Datasets

## Purpose

This folder stores datasets specifically related to doctoral research, academic experimentation, thesis development, systematic reviews, and reproducibility studies. Research datasets require stricter documentation than general ML datasets — methodology, citations, and provenance are as important as the data itself.

---

## Naming Convention

```text
<study>-<description>-<version>.<ext>

# Examples:
thesis-conjoint-pilot-v1.parquet
tbca-preference-experiment-v1.parquet
systematic-review-coding-v1.csv
absa-annotation-round1-v1.parquet
experiment-prospect-debiasing-v1.parquet
```

---

## Folder Structure

```text
research/
│
├── thesis/               # core dissertation datasets
├── conjoint-analysis/    # conjoint study data
├── absa/                 # aspect-based sentiment annotation
├── systematic-review/    # literature review coding sheets
├── experiments/          # experimental results and logs
└── pilot-studies/        # small-scale preliminary studies
```

---

## Documentation Requirements

Research datasets demand more rigorous documentation than standard ML datasets. For every dataset create:

- a **dataset card** in `datasets/dataset-cards/`
- a **metadata file** in `datasets/metadata/`
- a **provenance record** in `datasets/raw/`
- a **methodology note** (see template below)

---

## Methodology Note Template

```markdown
# Methodology Note — [Dataset Name]

## Research Question
What research question does this dataset support?

## Data Collection Protocol
- Collection method: (survey / annotation / experiment / literature coding)
- Instrument: (questionnaire, coding scheme, annotation guidelines)
- Sample: (who, how many, how selected)
- Period: YYYY-MM-DD to YYYY-MM-DD

## Inclusion / Exclusion Criteria
- Included: ...
- Excluded: ...

## Inter-Rater Reliability (if annotated)
- Metric: Cohen's Kappa / Krippendorff's Alpha
- Score: 
- Annotators: 

## Preprocessing Applied
1. step one
2. step two

## Limitations
- limitation one
- limitation two

## Citation
Author, A. (Year). Title. Source. DOI.
```

---

## Reproducibility Checklist

Before using a research dataset in experiments:

- [ ] Methodology documented
- [ ] Preprocessing steps recorded and versioned
- [ ] Train / val / test split frozen and saved
- [ ] Random seeds fixed and logged
- [ ] Dataset version referenced in experiment log
- [ ] Dataset card created
- [ ] Citation included

---

## Conjoint Analysis Dataset Notes

Specific to TBCA research:

| Aspect | Consideration |
|---|---|
| Choice tasks | number of tasks per respondent (typically 8–12) |
| Profile design | orthogonal or D-optimal design |
| Attributes | price, brand, quality, delivery (domain-specific) |
| Utility estimation | MNL part-worth extraction |
| Debiasing | Prospect Theory corrections applied post-estimation |
| ML input | utility scores as features for DeBERTa-v3 pipeline |

---

## Inter-Rater Reliability

For annotated datasets (ABSA, coding sheets, preference labels):

```python
from sklearn.metrics import cohen_kappa_score

# Compute Cohen's Kappa between two annotators
kappa = cohen_kappa_score(annotator_1_labels, annotator_2_labels)
print(f"Cohen's Kappa: {kappa:.4f}")

# Interpretation:
# < 0.20 → slight agreement
# 0.21–0.40 → fair
# 0.41–0.60 → moderate
# 0.61–0.80 → substantial
# 0.81–1.00 → almost perfect
```

---

## Citation Format (APA 7)

```text
Author, A. A., & Author, B. B. (Year). Title of dataset [Data set].
Repository Name. https://doi.org/xxxxx
```

---

## Best Practices

- freeze splits before any experiment — never reshuffle between runs
- fix and log all random seeds (`numpy`, `torch`, `random`)
- version datasets alongside experiment logs in MLflow
- document inter-rater reliability for any annotated data
- cite data sources in publications with DOI where available

**Common pitfalls:** undocumented methodology · missing inter-rater reliability · re-splitting between experiments · no seed control · missing citations
