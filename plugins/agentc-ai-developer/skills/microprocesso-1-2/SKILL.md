---
name: microprocesso-1-2
description: Complete knowledge about Microprocesso 1.2 (Setup Local + Observability) - Python virtual environment setup, dependency installation, .env configuration, LangSmith integration, validation, and troubleshooting. Use when user needs detailed guidance on any of the 8 setup activities or encounters errors during environment setup.
allowed-tools: Read, Bash, Write
---

name: microprocesso-1-2
description: Complete knowledge about Microprocesso 1.2 (Setup Local + Observability) - Python virtual environment setup, dependency installation, .env configuration, LangSmith integration, validation, and troubleshooting. Use when user needs detailed guidance on any of the 8 setup activities or encounters errors during environment setup.
allowed-tools: Read, Bash, Write

# Microprocesso 1.2: Setup Local + Observability

Complete knowledge base for implementing Microprocesso 1.2 - the environment setup phase that follows Brief Minimo planning (`/brief`).

## Purpose

Microprocesso 1.2 guides you through setting up a reproducible, fully observable local development environment for your AI agent project.

**Key outcomes**:

- ✅ Python virtual environment with isolation
- ✅ Dependencies: LangChain, Anthropic, LangSmith, python-dotenv
- ✅ Environment configuration (.env + .gitignore)
- ✅ LangSmith integration for observability
- ✅ Complete validation and testing

**Total time**: ~1.5 hours | **Result**: Production-ready local environment with full observability

## Prerequisites

Before starting Microprocesso 1.2:

✅ Completed `/brief` command (Microprocesso 1.1)
✅ README.md with Brief Minimo specification
✅ Project repository created
✅ Python 3.10+ installed
✅ LangSmith account (free: smith.langchain.com)
✅ 1.5 hours available

## The 8 Setup Activities - Quick Overview

1. **Create Python venv** - Isolated Python environment
1. **Activate venv** - Load the isolated environment
1. **Install dependencies** - Core packages: langchain, anthropic, langsmith, python-dotenv
1. **Create .env** - Store API keys (LANGSMITH_API_KEY, ANTHROPIC_API_KEY)
1. **Create .env.example** - Template for team (no secrets)
1. **Create requirements.txt** - Lock dependency versions
1. **Create .gitignore** - Protect secrets from git commits
1. **Test LangSmith** - Verify observability works

For detailed step-by-step instructions on each activity, see: **REFERENCE.md**

## Operating Modes

### Guiado (Guided - Full Manual Control)

**Best for**: Learning, understanding each step

- Command explains what to do
- You execute commands manually
- Command validates results
- You maintain full control

### Automático (Automatic - Hands-Off)

**Best for**: Speed, reproducibility

- Command describes what will happen
- Executes bash commands automatically
- You monitor progress
- Fastest approach (~20 minutes)

### Misto (Mixed - Choose Per Activity)

**Best for**: Flexibility

- For each activity: Choose Manual or Automatic
- You control learning/speed trade-off
- Balanced approach (~1.5 hours)

## Key Concepts

**Virtual Environment (venv)**

- Isolated Python environment specific to your project
- Each project has its own packages and versions
- Prevents conflicts between projects
- Always activate before working: `source venv/bin/activate`

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
- Activated: `@trace` decorator on functions

**Reproducibility**

- requirements.txt locks exact dependency versions
- Team members use `pip install -r requirements.txt` to recreate environment
- Ensures consistent behavior across machines

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

# Activate environment
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Lock current dependencies
pip freeze > requirements.txt

# Test setup
python validate_setup.py

# Check API keys loaded
python -c "import os; print(os.getenv('LANGSMITH_API_KEY'))"

# Run LangSmith tests
python test_langsmith.py

```text


## Next Steps After Setup

After completing all 8 activities:

1. **Verify everything works** - Run `python validate_setup.py`
2. **Check LangSmith dashboard** - Visit smith.langchain.com/projects
3. **Start coding** - Begin Microprocesso 1.3 (coming soon)
4. **Share with team** - They use `requirements.txt` to setup
5. **Monitor observability** - View all traces in LangSmith


## File Structure Created

```text

project-root/
├── venv/                    # Virtual environment (NOT committed)
├── .env                     # Secrets (NOT committed)
├── .env.example            # Template (committed)
├── .gitignore              # Prevents committing .env
├── requirements.txt        # Locked dependencies
├── test_langsmith.py       # Integration test
├── validate_setup.py       # Setup validation
└── README.md               # Your Brief Minimo spec

```text


## Comprehensive References

For detailed guidance on specific topics:

- **Step-by-step instructions**: See **REFERENCE.md** (8 activities with templates)
- **Troubleshooting guide**: See **TROUBLESHOOTING.md** (common issues and solutions)
- **Validation scripts**: See **VALIDATION.md** (setup testing and verification)


This skill provides guidance for `/setup-local-observability` command and help when users encounter setup issues. See plugin README.md for complete overview.
````
