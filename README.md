# Automated Irish Census Pipeline - Airflow + GitHub Actions

An automated data pipeline that fetches live population data from Ireland's CSO API, validates data quality, and runs on a weekly schedule. Orchestrated with Apache Airflow, containerised with Docker, and tested on every push via GitHub Actions CI/CD.

![CI](https://github.com/SRG-Cy/airflow-pipeline/actions/workflows/ci.yml/badge.svg)

---

## 🏗️ Architecture

```
CSO PxStat API (Ireland)
        │
        ▼
⚙️ Airflow DAG (weekly schedule)
        │
        ├── Task 1: fetch_cso_data
        │     └── Calls CSO API, retrieves population data
        │           └── Pushes record count via XCom
        │
        └── Task 2: validate_data
              └── Pulls record count from XCom
                    └── Fails pipeline if data quality check fails
```

---

## 🔄 CI/CD Pipeline

Every push to `main` triggers a GitHub Actions workflow that:

1. Spins up a fresh Ubuntu environment
2. Installs Python 3.11 and Apache Airflow
3. Validates DAG syntax across all files in `dags/`
4. Initialises Airflow and confirms DAGs register correctly

If any step fails, the push is flagged immediately — catching errors before they reach production.

---

## 📋 DAG - `cso_population_pipeline`

| Property | Value |
|----------|-------|
| Schedule | Weekly (`@weekly`) |
| Start date | 2024-01-01 |
| Catchup | Disabled |
| Retries | 1 (5 minute delay) |
| Tags | `cso`, `ireland`, `population` |

### Tasks

**`fetch_cso_data`** - calls the CSO PxStat API, retrieves population data for all 26 Irish counties across 26 census years (1841-2022), and pushes the record count to Airflow XCom for downstream validation.

**`validate_data`** - pulls the record count from XCom and validates it exceeds the minimum threshold (100 records). Fails loudly if the API returns unexpected data, preventing bad data from propagating downstream.

### Task Dependencies

```
fetch_cso_data >> validate_data
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Apache Airflow 2.8.1 | Pipeline orchestration and scheduling |
| Docker Compose | Containerised local deployment |
| GitHub Actions | CI/CD - automated DAG validation on every push |
| Python 3.11 | DAG logic and API calls |
| PostgreSQL 15 | Airflow metadata database |

---

## 📁 Project Structure

```
airflow-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml              ← GitHub Actions CI pipeline
├── dags/
│   └── cso_pipeline_dag.py     ← Airflow DAG definition
├── tests/
│   └── test_dags.py            ← DAG syntax and load tests
├── docker-compose.yml          ← Airflow + PostgreSQL containers
└── .gitignore
```

---

## 🚀 How to Run Locally

### Prerequisites
- Docker Desktop
- Git

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/SRG-Cy/airflow-pipeline.git
cd airflow-pipeline
```

**2. Start all containers**
```bash
docker compose up -d
```

This starts:
- PostgreSQL (port 5433) - Airflow metadata database
- Airflow Init - creates database tables and admin user
- Airflow Webserver (port 8080) — UI
- Airflow Scheduler - DAG runner

**3. Wait 2 minutes then open Airflow UI**

Go to [http://localhost:8080](http://localhost:8080)

Login: `admin` / `admin123`

**4. Trigger the DAG**

- Find `cso_population_pipeline` in the DAG list
- Toggle to unpause
- Click ▶ Trigger DAG
- Click into the DAG → Graph view to watch tasks execute

**5. Stop containers**
```bash
docker compose stop
```

---

## 🧪 Running Tests Locally

```bash
pip install apache-airflow==2.8.1 pytest
pytest tests/
```

---

## 🌐 Data Source

- **Publisher:** Central Statistics Office (CSO) Ireland
- **API:** [CSO PxStat API](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FY001/JSON-stat/2.0/en)
- **Dataset:** FY001 — Population at Each Census
- **Coverage:** 26 counties, 26 census years, 1841–2022
- **Licence:** Public Sector Information (PSI) Licence

---

## 🔗 Related Projects

- [irish-ppr-pipeline](https://github.com/SRG-Cy/irish-ppr-pipeline) — End-to-end ELT pipeline on Irish Property Price Register (Python, dbt, PostgreSQL, Metabase)
- [cso-census-warehouse](https://github.com/SRG-Cy/cso-census-warehouse) — Star schema data warehouse on CSO Census data (dbt, PostgreSQL, Star Schema)

---

---

## 📄 Licence

MIT
