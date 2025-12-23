---
description: "This skill activates when the user asks about Aurora Serverless v2, Data API, database operations, N+1 queries, batch operations, or persistent storage for agents. Trigger on: 'Aurora Serverless', 'Data API', 'database queries', 'N+1 problem', 'batch insert', 'RDS Data API'."
---

# Aurora Serverless v2 with Data API Guide

## Overview

This project uses Aurora Serverless v2 with **Data API ONLY**:
- No VPC or NAT Gateway required
- HTTP-based access (no direct connections)
- Automatic connection pooling
- Pay-per-request pricing

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    AURORA DATA API                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │   Agent     │───▶│  Data API   │───▶│ Aurora          │  │
│  │  (Lambda/   │    │  (HTTP)     │    │ Serverless v2   │  │
│  │   ECS)      │    │             │    │                 │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│                                                               │
│  Benefits:                                                    │
│  • No VPC needed for Lambda/ECS                              │
│  • Automatic connection pooling                               │
│  • Built-in retry logic                                       │
│  • Works with IAM authentication                              │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Data API Client Setup

```python
"""Aurora Data API client configuration."""
import boto3
from functools import lru_cache
import os

@lru_cache(maxsize=1)
def get_data_api_client():
    """Get configured RDS Data API client."""
    return boto3.client('rds-data', region_name=os.getenv('AWS_REGION', 'us-east-1'))

def get_database_config() -> dict:
    """Get database configuration from SSM."""
    ssm = boto3.client('ssm')
    
    # Get from Parameter Store
    cluster_arn = ssm.get_parameter(
        Name='/prod/agent/aurora_cluster_arn',
        WithDecryption=True
    )['Parameter']['Value']
    
    secret_arn = ssm.get_parameter(
        Name='/prod/agent/aurora_secret_arn',
        WithDecryption=True
    )['Parameter']['Value']
    
    database = ssm.get_parameter(
        Name='/prod/agent/aurora_database_name'
    )['Parameter']['Value']
    
    return {
        'resourceArn': cluster_arn,
        'secretArn': secret_arn,
        'database': database,
    }
```

---

## CRITICAL: Avoid N+1 Queries

### BAD: N+1 Pattern (PROHIBITED)

```python
# ❌ NEVER DO THIS - causes N+1 queries
def save_messages_bad(messages: list) -> None:
    """BAD: One query per message."""
    client = get_data_api_client()
    config = get_database_config()
    
    for message in messages:
        # This creates N queries for N messages!
        client.execute_statement(
            **config,
            sql="INSERT INTO messages (id, content, role) VALUES (:id, :content, :role)",
            parameters=[
                {'name': 'id', 'value': {'stringValue': message['id']}},
                {'name': 'content', 'value': {'stringValue': message['content']}},
                {'name': 'role', 'value': {'stringValue': message['role']}},
            ]
        )
```

### GOOD: Batch Operations (REQUIRED)

```python
# ✅ CORRECT - Single batch query
def save_messages_good(messages: list) -> None:
    """GOOD: Batch insert all messages."""
    client = get_data_api_client()
    config = get_database_config()
    
    # Build parameter sets for batch
    parameter_sets = [
        [
            {'name': 'id', 'value': {'stringValue': msg['id']}},
            {'name': 'content', 'value': {'stringValue': msg['content']}},
            {'name': 'role', 'value': {'stringValue': msg['role']}},
        ]
        for msg in messages
    ]
    
    # Single batch execute
    client.batch_execute_statement(
        **config,
        sql="INSERT INTO messages (id, content, role) VALUES (:id, :content, :role)",
        parameterSets=parameter_sets
    )
```

---

## Query Patterns

### Single Query

```python
def get_user_by_id(user_id: str) -> dict | None:
    """Get single user by ID."""
    client = get_data_api_client()
    config = get_database_config()
    
    result = client.execute_statement(
        **config,
        sql="SELECT id, name, email, created_at FROM users WHERE id = :user_id",
        parameters=[
            {'name': 'user_id', 'value': {'stringValue': user_id}}
        ]
    )
    
    if not result.get('records'):
        return None
    
    return _parse_user_record(result['records'][0])
```

### Query with IN Clause (Multiple IDs)

