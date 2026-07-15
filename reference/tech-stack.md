# Corax Arcana — Technology Stack by Phase

## Phase 1 — Product foundation

Establishing the skeleton: a functional app running in production, a well-modeled database, first real contact with cloud deployment. No heavy orchestration framework yet — that comes in Phase 2, once real data is actually flowing.

### Backend and API
- **Python + FastAPI** — *Software Eng / Data Eng*. Backend REST API. Native Python type hints + auto-generated Swagger docs. Reinforces intermediate Python with real typing (Pydantic), plus API design every DE needs to consume and build.
- **PostgreSQL** — *Analytics Eng / Data Eng*. Main transactional database, most common in BR data job postings. Advanced SQL: joins, window functions, indexes, constraints, normalization.
- **SQLAlchemy + Alembic** — *Data Eng / Software Eng*. ORM and migration management. Alembic versions the schema as code — same versioning discipline used later in dbt.

### Frontend
- **Next.js 14 + React** — *Software Eng*. Not the career focus, but a functional frontend makes the project demonstrable. Basic frontend knowledge is increasingly valued for AE roles delivering custom dashboards.
- **Tailwind CSS** — *Software Eng*. Utility-first styling, quick to apply without deep CSS knowledge.

### Cache and queues (preparation for Phase 2)
- **Redis** — *Data Eng*. Cache for Scryfall data and sessions. Introduced early because it's light to learn and essential for any production data pipeline. Appears directly in streaming architecture and feature store caching.

### Infrastructure and deployment (first cloud)
- **Docker + Docker Compose** — *Data Eng / Cloud*. Containerize the whole stack to run locally like production. Prerequisite for practically every DE job — used to run Airflow, dbt, local databases.
- **Railway (hosting)** — *Cloud*. Simplified deployment — deploy Docker Compose directly, no VPC/IAM/networking setup. First real feeling of production deployment (domain, env vars, logs, billing) without AWS's full complexity.
- **GitHub Actions (CI/CD)** — *Data Eng / Cloud*. Automated test and deploy pipeline on every push. Mentioned in nearly every Data/Analytics Engineer job description.

---

## Phase 2 — Differentiation and retention

The heart of the career transition: orchestration with Airflow, modeling with dbt, and the first real data pipeline in production (price collection, history, alerts). This phase alone is already a respectable Data Engineering portfolio.

### Data orchestration
- **Apache Airflow** — *Data Eng*. Orchestrates daily jobs: price updates, alerts, rotation reminders. Most requested orchestration tool in BR DE jobs. DAGs, scheduling, retries, sensors, TaskFlow API.
- **Python (ETL scripts)** — *Data Eng*. Extraction from Scryfall, price transformation, database loading. Real ETL/ELT patterns, error handling, idempotency, structured logging.

### Analytical modeling
- **dbt (data build tool)** — *Analytics Eng / Data Eng*. Transforms raw PostgreSQL data into clean analytical models (staging, intermediate, marts). #1 requested tool in AE jobs today. Layered modeling, data tests, auto-documentation, Jinja macros.
- **DuckDB** — *Analytics Eng*. Embedded analytical database for fast local analyses over price history without overloading transactional PostgreSQL. Growing fast in AE job postings as a lightweight warehouse alternative.

### Visualization and BI
- **Power BI** — *Analytics Eng*. Internal business metrics dashboard (DAU, Free→Pro conversion, GMV) connected to the dbt data mart. Already mastered — here it proves understanding of the full cycle: raw → modeled → visualized.

### Notifications and messaging
- **BullMQ + Redis** — *Data Eng*. Async notification queue (push, email). Introduces async processing and message queues — the conceptual gateway to Kafka (Phase 4).

### Mobile/PWA
- **Workbox (Service Worker)** — *Software Eng*. Google's library for PWA offline caching. Not a data focus, but quick to implement and makes the product truly usable on mobile.

---

## Phase 3 — Community and growth

