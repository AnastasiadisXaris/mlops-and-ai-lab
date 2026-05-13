# Public Datasets

## Purpose

This folder stores publicly available datasets used for Machine Learning, Deep Learning, NLP, recommendation systems, marketing analytics, research experimentation, and MLOps pipelines.

---

## Naming Convention

```text
<domain>-<source>-<description>-<version>.<ext>

# Examples:
recommendation-movielens-100k-v1.parquet
nlp-imdb-sentiment-v1.parquet
marketing-amazon-reviews-v1.parquet
tabular-uci-adult-income-v1.parquet
```

---

## Folder Structure

```text
public/
│
├── recommendation/       # MovieLens, Amazon, Last.fm, Instacart
├── nlp/                  # IMDB, AG News, Wikipedia, Common Crawl
├── marketing/            # Amazon Reviews, survey benchmarks
├── tabular/              # UCI, Kaggle tabular datasets
├── time-series/          # stock prices, energy, web traffic
├── images/               # CIFAR-10, MNIST, COCO subsets
└── research/             # academic benchmark datasets
```

---

## Recommended Sources

| Source | URL | Best For |
|---|---|---|
| Kaggle | kaggle.com/datasets | general ML, competitions |
| UCI Repository | archive.ics.uci.edu | academic benchmarks |
| Hugging Face Datasets | huggingface.co/datasets | NLP, LLM, multimodal |
| Google Dataset Search | datasetsearch.research.google.com | discovery |
| OpenML | openml.org | reproducible ML experiments |
| Papers With Code | paperswithcode.com/datasets | research benchmarks |
| Zenodo | zenodo.org | academic datasets |

---

## Key Datasets by Domain

### Recommendation Systems

| Dataset | Size | Task |
|---|---|---|
| MovieLens 100K | 100K ratings | collaborative filtering |
| MovieLens 1M | 1M ratings | collaborative filtering |
| Amazon Reviews | millions | product recommendation |
| Last.fm | 360K users | music recommendation |
| Instacart 2017 | 3M orders | grocery recommendation |

### NLP

| Dataset | Size | Task |
|---|---|---|
| IMDB Reviews | 50K | sentiment analysis |
| AG News | 120K | text classification |
| SQuAD 2.0 | 150K | question answering |
| CNN/DailyMail | 300K | summarization |
| Wikipedia | multilingual | embeddings / RAG |

### Tabular / Marketing

| Dataset | Size | Task |
|---|---|---|
| Adult Income (UCI) | 48K | binary classification |
| Bank Marketing (UCI) | 45K | churn prediction |
| Online Retail (UCI) | 540K | RFM analysis |

---

## Download Examples

```python
# HuggingFace Datasets
from datasets import load_dataset
dataset = load_dataset("imdb")
df = dataset["train"].to_pandas()
df.to_parquet("datasets/public/nlp/imdb-sentiment-v1.parquet", index=False)

# Kaggle CLI
# kaggle datasets download -d username/dataset-name -p datasets/public/tabular/

# MovieLens
import urllib.request
url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
urllib.request.urlretrieve(url, "datasets/public/recommendation/ml-100k.zip")
```

---

## License Reference

Always document the license before using a dataset in a project:

| License | Commercial Use | Attribution Required |
|---|---|---|
| CC0 | ✅ | ❌ |
| CC BY 4.0 | ✅ | ✅ |
| CC BY-NC 4.0 | ❌ | ✅ |
| MIT | ✅ | ✅ |
| Custom / Research Only | ❌ | check terms |

---

## Best Practices

- keep original downloaded files untouched in `public/`
- process and transform in `datasets/processed/` only
- document the download date and source URL in the metadata file
- verify checksums after downloading large datasets
- check license compatibility before using in commercial projects

**Common pitfalls:** modifying original files · missing license documentation · broken download links with no local backup · using research-only datasets in production
