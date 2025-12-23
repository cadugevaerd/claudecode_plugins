---
description: Initial setup - install dependencies, create project structure, initialize CLAUDE.md
argument-hint: "[project-path]"
allowed-tools:
  - Bash
  - Write
  - Read
  - Glob
  - mcp__plugin_systemic-agent-orchestrator_serena__list_dir
  - mcp__plugin_systemic-agent-orchestrator_serena__check_onboarding_performed
  - mcp__plugin_systemic-agent-orchestrator_serena__onboarding
  - mcp__plugin_systemic-agent-orchestrator_serena__write_memory
---

# Setup Systemic Agent Orchestrator

Automated setup that installs all dependencies and creates project structure for AI agent development.

## Arguments

- `project-path`: Optional. Path to project (default: current directory)

## Instructions

Execute all steps automatically. Skip steps where dependencies are already installed.

### Step 1: Check and Install uv

```bash
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "[INSTALLED] uv"
else
    echo "[OK] uv already installed: $(uv --version)"
fi
```

### Step 2: Check Python Version

```bash
python3 --version
```
Require Python 3.10+. If not available, display error and stop.

### Step 3: Initialize Python Project (if needed)

Check if `pyproject.toml` exists:
```bash
if [ ! -f pyproject.toml ]; then
    uv init --no-readme
    echo "[CREATED] pyproject.toml"
else
    echo "[OK] pyproject.toml exists"
fi
```

### Step 4: Install Dev Dependencies

```bash
uv add --dev ruff pytest pytest-cov pytest-asyncio
```
Skip packages already in pyproject.toml.

### Step 5: Create Project Structure

Create standard agent project directories if they don't exist:

```
project/
├── src/
│   ├── __init__.py
│   ├── nodes/
│   │   └── __init__.py
│   ├── state.py
│   └── graph.py
├── tests/
│   ├── __init__.py
│   └── test_graph.py
├── config/
│   └── models.yaml
├── CLAUDE.md
└── pyproject.toml
```

For each directory/file:
- Check if exists
- Create only if missing
- Report status

### Step 6: Initialize CLAUDE.md

If CLAUDE.md doesn't exist, create with template:

```markdown
# CLAUDE.md - [Project Name]

## Project Overview
AI Agent project using LangGraph Graph API.

## Architecture
- **Graph API**: StateGraph pattern (NO Functional API)
- **State**: TypedDict with Annotated fields
- **Prompts**: Langsmith hub (no local prompts)

## Development Rules

### Code Style
- Max 200 lines per file (split if larger)
- Max 500 lines per module
- Type hints required
- English code, Portuguese responses

### Testing
- Min 70% coverage
- Run: `uv run pytest --cov=src tests/`

### Commits
- Use `/git-commit-helper:quick-commit`

## Commands
- `/systemic-agent-orchestrator:validate-stack` - Validate project
- `/systemic-agent-orchestrator:micro-task` - Fix specific issues
- `/systemic-agent-orchestrator:add-node` - Add new node

## Key Files
- `src/state.py` - AgentState definition
- `src/graph.py` - Graph builder
- `src/nodes/` - Node implementations
- `config/models.yaml` - Model configurations
```

### Step 7: Initialize config/models.yaml

If config/models.yaml doesn't exist, create with template:

```yaml
# Model configurations for each node
# Format: provider:model_name
# Valid providers: anthropic, anthropic_bedrock, openai, google_genai, xai

nodes:
  # Example node configuration
  # planner:
  #   model: anthropic:claude-sonnet-4-20250514
  #   temperature: 0.7
  #   description: Plans the execution strategy
```

### Step 8: Initialize src/state.py

If src/state.py doesn't exist, create with template:

```python
"""Agent state definition."""

from typing import Annotated, TypedDict

from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State for the agent graph."""

    messages: Annotated[list[BaseMessage], add_messages]
    # Add more fields as needed
```

### Step 9: Run Serena Onboarding

Check if Serena onboarding was performed:
- Call `mcp__plugin_systemic-agent-orchestrator_serena__check_onboarding_performed`
- If not performed, call `mcp__plugin_systemic-agent-orchestrator_serena__onboarding`
- Follow onboarding instructions to create project context

### Step 10: Verify Setup

Run quick validation:
```bash
uv run python -c "import sys; print(f'Python {sys.version}')"
uv run ruff --version
```

## Output Format

```
=== Systemic Agent Orchestrator Setup ===
Project: /path/to/project

DEPENDENCIES:
[OK] uv: 0.5.11
[OK] Python: 3.12.0
[INSTALLED] ruff, pytest, pytest-cov

PROJECT STRUCTURE:
[OK] pyproject.toml
[CREATED] src/
[CREATED] src/nodes/
[CREATED] tests/
[CREATED] config/

FILES:
[CREATED] CLAUDE.md (57 lines)
[CREATED] config/models.yaml
[CREATED] src/state.py
[OK] src/__init__.py

SERENA:
[OK] Onboarding completed
[OK] Project context initialized

=== Setup Complete ===

Next steps:
1. Review CLAUDE.md and customize for your project
2. Run /systemic-agent-orchestrator:init-agent to start agent development
3. Run /systemic-agent-orchestrator:validate-stack to verify setup
```

## Error Handling

If any step fails:
1. Report the specific error
2. Provide manual fix instructions
3. Continue with remaining steps if possible
4. Show summary of what succeeded/failed

## Notes

- This command is idempotent - safe to run multiple times
- Existing files are never overwritten
- Run at project start or after cloning
