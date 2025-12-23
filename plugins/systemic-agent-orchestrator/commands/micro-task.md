---
description: Execute a focused micro-task following project guardrails (fix tests, add validation, refactor function)
argument-hint: "<task-description>"
allowed-tools:
  - mcp__plugin_systemic-agent-orchestrator_serena__list_dir
  - mcp__plugin_systemic-agent-orchestrator_serena__search_for_pattern
  - mcp__plugin_systemic-agent-orchestrator_serena__find_symbol
  - mcp__plugin_systemic-agent-orchestrator_serena__get_symbols_overview
  - mcp__plugin_systemic-agent-orchestrator_serena__replace_symbol_body
  - mcp__plugin_systemic-agent-orchestrator_serena__insert_after_symbol
  - mcp__plugin_systemic-agent-orchestrator_serena__insert_before_symbol
  - Bash
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

### 1. Understand Task (2 min)
- Parse task description
- Identify affected files/symbols
- Verify scope is micro (≤3 files, ≤100 lines)

### 2. Locate Code (2 min)
Use Serena tools to find relevant code:
```
get_symbols_overview -> find_symbol -> search_for_pattern
```

### 3. Plan Changes (1 min)
List exact changes:
```
File: src/nodes/planner.py
Symbol: validate_input
Action: Add null check for 'messages' field
Lines: ~5 new lines
```

### 4. Implement (5 min)
Use Serena symbolic editing:
- `replace_symbol_body` for function updates
- `insert_after_symbol` for new code
- `insert_before_symbol` for imports

### 5. Verify (2 min)
Run quick validation:
```bash
# Syntax check
uv run python -m py_compile <modified_files>

# Quick test
uv run pytest tests/ -x -q --tb=short
```

### 6. Report
```
=== Micro-Task Complete ===
Task: {description}
Files: {count} modified
Lines: {count} changed

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
1. Read test file, understand failure
2. Locate tested function
3. Fix bug in function
4. Re-run test to confirm

### Example 2: Add validation
```
/micro-task add input validation to executor node
```
1. Find executor node function
2. Add validation at function start
3. Add test for validation
4. Run tests

### Example 3: Refactor function
```
/micro-task extract API call logic from planner to separate function
```
1. Identify code to extract
2. Create new function
3. Update original to call new function
4. Update tests if needed

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
