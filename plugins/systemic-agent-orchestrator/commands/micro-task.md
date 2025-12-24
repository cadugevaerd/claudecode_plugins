---
description: Execute a focused micro-task following project guardrails (fix tests, add validation, refactor function)
argument-hint: "<task-description>"
allowed-tools:
  # Claude Code native tools
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  # Serena symbolic tools
  - mcp__plugin_systemic-agent-orchestrator_serena__list_dir
  - mcp__plugin_systemic-agent-orchestrator_serena__search_for_pattern
  - mcp__plugin_systemic-agent-orchestrator_serena__find_symbol
  - mcp__plugin_systemic-agent-orchestrator_serena__get_symbols_overview
  - mcp__plugin_systemic-agent-orchestrator_serena__replace_symbol_body
  - mcp__plugin_systemic-agent-orchestrator_serena__insert_after_symbol
  - mcp__plugin_systemic-agent-orchestrator_serena__insert_before_symbol
  # Serena memories (read + write)
  - mcp__plugin_systemic-agent-orchestrator_serena__list_memories
  - mcp__plugin_systemic-agent-orchestrator_serena__read_memory
  - mcp__plugin_systemic-agent-orchestrator_serena__write_memory
  # Knowledge MCPs - MUST USE
  - mcp__plugin_langchain-ecosystem-helper_langchain-docs__SearchDocsByLangChain
  - mcp__plugin_aws-documentation-helper_aws-knowledge-mcp-server__aws___search_documentation
  # Serena initialization
  - mcp__plugin_systemic-agent-orchestrator_serena__initial_instructions
---

# Micro-Task Execution

Execute a small, focused task following all project guardrails.

## Arguments

- `task-description`: Brief description of the micro-task (e.g., "fix failing tests", "add input validation to planner node")

## Scope Limits

Micro-tasks are LIMITED to:
- **Max 3 files** modified
- **Max 100 lines** changed total
- **Single concern** only
- **No new dependencies** without explicit approval

If task exceeds these limits, STOP and suggest breaking into smaller tasks.

## Infrastructure Context (Production Requirements)

**⚠️ CRITICAL: All agents run on AgentCore Runtime in production.**

### Data Types: Agent Memory vs Systemic Data

**Understanding the difference is CRITICAL for choosing the right access pattern.**

| Aspect | Agent Memory | Systemic Data |
| ------ | ------------ | ------------- |
| **What** | User/session context managed by AgentCore | Business/operational data of the application |
| **Examples** | User preferences, conversation history, user profile, mentioned entities | Products, orders, configurations, logs, business entities |
| **Persistence** | AgentCore Memory Service | Aurora Serverless v2 |
| **Access** | MCP Gateway tools | DATA_API (`boto3.client('rds-data')`) |
| **Scope** | Per-user, per-session | Application-wide |

**Decision Rule:**

- If it's about **the user or the conversation** → **Agent Memory** (MCP Gateway)
- If it's about **the business or system** → **Systemic Data** (DATA_API)

**Concrete Examples:**

```python
# AGENT MEMORY - User/conversation context
store_user_preference(user_id, "response_style", "concise")  # User prefers short answers
store_entity(user_id, "travel_date", "January 2025")         # User mentioned travel plans
retrieve_user_context(user_id)                                # Get user profile + history

# SYSTEMIC DATA - Business/operational data
query_products(category="electronics")                        # Query product catalog
create_order(user_id, items=[...])                           # Create business transaction
get_system_config("feature_flags")                           # Application configuration
```

### AgentCore Runtime Rules

1. **Runtime Environment**: Every agent will be deployed and executed in the **Bedrock AgentCore Runtime**
   - Entry point must be `main.py` with `create_agent()` function
   - Use `AgentCoreRuntime` wrapper for the graph
   - Configure `RuntimeConfig` for dev/prod environments

2. **Memory via MCP Gateway ONLY**: Any task involving memory operations **MUST use tools registered in the MCP Gateway**
   - ❌ **NEVER** implement memory directly in nodes
   - ❌ **NEVER** access databases directly from agent code
   - ✅ **ALWAYS** use `MCPGateway.register_tool()` for memory operations
   - ✅ **ALWAYS** define memory tools as `@tool` decorated functions

