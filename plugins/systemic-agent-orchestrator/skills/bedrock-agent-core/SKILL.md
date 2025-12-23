---
description: "This skill activates when the user asks about AWS Bedrock Agent Core, agent runtime, agent memory, short-term memory, long-term memory, MCP gateway, or production agent deployment. Trigger on: 'Bedrock Agent Core', 'agent memory', 'long-term memory', 'MCP gateway', 'agent runtime', 'production agent'."
---

# AWS Bedrock Agent Core Guide

## Overview

Bedrock Agent Core provides:
- **Agent Runtime** - Execution environment for LangGraph agents
- **Short-term Memory** - Session-based conversation context
- **Long-term Memory** - Persistent user/entity knowledge
- **MCP Gateway** - Tool integration across environments

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEDROCK AGENT CORE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌───────────────┐    ┌──────────────────┐ │
│  │  API Gateway │───▶│ Agent Runtime │───▶│   MCP Gateway    │ │
│  │   (HTTP)     │    │  (LangGraph)  │    │   (Tools)        │ │
│  └──────────────┘    └───────────────┘    └──────────────────┘ │
│                             │                                    │
│                      ┌──────┴──────┐                            │
│                      │             │                             │
│              ┌───────▼───────┐ ┌───▼────────────┐              │
│              │  Short-term   │ │   Long-term    │              │
│              │    Memory     │ │    Memory      │              │
│              │  (Session)    │ │  (Persistent)  │              │
│              └───────────────┘ └────────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Entry Point: main.py

All agents must have a `main.py` entry point:

```python
"""Agent entry point for Bedrock Agent Core Runtime."""
from agent_core import AgentCoreRuntime
from src.graph import build_agent_graph
from src.config import get_runtime_config

def create_agent():
    """Create and configure the agent for runtime."""
    graph = build_agent_graph()
    config = get_runtime_config()
    
    return AgentCoreRuntime(
        graph=graph,
        memory_config=config.memory,
        gateway_config=config.gateway,
    )

# Runtime expects this
agent = create_agent()

if __name__ == "__main__":
    # Local development
    from langchain_core.messages import HumanMessage
    
    result = agent.invoke({
        "messages": [HumanMessage(content="Hello")]
    })
    print(result)
```

---

## Memory Configuration

### Short-term Memory (Session)

For conversation context within a session:

```python
from agent_core.memory import ShortTermMemory

short_term = ShortTermMemory(
    max_messages=50,       # Limit conversation length
    summarize_after=30,    # Summarize older messages
)
```

### Long-term Memory (Persistent)

**REQUIRED** for human-facing agents:

```python
from agent_core.memory import LongTermMemory

long_term = LongTermMemory(
    storage="aurora",      # Aurora Serverless v2
    entity_extraction=True,  # Extract entities from conversations
    user_profiles=True,    # Maintain user preferences
)
```

### Combined Configuration

```python
from agent_core.memory import MemoryConfig

memory_config = MemoryConfig(
    short_term=ShortTermMemory(max_messages=50),
    long_term=LongTermMemory(storage="aurora"),
    checkpoint_storage="postgres",  # For LangGraph checkpoints
)
```

---

## MCP Gateway Integration

The MCP Gateway enables tool access across environments:

```python
from agent_core.gateway import MCPGateway

gateway = MCPGateway(
    environment="production",  # dev, homolog, production
    tools=[
        "database_query",
        "send_email",
        "calendar_booking",
    ],
    auth_method="iam",  # Use IAM roles
)
```

### Tool Definition

```python
from agent_core.tools import AgentCoreTool
from langchain_core.tools import tool

@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base."""
    # Implementation
    return results

# Register with gateway
gateway.register_tool(search_knowledge_base)
```

---

## Environment Configuration

### Development

```python
config = RuntimeConfig(
    environment="development",
    memory=MemoryConfig(
        short_term=ShortTermMemory(max_messages=50),
        # No long-term in dev
    ),
    gateway=MCPGateway(
        environment="development",
        local_mode=True,  # Use local MCP servers
    ),
)
```

### Production

```python
config = RuntimeConfig(
    environment="production",
    memory=MemoryConfig(
        short_term=ShortTermMemory(max_messages=50, summarize_after=30),
        long_term=LongTermMemory(
            storage="aurora",
            connection_string_ssm="/prod/agent/aurora_connection",
        ),
    ),
    gateway=MCPGateway(
        environment="production",
        auth_method="iam",
        allowed_tools=[
            "database_query",
            "send_notification",
        ],
    ),
    observability=ObservabilityConfig(
        langsmith_enabled=True,
        cloudwatch_enabled=True,
        log_level="INFO",
    ),
)
```

---

## State with Memory Integration

Extend AgentState to include memory:

```python
from typing import TypedDict, Annotated
from operator import add
from agent_core.memory import MemoryContext

class AgentState(TypedDict):
    # Standard fields
    messages: Annotated[list, add]
    current_step: str
    
    # Memory fields
    user_id: str
    session_id: str
    memory_context: MemoryContext
    
    # Context from long-term memory
    user_profile: dict | None
    relevant_memories: list[str]
```

### Memory-Aware Node

```python
def memory_aware_node(state: AgentState) -> dict:
    """Node that uses long-term memory."""
    # Retrieve user context
    user_profile = state.get('user_profile', {})
    relevant_memories = state.get('relevant_memories', [])
    
    # Use in prompt
    context = f"""
    User Preferences: {user_profile.get('preferences', 'None')}
    Previous Interactions: {len(relevant_memories)} relevant memories
    """
    
    # ... rest of node logic
    
    return {
        "messages": [response],
        # Optionally update memory
        "memory_updates": [
            {"type": "preference", "key": "topic", "value": "travel"}
        ]
    }
```

---

## Deployment Requirements

### Required AWS Resources

| Resource | Purpose |
|----------|---------|
| ECS Fargate | Container runtime |
| ECR | Docker images |
| Aurora Serverless v2 | Long-term memory storage |
| SSM Parameter Store | Secrets management |
| API Gateway v2 | HTTP endpoint |
| CloudWatch Logs | Logging |

### IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock-agent:*",
        "rds-data:*",
        "ssm:GetParameter",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Memory Decision Tree

```
Is the agent human-facing?
│
├─ YES ─▶ Long-term memory REQUIRED
│         │
│         └─ What data to store?
│            ├─ User preferences
│            ├─ Conversation summaries
│            ├─ Entity mentions
│            └─ Custom data per use case
│
└─ NO (API/system integration)
          │
          └─ Long-term memory OPTIONAL
             Only if:
             ├─ Need to track patterns
             ├─ Need historical context
             └─ Compliance requires it
```

---

## Testing Locally

```bash
# Start local runtime
langgraph dev

# Or with agent-core CLI
agent-core run --local

# Test with curl
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "user_id": "test-user",
    "session_id": "test-session"
  }'
```

---

## DO and DON'T

### DO:
- Use `main.py` as entry point
- Configure long-term memory for human-facing agents
- Use SSM for connection strings
- Test locally with `langgraph dev`
- Separate dev/prod configurations

### DON'T:
- Hardcode credentials
- Skip long-term memory for user-facing agents
- Mix environment configurations
- Store secrets in code
- Ignore memory limits (can cause OOM)
