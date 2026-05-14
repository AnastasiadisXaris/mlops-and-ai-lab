# Contributing

This document explains how the repository is organized, how to add new content, and the conventions to follow.

---

## Repository Philosophy

This repository is both a **personal knowledge base** and a **portfolio lab**. Every addition should serve one of these purposes:

- deepen understanding of a topic
- document a useful pattern or decision
- provide a runnable, testable example
- support the doctoral research (TBCA framework, conjoint analysis, NLP)

---

## Structure Overview

```text
mlops-and-ai-lab/
│
├── mlops/              # ML lifecycle, experiment tracking, serving, monitoring
│   └── examples/       # runnable MLOps examples (tracking, serving, monitoring)
├── architecture/       # system design patterns and diagrams
├── devops/             # Docker, Kubernetes, CI/CD, infrastructure
├── django/             # backend engineering, APIs, SaaS
├── llms/               # LLM applications, RAG, agents, LLMOps
│   └── examples/       # runnable LLM examples (rag/)
├── marketing-ai/       # consumer analytics, conjoint analysis, recommenders
├── datasets/           # data management, schemas, preprocessing scripts
├── projects/           # project architectures and roadmaps
├── papers/             # academic papers and research notes
├── notes/              # engineering and research notes
└── tools/              # curated tooling reference
```

---

## Adding a New Note or Document

1. Choose the correct section folder (e.g. `notes/mlops/`, `papers/llms/`)
2. Follow the naming convention for that folder (see its `README.md`)
3. Use the section's heading hierarchy: one `#` title, `##` for sections, `###` for subsections

**Example:**
```bash
# New MLOps note
notes/mlops/cusum-retraining-trigger.md

# New paper annotation
papers/conjoint-analysis/green-rao-1971-annotation.md
```

---

## Adding a Working Example

Working examples live in `<section>/examples/` folders:

```text
mlops/examples/tracking/
mlops/examples/serving/
mlops/examples/monitoring/
llms/examples/rag/
```

Every example folder must contain:

| File | Required | Purpose |
|---|---|---|
| `README.md` | ✅ | usage instructions, what it demonstrates |
| `requirements.txt` | ✅ | pinned dependencies |
| `<name>.py` | ✅ | main implementation |
| `test_<name>.py` | ✅ | pytest suite |

Tests must run **without external services** — use mocks or stubs for MLflow, databases, and LLM APIs.

---

## Adding a New Dataset

1. Store raw files in `datasets/raw/<domain>/` — never modify raw data
2. Add a dataset card in `datasets/dataset-cards/`
3. Add a metadata file in `datasets/metadata/`
4. Add a schema in `datasets/schemas/`
5. Add preprocessing script in `datasets/scripts/cleaning/`

See `datasets/README.md` for the full data lifecycle.

---

## Heading Hierarchy

All READMEs follow a strict heading hierarchy:

```markdown
# Title              ← exactly one per file
## Section           ← major sections
### Subsection       ← sub-topics within a section
**Bold label:**      ← inline labels (not headings)
```

Never use `#` for anything other than the document title.

---

## Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Python scripts | `snake_case.py` | `train_and_track.py` |
| Markdown notes | `kebab-case.md` | `rag-chunking-strategies.md` |
| Dataset files | `<domain>-<desc>-<version>.<ext>` | `consumer-conjoint-v1.parquet` |
| Schema files | `<dataset>-schema-<version>.json` | `consumer-conjoint-schema-v1.json` |
| Docker files | `Dockerfile.<service>` | `Dockerfile.api` |

---

## Code Quality

For all Python files:

- use type hints where practical
- add a module docstring with purpose, inputs, outputs, and usage
- use `argparse` for CLI scripts — no hardcoded paths
- log row counts, shapes, and key decisions with the `logging` module
- tests must be runnable with `pytest` without any setup beyond `pip install -r requirements.txt`

---

## Upgrading Sub-Folder READMEs

If you add new sub-folders with placeholder READMEs, run:

```bash
python upgrade_readmes.py
```

This upgrades any README ≤ 20 lines with structured content. Add folder-specific knowledge to the `FOLDER_KNOWLEDGE` dict in `upgrade_readmes.py` before running.

---

## Commit Message Convention

```text
feat:  add new example or document
fix:   correct an error or broken path
docs:  update README or documentation
refactor: restructure without changing content
chore: dependency updates, gitignore, tooling
```

**Examples:**
```bash
git commit -m "feat: add LLM fine-tuning example with LoRA"
git commit -m "fix: move RAG files to llms/examples/rag/"
git commit -m "docs: update mlops/examples README with serving endpoint"
```
