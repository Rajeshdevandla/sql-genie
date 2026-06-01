import json
import logging
import re
from typing import Optional

import boto3

logger = logging.getLogger(__name__)

DANGEROUS_KEYWORDS = [
    "DROP", "DELETE", "TRUNCATE", "INSERT", "UPDATE",
    "ALTER", "CREATE", "REPLACE", "GRANT", "REVOKE",
]

SAMPLE_SCHEMAS = {
    "ecommerce": """
    Table: customers (id, name, email, city, created_at)
    Table: orders (id, customer_id, total_amount, status, created_at)
    Table: products (id, name, category, price, stock_quantity)
    """,
    "hr": """
    Table: employees (id, name, department, salary, hire_date, manager_id)
    Table: departments (id, name, budget, location)
    """,
}


def is_safe_query(sql):
    """Check if SQL is read-only (SELECT only)."""
    sql_upper = sql.upper().strip()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in sql_upper:
            return False, f'Unsafe keyword: {keyword}'
    if not sql_upper.startswith('SELECT'):
        return False, 'Only SELECT queries are allowed'
    return True, None


class SQLGenerator:
    """
    Converts natural language questions into SQL using Amazon Bedrock.

    Flow: question + schema -> Bedrock prompt -> extract SQL -> safety check -> return
    """

    def __init__(self, aws_region, aws_access_key_id, aws_secret_access_key, model_id):
        self.bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.model_id = model_id
        logger.info("SQLGenerator initialized")

    def generate(self, question: str, schema: str) -> dict:
        """Generate SQL from a natural language question."""
        if not question.strip():
            raise ValueError("Question cannot be empty")
        if not schema.strip():
            raise ValueError("Schema cannot be empty")

        prompt = f"""You are a SQL expert. Given a schema and question, write a SELECT SQL query.

Only write SELECT queries. Be concise. Return SQL in a code block, then explain it.

Schema: {schema}

Question: {question}"""

        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            })
            response = self.bedrock.invoke_model(modelId=self.model_id, body=body)
            result = json.loads(response['body'].read())
            raw = result['content'][0]['text']

            sql = self._extract_sql(raw)
            explanation = self._extract_explanation(raw)
            is_safe, safety_msg = is_safe_query(sql)

            return {
                "sql": sql,
                "explanation": explanation,
                "is_safe": is_safe,
                "safety_message": safety_msg,
            }
        except Exception as e:
            logger.error(f'SQL generation failed: {e}')
            raise RuntimeError(f'Failed to generate SQL: {str(e)}')

    def _extract_sql(self, text: str) -> str:
        import re
        match = re.search(r'```sql(.+?)```', text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r'```(.+?)```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _extract_explanation(self, text: str) -> str:
        import re
        cleaned = re.sub(r'```.*?```', '', text, flags=re.DOTALL).strip()
        return cleaned if cleaned else 'No explanation provided.'