3. **Memory Architecture**:

   ```text
   Node → calls tool → MCP Gateway → Memory Storage
   ```

   - Short-term memory: Session-based, managed by AgentCore
   - Long-term memory: Must be a registered tool in MCP Gateway
   - User profiles: Access via `get_user_profile` tool
   - Entity storage: Access via `store_entity` / `retrieve_entity` tools

4. **Systemic Persistence (Aurora Serverless + DATA_API)**:
   - All systemic data (non-memory) uses **Aurora Serverless v2**
   - All database operations MUST use **DATA_API** (RDS Data API)
   - ❌ **NEVER** use direct psycopg2/pg8000 connections
   - ✅ **ALWAYS** use `boto3.client('rds-data')` for queries
   - Connection strings stored in SSM Parameter Store

### Example: Memory Tool Pattern

```python
# ✅ CORRECT: Memory as MCP Gateway Tool
from agent_core.tools import AgentCoreTool
from langchain_core.tools import tool

@tool
def store_user_preference(user_id: str, key: str, value: str) -> str:
    """Store a user preference in long-term memory."""
    # Implementation via Aurora/DynamoDB
    return f"Stored {key}={value} for user {user_id}"

@tool
def retrieve_user_context(user_id: str) -> dict:
    """Retrieve user context from long-term memory."""
    # Implementation via Aurora/DynamoDB
    return {"preferences": {...}, "history": [...]}

# Register with gateway
gateway.register_tool(store_user_preference)
gateway.register_tool(retrieve_user_context)
```

```python
# ❌ WRONG: Direct memory access in node
def planner_node(state: AgentState) -> dict:
    # WRONG - direct DB access
    conn = psycopg2.connect(...)  # ❌ NEVER DO THIS
    user_data = conn.execute("SELECT * FROM users...")  # ❌

    # WRONG - in-memory storage
    global user_cache  # ❌ NEVER DO THIS
    user_cache[user_id] = data  # ❌
```

### Example: Systemic Persistence (DATA_API)

```python
# ✅ CORRECT: Using Aurora DATA_API
import boto3

rds_data = boto3.client('rds-data')

@tool
def query_system_data(entity_type: str, entity_id: str) -> dict:
    """Query systemic data from Aurora via DATA_API."""
    response = rds_data.execute_statement(
        resourceArn='arn:aws:rds:us-east-1:123456789:cluster:my-cluster',
        secretArn='arn:aws:secretsmanager:us-east-1:123456789:secret:my-secret',
        database='agent_db',
        sql='SELECT * FROM entities WHERE type = :type AND id = :id',
        parameters=[
            {'name': 'type', 'value': {'stringValue': entity_type}},
            {'name': 'id', 'value': {'stringValue': entity_id}},
        ]
    )
    return response['records']

@tool
def store_system_data(entity_type: str, entity_id: str, data: dict) -> str:
    """Store systemic data to Aurora via DATA_API."""
    rds_data.execute_statement(
        resourceArn='arn:aws:rds:us-east-1:123456789:cluster:my-cluster',
        secretArn='arn:aws:secretsmanager:us-east-1:123456789:secret:my-secret',
        database='agent_db',
        sql='INSERT INTO entities (type, id, data) VALUES (:type, :id, :data)',
        parameters=[
            {'name': 'type', 'value': {'stringValue': entity_type}},
            {'name': 'id', 'value': {'stringValue': entity_id}},
            {'name': 'data', 'value': {'stringValue': json.dumps(data)}},
        ]
    )
    return f"Stored {entity_type}/{entity_id}"
```

```python
# ❌ WRONG: Direct psycopg2 connection
import psycopg2  # ❌ NEVER import this

conn = psycopg2.connect(
    host="my-aurora-cluster.cluster-xyz.us-east-1.rds.amazonaws.com",
    database="agent_db",
    user="admin",
    password="secret"  # ❌ Hardcoded credentials!
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM entities")  # ❌ Direct connection
```

### Infrastructure Checklist

Before implementing any micro-task, verify:

