---
description: Generate a LangGraph agent template with best practices for 2025
arguments:
  - name: type
    description: "Agent type: react, multi-agent, supervisor, custom"
    required: true
  - name: features
    description: "Comma-separated features: memory, hitl, streaming, tools"
    required: false
allowed_tools:
  - mcp__langchain-docs__SearchDocsByLangChain
  - Write
  - Read
---

# LangGraph Agent Generator

Generate production-ready LangGraph agent code following 2025 best practices.

## Agent Type: $ARGUMENTS.type
## Features: $ARGUMENTS.features

## Instructions

Based on the requested agent type, generate the appropriate template:

### ReAct Agent (`react`)
```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

@tool
def example_tool(query: str) -> str:
    """Example tool description."""
    return f"Result for: {query}"

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
checkpointer = MemorySaver()

agent = create_react_agent(
    model=model,
    tools=[example_tool],
    checkpointer=checkpointer,
    prompt="You are a helpful assistant."
)

# Usage
config = {"configurable": {"thread_id": "session-1"}}
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]}, config)
```

### Multi-Agent (`multi-agent` or `supervisor`)
```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]

# Specialized agents
research_agent = create_react_agent(model, [search_tool])
code_agent = create_react_agent(model, [execute_tool])

def supervisor(state: State) -> Command:
    # Route based on task
    task = classify_task(state["messages"][-1])
    if task == "research":
        return Command(goto="research")
    elif task == "code":
        return Command(goto="code")
    return Command(goto=END)

graph = StateGraph(State)
graph.add_node("supervisor", supervisor)
graph.add_node("research", research_agent)
graph.add_node("code", code_agent)
graph.add_edge(START, "supervisor")
graph.add_edge("research", "supervisor")
graph.add_edge("code", "supervisor")

app = graph.compile(checkpointer=checkpointer)
```

### Custom Agent (`custom`)
```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]
    # Add custom state fields

def agent_node(state: State):
    # Agent logic
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State):
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return END

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

## Feature Additions

### Memory (`memory`)
```python
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
app = graph.compile(checkpointer=checkpointer)
```

### Human-in-the-Loop (`hitl`)
```python
from langgraph.types import interrupt, Command

def review_node(state):
    decision = interrupt({
        "action": "review_required",
        "data": state["pending_action"]
    })
    if decision == "approve":
        return Command(goto="execute")
    return Command(goto="abort")
```

### Streaming (`streaming`)
```python
async for chunk in app.astream(input, mode="messages"):
    print(chunk)
```

### Tools (`tools`)
```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description for LLM."""
    return result
```

## Output

Generate the complete agent code based on the type and features requested, including:
1. All necessary imports
2. Tool definitions (if applicable)
3. State schema
4. Graph construction
5. Usage example with streaming
