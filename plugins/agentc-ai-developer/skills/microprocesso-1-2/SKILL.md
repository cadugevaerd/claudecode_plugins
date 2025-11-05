---
name: microprocesso-1-2
description: Complete knowledge about Microprocesso 1.2 (Setup Local + Observability) - LangGraph project initialization, .env configuration, LangSmith integration, validation, and troubleshooting. Use when user needs detailed guidance on setup activities or encounters errors during environment setup.
allowed-tools: Read, Bash, Write
---

name: microprocesso-1-2
description: Complete knowledge about Microprocesso 1.2 (Setup Local + Observability) - LangGraph project initialization, .env configuration, LangSmith integration, validation, and troubleshooting. Use when user needs detailed guidance on setup activities or encounters errors during environment setup.
allowed-tools: Read, Bash, Write

# Microprocesso 1.2: Setup Local + Observability

Complete knowledge base for implementing Microprocesso 1.2 - the environment setup phase that follows Brief Minimo planning (`/brief`).

## Purpose

Microprocesso 1.2 guides you through setting up a reproducible, fully observable LangGraph project with LangSmith integration.

**Key outcomes**:

- ✅ LangGraph project scaffolded with `langgraph new`
- ✅ Environment configuration (.env + .gitignore created automatically)
- ✅ LLM provider API key configured (your chosen provider)
- ✅ LangSmith integration for observability
- ✅ Project ready for agent development

**Total time**: ~15 minutes | **Result**: Production-ready LangGraph project with full observability

## Prerequisites

Before starting Microprocesso 1.2:

✅ Completed `/brief` command (Microprocesso 1.1)
✅ README.md with Brief Minimo specification
✅ Python 3.8+ installed
✅ LangSmith account (free: smith.langchain.com)
✅ LLM provider API key (your chosen provider)
✅ `langgraph-cli` installed (`pip install langgraph`)

## The 4 Setup Activities - Quick Overview

1. **Verify Prerequisites** - Check all requirements before starting
1. **Initialize Project** - Run `langgraph new PROJECT_NAME` (skip if project exists)
1. **Configure Secrets** - Add LANGSMITH_API_KEY and LLM_API_KEY to .env
1. **Validate Setup** - Test LangSmith connection and verify observability works

For detailed step-by-step instructions on each activity, see: **REFERENCE.md**

## Key Concepts

**LangGraph Project Structure**

- `langgraph.json` defines your project configuration
- Auto-generated virtual environment with dependencies isolated
- Supports multiple language targets (Python, JavaScript)
- Ready for local development and LangGraph cloud deployment

**Environment Variables (.env)**

- File containing secrets: API keys, configuration
- NEVER committed to git (use .gitignore)
- Loaded at runtime: `from dotenv import load_dotenv; load_dotenv()`
- Use .env.example as template documentation

**LangSmith Integration**

- Observability platform for tracing agent execution
- All traces automatically sent and visible in dashboard
- Free tier generous and production-ready
- Requires: API key from smith.langchain.com
- Activated: `@traceable` decorator on functions or automatic with LangGraph

**Flexibility with LLM Providers**

- Choose any LLM provider: Anthropic Claude, OpenAI GPT, Google Gemini, etc.
- Configure via environment variable (LLM_API_KEY or provider-specific)
- Switch providers without changing codebase structure

## Common Issues and Quick Fixes

**"ModuleNotFoundError: No module named 'langchain'"**

- Verify venv is activated: `which python` should show venv path
- Check packages installed: `pip list | grep langchain`
- Reinstall if needed: `pip install langchain`

**".env not found or variables not loading"**

- Check .env exists in project root: `ls -la .env`
- Check file has keys: `grep LANGSMITH .env`
- Verify .env is loaded: `from dotenv import load_dotenv; load_dotenv()`

**"LangSmith traces not appearing"**

- Check API key correct: `echo $LANGSMITH_API_KEY`
- Verify .env has: `LANGSMITH_API_KEY=xxx`
- Check decorator: `@trace` (case sensitive)
- Wait 30 seconds and refresh dashboard

**"pip install hangs or timeout"**

- Check internet connection
- Try: `pip install --upgrade pip`
- Clear cache: `pip cache purge`
- Install one package at a time to isolate

For comprehensive troubleshooting: See **TROUBLESHOOTING.md**

## Quick Commands Reference

````bash

# Initialize a new LangGraph project
langgraph new my-agent-project

# Check if langgraph-cli is installed
langgraph version

# Run local development server
langgraph dev

# Activate virtual environment
source .venv/bin/activate        # Linux/macOS (if using .venv)
.venv\Scripts\activate           # Windows

# Install dependencies from lock file
pip install -r requirements.txt

# Check API keys loaded
python -c "import os; print(os.getenv('LANGSMITH_API_KEY'))"

# Validate LangSmith connection
langgraph test

```text


## Next Steps After Setup

After completing all 4 activities:

1. **Verify LangSmith connection** - Check smith.langchain.com/projects
2. **Review langgraph.json** - Understand your project configuration
3. **Start developing** - Begin Microprocesso 1.3 (Spike Agentic)
4. **Monitor observability** - View all traces in LangSmith dashboard
5. **Test locally** - Run `langgraph dev` for local testing


## File Structure Created by `langgraph new`

```text

project-root/
├── langgraph.json              # Project configuration
├── .env                        # Your secrets (NOT committed)
├── .env.example                # Template (committed)
├── .gitignore                  # Protects .env, __pycache__, etc
├── pyproject.toml             # Python package configuration
├── requirements.txt           # Locked dependencies (if using pip)
├── src/                       # Your source code
│   └── agent/
│       └── graph.py           # Your LangGraph implementation
└── README.md                  # Your Brief Minimo spec

```text


## Comprehensive References

For detailed guidance on specific topics:

- **Step-by-step instructions**: See **REFERENCE.md** (4 activities with templates)
- **Troubleshooting guide**: See **TROUBLESHOOTING.md** (common issues and solutions)
- **LangGraph documentation**: https://langchain-ai.github.io/langgraph/


This skill provides guidance for `/setup-local-observability` command and help when users encounter setup issues. See plugin README.md for complete overview.
````
