---
description: "This skill activates when the user asks about hybrid workflows, combining defined steps with LLM decisions, workflow architecture, agent patterns, or production agent design. Trigger on: 'design agent workflow', 'hybrid architecture', 'combine rules with AI', 'production agent pattern', 'defined steps vs LLM', 'workflow design'."
---

# Hybrid Workflow Pattern

## Concept

The Hybrid Workflow Pattern combines:
- **Defined Steps**: Predictable, deterministic actions (validation, data fetch, API calls)
- **LLM Decisions**: Intelligent routing, content generation, complex reasoning

This produces agents that are both **controllable** and **intelligent**.

---

## Architecture Overview

```
[Input] -> [Validator] -> [Router (LLM)] -> [Branch A: Defined Steps]
                                |           [Branch B: LLM Processing]
                                |           [Branch C: Human Review]
                                v
                          [Aggregator] -> [Output]
```

Key principle: **Structure where possible, intelligence where needed.**

---

## Implementation

### State Definition

```python
from typing import TypedDict, Annotated, Literal
from operator import add
from enum import Enum

class WorkflowPhase(str, Enum):
    INTAKE = "intake"
    ANALYSIS = "analysis"
    EXECUTION = "execution"
    REVIEW = "review"
    COMPLETE = "complete"

class AgentState(TypedDict):
    messages: Annotated[list, add]
    phase: WorkflowPhase
    input_data: dict
    analysis_result: dict | None
    execution_result: dict | None
    errors: list[str]
```

### Defined Step Nodes (No LLM)

```python
def validate_input_node(state: AgentState) -> dict:
    """Defined step: Validate input structure."""
    errors = []
    input_data = state['input_data']
    
    # Deterministic validation rules
    if 'query' not in input_data:
        errors.append("Missing required field: query")
    if len(input_data.get('query', '')) < 10:
        errors.append("Query too short (min 10 chars)")
    
    return {
        "errors": errors,
        "phase": WorkflowPhase.ANALYSIS if not errors else WorkflowPhase.COMPLETE
    }

def fetch_context_node(state: AgentState) -> dict:
    """Defined step: Fetch relevant context from database."""
    query = state['input_data']['query']
    
    # Deterministic database lookup
    context = database.search(query, limit=5)
    
    return {
        "input_data": {**state['input_data'], "context": context}
    }

def format_output_node(state: AgentState) -> dict:
    """Defined step: Format final output."""
    result = state.get('execution_result', {})
    
    # Deterministic formatting
    formatted = {
        "status": "success" if not state['errors'] else "error",
        "data": result,
        "errors": state['errors']
    }
    
    return {"execution_result": formatted, "phase": WorkflowPhase.COMPLETE}
```

### LLM Decision Nodes

```python
from config import get_model_for_node
from langsmith import Client

client = Client()

def analyze_intent_node(state: AgentState) -> dict:
    """LLM decision: Analyze user intent and classify."""
    model = get_model_for_node("analyzer")
    prompt = client.pull_prompt("my-org/intent-analyzer")
    
    response = model.invoke(
        prompt.format(
            query=state['input_data']['query'],
            context=state['input_data'].get('context', [])
        )
    )
    
    # Parse structured response
    analysis = parse_analysis(response.content)
    
    return {
        "analysis_result": analysis,
        "phase": WorkflowPhase.EXECUTION
    }

def generate_response_node(state: AgentState) -> dict:
    """LLM decision: Generate final response."""
    model = get_model_for_node("generator")
    prompt = client.pull_prompt("my-org/response-generator")
    
    response = model.invoke(
        prompt.format(
            query=state['input_data']['query'],
            analysis=state['analysis_result'],
            context=state['input_data'].get('context', [])
        )
    )
    
    return {
        "messages": [response],
        "phase": WorkflowPhase.REVIEW
    }
```

### Hybrid Router

```python
def route_by_intent(state: AgentState) -> str:
    """Route based on analyzed intent."""
    intent = state['analysis_result'].get('intent')
    confidence = state['analysis_result'].get('confidence', 0)
    
    # High confidence: automatic routing
    if confidence > 0.9:
        routing_map = {
            "simple_query": "direct_answer",
            "complex_query": "deep_analysis",
            "action_request": "tool_execution",
        }
        return routing_map.get(intent, "fallback")
    
    # Low confidence: human review
    return "human_review"
```

### Complete Graph

```python
from langgraph.graph import StateGraph, START, END

def build_hybrid_workflow():
    graph = StateGraph(AgentState)
    
    # Defined steps (no LLM)
    graph.add_node("validate", validate_input_node)
    graph.add_node("fetch_context", fetch_context_node)
    graph.add_node("format_output", format_output_node)
    
    # LLM nodes
    graph.add_node("analyze", analyze_intent_node)
    graph.add_node("generate", generate_response_node)
    graph.add_node("deep_analysis", deep_analysis_node)
    
    # Human review
    graph.add_node("human_review", human_review_node)
    
    # Edges
    graph.add_edge(START, "validate")
    graph.add_conditional_edges(
        "validate",
        lambda s: "fetch" if not s['errors'] else "end",
        {"fetch": "fetch_context", "end": END}
    )
    graph.add_edge("fetch_context", "analyze")
    graph.add_conditional_edges(
        "analyze",
        route_by_intent,
        {
            "direct_answer": "generate",
            "deep_analysis": "deep_analysis",
            "human_review": "human_review",
            "fallback": "generate"
        }
    )
    graph.add_edge("generate", "format_output")
    graph.add_edge("deep_analysis", "generate")
    graph.add_edge("human_review", "generate")
    graph.add_edge("format_output", END)
    
    return graph.compile()
```

---

## When to Use Each Type

### Use Defined Steps For:
- Input validation
- Data fetching (database, API)
- Output formatting
- Rate limiting
- Logging and metrics
- Cache management
- Error collection

### Use LLM Decisions For:
- Intent classification
- Content generation
- Complex reasoning
- Natural language understanding
- Dynamic routing
- Creative tasks

---

## Key Principles

1. **Separate Concerns**: Keep defined steps and LLM decisions in separate nodes
2. **Predictable Flow**: Critical paths should be deterministic
3. **Fallback Paths**: Always have human review or fallback options
4. **State Tracking**: Use phase/stage in state for clarity
5. **Error Handling**: Defined steps for error collection, LLM for error messaging

---

## DO and DON'T

### DO:
- Separate deterministic logic from LLM calls
- Use defined steps for validation and formatting
- Route based on confidence levels
- Include human review paths
- Track workflow phase in state

### DON'T:
- Mix validation logic with LLM calls
- Skip defined validation steps
- Trust LLM routing without confidence checks
- Forget fallback paths
