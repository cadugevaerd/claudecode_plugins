# Microprocesso 1.2: Activity Reference

Complete step-by-step instructions for all 4 setup activities.

## Activity 1: Verify Prerequisites

**Purpose**: Ensure all requirements are met before starting setup

**Verification Checklist**:

```bash
# Check Brief Minimo exists
ls -la README.md || ls -la BRIEF.md

# Check Python version
python --version
# Should be 3.8 or higher

# Check langgraph-cli is installed
langgraph version

# Check LangSmith account
echo "Visit smith.langchain.com to verify your account"

# Check LLM API key exists
echo "Verify your LLM provider API key (OpenAI, Anthropic, Google, etc)"
```

**Success Criteria**:

- ✅ README.md or BRIEF.md exists with your project specification
- ✅ Python 3.8+ installed
- ✅ `langgraph --version` outputs a version number
- ✅ LangSmith account created and verified
- ✅ LLM provider API key ready to use

**Troubleshooting**:

- If Python not found: Install from python.org
- If langgraph-cli not found: Run `pip install langgraph`
- If no LangSmith account: Visit smith.langchain.com and sign up (free)

______________________________________________________________________

## Activity 2: Initialize Project

**Purpose**: Create LangGraph project structure with `langgraph new` (uv handles virtual environment automatically)

**Prerequisites Check**:

Before running, verify:

```bash
# Check if project already exists
ls -la langgraph.json 2>/dev/null && echo "Project exists - SKIP THIS ACTIVITY"
ls -la src/ 2>/dev/null && echo "Project exists - SKIP THIS ACTIVITY"
```

**If project exists**: Skip to Activity 3 (Configure Secrets)

**If project doesn't exist**: Execute initialization

**Command**:

```bash
# Option 1: Interactive mode (recommended)
langgraph new my-agent-project

# Option 2: With specific template
langgraph new my-agent-project --template new-langgraph-project-python

# Option 3: In current directory
cd my-agent-project
langgraph new .
```

**What `langgraph new` creates**:

- `langgraph.json` - Project configuration file
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules (protects .env, __pycache__)
- `pyproject.toml` - Python package configuration
- `uv.lock` - Dependency lock file (managed by uv automatically)
- `src/agent/graph.py` - Your LangGraph implementation skeleton

**Verification**:

```bash
# Check project created
ls -la langgraph.json

# Check .env.example exists
ls -la .env.example

# Check .gitignore exists
ls -la .gitignore

# Check uv.lock exists
ls -la uv.lock
```

**Success Criteria**:

- ✅ `langgraph.json` exists and is valid JSON
- ✅ `.env.example` exists (no secrets)
- ✅ `.gitignore` protects sensitive files
- ✅ `uv.lock` exists (uv manages dependencies automatically)
- ✅ `pyproject.toml` exists

**Troubleshooting**:

- If `langgraph new` fails: Check Python 3.8+ and `pip install --upgrade langgraph`
- If permission denied: Try `python -m langgraph new my-project`
- If directory already exists: Choose different directory name or use `langgraph new . --force`

______________________________________________________________________

## Activity 3: Configure Secrets

**Purpose**: Add LLM provider API key to .env for local development

### Step 1: Create .env from .env.example

```bash
# Copy template
cp .env.example .env

# Verify it was created
ls -la .env
cat .env
```

### Step 2: Edit .env with your API keys

Using VS Code or your editor:

```bash
# Open in editor
code .env          # VS Code
nano .env          # nano
vim .env           # vim
```

### Step 3: Add Required Variables

Minimum required (update with your actual keys):

```text
# LangSmith Configuration
LANGSMITH_API_KEY=lsv2_your_actual_key_from_smith_langchain_com

# LLM Provider (choose one and add your key)
OPENAI_API_KEY=sk-proj-your-openai-key           # For OpenAI
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key      # For Anthropic
# OR
GOOGLE_API_KEY=your-google-gemini-key            # For Google
```

### How to Get API Keys

1. **LangSmith**: Visit smith.langchain.com → Settings → Create API Key
1. **OpenAI**: Visit platform.openai.com → API keys → Create new key
1. **Anthropic**: Visit console.anthropic.com → API Keys → Create new key
1. **Google**: Visit ai.google.dev → Get API Key

### Step 4: Verify .env is Protected

```bash
# Check .gitignore protects .env
cat .gitignore | grep "^.env"
# Should output: .env

# Verify .env won't be committed
git status
# Should NOT show .env in Untracked files
```

### Step 5: Test Loading in Python

```bash
# Test loading (uv runs in environment automatically)
uv run python << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv()

print("LANGSMITH_API_KEY loaded:", bool(os.getenv('LANGSMITH_API_KEY')))
print("LLM API key loaded:", bool(
    os.getenv('OPENAI_API_KEY') or
    os.getenv('ANTHROPIC_API_KEY') or
    os.getenv('GOOGLE_API_KEY')
))
EOF
```

