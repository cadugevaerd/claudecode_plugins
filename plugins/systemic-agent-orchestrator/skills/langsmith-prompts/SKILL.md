---
description: "This skill activates when the user asks about Langsmith prompts, prompt management, storing prompts, versioning prompts, or retrieving prompts from Langsmith. Trigger on: 'store prompt in Langsmith', 'pull prompt', 'version prompts', 'prompt management', 'hub.pull', 'client.pull_prompt'."
---

# Langsmith Prompts Guide

## Why Langsmith for Prompts?

This project **PROHIBITS** local prompt definitions. All prompts must be stored in Langsmith because:

1. **Version Control**: Track prompt changes over time
2. **A/B Testing**: Test prompt variations in production
3. **Analytics**: Monitor prompt performance
4. **Collaboration**: Team can edit prompts without code changes
5. **Rollback**: Quickly revert to previous prompt versions

---

## Setup

### 1. Configure Environment

```bash
export LANGCHAIN_API_KEY="lsv2_..."
export LANGCHAIN_PROJECT="my-agent"
export LANGCHAIN_TRACING_V2="true"
```

### 2. Initialize Client

```python
from langsmith import Client

client = Client()
```

---

## Creating Prompts in Langsmith

### Via Python SDK

```python
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

client = Client()

# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a {role} assistant.

Your task: {task_description}

Guidelines:
- Be concise and accurate
- Use structured output when appropriate
- Ask for clarification if needed"""),
    ("human", "{user_input}")
])

# Push to Langsmith
client.push_prompt(
    "my-org/planner-prompt",
    object=prompt,
    description="Planner node prompt for workflow routing",
    tags=["production", "planner"]
)
```

### Via Langsmith UI

1. Go to https://smith.langchain.com
2. Navigate to "Prompts"
3. Click "New Prompt"
4. Create prompt with variables using `{variable_name}` syntax
5. Save and version

---

## Retrieving Prompts

### Basic Pull

```python
from langsmith import Client

client = Client()
prompt = client.pull_prompt("my-org/planner-prompt")

# Use the prompt
formatted = prompt.format(
    role="planning",
    task_description="Route user requests",
    user_input="I need help with my order"
)
```

### With Version

```python
# Pull specific version
prompt = client.pull_prompt("my-org/planner-prompt:v2")

# Pull latest
prompt = client.pull_prompt("my-org/planner-prompt:latest")
```

### Using LangChain Hub

```python
from langchain import hub

# Alternative: use hub
prompt = hub.pull("my-org/planner-prompt")
```

---

## Best Practices

### Naming Convention

```
{organization}/{node-name}-prompt

Examples:
- acme-corp/planner-prompt
- acme-corp/executor-prompt
- acme-corp/reviewer-prompt
- acme-corp/error-handler-prompt
```

### Prompt Structure

```python
# Good: Clear sections, variables documented
"""You are a {role} assistant for {domain}.

## Task
{task_description}

## Input
{user_input}

## Context (if available)
{context}

## Output Format
Respond with JSON:
{
  "decision": "action_name",
  "reasoning": "explanation",
  "confidence": 0.0-1.0
}
"""
```

### Variables

Use descriptive variable names:
- `{user_input}` - Raw user message
- `{context}` - Retrieved context
- `{history}` - Conversation history
- `{task_description}` - Current task
- `{constraints}` - Rules/limitations

### Tagging

```python
client.push_prompt(
    "my-org/prompt-name",
    object=prompt,
    tags=[
        "production",      # Environment
        "planner",         # Node type
        "v2",              # Version indicator
        "claude-optimized" # Model optimization
    ]
)
```

---

## Integration Pattern

### In Node Functions

```python
from langsmith import Client
from functools import lru_cache

_client = None

def get_langsmith_client() -> Client:
    global _client
    if _client is None:
        _client = Client()
    return _client

@lru_cache(maxsize=10)
def get_prompt(prompt_name: str):
    """Cache prompts to avoid repeated API calls."""
    client = get_langsmith_client()
    return client.pull_prompt(prompt_name)

def planner_node(state: AgentState) -> dict:
    """Planner node using Langsmith prompt."""
    prompt = get_prompt("my-org/planner-prompt")
    model = get_model_for_node("planner")
    
    formatted = prompt.format(
        role="workflow planner",
        task_description="Analyze request and decide next action",
        user_input=state['messages'][-1].content,
        context=state.get('context', '')
    )
    
    response = model.invoke(formatted)
    return {"messages": [response]}
```

### Error Handling

```python
import os
import logging

def get_prompt_safe(prompt_name: str, fallback: str = None):
    """Get prompt with fallback for development."""
    try:
        return get_prompt(prompt_name)
    except Exception as e:
        if fallback and os.getenv('ENVIRONMENT') == 'development':
            logging.warning(f"Using fallback prompt for {prompt_name}: {e}")
            from langchain_core.prompts import ChatPromptTemplate
            return ChatPromptTemplate.from_template(fallback)
        raise
```

---

## Workflow

1. **Create prompt** in Langsmith UI or via SDK
2. **Test prompt** with sample inputs in Langsmith
3. **Version prompt** when satisfied
4. **Deploy code** that references the prompt by name
5. **Monitor performance** in Langsmith dashboard
6. **Iterate** by creating new versions

---

## DO and DON'T

### DO:
- Store ALL prompts in Langsmith
- Use descriptive prompt names
- Version important prompts
- Tag prompts for organization
- Cache prompts in production
- Use structured variables

### DON'T:
- Define prompts in Python code
- Use hardcoded strings for prompts
- Skip prompt versioning
- Forget to handle prompt loading errors
- Store sensitive data in prompts
