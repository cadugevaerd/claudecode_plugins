---
name: microprocesso-1-2
description: Complete knowledge about Microprocesso 1.2 (Setup Local + Observability) - Python virtual environment setup, dependency installation, .env configuration, LangSmith integration, validation, and troubleshooting. Use when user needs detailed guidance on any of the 8 setup activities or encounters errors during environment setup.
allowed-tools: Read, Bash, Write
---

# Microprocesso 1.2: Setup Local + Observability

Complete knowledge base for implementing Microprocesso 1.2 - the environment setup phase that follows Brief Minimo planning (`/brief`).

## Purpose

Microprocesso 1.2 guides you through setting up a reproducible, fully observable local development environment for your AI agent project. This includes:

- ✅ Python virtual environment with isolation
- ✅ Dependency management (LangChain, Anthropic, LangSmith, python-dotenv)
- ✅ Environment configuration (.env + .gitignore)
- ✅ LangSmith integration for observability and tracing
- ✅ Complete validation and testing

**Total time**: ~1.5 hours
**Result**: Production-ready local environment with full observability

---

## Prerequisites

Before starting Microprocesso 1.2, you should have:

✅ Completed `/brief` command (Microprocesso 1.1)
✅ README.md with your Brief Minimo specification
✅ Project repository created (done by `/brief`)
✅ Python 3.8+ installed on your system
✅ 1.5 hours of focused time
✅ LangSmith account (free tier available at smith.langchain.com)

---

## The 8 Setup Activities

Microprocesso 1.2 consists of 8 structured activities:

### Activity 1: Create and Activate Python Virtual Environment

**Purpose**: Isolate project dependencies from system Python

**What to do**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Verification**:
- Prompt should show `(venv)` prefix
- `which python` should point to venv directory
- `python --version` should show Python 3.8+

**Troubleshooting**:
- If `python -m venv` fails: Try `python3 -m venv venv`
- If activation doesn't work: Check your shell compatibility (bash/zsh/powershell)
- If permission denied: Use `chmod +x venv/bin/activate`

---

### Activity 2: Install Core Dependencies

**Purpose**: Install minimal LLM framework and utility packages

**Packages to install**:
- `langchain` - LLM orchestration framework
- `anthropic` - Anthropic API client
- `langsmith` - Observability and tracing
- `python-dotenv` - Environment variable management

**What to do**:
```bash
pip install langchain anthropic langsmith python-dotenv
```

**Verification**:
```bash
pip list | grep -E "langchain|anthropic|langsmith|python-dotenv"
```

**Expected output**:
```
anthropic           x.x.x
langchain          x.x.x
langsmith          x.x.x
python-dotenv      x.x.x
```

**Troubleshooting**:
- If installation is slow: Network issue or PyPI mirror problem
- If version conflicts: Clear pip cache with `pip cache purge`
- If specific package fails: Try installing without version constraints first

---

### Activity 3: Create .env File with LangSmith Credentials

**Purpose**: Store API keys and configuration securely

**Steps**:
1. Go to smith.langchain.com
2. Sign up (free) or log in
3. Create new API key in settings
4. Create `.env` file in project root

**Template `.env` file**:
```bash
# LangSmith Configuration
LANGSMITH_API_KEY=<your-api-key-from-smith.langchain.com>
LANGSMITH_PROJECT="<your-project-name>"
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Anthropic Configuration
ANTHROPIC_API_KEY=<your-api-key-from-console.anthropic.com>

# Environment
ENVIRONMENT=development
```

**Verification**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
print(f"LangSmith API Key loaded: {bool(os.getenv('LANGSMITH_API_KEY'))}")
print(f"Anthropic API Key loaded: {bool(os.getenv('ANTHROPIC_API_KEY'))}")
```

**Security Note**: Never commit `.env` to Git. Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

**Troubleshooting**:
- If keys not loading: Check file is in project root (not subdirectory)
- If dotenv not found: Install with `pip install python-dotenv`
- If wrong credentials: Verify keys from respective consoles

---

### Activity 4: Create .env.example for Documentation

**Purpose**: Document what environment variables are needed (without secrets)

**Template `.env.example`**:
```bash
# LangSmith Configuration
LANGSMITH_API_KEY=your-api-key-here
LANGSMITH_PROJECT=your-project-name
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Anthropic Configuration
ANTHROPIC_API_KEY=your-api-key-here

