---
description: Validate LangGraph project structure against production-ready checklist (architecture, state, async, control flow, production)
allowed-tools: Read, Glob, Grep, Task
---

# Validate LangGraph Checklist Command

You are tasked with validating a LangGraph project against a comprehensive production-ready checklist.

## Context Discovery

First, identify the LangGraph project structure:

- Find graph files: !`find . -name "*.py" -exec grep -l "StateGraph\|CompiledGraph" {} \; 2>/dev/null | head -20`
- Find state definitions: !`find . -name "*.py" -exec grep -l "TypedDict\|BaseModel" {} \; 2>/dev/null | head -20`
- Find langgraph.json: !`find . -name "langgraph.json" 2>/dev/null`
- Find node functions: !`grep -r "def.*node\|async def.*node" --include="*.py" -l 2>/dev/null | head -10`

## Validation Pipeline

Execute the validation in 5 phases:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 PIPELINE DE VALIDAÇÃO DO PROJETO                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  ║
║   │ 1. DESIGN   │───▶│ 2. STATE    │───▶│ 3. FLUXO    │───▶│ 4. ASYNC    │  ║
║   │ & Arquitet. │    │ Management  │    │ & Controle  │    │ & Perform.  │  ║
║   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  ║
║                                    │                                         ║
║                                    ▼                                         ║
║                          ┌─────────────────┐                                 ║
║                          │  5. PRODUÇÃO    │                                 ║
║                          │  & UX/Feedback  │                                 ║
║                          └─────────────────┘                                 ║
║                                    │                                         ║
║                                    ▼                                         ║
║                            ✅ DEPLOY READY                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

______________________________________________________________________

## Phase 1: Architecture & Design

### Validation Criteria

| # | Item | How to Verify |
|---|------|---------------|
| 1.1 | Each node has **single responsibility** | Check node functions < 50 lines, one main action |
| 1.2 | I/O nodes (API, DB, LLM) **separated** from pure logic | Look for mixed concerns in nodes |
| 1.3 | **Subgraphs** used for complex flows | Check for `CompiledGraph` as nodes |
| 1.4 | Node names are **descriptive** | Names like `extract_entities` vs `node_1` |
| 1.5 | Graph **compiled** with `.compile()` | Search for `.compile()` call |

### What to Search

```python
# Good patterns (✅)
def extract_invoice_metadata(state: AgentState) -> dict:  # Single responsibility
def call_llm_categorize(state: AgentState) -> dict:       # Clear I/O node

# Bad patterns (❌)
def process_everything(state):  # God node
    extract_data()
    call_api()
    save_to_db()
    send_email()
```

______________________________________________________________________

## Phase 2: State Management

### Validation Criteria

| # | Item | How to Verify |
|---|------|---------------|
| 2.1 | State defined with **TypedDict** | Search for `class.*TypedDict` |
| 2.2 | Lists use **`Annotated[list, operator.add]`** | Check reducers for accumulating lists |
| 2.3 | Parallel nodes have reducers to **avoid data loss** | Verify fan-out patterns |
| 2.4 | State contains **raw data** (not formatted prompts) | No pre-built prompts in state |
| 2.5 | Sensitive fields use **appropriate types** | Not generic strings |
| 2.6 | Custom reducers tested with **edge cases** | Check tests for reducers |

### What to Search

```python
# Good patterns (✅)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    transactions: list[TransactionExtracted]  # Structured data

# Bad patterns (❌)
class State(TypedDict):
    prompt: str  # Pre-formatted prompt
    data: Any    # Untyped
```

______________________________________________________________________

## Phase 3: Control Flow

### Validation Criteria

| # | Item | How to Verify |
|---|------|---------------|
| 3.1 | Simple routing uses **conditional_edges** | Not Command for simple routing |
| 3.2 | **Command** used for route + state update together | Search for `Command(update=..., goto=...)` |
| 3.3 | **Command.PARENT** used to exit subgraphs | Subgraphs return to parent correctly |
| 3.4 | **Send** used for dynamic N parallelism (Map-Reduce) | Search for `Send(` pattern |
| 3.5 | Send passes **isolated state** to workers | Each Send has its own state dict |
| 3.6 | HITL uses **interrupt()** + **Command(resume=...)** | Human-in-the-loop pattern |
| 3.7 | Agent handoffs use **Command** with payload | Multi-agent communication |

### What to Search

```python
# Conditional edges (simple routing)
builder.add_conditional_edges("node", router_function)

# Command (route + update state)
return Command(update={"status": "done"}, goto="next_node")

# Send (dynamic parallelism)
return [Send("worker", {"item": i}) for i in items]

# HITL
interrupt("Please review...")
Command(resume=user_input)
```

