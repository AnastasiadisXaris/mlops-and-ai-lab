# Private Datasets

## Purpose

This folder stores restricted, confidential, or sensitive datasets — internal surveys, customer analytics, CRM exports, thesis data, and proprietary ML datasets that must not be publicly exposed.

---

## Naming Convention

```text
<domain>-<description>-<version>.<ext>

# Examples:
crm-customer-profiles-v1.parquet
survey-conjoint-raw-v1.csv
analytics-web-sessions-v2.parquet
thesis-preference-data-v1.parquet
```

---

## Folder Structure

```text
private/
│
├── surveys/              # internal survey responses
├── crm/                  # customer profiles, purchase history
├── experiments/          # thesis and research data
├── consumer-preferences/ # conjoint and preference data
├── analytics/            # internal analytics exports
└── secure-backups/       # encrypted dataset backups
```

---

## ⚠️ Security Rules

**Never commit to Git:**

```text
- personal identifiers (names, emails, phone numbers)
- raw CRM exports
- API keys or credentials embedded in data files
- confidential business metrics
- unencrypted sensitive datasets
```

**Always apply before storage:**

- anonymize or pseudonymize personal identifiers
- encrypt files containing sensitive data
- restrict folder access via `.gitignore`

---

## .gitignore Configuration

Add to your root `.gitignore` to prevent accidental commits:

```gitignore
# Private datasets
datasets/private/**/*.csv
datasets/private/**/*.parquet
datasets/private/**/*.json
datasets/private/**/*.xlsx

# Allow README and metadata only
!datasets/private/**/README.md
!datasets/private/**/metadata*.json
```

---

## DVC Integration

Large or sensitive datasets should be tracked with DVC instead of Git:

```bash
# Track a private dataset with DVC
dvc add datasets/private/surveys/conjoint-raw-v1.parquet

# Push to remote storage (S3, MinIO, GDrive)
dvc push

# Pull on another machine
dvc pull
```

DVC stores the actual file remotely and only commits a `.dvc` pointer to Git — keeping sensitive data out of the repository history.

---

## Anonymization Checklist

Before storing any dataset in this folder:

- [ ] Remove or hash direct identifiers (name, email, phone, ID numbers)
- [ ] Generalize quasi-identifiers (age → age bracket, postcode → region)
- [ ] Verify no combinations of columns re-identify individuals
- [ ] Document what was anonymized and how
- [ ] Confirm compliance with applicable regulations (GDPR)

---

## Access Control

| Level | Who | Access |
|---|---|---|
| Owner | dataset author | full read/write |
| Collaborator | trusted team member | read only |
| Public | anyone | no access |

Restrict access at the storage level — do not rely solely on `.gitignore`.

---

## Best Practices

- treat private datasets as infrastructure — version, document, and back up
- use DVC remote storage for files over 10 MB
- store only anonymized copies locally; keep originals in secure remote storage
- document retention policy — how long is each dataset kept?
- audit access logs periodically

**Common pitfalls:** accidentally committing sensitive files · relying on `.gitignore` alone · storing identifiable data without anonymization · no backup strategy · undocumented data retention