# Environment
ENVIRONMENT=development
```

**Purpose**: Team members can copy this, rename to `.env`, and fill in their own keys

---

### Activity 5: Create requirements.txt for Reproducibility

**Purpose**: Lock dependency versions for reproducible environments

**What to do**:
```bash
pip freeze > requirements.txt
```

**Typical output**:
```
anthropic==0.7.0
langchain==0.0.300
langsmith==0.0.21
python-dotenv==1.0.0
requests==2.31.0
pydantic==2.0.0
...
```

**For team sharing**: Commit `requirements.txt` to Git
```bash
git add requirements.txt
git commit -m "docs: add reproducible dependency list"
```

**For onboarding**:
New team member can reproduce exact environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Activity 6: Create .gitignore for Project Files

**Purpose**: Prevent committing sensitive/temporary files

**Template `.gitignore`**:
```
# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.cache/
tmp/
```

---

### Activity 7: Test LangSmith Integration

**Purpose**: Verify observability pipeline is working

**Create test file** (`test_langsmith.py`):
```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from langchain.callbacks.tracers import LangChainTracer
from langsmith.client import Client

# Load environment variables
load_dotenv()

# Initialize LangSmith client
langsmith_client = Client()

# Create tracer
tracer = LangChainTracer(client=langsmith_client)

# Initialize Anthropic client
client = Anthropic()

# Simple test
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello!"}
    ]
)

print("✅ LangSmith integration working!")
print(f"Response: {message.content[0].text}")
print(f"Check your traces at: https://smith.langchain.com")
```

**Run test**:
```bash
python test_langsmith.py
```

**Expected output**:
```
✅ LangSmith integration working!
Response: Hello! 👋
Check your traces at: https://smith.langchain.com
```

**Troubleshooting**:
- If connection fails: Check LANGSMITH_API_KEY is correct
- If 401 error: API key has been revoked, get new one
- If timeout: Check internet connection
- If module not found: Run `pip install langchain langsmith anthropic`

---

### Activity 8: Create Validation Script

**Purpose**: Run comprehensive environment validation

**Create file** (`validate_setup.py`):
```python
#!/usr/bin/env python3
"""Validate Microprocesso 1.2 setup completeness."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_venv():
    """Check if virtual environment is active."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    else:
        print("❌ Virtual environment NOT active - run: source venv/bin/activate")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required = ['langchain', 'anthropic', 'langsmith', 'python-dotenv']
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} NOT installed")

    return len(missing) == 0

def check_env_file():
    """Check if .env file exists with required keys."""
    load_dotenv()

    required_keys = ['LANGSMITH_API_KEY', 'ANTHROPIC_API_KEY']
    missing = []

    if not Path('.env').exists():
        print("❌ .env file NOT found")
        return False

    print("✅ .env file exists")

    for key in required_keys:
        if os.getenv(key):
            print(f"✅ {key} configured")
        else:
            missing.append(key)
            print(f"❌ {key} NOT configured")

    return len(missing) == 0

def check_gitignore():
    """Check if .gitignore includes .env."""
    if not Path('.gitignore').exists():
        print("⚠️  .gitignore not found (optional)")
        return False

    with open('.gitignore') as f:
        content = f.read()

    if '.env' in content:
        print("✅ .gitignore includes .env")
        return True
    else:
        print("⚠️  .gitignore doesn't include .env")
        return False