Less pure data-technical weight, more product/architecture weight — WebSockets, messaging system, marketplace. Demonstrates systems thinking, not just isolated pipelines.

### Real-time and communication
- **WebSockets (Socket.io)** — *Software Eng*. Internal chat for trade negotiations. Not a direct DE/AE focus, but shows ability to architect stateful systems with bidirectional communication.

### Product data and analytics
- **PostHog (self-hosted or cloud)** — *Analytics Eng*. Tracking product events: likes, comments, group creation. Feeds conversion funnels and cohort analysis — central to an AE's job at product companies.
- **dbt — model expansion** — *Analytics Eng*. New analytical models: social engagement, winrate per tournament, EDH group activity. Community data becomes the richest part of the data mart. This is the type of modeling most tested in senior AE interviews.

### Search and discovery
- **PostgreSQL Full Text Search** — *Data Eng*. Search for decks, players, cards in the social feed. Using Postgres's native FTS before jumping to Elasticsearch avoids unnecessary early complexity — knowing when NOT to use a heavy tool is a senior-engineer decision.

### Image generation (sharing)
- **Satori or Puppeteer** — *Software Eng*. Generating a deck image to share on social media. Not a data focus, but visually impressive and quick to implement with existing Python/JS knowledge.

---

## Phase 4 — Scale, advanced AI, and innovation

The most technically advanced phase: Spark for large-scale processing, real ML models, AWS as the main cloud, public API. The difference between "I know how to use data tools" and "I know how to architect an end-to-end data system."

### Large-scale processing
- **Apache Spark (PySpark)** — *Data Eng*. Processing accumulated price history (potentially millions of rows after 1+ year) and training forecasting models. Cited in most senior DE job postings — used for real here, not just in a tutorial.
- **Databricks Free Edition** — *Data Eng / Cloud*. Managed environment to run Spark without configuring a cluster from scratch. Directly applies the existing Databricks Lakehouse Fundamentals certification.

### Machine Learning
- **scikit-learn** — *Data Eng*. Models for ban prediction and card appreciation projection. ML applied to real product data (not a Kaggle dataset) sets apart a DE/AE portfolio aiming toward ML Engineering.
- **MLflow** — *Data Eng*. Experiment tracking and model versioning. MLOps is increasingly mentioned in hybrid DE job postings.
- **Claude API (Anthropic)** — *Data Eng / Software Eng*. Card lore generation and opening hand analysis via LLM. LLM integration in production is currently the hottest market competency — structured prompt engineering for a real product counts a lot.

### Cloud — migration to AWS
- **AWS S3** — *Cloud / Data Eng*. Storage for images, backups, and a data lake for raw price history before Spark processing. Foundation of any data lake architecture — first real cloud experience beyond Railway.
- **AWS RDS (PostgreSQL)** — *Cloud*. Migrating the transactional database from Railway to managed RDS, with automatic backups and performance control. Natural progression from simplified hosting to real managed cloud.
- **AWS Lambda** — *Cloud / Data Eng*. Serverless functions for specific tasks: tax report generation, payment webhook processing. Frequently cited in DE job postings for event-driven pipelines.
- **Terraform** — *Cloud / Data Eng*. Infrastructure as code to provision AWS resources in a versioned, reproducible way. Increasingly expected in senior DE roles.

### API and integrations
- **FastAPI (expansion) + Swagger/OpenAPI** — *Software Eng / Data Eng*. Public API for developers with automatic documentation and rate limiting. Mature public API design (versioning, rate limiting, auth) valued in both DE and SWE.
- **Stripe / Pagar.me** — *Software Eng*. Payment gateway for the marketplace and Pro subscriptions. Not a data focus, but shows the ability to securely integrate critical financial systems.

### Mobile app
- **React Native + Expo** — *Software Eng*. Native iOS/Android app with native camera for card scanning. Not a data career focus, but completes the product as something genuinely publishable on app stores.