- [ ] Does this task involve memory? → Must use MCP Gateway tool
- [ ] Does this task need user context? → Use `retrieve_user_context` tool
- [ ] Does this task store data? → Use appropriate MCP Gateway tool
- [ ] Does this task need database access? → Must use DATA_API (rds-data)
- [ ] Is the code compatible with AgentCore Runtime?
- [ ] Are ARNs stored in SSM/Secrets Manager (not hardcoded)?

## Workflow

### 0. Load Serena Manual (REQUIRED - First Step)

**Before starting ANY micro-task, execute the Serena initial instructions.**

```python
mcp__plugin_systemic-agent-orchestrator_serena__initial_instructions()
```

This loads the 'Serena Instructions Manual' with essential guidelines for symbolic operations, memory management, and project context handling.

**⚠️ NEVER skip this step. Execute it at the beginning of every micro-task.**

### 1. Understand Task (1 min)
- Parse task description
- Identify affected files/symbols
- Verify scope is micro (≤3 files, ≤100 lines)
- Extract keywords for knowledge search

### 2. Knowledge Fetch (2 min) - PARALLEL & MANDATORY
**⚠️ ALWAYS execute ALL searches before coding. Never skip MCPs.**

Execute these searches IN PARALLEL:

#### 2.1 Serena Memories (REQUIRED)
```python
# Step 1: List all memories
list_memories()

# Step 2: Read relevant ones based on task keywords
read_memory("langgraph-langchain-langsmith-agents-2025")  # if LangGraph/agent task
read_memory("claude-code-hooks-format")                    # if hooks task
```

#### 2.2 MCP LangChain Docs (REQUIRED for Python/Agent tasks)
**MUST call `SearchDocsByLangChain` for any task involving:**
- LangGraph, nodes, edges, state, agents
- LangChain, LCEL, chains, prompts
- Any Python agent code

```python
# ALWAYS execute - extract search query from task
SearchDocsByLangChain(query="<extracted-problem-pattern>")

# Examples:
SearchDocsByLangChain(query="conditional edges routing LangGraph")
SearchDocsByLangChain(query="StateGraph add node pattern")
SearchDocsByLangChain(query="LangGraph state reducer")
```

#### 2.3 MCP AWS Docs (REQUIRED for AWS tasks)
**MUST call `aws___search_documentation` for any task involving:**
- AWS services (Lambda, S3, DynamoDB, Bedrock, etc.)
- Terraform AWS resources
- CloudFormation

```python
# ALWAYS execute for AWS tasks
aws___search_documentation(search_phrase="<aws-topic>", topics=["general"])

# Examples:
aws___search_documentation(search_phrase="Bedrock agent memory", topics=["general"])
aws___search_documentation(search_phrase="Aurora Serverless Data API", topics=["reference_documentation"])
```

#### 2.4 Project Skills (Check if applicable)
Read relevant skill files:
- `langgraph-graph-api/SKILL.md` - StateGraph patterns
- `langsmith-prompts/SKILL.md` - Prompt management
- `models-yaml-config/SKILL.md` - Model configuration

**Output**: Use ALL fetched knowledge silently as implementation context.

### 3. Locate Code (2 min)
Use Serena tools to find relevant code:
```
get_symbols_overview -> find_symbol -> search_for_pattern
```

### 4. Plan Changes (1 min)
List exact changes:
```
File: src/nodes/planner.py
Symbol: validate_input
Action: Add null check for 'messages' field
Lines: ~5 new lines
```

### 5. Implement (5 min)
Use Serena symbolic editing or Claude Code native tools:
- `replace_symbol_body` for function updates
- `insert_after_symbol` for new code
- `insert_before_symbol` for imports
- `Edit` for precise line changes

### 5.5 Add Debug Logs (1 min) - REQUIRED FOR FIXES

**After implementing a fix, add strategic logging to facilitate future debugging.**

#### When to Add Logs
- ✅ Bug fixes (errors, edge cases, validation issues)
- ✅ Complex logic changes
- ✅ Integration points (API calls, external services)
- ❌ Skip for trivial changes (typos, formatting)

