# SQLGenie

Convert natural language questions into SQL queries using Amazon Bedrock. Includes a safety layer that blocks destructive queries and returns only SELECT statements.

---

## What this does

You type a question like "show me the top 10 customers by total spend" and the app generates the correct SQL for your database schema. It also explains what the query does and validates that it's safe to run.

## How it works

```
User question + database schema
          │
          ▼
    Amazon Bedrock (Claude)
          │
          ▼
    Extract SQL from response
          │
          ▼
    Safety check (SELECT only, no DROP/DELETE/etc)
          │
          ▼
    Return SQL + explanation
```

## Tech stack

| Component | Technology |
|-----------|-----------|
| LLM | Amazon Bedrock (Claude 3 Haiku) |
| API | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker |

## Project structure

```
sql-genie/
├── config.py           # env var config
├── core/
│   └── sql_generator.py  # NL-to-SQL + safety validation
├── api/
│   └── main.py         # FastAPI routes
├── requirements.txt
├── .env.example
└── Dockerfile
```

## Getting started

```bash
git clone https://github.com/Rajeshdevandla/sql-genie.git
cd sql-genie
cp .env.example .env
# fill in your AWS credentials
pip install -r requirements.txt
uvicorn api.main:app --reload
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /schemas | List sample schemas to try |
| POST | /generate | Generate SQL from a question |

**Example:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show me top 5 customers by total order amount",
    "schema": "",
    "schema_name": "ecommerce"
  }'
```

## Sample schemas

Built-in schemas you can use without setting up a real database:
- `ecommerce` — customers, orders, products, order_items
- `hr` — employees, departments, projects

## Safety features

- Only SELECT queries are returned — no INSERT, UPDATE, DELETE, DROP, etc.
- Any query failing the safety check returns a 400 error with a reason
- Basic keyword matching for now — a real system would use a SQL parser

---

Built as part of a GenAI portfolio for cloud/AI engineering roles.
