---
description: Validate entire agent project against all guardrail rules
argument-hint: "[path]"
allowed-tools:
  - mcp__plugin_systemic-agent-orchestrator_serena__list_dir
  - mcp__plugin_systemic-agent-orchestrator_serena__search_for_pattern
  - mcp__plugin_systemic-agent-orchestrator_serena__find_symbol
  - mcp__plugin_systemic-agent-orchestrator_serena__get_symbols_overview
  - Bash
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

### 10. Python Test Coverage (CRITICAL)
Run: `uv run pytest --cov=src --cov-fail-under=70 tests/ -q`
- FAIL if coverage < 70%
- Report coverage percentage per module
- List uncovered lines if below threshold

### 11. Terraform Validation (if infra/ exists)
Run these validations in sequence:

#### 11a. Terraform Format
```bash
terraform fmt -check -recursive infra/
```
FAIL if files not formatted.

#### 11b. Terraform Validate
```bash
cd infra/ && terraform init -backend=false && terraform validate
```
FAIL if syntax errors.

#### 11c. TFLint
```bash
tflint --recursive infra/
```
FAIL if linting errors. Check for:
- Deprecated syntax
- Invalid resource references
- Missing required attributes

#### 11d. TFSec Security Scan
```bash
tfsec infra/ --minimum-severity HIGH
```
FAIL if HIGH or CRITICAL vulnerabilities. Report:
- Security issue description
- Affected resource
- Remediation steps

#### 11e. Terraform Test (if tests exist)
```bash
cd infra/ && terraform test
```
Run integration tests if `*.tftest.hcl` files exist.

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

PYTHON TESTING:
[PASS] Coverage: 78% (minimum: 70%)
  - src/nodes/planner.py: 85%
  - src/nodes/executor.py: 72%
  - src/state.py: 100%

TERRAFORM VALIDATION:
[PASS] Format: All files formatted
[PASS] Validate: Syntax valid
[PASS] TFLint: No linting errors
[PASS] TFSec: No HIGH/CRITICAL vulnerabilities
[PASS] Terraform Test: 3/3 tests passed

=== Summary ===
Passed: 14/15
Warnings: 1
Failed: 0

Status: READY FOR DEPLOYMENT
```

## Exit Codes

- All passed: Display success message
- Warnings only: Display warnings with suggestions
- Any failures: Display failures with fix instructions, DO NOT PROCEED

## Failure Actions

When validation fails:
1. **Coverage < 70%**: List uncovered functions, suggest tests to write
2. **TFSec HIGH/CRITICAL**: Show exact resource and remediation
3. **TFLint errors**: Show exact line and fix
4. **Functional API found**: Show file:line and correct pattern

## Next Steps

Based on results, suggest:
- For failures: Specific fix instructions (MUST FIX BEFORE PROCEEDING)
- For warnings: Improvement suggestions
- For success: Deployment readiness confirmation
