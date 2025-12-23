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
  # Serena memories
  - mcp__plugin_systemic-agent-orchestrator_serena__list_memories
  - mcp__plugin_systemic-agent-orchestrator_serena__read_memory
  # Knowledge MCPs
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

### 2. Knowledge Fetch (2 min) - PARALLEL
**ALWAYS run before coding.** Search in parallel for relevant knowledge:

#### 2.1 Serena Memories
```
list_memories -> read_memory (relevant ones)
```
Look for memories matching task keywords (e.g., "langgraph", "agents", "hooks").

#### 2.2 MCP Documentation Search
Based on task keywords, query relevant MCPs in parallel:

| Keywords | MCP to Search |
|----------|---------------|
| LangGraph, node, edge, state, agent, LangChain, LCEL, prompt | `SearchDocsByLangChain` |
| AWS, Lambda, S3, DynamoDB, Bedrock, CloudFormation | `aws___search_documentation` |

**Search query format**: Extract the core problem/pattern from task description.
```
Example task: "fix conditional edge routing in planner"
Search query: "conditional edges routing LangGraph"
```

#### 2.3 Project Skills
Check if task relates to existing skills:
- `langgraph-graph-api/` - StateGraph patterns
- `langsmith-prompts/` - Prompt management
- `models-yaml-config/` - Model configuration

**Output**: Use fetched knowledge silently as implementation context.

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

### 6. Verify (2 min)
Run quick validation:
```bash
# Syntax check
uv run python -m py_compile <modified_files>

# Quick test
uv run pytest tests/ -x -q --tb=short
```

### 7. Report
```
=== Micro-Task Complete ===
Task: {description}
Files: {count} modified
Lines: {count} changed

Knowledge Used:
- Memory: langgraph-langchain-langsmith-agents-2025
- MCP: LangChain docs (conditional routing pattern)

Changes:
- src/nodes/planner.py: Added null check in validate_input()

Verification:
[PASS] Syntax valid
[PASS] Tests passing

Next: Run /validate-stack for full validation
```

## Examples

### Example 1: Fix failing tests
```
/micro-task fix test_planner_handles_empty_messages
```
1. **Knowledge Fetch**: Search LangChain docs for "empty messages handling"
2. Read test file, understand failure
3. Locate tested function
4. Apply pattern from docs, fix bug
5. Re-run test to confirm

### Example 2: Add validation to LangGraph node
```
/micro-task add input validation to executor node
```
1. **Knowledge Fetch** (parallel):
   - Memory: `langgraph-langchain-langsmith-agents-2025`
   - MCP: `SearchDocsByLangChain("node input validation LangGraph")`
2. Find executor node function
3. Apply validation pattern from fetched knowledge
4. Add test for validation
5. Run tests

### Example 3: Refactor function
```
/micro-task extract API call logic from planner to separate function
```
1. **Knowledge Fetch**: Check skill `langgraph-graph-api/` for patterns
2. Identify code to extract
3. Create new function following patterns
4. Update original to call new function
5. Update tests if needed

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
