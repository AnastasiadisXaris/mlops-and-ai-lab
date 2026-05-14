"""
upgrade_readmes.py — Upgrade placeholder sub-READMEs with structured content.

For each README ≤ 15 lines, generates a proper sub-README with:
    - correct title
    - purpose description
    - what belongs here
    - naming convention
    - link back to parent section

Usage:
    python upgrade_readmes.py --dry-run   # preview without writing
    python upgrade_readmes.py             # write all upgrades
    python upgrade_readmes.py --path django/authentication  # single folder
"""

import argparse
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Knowledge base — folder-specific descriptions
# ─────────────────────────────────────────────────────────────────
FOLDER_KNOWLEDGE = {
    # django
    "django/admin":              ("Django Admin customization", "custom ModelAdmin, list_display, list_filter, inline models, admin actions, permissions"),
    "django/analytics":          ("Django analytics integration", "event tracking, user behavior logging, dashboard backends, analytics APIs"),
    "django/apps":               ("Django application modules", "app configs, AppConfig, modular app design, app-level signals and models"),
    "django/api":                ("Django REST API patterns", "ViewSets, Routers, Serializers, API versioning, pagination, filtering"),
    "django/architecture":       ("Django backend architecture", "project structure, service layers, repository patterns, dependency injection"),
    "django/authentication":     ("Django authentication", "JWT, OAuth2, session auth, social login, custom user models, token management"),
    "django/authorization":      ("Django authorization and permissions", "RBAC, object-level permissions, custom Permission classes, groups"),
    "django/caching":            ("Django caching strategies", "Redis cache, cache decorators, per-view cache, fragment caching, cache invalidation"),
    "django/ci-cd":              ("CI/CD for Django projects", "GitHub Actions workflows, test automation, Docker builds, deployment pipelines"),
    "django/database":           ("Django database configuration", "PostgreSQL setup, connection pooling, read replicas, migrations best practices"),
    "django/deployment":         ("Django deployment configuration", "Gunicorn, Nginx, Supervisor, environment configs, health checks"),
    "django/diagrams":           ("Django architecture diagrams", "request flow, data flow, service interaction, system design visuals"),
    "django/docker":             ("Docker for Django", "Dockerfiles, multi-stage builds, docker-compose for local dev, entrypoints"),
    "django/environments":       ("Django environment management", "dev/staging/prod settings, django-environ, .env files, secrets management"),
    "django/examples":           ("Django working examples", "complete mini-apps, API examples, auth examples, integration demos"),
    "django/kubernetes":         ("Kubernetes for Django", "Deployments, Services, Ingress, HPA, secrets, configmaps for Django apps"),
    "django/media":              ("Django media file handling", "MEDIA_ROOT, S3 storage backends, file uploads, image processing"),
    "django/middleware":         ("Django custom middleware", "request/response middleware, timing middleware, auth middleware, logging"),
    "django/ml-integration":     ("Django ML integration patterns", "async inference calls, model serving clients, result caching, task queues"),
    "django/models":             ("Django ORM models", "model design, relationships, custom managers, abstract models, indexes"),
    "django/monitoring":         ("Django monitoring and observability", "Prometheus metrics, Sentry, health check endpoints, structured logging"),
    "django/multi-tenancy":      ("Django multi-tenancy patterns", "tenant isolation, shared schema, separate schema, row-level isolation"),
    "django/payments":           ("Django payments integration", "Stripe, webhooks, subscription models, billing, invoice generation"),
    "django/rag":                ("RAG integration with Django", "document upload, embedding pipeline, vector search API, LLM response streaming"),
    "django/recommendation-system": ("Recommendation system in Django", "recommendation API, async model calls, result caching, user-item data models"),
    "django/scripts":            ("Django management commands and scripts", "custom manage.py commands, data migrations, seed scripts, cron jobs"),
    "django/security":           ("Django security hardening", "HTTPS, CSRF, XSS, SQL injection, security headers, SECRET_KEY rotation"),
    "django/serializers":        ("DRF serializers", "ModelSerializer, nested serializers, validation, custom fields, write methods"),
    "django/signals":            ("Django signals", "post_save, pre_delete, custom signals, signal receivers, async signals"),
    "django/static":             ("Django static files", "STATICFILES_DIRS, collectstatic, WhiteNoise, CDN integration, compression"),
    "django/tasks":              ("Django background tasks", "Celery tasks, periodic tasks, task routing, retry logic, task monitoring"),
    "django/templates":          ("Django templates", "template inheritance, template tags, custom filters, Jinja2 integration"),
    "django/testing":            ("Django testing", "pytest-django, APIClient, factory_boy, fixtures, mock patches, coverage"),
    "django/views":              ("Django views", "function-based, class-based, ViewSets, mixins, async views, response patterns"),
    "django/websocket":          ("Django WebSockets", "Django Channels, ASGI, Redis channel layer, real-time notifications, chat"),

    # llms
    "llms/APIs":                 ("LLM API integrations", "Anthropic, OpenAI, Groq, HuggingFace Inference API, rate limiting, error handling"),
    "llms/agents":               ("AI agent architectures", "ReAct agents, tool calling, agent memory, multi-step reasoning, agent orchestration"),
    "llms/alignment":            ("LLM alignment techniques", "RLHF, DPO, Constitutional AI, safety fine-tuning, output filtering"),
    "llms/architecture":         ("LLM architecture notes", "transformer internals, attention mechanisms, positional encoding, KV cache"),
    "llms/benchmarking":         ("LLM benchmarking", "MMLU, HumanEval, HellaSwag, custom domain benchmarks, evaluation harnesses"),
    "llms/datasets":             ("LLM training and evaluation datasets", "instruction datasets, preference datasets, evaluation sets"),
    "llms/deployment":           ("LLM deployment patterns", "vLLM, TGI, Ollama, BentoML serving, GPU allocation, batching strategies"),
    "llms/diagrams":             ("LLM system architecture diagrams", "RAG flows, agent loops, inference pipelines, system designs"),
    "llms/embeddings":           ("Embedding models and techniques", "Sentence Transformers, OpenAI embeddings, fine-tuning embeddings, MTEB benchmarks"),
    "llms/evaluation":           ("LLM evaluation methodologies", "faithfulness, relevance, hallucination rate, RAGAS, LLM-as-judge"),
    "llms/examples":             ("LLM working examples", "RAG demos, agent demos, fine-tuning examples, serving examples"),
    "llms/experiments":          ("LLM experiments and ablations", "prompt experiments, model comparisons, hyperparameter studies, ablation results"),
    "llms/fine-tuning":          ("LLM fine-tuning techniques", "LoRA, QLoRA, full fine-tuning, instruction tuning, dataset preparation"),
    "llms/inference":            ("LLM inference optimization", "quantization, KV cache, speculative decoding, batching, latency profiling"),
    "llms/llmops":               ("LLMOps practices", "prompt versioning, output monitoring, hallucination tracking, A/B testing, cost tracking"),
    "llms/memory":               ("LLM memory systems", "conversation history, vector memory, episodic memory, working memory patterns"),
    "llms/monitoring":           ("LLM monitoring and observability", "latency, token usage, hallucination rate, retrieval quality, cost dashboards"),
    "llms/multi-modal":          ("Multimodal AI systems", "vision-language models, image + text, audio + text, cross-modal retrieval"),
    "llms/notebooks":            ("LLM experimentation notebooks", "prompt exploration, model comparisons, RAG prototypes, fine-tuning experiments"),
    "llms/open-source":          ("Open-source LLM models", "Llama, Mistral, Gemma, DeepSeek, Qwen — deployment and fine-tuning notes"),
    "llms/orchestration":        ("LLM orchestration frameworks", "LangChain, LlamaIndex, CrewAI, Autogen — patterns and comparisons"),
    "llms/prompt-engineering":   ("Advanced prompt engineering", "chain-of-thought, few-shot, ReAct, structured outputs, prompt chaining"),
    "llms/prompting":            ("Prompting fundamentals", "zero-shot, few-shot, system prompts, prompt templates, instruction design"),
    "llms/quantization":         ("Model quantization techniques", "8-bit, 4-bit, GGUF, GPTQ, AWQ — trade-offs between quality and efficiency"),
    "llms/rag":                  ("RAG system architectures", "chunking strategies, retrieval patterns, hybrid search, reranking, RAG evaluation"),
    "llms/safety":               ("LLM safety and guardrails", "prompt injection, jailbreaks, output filtering, content moderation, red-teaming"),
    "llms/tokenization":         ("Tokenization in LLMs", "BPE, SentencePiece, tokenizer selection, token counting, context window management"),
    "llms/tools":                ("LLM tooling ecosystem", "LangChain, LlamaIndex, Ollama, vLLM, Hugging Face tools — installation and usage"),
    "llms/transformers":         ("Transformer architecture deep-dives", "self-attention, multi-head attention, feed-forward layers, positional encoding"),
    "llms/vector-databases":     ("Vector database systems", "Qdrant, ChromaDB, Pinecone, FAISS — setup, indexing, search, comparison"),
    "llms/workflows":            ("LLM workflow patterns", "multi-step pipelines, conditional routing, human-in-the-loop, approval workflows"),

    # marketing-ai
    "marketing-ai/APIs":                ("Marketing AI API integrations", "CRM APIs, ad platform APIs, analytics APIs, data ingestion clients"),
    "marketing-ai/agents":              ("AI agents for marketing", "campaign agents, reporting agents, content generation, customer support bots"),
    "marketing-ai/analytics":           ("Marketing analytics systems", "funnel analysis, cohort analysis, attribution modeling, KPI dashboards"),
    "marketing-ai/automation":          ("Marketing automation AI", "trigger-based campaigns, personalized workflows, email automation, A/B testing"),
    "marketing-ai/behavioral-analytics": ("Behavioral analytics", "clickstream analysis, session modeling, user journey mapping, engagement scoring"),
    "marketing-ai/campaign-optimization": ("Campaign optimization AI", "bid optimization, audience targeting, creative selection, budget allocation"),
    "marketing-ai/churn-prediction":    ("Customer churn prediction", "survival models, gradient boosting, early warning systems, retention triggers"),
    "marketing-ai/conjoint-analysis":   ("Conjoint analysis and utility estimation", "CBC, ACBC, part-worth utilities, MNL choice modeling, Prospect Theory debiasing, TBCA framework"),
    "marketing-ai/consumer-preference-modeling": ("Consumer preference modeling", "utility estimation, preference learning, choice models, MAUT, willingness-to-pay"),
    "marketing-ai/dashboards":          ("Marketing AI dashboards", "Streamlit, Grafana, BI dashboards, KPI tracking, real-time campaign monitoring"),
    "marketing-ai/datasets":            ("Marketing datasets", "survey data, CRM exports, campaign analytics, behavioral logs, conjoint data"),
    "marketing-ai/deployment":          ("Marketing AI deployment", "model serving, API endpoints, real-time scoring, batch prediction pipelines"),
    "marketing-ai/diagrams":            ("Marketing AI architecture diagrams", "system flows, data pipelines, model architectures, campaign automation flows"),
    "marketing-ai/evaluation":          ("Marketing AI evaluation", "CTR, conversion rate, NDCG, Precision@K, A/B test significance, uplift modeling"),
    "marketing-ai/examples":            ("Marketing AI working examples", "conjoint demos, recommendation demos, segmentation notebooks, churn prediction"),
    "marketing-ai/experimentation":     ("A/B testing and experimentation", "experiment design, statistical significance, multi-armed bandits, holdout groups"),
    "marketing-ai/feature-engineering": ("Marketing feature engineering", "RFM features, behavioral features, text features, temporal features"),
    "marketing-ai/llms":                ("LLMs in marketing", "campaign copy generation, customer support, product description, sentiment analysis"),
    "marketing-ai/marketing-mix-modeling": ("Marketing Mix Modeling (MMM)", "channel attribution, ROI estimation, budget optimization, Robyn, Meridian"),
    "marketing-ai/ml-models":           ("Predictive ML models for marketing", "classification, regression, ranking, clustering models for marketing tasks"),
    "marketing-ai/monitoring":          ("Marketing AI monitoring", "model drift, campaign performance, recommendation quality, data pipeline health"),
    "marketing-ai/nlp":                 ("NLP for marketing", "sentiment analysis, ABSA, entity extraction, topic modeling, review mining"),
    "marketing-ai/notebooks":           ("Marketing AI notebooks", "EDA, model training, campaign analysis, preference modeling experiments"),
    "marketing-ai/personalization":     ("Personalization engines", "dynamic content, product recommendations, email personalization, next-best-action"),
    "marketing-ai/predictive-analytics": ("Predictive analytics", "sales forecasting, demand prediction, customer lifetime value, lead scoring"),
    "marketing-ai/pricing-optimization": ("Dynamic pricing AI", "price elasticity, competitive pricing, willingness-to-pay estimation, revenue optimization"),
    "marketing-ai/rag":                 ("RAG for marketing intelligence", "knowledge base retrieval, campaign insight Q&A, product catalog search"),
    "marketing-ai/recommendation-systems": ("Recommendation systems for marketing", "product recommendations, content recommendations, cross-sell, upsell"),
    "marketing-ai/segmentation":        ("Customer segmentation", "RFM segmentation, behavioral clustering, psychographic profiling, dynamic segments"),
    "marketing-ai/sentiment-analysis":  ("Sentiment analysis for marketing", "review mining, brand monitoring, aspect-level sentiment, ABSA pipelines"),
    "marketing-ai/surveys":             ("Survey design and analysis", "conjoint surveys, NPS, satisfaction surveys, response bias correction"),

    # notes
    "notes/ai":              ("AI engineering notes", "concepts, architectures, model comparisons, research insights"),
    "notes/algorithms":      ("Algorithm notes", "ML algorithms, data structures, complexity, implementation notes"),
    "notes/architectures":   ("Architecture design notes", "system design decisions, trade-offs, patterns, lessons learned"),
    "notes/business":        ("Business and product notes", "product strategy, market insights, competitive analysis"),
    "notes/datasets":        ("Dataset notes", "data quality observations, preprocessing decisions, dataset comparisons"),
    "notes/debugging":       ("Debugging logs", "root causes, solutions, lessons learned from production issues"),
    "notes/deployments":     ("Deployment notes", "deployment configurations, release notes, rollback decisions"),
    "notes/devops":          ("DevOps notes", "infrastructure observations, tooling comparisons, configuration notes"),
    "notes/diagrams":        ("Architecture diagram notes", "design sketches, system flows, whiteboard notes"),
    "notes/django":          ("Django engineering notes", "patterns discovered, performance observations, gotchas"),
    "notes/experiments":     ("Experiment notes", "hypothesis, results, insights, next steps"),
    "notes/glossary":        ("Terminology glossary", "definitions, acronyms, domain-specific terms"),
    "notes/ideas":           ("Project and research ideas", "backlog ideas, feature concepts, research directions"),
    "notes/implementations": ("Implementation notes", "code decisions, library choices, integration notes"),
    "notes/learning":        ("Learning summaries", "course notes, book summaries, tutorial insights"),
    "notes/llms":            ("LLM engineering notes", "model behaviors, prompting observations, deployment findings"),
    "notes/marketing-ai":    ("Marketing AI notes", "consumer insights, model observations, campaign findings"),
    "notes/meeting-notes":   ("Meeting and discussion notes", "decisions, action items, discussion summaries"),
    "notes/ml":              ("Machine learning notes", "training observations, model comparisons, metric interpretations"),
    "notes/mlops":           ("MLOps notes", "pipeline observations, tooling comparisons, operational insights"),
    "notes/papers":          ("Paper reading notes", "key takeaways, critical assessments, connections to own work"),
    "notes/product":         ("Product notes", "feature ideas, UX observations, user feedback"),
    "notes/prompts":         ("Prompt engineering notes", "effective prompts, prompt patterns, model-specific observations"),
    "notes/references":      ("Reference notes", "links, citations, bookmarks, useful resources"),
    "notes/research":        ("Research notes", "thesis insights, theoretical connections, open questions"),
    "notes/roadmaps":        ("Learning and project roadmaps", "milestones, timelines, skill progression plans"),
    "notes/summaries":       ("Summary notes", "condensed overviews of topics, quick references"),
    "notes/system-design":   ("System design notes", "distributed systems, scalability patterns, design decisions"),
    "notes/thesis":          ("Doctoral thesis notes", "research questions, methodology decisions, supervisor feedback"),
    "notes/tutorials":       ("Tutorial notes", "step-by-step guides, how-to summaries, walkthrough notes"),
    "notes/workflows":       ("Workflow notes", "process improvements, automation ideas, operational patterns"),

    # papers
    "papers/annotations":         ("Annotated papers", "margin notes, key findings, critical observations per paper"),
    "papers/behavioral-economics": ("Behavioral economics papers", "Kahneman, Tversky, Thaler — prospect theory, bounded rationality, nudges"),
    "papers/bibliography":         ("Bibliography management", "BibTeX entries, citation collections, reference databases"),
    "papers/citations":            ("Citation index", "frequently cited works, citation networks, key references per topic"),
    "papers/conference":           ("Conference papers and proceedings", "NeurIPS, ICML, ACL, KDD, SIGIR — accepted and submitted papers"),
    "papers/conjoint-analysis":    ("Conjoint analysis papers", "Green & Rao, Louviere, choice modeling literature, TBCA-related papers"),
    "papers/consumer-behavior":    ("Consumer behavior research", "purchase decisions, behavioral patterns, attitude-behavior models"),
    "papers/datasets":             ("Dataset papers", "dataset description papers, benchmarks, data collection methodologies"),
    "papers/decision-theory":      ("Decision theory papers", "utility theory, expected utility, normative vs descriptive models"),
    "papers/diagrams":             ("Paper figures and diagrams", "extracted figures, architecture diagrams, conceptual models from papers"),
    "papers/drafts":               ("Paper drafts and manuscripts", "work-in-progress papers, submission versions, revision history"),
    "papers/evaluation":           ("Evaluation methodology papers", "metrics, benchmarks, evaluation frameworks, reproducibility studies"),
    "papers/examples":             ("Paper examples and templates", "writing examples, structure templates, abstract examples"),
    "papers/experiments":          ("Experimental result papers", "empirical studies, ablations, comparative experiments"),
    "papers/frameworks":           ("Theoretical frameworks", "conceptual models, theoretical contributions, framework papers"),
    "papers/literature-reviews":   ("Literature review papers", "systematic reviews, scoping reviews, narrative reviews"),
    "papers/llms":                 ("LLM research papers", "GPT, BERT, T5, LLaMA, alignment papers, scaling laws"),
    "papers/machine-learning":     ("Machine learning papers", "supervised, unsupervised, reinforcement learning, deep learning"),
    "papers/marketing-ai":         ("Marketing AI papers", "recommendation systems, personalization, customer analytics, ad targeting"),
    "papers/methodologies":        ("Research methodology papers", "survey design, experimental design, statistical methods"),
    "papers/nlp":                  ("NLP papers", "ABSA, sentiment analysis, information extraction, text classification"),
    "papers/notes":                ("Paper reading notes", "informal notes per paper, quick summaries, question lists"),
    "papers/personalization":      ("Personalization papers", "collaborative filtering, content-based filtering, hybrid systems"),
    "papers/publication-targets":  ("Target journals and venues", "journal profiles, impact factors, submission guidelines, deadlines"),
    "papers/rag":                  ("RAG papers", "Dense Passage Retrieval, RAG original, REALM, FiD, RETRO"),
    "papers/recommendation-systems": ("Recommendation system papers", "matrix factorization, neural CF, session-based, knowledge-graph"),
    "papers/references":           ("Reference collections", "curated reading lists, topic bibliographies"),
    "papers/scoping-reviews":      ("Scoping review papers", "domain mapping, concept identification, evidence gap analysis"),
    "papers/summaries":            ("Paper summaries", "structured 1-page summaries per paper"),
    "papers/systematic-reviews":   ("Systematic review papers", "PRISMA protocols, evidence synthesis, meta-analyses"),
    "papers/templates":            ("Paper writing templates", "abstract templates, section templates, review templates"),
    "papers/thesis":               ("Doctoral thesis papers", "dissertation chapters, thesis-related publications, supervisor drafts"),
    "papers/utility-theory":       ("Utility theory papers", "von Neumann-Morgenstern, MAUT, prospect theory, rank-dependent utility"),

    # projects
    "projects/APIs":               ("API project implementations", "REST APIs, GraphQL APIs, FastAPI projects, API documentation"),
    "projects/agents":             ("AI agent projects", "autonomous agents, multi-agent systems, tool-use implementations"),
    "projects/ai-apps":            ("AI application projects", "full-stack AI apps, AI-powered tools, intelligent interfaces"),
    "projects/analytics":          ("Analytics platform projects", "BI dashboards, data pipelines, reporting systems"),
    "projects/automation":         ("Automation projects", "workflow automation, task automation, RPA, scheduled jobs"),
    "projects/backend":            ("Backend system projects", "Django APIs, FastAPI services, microservices"),
    "projects/computer-vision":    ("Computer vision projects", "image classification, object detection, OCR, video analysis"),
    "projects/dashboards":         ("Dashboard projects", "Streamlit, Grafana, React dashboards, real-time monitoring"),
    "projects/datasets":           ("Dataset projects", "data collection, annotation, curation, synthetic generation"),
    "projects/deployment":         ("Deployment project architectures", "Kubernetes configs, Helm charts, CI/CD pipelines"),
    "projects/diagrams":           ("Project architecture diagrams", "system designs, data flows, deployment architectures"),
    "projects/django-apps":        ("Django application projects", "SaaS apps, APIs, admin panels, multi-tenant systems"),
    "projects/documentation":      ("Project documentation", "technical docs, architecture docs, API docs, runbooks"),
    "projects/evaluation":         ("Evaluation and benchmarking projects", "model evaluation frameworks, benchmark implementations"),
    "projects/examples":           ("Example and demo projects", "minimal working examples, proof-of-concepts, demos"),
    "projects/experiments":        ("Experimental projects", "research prototypes, hypothesis testing, ablation studies"),
    "projects/frontend":           ("Frontend project implementations", "React apps, Next.js, dashboards, UI components"),
    "projects/infrastructure":     ("Infrastructure projects", "Terraform configs, Kubernetes manifests, Docker setups"),
    "projects/integrations":       ("Integration projects", "third-party APIs, webhooks, data connectors"),
    "projects/llm-projects":       ("LLM application projects", "chatbots, RAG apps, agents, fine-tuning projects"),
    "projects/marketing-ai":       ("Marketing AI projects", "recommendation engines, conjoint tools, segmentation apps"),
    "projects/ml-projects":        ("ML project implementations", "end-to-end ML pipelines, model training projects"),
    "projects/mobile":             ("Mobile application projects", "React Native, Flutter, mobile ML inference"),
    "projects/monitoring":         ("Monitoring system projects", "drift detection dashboards, alerting systems, observability stacks"),
    "projects/nlp":                ("NLP project implementations", "text classifiers, NER systems, summarizers, ABSA pipelines"),
    "projects/notebooks":          ("Project notebooks", "exploratory analyses, model prototyping, visualization notebooks"),
    "projects/production":         ("Production system projects", "hardened, deployed, monitored production implementations"),
    "projects/prototypes":         ("Prototype projects", "quick MVPs, proof-of-concept implementations, early explorations"),
    "projects/rag-systems":        ("RAG system projects", "document Q&A, knowledge bases, retrieval pipelines"),
    "projects/recommendation-systems": ("Recommendation system projects", "collaborative filtering, hybrid recommenders, ranking systems"),
    "projects/research-projects":  ("Research project implementations", "thesis implementations, academic experiments, paper reproductions"),
    "projects/roadmaps":           ("Project roadmaps", "milestones, timelines, feature plans, release schedules"),
    "projects/saas-platforms":     ("SaaS platform projects", "multi-tenant apps, subscription systems, SaaS architectures"),
    "projects/templates":          ("Project templates", "starter templates, boilerplates, scaffolding"),
    "projects/thesis-projects":    ("Thesis implementation projects", "TBCA prototype, conjoint analysis tools, NLP pipelines"),
    "projects/time-series":        ("Time-series project implementations", "forecasting systems, anomaly detection, sequential models"),
    "projects/workflows":          ("Workflow system projects", "pipeline automation, DAG systems, orchestration implementations"),

    # tools
    "tools/ai":              ("AI development tools", "Hugging Face, PyTorch, TensorFlow, JAX, model hubs"),
    "tools/APIs":            ("API development tools", "Swagger, Postman, HTTPie, API testing frameworks"),
    "tools/automation":      ("Automation tools", "Makefile, scripts, task runners, workflow automation"),
    "tools/benchmarking":    ("Benchmarking tools", "pytest-benchmark, locust, k6, profiling tools"),
    "tools/cli":             ("CLI tools", "git, docker, kubectl, terraform, gh, dvc — usage and tips"),
    "tools/cloud":           ("Cloud platform tools", "AWS, GCP, Azure CLIs, cloud SDKs, cost management tools"),
    "tools/containers":      ("Container tools", "Docker, Docker Compose, Podman, container registries"),
    "tools/datasets":        ("Data tooling", "DVC, Great Expectations, Pandera, data validation tools"),
    "tools/debugging":       ("Debugging tools", "pdb, debugpy, logging, tracing, profiling tools"),
    "tools/deployment":      ("Deployment tools", "ArgoCD, FluxCD, Helm, Skaffold, deployment automation"),
    "tools/devops":          ("DevOps tooling", "Terraform, Ansible, Packer, infrastructure automation"),
    "tools/diagrams":        ("Diagram tools", "Mermaid, Draw.io, Excalidraw, PlantUML, architecture tools"),
    "tools/django":          ("Django-specific tools", "django-debug-toolbar, django-extensions, drf-spectacular"),
    "tools/documentation":   ("Documentation tools", "MkDocs, Sphinx, Docusaurus, ReadTheDocs, docstrings"),
    "tools/embeddings":      ("Embedding tools", "Sentence Transformers, OpenAI embeddings, MTEB, embedding evaluators"),
    "tools/evaluation":      ("Evaluation tools", "RAGAS, Eleuther LM eval harness, domain benchmark tools"),
    "tools/examples":        ("Tool usage examples", "real examples and configurations for tools in this ecosystem"),
    "tools/integrations":    ("Integration tools", "Zapier, n8n, webhook tools, data connector frameworks"),
    "tools/llms":            ("LLM tooling", "LangChain, LlamaIndex, Ollama, vLLM, Hugging Face Transformers"),
    "tools/ml":              ("ML framework tools", "scikit-learn, XGBoost, LightGBM, PyTorch, model selection tools"),
    "tools/mlops":           ("MLOps tooling", "MLflow, DVC, Evidently, BentoML, Weights & Biases"),
    "tools/monitoring":      ("Monitoring tools", "Prometheus, Grafana, Loki, Jaeger, Sentry, alerting tools"),
    "tools/notebooks":       ("Notebook tools", "Jupyter, VS Code notebooks, nbconvert, Papermill, Quarto"),
    "tools/orchestration":   ("Orchestration tools", "Kubernetes, Airflow, Prefect, Dagster, workflow orchestrators"),
    "tools/productivity":    ("Productivity tools", "VS Code extensions, Obsidian, Zotero, terminal tools"),
    "tools/research":        ("Research tools", "Zotero, Obsidian, LaTeX, academic writing and citation tools"),
    "tools/scraping":        ("Web scraping tools", "BeautifulSoup, Scrapy, Playwright, Selenium, scraping frameworks"),
    "tools/scripts":         ("Utility scripts", "helper scripts, automation scripts, one-off tools"),
    "tools/security":        ("Security tools", "bandit, trivy, snyk, OWASP tools, secrets scanning"),
    "tools/templates":       ("Tool configuration templates", "config templates, CI/CD templates, Dockerfile templates"),
    "tools/testing":         ("Testing tools", "pytest, coverage, factory_boy, hypothesis, load testing tools"),
    "tools/vector-databases": ("Vector database tools", "Qdrant, ChromaDB, Pinecone, FAISS, pgvector — setup and usage"),
    "tools/visualization":   ("Visualization tools", "Matplotlib, Plotly, Seaborn, Streamlit, Grafana, D3.js"),
    "tools/workflows":       ("Workflow tools", "Makefile, pre-commit hooks, task automation, dev workflow tools"),
}


