---
description: "This skill activates when the user asks about LangGraph Graph API, StateGraph, nodes, edges, conditional edges, state management, reducers, or building agent workflows. Trigger on: 'how to create a LangGraph agent', 'add node to graph', 'conditional routing', 'StateGraph patterns', 'LangGraph state', 'graph.add_node', 'graph.add_edge'. This skill PROHIBITS Functional API usage (@entrypoint, @task)."
---

# LangGraph Graph API Guide

## CRITICAL: Graph API Only

This project **ONLY** uses the Graph API (StateGraph). The Functional API (`@entrypoint`, `@task` decorators) is **PROHIBITED**.

## Why Graph API Over Functional API?

| Aspect | Graph API (Required) | Functional API (Prohibited) |
|--------|---------------------|----------------------------|
| Time Travel | Full debugging support | Limited (beta) |
| State Management | Explicit, predictable | Implicit, harder to debug |
| Subgraphs | Full composition support | Limited |
| Production Readiness | Battle-tested | Newer, less tested |
| Visualization | Full graph inspection | Limited |

---

## Core Pattern: StateGraph

### Step 1: Define State with TypedDict

```python
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    """Agent state with message history and context."""
    # Reducer: messages are concatenated (not replaced)
    messages: Annotated[list, add]
    # Simple fields: replaced on each update
    current_step: str
    context: dict
    errors: list[str]
```

### Step 2: Load Model from models.yaml

```python
import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_models_config() -> dict:
    """Load and cache models.yaml configuration."""
    config_path = Path(__file__).parent.parent / "config" / "models.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def get_model_config(node_name: str) -> dict:
    """Get configuration for a specific node."""
    config = load_models_config()
    return config['nodes'][node_name]
```

### Step 3: Create Node Functions

```python
from langchain_anthropic import ChatAnthropic
from langsmith import Client

langsmith_client = Client()

def planner_node(state: AgentState) -> dict:
    """Planner node - decides next action."""
    config = get_model_config("planner")
    provider, model_name = config['model'].split(':')

    model = ChatAnthropic(
        model=model_name,
        temperature=config['temperature'],
        max_tokens=config.get('max_tokens', 2048)
    )

    # Pull prompt from Langsmith (NOT local)
    prompt = langsmith_client.pull_prompt("my-org/planner-prompt")
    formatted = prompt.format(messages=state['messages'], context=state.get('context', {}))
    response = model.invoke(formatted)

    return {"messages": [response]}
```

### Step 4: Build the Graph

```python
from langgraph.graph import StateGraph, START, END

def build_agent_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("reviewer", reviewer_node)

    # Add edges
    graph.add_edge(START, "planner")
    graph.add_conditional_edges(
        "planner",
        route_from_planner,
        {"execute": "executor", "review": "reviewer", "end": END}
    )
    graph.add_edge("executor", "reviewer")
    graph.add_edge("reviewer", END)

    return graph.compile()

app = build_agent_graph()
```

### Step 5: Routing Functions

```python
def route_from_planner(state: AgentState) -> str:
    """Route based on planner output."""
    last_message = state['messages'][-1]

    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "execute"

    content = last_message.content.lower()
    if any(word in content for word in ["review", "check", "validate"]):
        return "review"

    return "end"
```

---

## Common Patterns

### Checkpointing for Persistence

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

# Development
app_dev = graph.compile(checkpointer=MemorySaver())

# Production
pg_checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
app_prod = graph.compile(checkpointer=pg_checkpointer)

# Invoke with thread_id
config = {"configurable": {"thread_id": "user-123-session-1"}}
result = app.invoke({"messages": [user_message]}, config=config)
```

### Human-in-the-Loop

```python
from langgraph.types import interrupt, Command

def approval_node(state: AgentState) -> Command:
    decision = interrupt({
        "action": "approval_required",
        "data": state.get('pending_action'),
        "options": ["approve", "reject", "modify"]
    })

    if decision == "approve":
        return Command(goto="execute_action")
    elif decision == "reject":
        return Command(goto="abort")
    return Command(goto="modify_action", update={"feedback": decision})
```

### Subgraphs

```python
class DocState(TypedDict):
    documents: list
    summaries: list

def build_doc_subgraph():
    doc_graph = StateGraph(DocState)
    doc_graph.add_node("parse", parse_documents_node)
    doc_graph.add_node("summarize", summarize_node)
    doc_graph.add_edge(START, "parse")
    doc_graph.add_edge("parse", "summarize")
    doc_graph.add_edge("summarize", END)
    return doc_graph.compile()

# Use in main graph
main_graph.add_node("process_docs", build_doc_subgraph())
```

---

## State Management

### Reducers for Accumulating Fields

```python
class AgentState(TypedDict):
    messages: Annotated[list, add]      # Accumulates
    tool_results: Annotated[list, add]  # Accumulates
    current_phase: str                   # Replaces
    context: dict                        # Replaces
```

### Custom Reducers

```python
def merge_dicts(existing: dict, new: dict) -> dict:
    return {**existing, **new}

class AgentState(TypedDict):
    metadata: Annotated[dict, merge_dicts]
```

---

## DO and DON'T

### DO:
- Use `StateGraph` for all workflows
- Load models from `models.yaml`
- Pull prompts from Langsmith
- Define explicit state with `TypedDict`
- Use `Annotated` reducers for list fields
- Keep nodes under 50 lines

### DON'T:
- Use `@entrypoint` or `@task` decorators
- Define prompts in Python code
- Hardcode model names
- Create files over 500 lines

---

## Quick Reference

```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]

def node(state: State) -> dict:
    return {"messages": [...]}

graph = StateGraph(State)
graph.add_node("name", node_function)
graph.add_edge(START, "name")
graph.add_conditional_edges("source", router_fn, {"a": "node_a", "b": END})
app = graph.compile(checkpointer=MemorySaver())
result = app.invoke({"messages": [...]}, config={"configurable": {"thread_id": "123"}})
```
