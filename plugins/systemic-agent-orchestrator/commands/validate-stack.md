---
description: Validate entire agent project against all guardrail rules
argument-hint: "[path]"
allowed-tools:
  - mcp__plugin_systemic-agent-orchestrator_serena__list_dir
  - mcp__plugin_systemic-agent-orchestrator_serena__search_for_pattern
  - mcp__plugin_systemic-agent-orchestrator_serena__find_symbol
  - mcp__plugin_systemic-agent-orchestrator_serena__get_symbols_overview
  - Bash
  - Skill
---

# Validate Agent Stack

Run comprehensive validation against all project guardrails with automatic fix capability.

## Arguments

- `path`: Optional. Path to agent project (default: current directory)

## Instructions

Perform these validations in order, collecting all failures:

### 0. CLAUDE.md Line Count (CRITICAL)
Check CLAUDE.md file size:
- Count total lines in CLAUDE.md
- **FAIL if > 200 lines**
- Warn if > 180 lines (approaching limit)

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

## Output Format - Initial Validation

```
=== Stack Validation Report ===
Project: {project_path}
Timestamp: {timestamp}

CRITICAL CHECKS:
[PASS] CLAUDE.md: 145 lines (limit: 200)
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
Passed: 15/16
Warnings: 1
Failed: 0

Status: READY FOR DEPLOYMENT
```

## Auto-Fix Flow

When failures are detected, automatically trigger fixes using `/systemic-agent-orchestrator:micro-task`:

### Step 1: Collect All Failures
After running all validations, compile a list of failures with:
- Check name
- File path (if applicable)
- Line number (if applicable)
- Specific issue description
- Expected fix

### Step 2: Execute Auto-Fix for Each Failure

For each failure, invoke the micro-task skill:

```
Skill: systemic-agent-orchestrator:micro-task
Args: Fix {check_name} issue in {file_path}: {issue_description}
```

**Auto-fix mapping by check type:**

| Check | Micro-task Description |
|-------|----------------------|
| CLAUDE.md > 200 lines | Refactor CLAUDE.md to be under 200 lines, consolidating redundant sections |
| Functional API | Replace @entrypoint/@task with StateGraph pattern in {file} |
| Local Prompts | Move inline prompt to Langsmith and use client.pull_prompt in {file} |
| models.yaml missing | Create models.yaml entry for node {node_name} |
| File > 500 lines | Split {file} into smaller modules under 500 lines each |
| Ruff errors | Fix ruff linting errors in {file}: {errors} |
| Missing imports | Add required imports to {file}: {imports} |
| State definition | Fix AgentState in src/state.py: {issue} |
| Coverage < 70% | Add tests for uncovered code in {module} |
| Terraform format | Run terraform fmt on {file} |
| TFLint errors | Fix TFLint issue in {file}: {error} |
| TFSec vulnerabilities | Fix security issue in {file}: {vulnerability} |

### Step 3: Re-validate After Fixes

After all micro-tasks complete, run the full validation again:

```
=== Re-validation After Auto-Fix ===

Fixes Applied: 3
1. [FIXED] Functional API in src/nodes/planner.py
2. [FIXED] Ruff errors in src/utils/helpers.py
3. [FIXED] Missing tests for src/nodes/executor.py

Re-running validation...

[Results of second validation pass]

=== Final Status ===
Original Failures: 3
Fixed: 3
Remaining: 0

Status: READY FOR DEPLOYMENT
```

### Step 4: Handle Persistent Failures

If any issues remain after auto-fix:

```
=== Persistent Issues (Manual Intervention Required) ===

1. [FAIL] TFSec: S3 bucket lacks encryption
   File: infra/storage.tf:45
   Reason: Auto-fix could not determine encryption key
   Action: Manually add aws_kms_key resource and reference in bucket

2. [FAIL] Coverage: src/nodes/complex.py at 45%
   Reason: Complex branching logic requires manual test design
   Action: Write tests for handle_edge_cases() and process_special_input()

Please fix these manually and run /systemic-agent-orchestrator:validate-stack again.
```

## Exit Codes

- All passed (first run): Display success message
- All passed (after fix): Display fixes applied and success
- Warnings only: Display warnings with suggestions
- Persistent failures: Display what could not be auto-fixed with manual instructions

## Important Notes

1. **Automatic execution**: Fixes are applied without user confirmation
2. **Idempotency**: Running validation multiple times is safe
3. **Atomic fixes**: Each micro-task fixes one specific issue
4. **Re-validation**: Always re-run full validation after fixes
5. **Fail-safe**: If a fix introduces new issues, they will be caught in re-validation
