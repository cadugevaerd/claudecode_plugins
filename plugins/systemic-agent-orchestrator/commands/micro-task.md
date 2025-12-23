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

## Workflow

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

1. **Graph API Only**: No @entrypoint, @task decorators
2. **Langsmith Prompts**: No inline prompt strings
3. **File Size**: Keep files under 500 lines
4. **Coverage**: New code needs tests (aim for 70%+)
5. **Symbolic Editing**: Use Serena tools, not raw file edits

## When to Escalate

Convert to full task if:
- Requires >3 files
- Needs new dependency
- Architectural change needed
- Cross-cutting concern

Say: "This task is larger than micro-scope. Suggest running /discovery first."