```python
def get_users_by_ids(user_ids: list[str]) -> list[dict]:
    """Get multiple users by IDs - single query."""
    if not user_ids:
        return []
    
    client = get_data_api_client()
    config = get_database_config()
    
    # Build IN clause with positional parameters
    placeholders = ', '.join([f':id{i}' for i in range(len(user_ids))])
    parameters = [
        {'name': f'id{i}', 'value': {'stringValue': uid}}
        for i, uid in enumerate(user_ids)
    ]
    
    result = client.execute_statement(
        **config,
        sql=f"SELECT id, name, email FROM users WHERE id IN ({placeholders})",
        parameters=parameters
    )
    
    return [_parse_user_record(r) for r in result.get('records', [])]
```

### Pagination

```python
def get_messages_paginated(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0
) -> tuple[list[dict], int]:
    """Get messages with pagination."""
    client = get_data_api_client()
    config = get_database_config()
    
    # Get total count
    count_result = client.execute_statement(
        **config,
        sql="SELECT COUNT(*) as total FROM messages WHERE conversation_id = :conv_id",
        parameters=[
            {'name': 'conv_id', 'value': {'stringValue': conversation_id}}
        ]
    )
    total = count_result['records'][0][0]['longValue']
    
    # Get page
    result = client.execute_statement(
        **config,
        sql="""
            SELECT id, content, role, created_at 
            FROM messages 
            WHERE conversation_id = :conv_id
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :offset
        """,
        parameters=[
            {'name': 'conv_id', 'value': {'stringValue': conversation_id}},
            {'name': 'limit', 'value': {'longValue': limit}},
            {'name': 'offset', 'value': {'longValue': offset}},
        ]
    )
    
    return [_parse_message(r) for r in result.get('records', [])], total
```

---

## Transaction Support

```python
def transfer_with_transaction(from_id: str, to_id: str, amount: float) -> bool:
    """Execute multiple statements in transaction."""
    client = get_data_api_client()
    config = get_database_config()
    
    # Begin transaction
    tx = client.begin_transaction(**config)
    transaction_id = tx['transactionId']
    
    try:
        # Debit source
        client.execute_statement(
            **config,
            transactionId=transaction_id,
            sql="UPDATE accounts SET balance = balance - :amount WHERE id = :id",
            parameters=[
                {'name': 'amount', 'value': {'doubleValue': amount}},
                {'name': 'id', 'value': {'stringValue': from_id}},
            ]
        )
        
        # Credit destination
        client.execute_statement(
            **config,
            transactionId=transaction_id,
            sql="UPDATE accounts SET balance = balance + :amount WHERE id = :id",
            parameters=[
                {'name': 'amount', 'value': {'doubleValue': amount}},
                {'name': 'id', 'value': {'stringValue': to_id}},
            ]
        )
        
        # Commit
        client.commit_transaction(**config, transactionId=transaction_id)
        return True
        
    except Exception as e:
        # Rollback on error
        client.rollback_transaction(**config, transactionId=transaction_id)
        raise
```

---

## Schema Design for Agents

### Conversations Table

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    INDEX idx_user_agent (user_id, agent_id),
    INDEX idx_started_at (started_at)
);
```

### Messages Table

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_conversation (conversation_id, created_at)
);
```

### User Memories Table (Long-term)

```sql
CREATE TABLE user_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    memory_type VARCHAR(50) NOT NULL, -- 'preference', 'fact', 'entity'
    key VARCHAR(255) NOT NULL,
    value JSONB NOT NULL,
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (user_id, memory_type, key),
    INDEX idx_user_type (user_id, memory_type)
);
```

---

## Data API Limits

| Limit | Value |
|-------|-------|
| Max result size | 1 MB |
| Max SQL statement length | 64 KB |
| Max batch size | 100 parameter sets |
| Request timeout | 45 seconds |
| Max concurrent connections | Based on ACU |

### Handling Large Results

```python
def get_all_messages_chunked(conversation_id: str, chunk_size: int = 100) -> list[dict]:
    """Handle large result sets with chunking."""
    all_messages = []
    offset = 0
    
    while True:
        messages, total = get_messages_paginated(
            conversation_id,
            limit=chunk_size,
            offset=offset
        )
        
        all_messages.extend(messages)
        
        if len(all_messages) >= total:
            break
            
        offset += chunk_size
    
    return all_messages
```

---

## DO and DON'T

### DO:
- Use Data API (no direct connections)
- Batch inserts/updates
- Use transactions for multi-step operations
- Paginate large result sets
- Store connection info in SSM

### DON'T:
- Use N+1 query patterns
- Hardcode credentials
- Skip pagination for large tables
- Exceed batch size limits
- Ignore transaction rollbacks on error