def main():
    """Run all validation checks."""
    print("=" * 50)
    print("Microprocesso 1.2 Setup Validation")
    print("=" * 50)
    print()

    checks = [
        ("Virtual Environment", check_venv),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        (".gitignore", check_gitignore),
    ]

    results = []
    for name, check in checks:
        print(f"\n📋 Checking: {name}")
        result = check()
        results.append((name, result))
        print()

    print("=" * 50)
    print("Summary")
    print("=" * 50)

    for name, result in results:
        status = "✅ PASS" if result else "⚠️  CHECK"
        print(f"{status}: {name}")

    all_pass = all(r for _, r in results)

    if all_pass:
        print("\n✅ All checks passed! Your environment is ready.")
        return 0
    else:
        print("\n⚠️  Some checks need attention. See above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Run validation**:
```bash
python validate_setup.py
```

**Expected output**:
```
==================================================
Microprocesso 1.2 Setup Validation
==================================================

📋 Checking: Virtual Environment
✅ Virtual environment is active

📋 Checking: Dependencies
✅ langchain installed
✅ anthropic installed
✅ langsmith installed
✅ python-dotenv installed

📋 Checking: Environment File
✅ .env file exists
✅ LANGSMITH_API_KEY configured
✅ ANTHROPIC_API_KEY configured

📋 Checking: .gitignore
✅ .gitignore includes .env

==================================================
Summary
==================================================
✅ PASS: Virtual Environment
✅ PASS: Dependencies
✅ PASS: Environment File
✅ PASS: .gitignore

✅ All checks passed! Your environment is ready.
```

---

## Troubleshooting Common Issues

### "ModuleNotFoundError: No module named 'langchain'"

**Cause**: Dependencies not installed in active virtual environment

**Solution**:
1. Verify venv is active: `which python` should show venv path
2. Reinstall: `pip install langchain anthropic langsmith python-dotenv`
3. Verify: `python -c "import langchain; print(langchain.__version__)"`

---

### "Error: Failed to load API key from .env"

**Cause**: Environment variable not loaded or .env file missing

**Solution**:
1. Verify .env exists in project root: `ls -la .env`
2. Verify keys are set: `grep LANGSMITH .env`
3. Reload in Python: `from dotenv import load_dotenv; load_dotenv()`
4. If still failing: Check for typos in key names

---

### "401 Unauthorized - Invalid API Key"

**Cause**: Incorrect or expired API key

**Solution**:
1. Go to smith.langchain.com
2. Check if API key is still valid in settings
3. Create new key if needed
4. Update .env with new key
5. Test with validation script

---

### "pip install hangs or times out"

**Cause**: Network issues or slow PyPI mirror

**Solution**:
1. Try different PyPI index: `pip install -i https://mirrors.aliyun.com/pypi/simple/ langchain`
2. Upgrade pip: `pip install --upgrade pip`
3. Clear cache: `pip cache purge`
4. Try installing one package at a time

---

### "No module named 'dotenv' after importing"

**Cause**: python-dotenv not installed

**Solution**:
```bash
pip install python-dotenv
# Verify
python -c "import dotenv; print(dotenv.__version__)"
```

---

## Operating Modes

The `/setup-local-observability` command supports 3 different operating modes:

### Mode 1: Guiado (Guided - Full Manual Control)

**Best for**: Learning, understanding each step, complete control

**How it works**:
- Command explains each activity
- Provides templates you can copy/paste
- You execute commands manually
- Command validates results
- You can stop/review at any point

**Flow**:
```
/setup-local-observability --mode guiado
├─ Activity 1: Create venv [copy this: python -m venv venv]
│  └─ You run: python -m venv venv
│  └─ Command validates: "✅ venv created"
├─ Activity 2: Activate venv [copy this: source venv/bin/activate]
│  └─ You run: source venv/bin/activate
│  └─ Command validates: "✅ venv active"
└─ [Continue for all 8 activities]
```

---

### Mode 2: Automático (Automatic - Hands-Off)

**Best for**: Speed, reproducibility, when you trust the setup

**How it works**:
- Command describes what it will do
- Command executes bash commands automatically
- You monitor progress
- Command validates each step
- Fast setup without manual intervention

**Flow**:
```
/setup-local-observability --mode automatico
├─ Step 1: Creating Python venv...
│  └─ Executing: python -m venv venv [✓]
├─ Step 2: Installing dependencies...
│  └─ Executing: pip install langchain anthropic langsmith python-dotenv [✓]
├─ Step 3: Setting up .env...
│  └─ Executing: cat > .env <<EOF ... [✓]
└─ [Continue through all 8 activities]

Total time: ~20 minutes
```

---

### Mode 3: Misto (Mixed - Choose Per Activity)

**Best for**: Flexibility, choosing control level per activity

**How it works**:
- For each activity, choose: Manual or Automatic
- Some activities manual (to understand), others automatic (to save time)
- Full control with minimal busywork

**Flow**:
```
/setup-local-observability --mode misto

Activity 1: Create venv
  ├─ Manual or Automatic? [A]utomatic
  └─ Executing: python -m venv venv [✓]

Activity 2: Activate venv
  ├─ Manual or Automatic? [M]anual
  └─ Execute: source venv/bin/activate [you run this]

Activity 3: Install dependencies
  ├─ Manual or Automatic? [A]utomatic
  └─ Executing: pip install ... [✓]

[Continue, choosing for each activity]
```

---

## Next Steps After Microprocesso 1.2

After completing setup, you're ready to:

1. **Start Development**: Your environment is reproducible and observable
2. **Create Agent Code**: Using the Brief Minimo spec as your reference
3. **Test with LangSmith**: All traces automatically sent to your project
4. **Share with Team**: They can reproduce environment with `requirements.txt`
5. **Monitor Observability**: View all traces in LangSmith dashboard

---

## Quick Reference

**Essential commands**:
```bash
# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test setup
python validate_setup.py

# View LangSmith traces
# → Open https://smith.langchain.com/projects/
```

**Files created**:
```
project-root/
├── venv/                      # Virtual environment
├── .env                       # Secrets (NOT committed)
├── .env.example              # Template (committed)
├── .gitignore                # Excludes sensitive files
├── requirements.txt          # Locked dependencies
├── test_langsmith.py         # LangSmith integration test
├── validate_setup.py         # Setup validation script
└── README.md                 # Your Brief Minimo spec
```

---

**Developed for agentc-ai-developer plugin** 🚀