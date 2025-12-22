---
description: "This skill should be used when the user asks about LangGraph agent development, ReAct agents, multi-agent systems, state management, checkpointing, human-in-the-loop, streaming, or subgraphs. Trigger on questions like 'how to create an agent with LangGraph', 'LangGraph state management', 'multi-agent orchestration', 'create_react_agent usage'."
---

# LangGraph Development Guide (2025)

## Overview

LangGraph is the **recommended framework** for building AI agents in 2025. It provides a graph-based approach to agent workflows with built-in support for state management, persistence, human-in-the-loop, and streaming.

**Version**: LangGraph 0.3+
**Companies in Production**: LinkedIn, Uber, Replit, Klarna, Elastic

## Core Concepts

### Three Main Components

1. **State**: Shared data structure representing current snapshot
2. **Nodes**: Python functions encoding agent logic
3. **Edges**: Functions determining which node to execute next

### Two APIs Available

#### Graph API (StateGraph) - Full Control
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
app = graph.compile(checkpointer=checkpointer)
```

#### Functional API - Python Native (January 2025)
```python
from langgraph.func import entrypoint, task

@task
async def my_task(input: str) -> str:
    return f"Processed: {input}"

@entrypoint(checkpointer=checkpointer)
async def my_workflow(input: str) -> str:
    result = await my_task(input)
    return result
```

### API Comparison

| Aspect | Functional API | Graph API |
|--------|---------------|-----------|
| Control Flow | Python native (if, for) | Explicit graph definition |
| State | Local scope | Declared State + reducers |
| Time Travel | Limited (beta) | Full support |
| Checkpointing | Per entrypoint | Per superstep |

## ReAct Agents (Reasoning + Acting)

### Using Prebuilt Agent
```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 25°C"

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

agent = create_react_agent(
    model=model,
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

# Execute
result = agent.invoke({"messages": [{"role": "user", "content": "Weather in Tokyo?"}]})
```

### Custom ReAct from Scratch
```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: Annotated[list, add]

def agent_node(state: AgentState):
    response = model.bind_tools(tools).invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()
```

## State Management & Persistence

### Checkpointers (Development vs Production)
```python
from langgraph.checkpoint.memory import MemorySaver      # Development
from langgraph.checkpoint.postgres import PostgresSaver  # Production
from langgraph.checkpoint.redis import RedisSaver        # Production

# Development
checkpointer = MemorySaver()

# Production with PostgreSQL
checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)

# Production with Redis
checkpointer = RedisSaver(redis_client)

# Compile with checkpointer
app = graph.compile(checkpointer=checkpointer)
```

### Thread-Based Conversations
```python
config = {"configurable": {"thread_id": "user-123-session-1"}}

# First message
result1 = app.invoke({"messages": [HumanMessage("Hello")]}, config=config)

# Follow-up (remembers previous)
result2 = app.invoke({"messages": [HumanMessage("What did I say?")]}, config=config)
```

### State Schema with Reducers
```python
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]  # Concatenates lists
    current_step: str               # Replaces value
    results: Annotated[list, add]   # Concatenates lists
```

## Memory (Short-Term & Long-Term)

### Short-Term Memory (Thread-Scoped)
Automatically handled by checkpointers within a thread.

### Long-Term Memory (Cross-Thread via Store)
```python
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore

store = PostgresStore(conn_string=DATABASE_URL)

app = graph.compile(checkpointer=checkpointer, store=store)

# Access store in nodes
def my_node(state, config, store):
    namespace = ("user", config["configurable"]["user_id"])

    # Retrieve memories
    memories = store.search(namespace, query="preferences")

    # Save memory
    store.put(namespace, "preference", {"theme": "dark"})
```

## Human-in-the-Loop

### Using `interrupt` Function (Recommended since v0.2.31)
```python
from langgraph.types import interrupt, Command

def review_node(state):
    decision = interrupt({
        "action": "review_required",
        "data": state["pending_action"],
        "options": ["approve", "reject", "modify"]
    })

    if decision == "approve":
        return Command(goto="execute")
    elif decision == "reject":
        return Command(goto="abort")
    else:
        return Command(goto="modify", update={"action": decision})
