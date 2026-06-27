# SQLGenie

Convert natural language questions into SQL using Amazon Bedrock (Claude 3 Haiku). Includes a safety layer that blocks all destructive operations and returns only SELECT statements.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Amazon Bedrock](https://img.shields.io/badge/Amazon_Bedrock-FF9900?style=flat-square&logo=amazonaws)](https://aws.amazon.com/bedrock/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

## What Problem This Solves

Writing SQL is a barrier to data access for non-technical users. SQLGenie removes that barrier: type a question in plain English, get a validated, safe SQL query back in under a second, with an explanation of what it does and why.

**Safety-first:** Only SELECT statements are returned. Any query containing INSERT, UPDATE, DELETE, DROP, TRUNCATE, or ALTER is automatically rejected before it reaches the user.

## Demo

```
Input: "Show me the top 5 customers by total order amount in the last 90 days"

SQL:
  SELECT c.customer_id, c.name, SUM(o.total) as total_spend
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  WHERE o.created_at >= NOW() - INTERVAL '90 days'
  GROUP BY c.customer_id, c.name
  ORDER BY total_spend DESC
  LIMIT 5;

Explanation: Joins customers with orders, filters to last 90 days,
             groups by customer, sums totals, returns top 5 by spend.

Safety check: PASS - SELECT only, no destructive operations.
```

## Architecture

```
User question + schema selection
        |
        v
  FastAPI /generate endpoint
        |
        v
  Prompt builder (schema + question -> structured prompt)
        |
        v
  Amazon Bedrock (Claude 3 Haiku)
        |
        v
  SQL extractor (parse SQL from LLM response)
        |
        v
  Safety validator (SELECT-only enforcement)
        |
        |-- PASS -> return SQL + explanation
        |-- FAIL -> return 400 + reason
```

**Key design decisions:**
- Schema injected into prompt so Claude understands your table structure
- Safety check runs on extracted SQL, not raw LLM output (avoids false positives)
- Three built-in schemas let you test without a real database
- Stateless API: each request is fully self-contained

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Amazon Bedrock (Claude 3 Haiku) |
| API | FastAPI + uvicorn |
| Frontend | Streamlit |
| Containerization | Docker |

## Quick Start

```bash
git clone https://github.com/Rajeshdevandla/sql-genie.git
cd sql-genie
cp .env.example .env
# Fill in your AWS credentials
pip install -r requirements.txt
uvicorn api.main:app --reload
```

API docs auto-generated at: http://localhost:8000/docs

**Required environment variables:**

| Variable | Description |
|---|---|
| `AWS_REGION` | AWS region (e.g. `us-east-1`) |
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |

### Run with Docker

```bash
docker build -t sql-genie .
docker run -p 8000:8000 --env-file .env sql-genie
```

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| GET | /schemas | List available sample schemas |
| POST | /generate | Generate SQL from a question |

**Generate SQL:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me top 5 customers by total order amount", "schema_name": "ecommerce"}'
```

**Response:**
```json
{
  "sql": "SELECT customer_id, name, SUM(total) FROM orders GROUP BY 1,2 ORDER BY 3 DESC LIMIT 5;",
  "explanation": "Groups orders by customer, sums totals, returns top 5 by spend.",
  "safety_check": "PASS",
  "schema_used": "ecommerce"
}
```

**Rejected query:**
```json
{
  "detail": "Safety check failed: query contains prohibited operation DROP."
}
```

## Built-in Sample Schemas

- **ecommerce** - `customers`, `orders`, `products`, `order_items`
- **hr** - `employees`, `departments`, `projects`
- **analytics** - `events`, `sessions`, `users`

## Project Structure

```
sql-genie/
|-- config.py              # env var config and validation
|-- core/
|   |-- sql_generator.py   # NL-to-SQL pipeline + safety validation
|-- api/
|   |-- main.py            # FastAPI routes
|-- frontend/
|   |-- app.py             # Streamlit UI
|-- schemas/               # built-in sample schemas
|-- requirements.txt
|-- .env.example
|-- Dockerfile
```

## What I'd Build Next

- **Real DB connection** - execute validated query against a live database and return actual results
- **Schema auto-detection** - infer schema from a live DB connection instead of manual input
- **SQL parser safety** - replace keyword matching with `sqlparse` for more accurate validation
- **Query history** - save past queries with ratings for reuse and refinement
- **Live hosted demo** - deploy to Hugging Face Spaces

## Related Projects

- [AskDocs AI](https://github.com/Rajeshdevandla/askdocs-ai) - PDF RAG chatbot using Amazon Bedrock and FAISS
- [AgentFlow](https://github.com/Rajeshdevandla/agent-flow) - Multi-agent orchestration with Constitutional AI safety layer
- [SupportGPT](https://github.com/Rajeshdevandla/support-gpt) - AI customer support with sentiment-aware escalation

---

Built by [Rajesh Kumar](https://rajeshdevandla.github.io) - Full Stack Java & AI Developer | Chicago, IL# SQLGenie

Convert natural language questions into SQL using Amazon Bedrock (Claude 3 Haiku). Includes a safety layer that blocks all destructive operations and returns only SELECT statements.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Amazon Bedrock](https://img.shields.io/badge/Amazon_Bedrock-FF9900?style=flat-square&logo=amazonaws)](https://aws.amazon.com/bedrock/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

## What Problem This Solves

Writing SQL is a barrier to data access for non-technical users. SQLGenie removes that barrier: type a question in plain English, get a validated, safe SQL query back in under a second, with an explanation of what it does and why.

**Safety-first:** Only SELECT statements are returned. Any query containing INSERT, UPDATE, DELETE, DROP, TRUNCATE, or ALTER is automatically rejected before it reaches the user.

## Demo

```
Input: "Show me the top 5 customers by total order amount in the last 90 days"

SQL:
  SELECT c.customer_id, c.name, SUM(o.total) as total_spend
  FROM customers c
  JOIN orders o ON c.customer_id = o.customer_id
  WHERE o.created_at >= NOW() - INTERVAL '90 days'
  GROUP BY c.customer_id, c.name
  ORDER BY total_spend DESC
  LIMIT 5;

Explanation: Joins customers with orders, filters to last 90 days,
             groups by customer, sums totals, returns top 5 by spend.

Safety check: PASS - SELECT only, no destructive operations.
```

## Architecture

```
User question + schema selection
        |
        v
  FastAPI /generate endpoint
        |
        v
  Prompt builder (schema + question -> structured prompt)
        |
        v
  Amazon Bedrock (Claude 3 Haiku)
        |
        v
  SQL extractor (parse SQL from LLM response)
        |
        v
  Safety validator (SELECT-only enforcement)
        |
        |-- PASS -> return SQL + explanation
        |-- FAIL -> return 400 + reason
```

**Key design decisions:**
- Schema injected into prompt so Claude understands your table structure
- Safety check runs on extracted SQL, not raw LLM output (avoids false positives)
- Three built-in schemas let you test without a real database
- Stateless API: each request is fully self-contained

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Amazon Bedrock (Claude 3 Haiku) |
| API | FastAPI + uvicorn |
| Frontend | Streamlit |
| Containerization | Docker |

## Quick Start

```bash
git clone https://github.com/Rajeshdevandla/sql-genie.git
cd sql-genie
cp .env.example .env
# Fill in your AWS credentials
pip install -r requirements.txt
uvicorn api.main:app --reload
```

API docs auto-generated at: http://localhost:8000/docs

**Required environment variables:**

| Variable | Description |
|---|---|
| `AWS_REGION` | AWS region (e.g. `us-east-1`) |
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |

### Run with Docker

```bash
docker build -t sql-genie .
docker run -p 8000:8000 --env-file .env sql-genie
```

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| GET | /schemas | List available sample schemas |
| POST | /generate | Generate SQL from a question |

**Generate SQL:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me top 5 customers by total order amount", "schema_name": "ecommerce"}'
```

**Response:**
```json
{
  "sql": "SELECT customer_id, name, SUM(total) FROM orders GROUP BY 1,2 ORDER BY 3 DESC LIMIT 5;",
  "explanation": "Groups orders by customer, sums totals, returns top 5 by spend.",
  "safety_check": "PASS",
  "schema_used": "ecommerce"
}
```

**Rejected query:**
```json
{
  "detail": "Safety check failed: query contains prohibited operation DROP."
}
```

## Built-in Sample Schemas

- **ecommerce** - `customers`, `orders`, `products`, `order_items`
- **hr** - `employees`, `departments`, `projects`
- **analytics** - `events`, `sessions`, `users`

## Project Structure

```
sql-genie/
|-- config.py              # env var config and validation
|-- core/
|   |-- sql_generator.py   # NL-to-SQL pipeline + safety validation
|-- api/
|   |-- main.py            # FastAPI routes
|-- frontend/
|   |-- app.py             # Streamlit UI
|-- schemas/               # built-in sample schemas
|-- requirements.txt
|-- .env.example
|-- Dockerfile
```

## What I'd Build Next

- **Real DB connection** - execute validated query against a live database and return actual results
- **Schema auto-detection** - infer schema from a live DB connection instead of manual input
- **SQL parser safety** - replace keyword matching with `sqlparse` for more accurate validation
- **Query history** - save past queries with ratings for reuse and refinement
- **Live hosted demo** - deploy to Hugging Face Spaces

## Related Projects

- [AskDocs AI](https://github.com/Rajeshdevandla/askdocs-ai) - PDF RAG chatbot using Amazon Bedrock and FAISS
- [AgentFlow](https://github.com/Rajeshdevandla/agent-flow) - Multi-agent orchestration with Constitutional AI safety layer
- [SupportGPT](https://github.com/Rajeshdevandla/support-gpt) - AI customer support with sentiment-aware escalation

---

Built by [Rajesh Kumar](https://rajeshdevandla.github.io) - Full Stack Java & AI Developer | Chicago, IL
