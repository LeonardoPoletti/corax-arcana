# Corax Arcana

> MTG Analytics Platform — Part of the KyberCorax Portfolio

A complete data platform for Magic: The Gathering players, collectors, and investors.
Built to demonstrate real-world data engineering and analytics engineering skills.

## Architecture

Raw data from the Scryfall API flows through a Medallion pipeline:

Bronze (raw) → Silver (clean) → Gold (aggregated) → Power BI + AI

## Stack

| Layer | Tools |
|---|---|
| Ingestion | Python, httpx, ijson, pyarrow |
| Storage | Parquet files, DuckDB |
| Transformation | dbt Core + dbt-duckdb |
| Orchestration | Apache Airflow |
| BI | Power BI Desktop |
| AI | sentence-transformers, ChromaDB, Ollama |
| API | FastAPI |
| Cloud | AWS S3, Databricks (Phase 8) |
| Quality | dbt tests, Soda Core |
| Dev | uv, pyenv, Ruff, pre-commit, pytest |

## Setup

```bash
# Clone the repo
gh repo clone LeonardoPoletti/corax-arcana
cd corax-arcana

# Install dependencies
uv sync
```

## Modules

1. MTG Knowledge Base
2. Deck Intelligence
3. Meta Analysis
4. Financial Intelligence
5. Match Guide
6. Social Features
7. AI Systems
8. Advanced Analytics Views

---

*KyberCorax Portfolio — Leonardo Jose Poletti*