**Success Criteria**:

- ✅ `.env` file exists in project root
- ✅ Contains LANGSMITH_API_KEY with valid key
- ✅ Contains LLM provider API key (OpenAI, Anthropic, Google, or other)
- ✅ `.env` is protected by .gitignore
- ✅ Python can load variables from .env
- ✅ `git status` does NOT show .env

**Troubleshooting**:

- If keys not loading: Ensure .env is in project root, not subdirectory
- If `load_dotenv` not found: Install with `pip install python-dotenv`
- If wrong API key: Verify from provider's console and copy exact string
- If git keeps tracking .env: Remove with `git rm --cached .env`

______________________________________________________________________

## Activity 4: Validate Setup

**Purpose**: Verify LangSmith connection and confirm observability works

### Step 1: Test LangSmith Connection

Option A: Using langgraph CLI:

```bash
langgraph test
```

Option B: Using Python with uv:

```bash
uv run python << 'EOF'
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Check if API keys loaded
langsmith_key = os.getenv('LANGSMITH_API_KEY')
llm_key = (os.getenv('OPENAI_API_KEY') or
           os.getenv('ANTHROPIC_API_KEY') or
           os.getenv('GOOGLE_API_KEY'))

print(f"✅ LangSmith API Key loaded: {bool(langsmith_key)}")
print(f"✅ LLM API Key loaded: {bool(llm_key)}")

if langsmith_key and llm_key:
    print("\n✅ Setup validation passed!")
    print("📊 View traces at: https://smith.langchain.com/projects")
else:
    print("\n❌ Setup incomplete - missing API keys")
    exit(1)
EOF
```

### Step 2: Run Development Server

```bash
# Start local development server
langgraph dev

# In another terminal, run your code
uv run python your_script.py
```

### Step 3: Verify Traces in LangSmith

1. Open smith.langchain.com in browser
1. Login with your account
1. Click on your project
1. Scroll down - should see recent traces
1. Click a trace to view input, output, latency, tokens

**Success Criteria**:

- ✅ No "ModuleNotFoundError" when importing langchain
- ✅ LANGSMITH_API_KEY environment variable loaded
- ✅ LLM provider API key environment variable loaded
- ✅ `langgraph dev` starts without errors
- ✅ Traces appear in smith.langchain.com within 30 seconds

**Troubleshooting**:

If traces not appearing:

```bash
# Check API key is correct
echo $LANGSMITH_API_KEY

# Check .env is being loaded
uv run python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('LANGSMITH_API_KEY')[:10])"

# Wait 30 seconds and refresh dashboard
# Sometimes traces take time to propagate

# Check network connectivity
ping smith.langchain.com

# Verify LangSmith account access
# Visit smith.langchain.com directly to test login
```

If `langgraph dev` fails:

```bash
# Sync dependencies with uv
uv sync

# Try reinstalling with uv
uv pip install -e .

# Check langgraph-cli version
langgraph --version
```

______________________________________________________________________

## Quick Activity Summary

| Activity | Command | Time | Key Files Created |
|----------|---------|------|-------------------|
| 1. Verify Prerequisites | `langgraph version` | 2 min | None |
| 2. Initialize Project | `langgraph new PROJECT` | 5 min | langgraph.json, .env.example, .gitignore |
| 3. Configure Secrets | `cp .env.example .env` + edit | 3 min | .env |
| 4. Validate Setup | `langgraph test` or `langgraph dev` | 5 min | None (view in LangSmith) |

**Total estimated time**: ~15 minutes

______________________________________________________________________

## When to Skip Activities

**Skip Activity 2** if:

- `langgraph.json` already exists in current directory
- `src/` directory already exists
- You have existing LangGraph project

→ Go directly to Activity 3 (Configure Secrets)

**Skip Activity 3** if:

- `.env` file already exists with API keys
- You're using environment variables set elsewhere

→ Go directly to Activity 4 (Validate Setup)

______________________________________________________________________

## File Structure Reference

```
project-root/
├── langgraph.json                    # ← Check this in Activity 2
├── .env                              # ← Create/edit in Activity 3
├── .env.example                      # ← Already exists, don't modify
├── .gitignore                        # ← Already exists, protects .env
├── pyproject.toml                    # ← Defines dependencies
├── uv.lock                           # ← Dependency lock file (managed by uv)
├── src/
│   └── agent/
│       └── graph.py                  # ← Your agent code here
└── README.md                         # ← Your Brief Minimo spec
```

All 4 activities complete when you see traces in smith.langchain.com! 🎉
