# Raw Datasets

## Purpose

This folder stores untouched original datasets exactly as received — from surveys, APIs, Kaggle downloads, CRM exports, web scraping, or manual collection. Raw datasets are the single source of truth and must remain immutable.

---

## Naming Convention

```text
<domain>-<source>-<description>-<YYYY-MM-DD>.<ext>

# Examples:
marketing-googleforms-consumer-survey-2026-01-10.csv
nlp-kaggle-amazon-reviews-2026-02-15.parquet
recommendation-grouplens-movielens-100k-2026-01-20.zip
crm-internal-purchase-history-2026-03-01.csv
```

Including the ingestion date in the filename enables provenance tracking without opening the file.

---

## Folder Structure

```text
raw/
│
├── surveys/              # survey exports (Google Forms, Typeform, etc.)
├── api-exports/          # API data pulls (CRM, analytics platforms)
├── kaggle/               # Kaggle dataset downloads
├── scraping/             # web-scraped data
├── internal/             # internal business data exports
└── research/             # academic and thesis datasets
```

---

## Immutability Rules

Raw data must never be modified. These rules are non-negotiable:

| Rule | Reason |
|---|---|
| Never clean or transform raw files | breaks reproducibility |
| Never overwrite with a newer version | destroys audit trail |
| Never delete rows or columns | silently corrupts downstream work |
| Never rename columns in-place | breaks schema contracts |
| Always copy to `processed/` before transforming | preserves original |

---

## Provenance Template

Document every raw dataset at ingestion time:

```markdown
## Provenance Record

- **Dataset:** marketing-googleforms-consumer-survey-2026-01-10.csv
- **Source:** Google Forms survey
- **URL / System:** internal
- **Collected by:** Anastasiadis Xaris
- **Date ingested:** 2026-01-10
- **Row count:** 1,223
- **Column count:** 18
- **File size:** 387 KB
- **Format:** CSV, UTF-8
- **Checksum (SHA256):** abc123...
- **License:** proprietary
- **Notes:** includes 23 incomplete responses — handle in preprocessing
```

---

## Checksum Verification

Verify file integrity after download or transfer:

```bash
# Generate checksum
sha256sum datasets/raw/surveys/consumer-survey-2026-01-10.csv

# Verify against stored value
echo "abc123... datasets/raw/surveys/consumer-survey-2026-01-10.csv" | sha256sum --check
```

Store checksums in the provenance record and in `datasets/metadata/`.

---

## Ingestion Script Template

```python
import hashlib
import shutil
from pathlib import Path
from datetime import date

def ingest_raw(source_path: str, domain: str, description: str) -> str:
    """
    Copy a file to raw/ with standardized naming and log provenance.
    """
    source = Path(source_path)
    today = date.today().isoformat()
    dest_name = f"{domain}-{description}-{today}{source.suffix}"
    dest = Path(f"datasets/raw/{domain}/{dest_name}")
    dest.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source, dest)

    # Compute checksum
    sha256 = hashlib.sha256(dest.read_bytes()).hexdigest()

    print(f"Ingested: {dest}")
    print(f"SHA256:   {sha256}")
    print(f"Size:     {dest.stat().st_size / 1024:.1f} KB")

    return str(dest)


if __name__ == "__main__":
    ingest_raw(
        source_path="downloads/consumer_survey_export.csv",
        domain="surveys",
        description="consumer-conjoint",
    )
```

---

## DVC Integration

For large raw files (> 10 MB), track with DVC instead of Git:

```bash
dvc add datasets/raw/kaggle/movielens-100k-2026-01-20.zip
git add datasets/raw/kaggle/movielens-100k-2026-01-20.zip.dvc
dvc push
```

---

## Best Practices

- ingest raw data immediately after collection — do not pre-clean before storing
- store one file per ingestion event, not cumulative merges
- record provenance at ingestion time, not after the fact
- use DVC for files over 10 MB
- keep raw files read-only where possible (`chmod 444`)

**Common pitfalls:** cleaning data before storing raw · missing ingestion dates · no checksum records · overwriting with updated exports · storing processed data in `raw/`
