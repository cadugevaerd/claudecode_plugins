---
description: Automated setup for LangGraph projects with LangSmith observability. Uses langgraph new to initialize project, configure environment, and validate setup. Continues from /brief. ~15 minutes total setup time.
allowed-tools: Read, Bash, Write
---

# Microprocesso 1.2: Setup Local + Observability

Automated setup for reproducible LangGraph project with LangSmith observability.

## Prerequisites

Verify before starting:

- Completed `/brief` (Microprocesso 1.1)
- README.md or BRIEF.md with Brief Minimo specification exists
- Python 3.8+ installed
- LangSmith account created (smith.langchain.com)
- LLM provider API key created (your chosen provider)
- `langgraph-cli` installed (`pip install langgraph`)
- If prerequisites cannot be verified, ask user for information

## Execution Flow

The setup follows 4 sequential activities:

1. **Verify Prerequisites** → Check Brief Minimo, Python, langgraph-cli, API keys
1. **Initialize Project** → Run `langgraph new PROJECT_NAME` (only if project doesn't exist)
1. **Configure Secrets** → Add LANGSMITH_API_KEY and LLM_API_KEY to .env
1. **Validate Setup** → Test LangSmith connection and generate first trace

What `langgraph new` creates automatically:

- `langgraph.json` (project configuration)
- `.env.example` (API key template)
- `.gitignore` (protects .env and other secrets)
- `pyproject.toml` and/or `requirements.txt` (locked dependencies)
- Python package structure (ready to develop)
- Virtual environment (isolated dependencies)

## Project Detection

Before executing `langgraph new`, verify if project already exists:

**Project exists if any of these are present:**

- `langgraph.json` file in current directory
- `pyproject.toml` with langgraph configuration
- `.venv` or `venv` directory (virtual environment)
- `src/` or `graph/` directories with Python code

**Execution path if project exists:**

Skip Activity 2 (Initialize Project), go directly to Activity 3 (Configure .env)

**Execution path if project doesn't exist:**

Execute Activity 2 to scaffold new project structure

## Validation Criteria

After completion, verify:

- `langgraph.json` exists and is valid JSON
- `.env` file exists with LLM provider API key
- `.env.example` exists (no secrets)
- `.gitignore` protects `.env`
- Virtual environment activated and ready
- LangSmith connection working (traces visible at smith.langchain.com)

## Next Steps

After successful setup:

- Run `/update-claude-md` to integrate guidance
- Proceed to `/spike-agentic` (Microprocesso 1.3)
- Share requirements.txt with team for reproducibility

## Detailed Knowledge

For step-by-step instructions, templates, and troubleshooting, see skill `microprocesso-1-2`.