def get_parent_section(path: Path) -> str:
    """Return the top-level section name."""
    parts = path.parts
    for i, p in enumerate(parts):
        if p in ["django", "llms", "marketing-ai", "notes", "papers", "projects", "tools",
                 "mlops", "architecture", "devops", "datasets"]:
            return p
    return parts[0] if parts else ""


def generate_readme(folder_path: Path, repo_root: Path) -> str:
    """Generate a smart README for a sub-folder."""
    rel = str(folder_path.relative_to(repo_root)).replace("\\", "/")
    folder_name = folder_path.name
    title = folder_name.replace("-", " ").replace("_", " ").title()
    parent = get_parent_section(folder_path.relative_to(repo_root))
    parent_readme = f"../../README.md" if folder_path.parent.parent == repo_root else "../README.md"

    # Get specific knowledge if available
    knowledge = FOLDER_KNOWLEDGE.get(rel)
    if knowledge:
        purpose, topics_str = knowledge
        topics = [t.strip() for t in topics_str.split(",")]
    else:
        purpose = f"Resources and notes related to {title.lower()}."
        topics = [folder_name.replace("-", " "), "examples", "notes", "references"]

    topics_md = "\n".join(f"- {t}" for t in topics)

    return f"""# {title}

## Purpose

{purpose}.

## What Belongs Here

{topics_md}

## Naming Convention

```text
<description>-<version>.<ext>
# or
<type>-<description>.md
```

## Notes

Add notes, examples, and resources as this folder grows.

→ [Back to {parent}/]({parent_readme})
"""