#### Logging Pattern
```python
import logging

logger = logging.getLogger(__name__)

def fixed_function(state: AgentState) -> AgentState:
    # Log entry with context
    logger.info(f"[fixed_function] called with {len(state.get('messages', []))} messages")

    # Log critical decision points
    if some_condition:
        logger.info(f"[fixed_function] condition met: {some_value}")

    # Log before potential failure points
    logger.info(f"[fixed_function] processing: {key_variable}")

    # Log exit with result summary
    logger.info(f"[fixed_function] completed, returning {len(result)} items")
    return result
```

#### Log Placement Guidelines
1. **Entry point**: Log function call with key input values
2. **Decision branches**: Log which path was taken and why
3. **Before risky operations**: Log state before potential failures
4. **Exit point**: Log success with result summary
5. **Catch blocks**: Log error details with context

#### Format Standard
```
[function_name] <action>: <relevant_values>
```

Examples:
```python
logger.info(f"[validate_input] checking messages: count={len(messages)}")
logger.info(f"[process_node] routing to: {next_node}")
logger.info(f"[api_call] response received: status={response.status_code}")
logger.warning(f"[parse_result] unexpected format: {type(data)}")
```

### 6. Verify (2 min)
Run quick validation:
```bash
# Syntax check
uv run python -m py_compile <modified_files>

# Quick test
uv run pytest tests/ -x -q --tb=short
```

### 7. Knowledge Persistence (1 min) - REQUIRED
**After implementing, save learnings to memory for future tasks.**

Evaluate what was learned and save if valuable:

```python
# Only save if NEW knowledge was acquired (not already in memories)
write_memory(
    memory_file_name="<topic>-patterns",  # e.g., "langgraph-routing-patterns"
    content="""# <Topic> Patterns

## Problem Solved
<Brief description of the problem>

## Solution Pattern
<Code pattern or approach that worked>

## Source
- MCP: LangChain docs / AWS docs
- Date: <today>

## Example
```python
<minimal working example>
```
"""
)
```

**When to save:**
- ✅ Found a new pattern not in existing memories
- ✅ Discovered a gotcha or edge case
- ✅ Found better approach than existing memory
- ❌ Skip if knowledge already exists in memories
- ❌ Skip if trivial fix (typo, simple bug)

**Memory naming convention:**
- `<domain>-<topic>-patterns` (e.g., `langgraph-routing-patterns`)
- `<domain>-gotchas` (e.g., `bedrock-gotchas`)

### 8. Report
```
=== Micro-Task Complete ===
Task: {description}
Files: {count} modified
Lines: {count} changed

Knowledge Fetched:
- Memory: langgraph-langchain-langsmith-agents-2025
- MCP LangChain: "conditional edges routing" (3 results)
- MCP AWS: (not applicable)

Knowledge Saved:
- NEW: langgraph-routing-patterns.md (conditional edge pattern)

Changes:
- src/nodes/planner.py: Added null check in validate_input()

Debug Logs Added:
- src/nodes/planner.py:validate_input() - entry/exit + error context

Verification:
[PASS] Syntax valid
[PASS] Tests passing

Next: Run /validate-stack for full validation
```

## Examples

### Example 1: Fix failing tests (LangGraph)
```
/micro-task fix test_planner_handles_empty_messages
```
**Step 2 - Knowledge Fetch (PARALLEL):**
```python
list_memories()
read_memory("langgraph-langchain-langsmith-agents-2025")
SearchDocsByLangChain(query="empty messages handling LangGraph state")
```
**Steps 3-8:**
- Locate tested function, apply pattern from docs
- Fix bug, re-run tests
- Save pattern to `langgraph-message-handling.md` if new

### Example 2: Add validation to LangGraph node
```
/micro-task add input validation to executor node
```
**Step 2 - Knowledge Fetch (PARALLEL):**
```python
list_memories()
read_memory("langgraph-langchain-langsmith-agents-2025")
SearchDocsByLangChain(query="node input validation LangGraph TypedDict")
```
**Steps 3-8:**
- Find executor node function
- Apply validation pattern from MCP docs
- Add test, run tests
- Save to `langgraph-validation-patterns.md` if new pattern found