```

### Resume Execution
```python
result = app.invoke(
    Command(resume="approved"),
    config={"configurable": {"thread_id": "..."}}
)
```

### Three Main Patterns
1. **Approve/Reject**: Pause before critical action
2. **Edit State**: Pause for manual state editing
3. **Get Input**: Request additional user input

## Streaming

### Five Streaming Modes
```python
# 1. values - Full state
async for chunk in app.astream(input, mode="values"):
    print(chunk)

# 2. updates - State deltas only
async for chunk in app.astream(input, mode="updates"):
    print(chunk)

# 3. messages - LLM tokens + metadata ("typing" effect)
async for chunk in app.astream(input, mode="messages"):
    print(chunk)

# 4. custom - Arbitrary user data
async for chunk in app.astream(input, mode="custom"):
    print(chunk)

# 5. debug - Detailed traces
async for chunk in app.astream(input, mode="debug"):
    print(chunk)
```

### Real-Time Token Streaming
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4", streaming=True)

async for event in app.astream_events(input, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="", flush=True)
```

## Multi-Agent Systems

### When to Use Multi-Agent
- **Context Management**: Specialized knowledge without overloading context
- **Distributed Development**: Different teams maintain different agents
- **Parallelization**: Concurrent subtask execution

### Supervisor Pattern
```python
def supervisor(state: State) -> Command:
    task_type = classify_task(state["messages"][-1])

    if task_type == "research":
        return Command(goto="research_agent")
    elif task_type == "code":
        return Command(goto="code_agent")
    return Command(goto=END)

graph = StateGraph(State)
graph.add_node("supervisor", supervisor)
graph.add_node("research_agent", research_agent)
graph.add_node("code_agent", code_agent)
graph.add_edge(START, "supervisor")
graph.add_edge("research_agent", "supervisor")
graph.add_edge("code_agent", "supervisor")
```

### Handoff Pattern
```python
def transfer_to_sales(state):
    """Transfer to sales agent."""
    return Command(goto="sales_agent")

agent = create_react_agent(
    model,
    tools=[transfer_to_sales, transfer_to_support, *other_tools]
)
```

## Subgraphs & Composition

### Creating Subgraphs
```python
# Document processing subgraph
class DocState(TypedDict):
    document: str
    summary: str

doc_graph = StateGraph(DocState)
doc_graph.add_node("extract", extract_node)
doc_graph.add_node("summarize", summarize_node)
doc_graph.add_edge("extract", "summarize")
doc_subgraph = doc_graph.compile()

# Main graph
main_graph = StateGraph(MainState)
main_graph.add_node("process_docs", doc_subgraph)  # Subgraph as node
```

## Tools & ToolNode

### Creating Tools
```python
from langchain_core.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> list:
    """Search the database for relevant records."""
    return db.search(query, limit=limit)
```

### ToolNode
```python
from langgraph.prebuilt import ToolNode

tools = [get_weather, search_database]
tool_node = ToolNode(tools)
graph.add_node("tools", tool_node)
```

### ToolRuntime (New in 2025)
```python
from langgraph.prebuilt import InjectedToolRuntime

@tool
def my_tool(query: str, runtime: InjectedToolRuntime) -> str:
    current_state = runtime.state
    memory = runtime.store.get(...)
    runtime.stream("Processing...")
    return result
```

## Best Practices

### Six Essential Production Features
1. **Parallelization**: Execute tools/nodes in parallel
2. **Streaming**: Real-time feedback
3. **Checkpointing**: Persistence and recovery
4. **Human-in-the-Loop**: Human supervision
5. **Tracing**: Complete observability (LangSmith)
6. **Task Queue**: Job management

### Implementation Patterns
1. **Workflow-first**: Explicit state machines with human gates
2. **Agent-first**: Autonomous reasoning with tool delegation
3. **Iteration-first**: Simple loops with reflection

### Hybrid Architecture (Recommended)
```python
# LangChain for prompt chains
from langchain_core.prompts import ChatPromptTemplate
chain = prompt | model | parser

# LangGraph for orchestration
graph = StateGraph(State)
graph.add_node("process", chain)  # Chain as node
```

## References

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangGraph 0.3 Release](https://blog.langchain.com/langgraph-0-3-release-prebuilt-agents/)
- [Functional API](https://blog.langchain.com/introducing-the-langgraph-functional-api/)
- [Deep Agents](https://blog.langchain.com/deep-agents/)
- [Multi-Agent Workflows](https://blog.langchain.com/langgraph-multi-agent-workflows/)

---

**Use the MCP tool `SearchDocsByLangChain` to find specific documentation and examples.**