______________________________________________________________________

## Phase 4: Async & Performance

### Validation Criteria

| # | Item | How to Verify |
|---|------|---------------|
| 4.1 | **All** I/O nodes are `async def` | Search for sync nodes with I/O |
| 4.2 | LLMs use **`ainvoke()`** | Not `.invoke()` |
| 4.3 | Tools use **`arun()`** | Not `.run()` |
| 4.4 | Graph uses **`ainvoke()`** or **`astream()`** | Entry point is async |
| 4.5 | Independent nodes configured for **fan-out** | Parallel edges from same source |
| 4.6 | **RetryPolicy** configured for API/LLM/DB nodes | Search for `retry=RetryPolicy` |
| 4.7 | **`max_concurrency`** defined for rate limits | Throttling configured |
| 4.8 | No **`time.sleep()`** inside async | Use `asyncio.sleep()` |
| 4.9 | No **sync calls inside async** | No blocking in async context |

### What to Search

```python
# Good patterns (✅)
async def call_api(state):
    result = await llm.ainvoke(messages)

builder.add_node("api", call_api, retry=RetryPolicy(max_attempts=3))

# Bad patterns (❌)
def call_api(state):  # sync!
    result = llm.invoke(messages)  # sync!

time.sleep(1)  # blocking!
```

______________________________________________________________________

## Phase 5: Production & UX

### Validation Criteria

| # | Item | How to Verify |
|---|------|---------------|
| 5.1 | **Streaming** implemented for real-time feedback | Search for `astream`, `stream_mode` |
| 5.2 | User receives **visual feedback** during processing | Progress indicators |
| 5.3 | **AsyncPostgresSaver** used in production | Not MemorySaver |
| 5.4 | Checkpointer uses **async context manager** | `async with` pattern |
| 5.5 | **`langgraph.json`** configured with `pip_installer: "uv"` | Check config file |
| 5.6 | **thread_id** generated/managed correctly per session | UUID per conversation |
| 5.7 | Structured logs for **observability** | Logger with context |
| 5.8 | **Environment variables** for secrets | No hardcoded secrets |
| 5.9 | **Health check** endpoint configured | API health endpoint |

### What to Search

```python
# Good patterns (✅)
async for event in graph.astream(input, stream_mode="updates"):
    yield event

async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)

# langgraph.json
{"pip_installer": "uv", "graphs": {...}}
```

______________________________________________________________________

## Output Format

Generate a detailed report with:

### 1. Executive Summary

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📋 LANGGRAPH VALIDATION REPORT                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   Project: [project_name]                                                    ║
║   Date: [current_date]                                                       ║
║   Overall Score: [X/Y items passed]                                          ║
║                                                                              ║
║   🏗️ Architecture:  [X/5]  [██████░░░░] 60%                                  ║
║   📦 State:         [X/6]  [████████░░] 80%                                  ║
║   🔀 Control Flow:  [X/7]  [██████████] 100%                                 ║
║   ⚡ Async:         [X/9]  [████░░░░░░] 40%                                  ║
║   🚀 Production:    [X/9]  [██████░░░░] 70%                                  ║
║                                                                              ║
║   Status: [READY FOR PRODUCTION / NEEDS IMPROVEMENTS]                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 2. Detailed Results Per Phase

For each phase, list:

- ✅ Passed items with evidence
- ❌ Failed items with specific issues found
- ⚠️ Warnings (partially compliant)
- 💡 Recommendations for improvement

### 3. Priority Actions

List the top 3-5 most critical issues to fix before production, ordered by impact.

### 4. Code Examples

For failed items, provide specific code snippets showing:

- Current problematic code
- Suggested fix

______________________________________________________________________

## Validation Process

1. **Read** the main graph file(s) identified above
1. **Search** for patterns using Grep for each checklist item
1. **Analyze** state definitions for proper typing and reducers
1. **Check** langgraph.json configuration
1. **Review** async patterns in node functions
1. **Generate** the report with findings

## Guidelines

### DO

- Be specific about file locations and line numbers
- Provide actionable recommendations
- Show code examples for fixes
- Highlight security concerns prominently

### DON'T

- Make assumptions about unread code
- Skip phases - complete all 5
- Give passing scores without evidence
- Ignore async/sync mixing issues

## Special Considerations

- If project uses **subgraphs**, validate each independently
- Check for **circular imports** in modular projects
- Verify **RetryPolicy** exists for all external API calls
- Ensure **HITL patterns** are correctly implemented if present