### Example 3: AWS Bedrock integration
```
/micro-task add Bedrock model invocation to analyzer node
```
**Step 2 - Knowledge Fetch (PARALLEL):**
```python
list_memories()
read_memory("langgraph-langchain-langsmith-agents-2025")
SearchDocsByLangChain(query="ChatBedrock LangChain invoke")
aws___search_documentation(search_phrase="Bedrock invoke model", topics=["reference_documentation"])
```
**Steps 3-8:**
- Find analyzer node
- Apply Bedrock invocation pattern from AWS + LangChain docs
- Test, verify
- Save to `bedrock-integration-patterns.md` if new

## Guardrails

All micro-tasks MUST follow:

### Code Quality

1. **Graph API Only**: No @entrypoint, @task decorators
2. **Langsmith Prompts**: No inline prompt strings
3. **File Size**: Keep files under 500 lines
4. **Coverage**: New code needs tests (aim for 70%+)
5. **Symbolic Editing**: Use Serena tools, not raw file edits

### Infrastructure (AgentCore)

1. **AgentCore Runtime**: All code must be compatible with Bedrock AgentCore Runtime
2. **Memory via MCP Gateway**: Any memory operation MUST be implemented as a tool in MCP Gateway
3. **No Direct DB Access**: Never access databases directly from nodes
4. **Entry Point**: Project must have `main.py` with `create_agent()` function
5. **DATA_API Only**: All Aurora Serverless access MUST use RDS Data API (`boto3.client('rds-data')`)
6. **No Hardcoded Secrets**: ARNs, connection strings stored in SSM/Secrets Manager

## Evaluation Criteria

Before marking a micro-task as complete, verify these criteria:

### Code Quality Evaluation

| Criterion  | Check                                     | Pass/Fail |
| ---------- | ----------------------------------------- | --------- |
| Graph API  | No `@entrypoint`, `@task` decorators      |           |
| Prompts    | Uses `hub.pull()` or `client.pull_prompt()` |           |
| File Size  | Modified files < 500 lines                |           |
| Tests      | New code has tests (70%+ coverage)        |           |

### Infrastructure Evaluation (AgentCore)

| Criterion           | Check                                                  | Pass/Fail |
| ------------------- | ------------------------------------------------------ | --------- |
| Memory Pattern      | Memory ops use MCP Gateway tools                       |           |
| No Direct DB        | No `psycopg2`, `pg8000`, direct connections in nodes   |           |
| Tool Registration   | Memory tools use `@tool` + `gateway.register_tool()`   |           |
| Runtime Compatible  | Code works with `AgentCoreRuntime` wrapper             |           |
| DATA_API Usage      | Aurora access uses `boto3.client('rds-data')`          |           |
| Secrets Management  | ARNs from SSM/Secrets Manager, no hardcoded values     |           |

### Evaluation Report Format

Add to the micro-task report:

```text
=== Infrastructure Evaluation ===
[PASS] Memory via MCP Gateway: Uses store_user_preference tool
[PASS] No Direct DB Access: No database imports in node code
[PASS] Tool Registration: All memory tools registered in gateway
[PASS] Runtime Compatible: Entry point follows AgentCore pattern
[PASS] DATA_API Usage: Uses boto3.client('rds-data') for Aurora
[PASS] Secrets Management: ARNs loaded from SSM Parameter Store

AgentCore Compliance: ✅ APPROVED
```

Or if failing:

```text
=== Infrastructure Evaluation ===
[FAIL] Memory via MCP Gateway: Direct psycopg2 connection in planner_node
[PASS] No Direct DB Access: -
[FAIL] Tool Registration: Memory function not decorated with @tool
[FAIL] DATA_API Usage: Uses psycopg2.connect() instead of rds-data
[FAIL] Secrets Management: Hardcoded database password in code

AgentCore Compliance: ❌ REQUIRES FIXES
Fixes Required:
1. Convert memory access to MCP Gateway tool pattern
2. Replace psycopg2 with boto3.client('rds-data')
3. Move credentials to SSM/Secrets Manager
```

## When to Escalate

Convert to full task if:
- Requires >3 files
- Needs new dependency
- Architectural change needed
- Cross-cutting concern

Say: "This task is larger than micro-scope. Suggest running /discovery first."
