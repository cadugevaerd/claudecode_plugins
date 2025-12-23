---
description: Validate entire agent project against all guardrail rules
argument-hint: "[path]"
allowed-tools:
  - mcp__plugin_serena_serena__read_file
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__search_for_pattern
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__execute_shell_command
---

# Validate Agent Stack

Run comprehensive validation against all project guardrails.

## Arguments

- `path`: Optional. Path to agent project (default: current directory)

## Instructions

Perform these validations in order:

### 1. Functional API Check (CRITICAL)
Search for prohibited patterns in all .py files:
- `@entrypoint` decorator
- `@task` decorator
- `from langgraph.func import`
- `langgraph.func.entrypoint`
- `langgraph.func.task`

### 2. Local Prompt Check (CRITICAL)
Search for inline prompts in all .py files:
- `ChatPromptTemplate.from_template("...` with long strings
- `SYSTEM_PROMPT =` or `USER_PROMPT =` constants
- Triple-quoted strings with "You are" or "Instructions"
- Files should have `hub.pull` or `client.pull_prompt` instead

### 3. models.yaml Validation
Verify config/models.yaml:
- File exists
- Valid YAML syntax
- Has `nodes` top-level key
- Each node has `model` and `temperature`
- Model format is `provider:model_name`
- Valid providers: anthropic, anthropic_bedrock, openai, google_genai, xai
- Temperature is 0.0-1.0
- Comments present for each node

### 4. Node-Config Sync
For each node function in src/nodes/:
- Verify corresponding entry exists in models.yaml
- Report any nodes missing configuration

### 5. File Size Check
For all .py files:
- Count lines
- Flag any file over 500 lines
- Warn for files over 400 lines

### 6. Ruff Linting
Run: `uv run ruff check src/ tests/`
Report any issues found.

### 7. Import Validation
Check graph files for required imports:
- `from langgraph.graph import StateGraph`
- `from typing import TypedDict, Annotated`
- `from operator import add`

### 8. Langsmith Integration
Verify prompts are pulled from Langsmith:
- `client.pull_prompt(` present in LLM nodes
- OR `hub.pull(` present
- No hardcoded prompt strings

### 9. State Definition
Verify src/state.py:
- Has `AgentState` TypedDict
- Uses `Annotated` for list fields
- Has `messages` field

### 10. Test Coverage (if tests exist)
Run: `uv run pytest --cov=src tests/ -q`
Report coverage percentage.

## Output Format

```
=== Stack Validation Report ===
Project: {project_path}
Timestamp: {timestamp}

CRITICAL CHECKS:
[PASS] Functional API: No prohibited patterns found
[PASS] Local Prompts: All prompts from Langsmith

CONFIGURATION:
[PASS] models.yaml: Valid configuration (4 nodes)
[PASS] Node-Config Sync: All nodes have config
[WARN] File Size: src/nodes/complex.py (487 lines - close to limit)

CODE QUALITY:
[PASS] Ruff Linting: No issues
[PASS] Imports: Required patterns present
[PASS] State: AgentState properly defined

INTEGRATION:
[PASS] Langsmith: Prompt integration verified

TESTING:
[INFO] Coverage: 78% (target: 70%)

=== Summary ===
Passed: 9/10
Warnings: 1
Failed: 0

Status: READY FOR DEPLOYMENT
```

## Exit Codes

- All passed: Display success message
- Warnings only: Display warnings with suggestions
- Any failures: Display failures with fix instructions

## Next Steps

Based on results, suggest:
- For failures: Specific fix instructions
- For warnings: Improvement suggestions
- For success: Deployment readiness confirmation