def upgrade_readmes(repo_root: Path, dry_run: bool = False,
                    target_path: str = None) -> None:
    """Find and upgrade all placeholder READMEs."""

    if target_path:
        candidates = [repo_root / target_path / "README.md"]
    else:
        candidates = list(repo_root.rglob("README.md"))

    upgraded = 0
    skipped  = 0

    for readme_path in sorted(candidates):
        if not readme_path.exists():
            print(f"  NOT FOUND: {readme_path}")
            continue

        # Skip root and top-level section READMEs
        rel = readme_path.relative_to(repo_root)
        depth = len(rel.parts)
        if depth <= 2:
            skipped += 1
            continue

        content = readme_path.read_text(encoding="utf-8")
        line_count = len(content.splitlines())

        if line_count > 15:
            skipped += 1
            continue

        new_content = generate_readme(readme_path.parent, repo_root)
        rel_str = str(rel)

        if dry_run:
            print(f"  [DRY RUN] Would upgrade ({line_count} lines): {rel_str}")
        else:
            readme_path.write_text(new_content, encoding="utf-8")
            print(f"  ✓ Upgraded ({line_count} → {len(new_content.splitlines())} lines): {rel_str}")
            upgraded += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary: {upgraded} upgraded, {skipped} skipped")


def parse_args():
    parser = argparse.ArgumentParser(description="Upgrade placeholder sub-READMEs.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--path", type=str, default=None,
                        help="Upgrade a single folder (e.g. django/authentication)")
    parser.add_argument("--repo-root", type=str, default=".",
                        help="Path to repo root (default: current directory)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    print(f"Repo root: {repo_root}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}\n")
    upgrade_readmes(repo_root, dry_run=args.dry_run, target_path=args.path)
