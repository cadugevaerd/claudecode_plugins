# Microprocesso 1.2: Detailed Activity Reference

Complete step-by-step instructions for all 8 setup activities.

## Activity 1: Create Python Virtual Environment

**Purpose**: Isolate project dependencies from system Python

**Commands**:

````bash
python -m venv venv

```text

On Windows, if `python` doesn't work:

```bash
python3 -m venv venv

```text

**Verification**:

```bash

# Check venv exists
ls -la venv/

# On Windows
dir venv\

```text

**Troubleshooting**:
- If `python -m venv` fails: Try `python3 -m venv venv`
- If permission denied: Use `chmod +x venv/bin/activate`
- If venv already exists: Delete with `rm -rf venv/` and create new


## Activity 2: Activate Virtual Environment

**Purpose**: Load the isolated environment so pip installs go to venv, not system

**On Linux/macOS**:

```bash
source venv/bin/activate

```text

**On Windows (PowerShell)**:

```powershell
venv\Scripts\activate

```text

**On Windows (cmd.exe)**:

```cmd
venv\Scripts\activate.bat

```text

**Verification** (you should see `(venv)` prefix in terminal):

```bash
(venv) $ which python
/path/to/project/venv/bin/python

(venv) $ python --version
Python 3.10.x

```text

**Troubleshooting**:
- If prompt doesn't show `(venv)`: Not activated, run command again
- If "command not found": Wrong path or venv not created yet
- If permission denied on macOS/Linux: Run `chmod +x venv/bin/activate`


## Activity 3: Install Core Dependencies

**Purpose**: Install packages needed for LLM development and observability

**Command** (with venv activated):

```bash
pip install langchain anthropic langsmith python-dotenv

```text

**Full install with additional packages** (optional):

```bash
pip install langchain anthropic langsmith python-dotenv pydantic pytest

```text

**Verification**:

```bash
pip list | grep -E "langchain|anthropic|langsmith|python-dotenv"

```text

Expected output:

```text

anthropic           0.34.x
langchain           0.1.x
langsmith           0.1.x
python-dotenv       1.0.x

```text

**Troubleshooting**:
- If installation is slow: Network issue or PyPI slow
- If version conflicts: `pip cache purge` then try again
- If specific package fails: Install packages individually
  ```bash
  pip install langchain
  pip install anthropic
  pip install langsmith
  pip install python-dotenv
````

## Activity 4: Create .env File

**Purpose**: Store API keys and configuration locally (NOT committed to git)

**Location**: Project root directory

**Template** (create file named `.env`):

````bash

# LangSmith Configuration
LANGSMITH_API_KEY=your-key-from-smith.langchain.com
LANGSMITH_PROJECT="your-project-name"
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Anthropic Configuration
ANTHROPIC_API_KEY=your-key-from-console.anthropic.com

# Environment
ENVIRONMENT=development

```text

**How to create**:

Using VS Code: Create file `.env` in project root, paste template

Using command line:

```bash
cat > .env << 'EOF'
LANGSMITH_API_KEY=your-key
LANGSMITH_PROJECT="your-project"
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
ANTHROPIC_API_KEY=your-key
ENVIRONMENT=development
EOF

```text

**Get API Keys**:
1. **LangSmith**: Visit smith.langchain.com → Sign up (free) → Settings → Create API key
2. **Anthropic**: Visit console.anthropic.com → Login → API Keys → Create new key

**Verification**:

```bash

# Check file exists
ls -la .env

# Check it has content
cat .env

# Test loading in Python
python << 'EOF'
from dotenv import load_dotenv
import os
load_dotenv()
print("LANGSMITH_API_KEY:", bool(os.getenv('LANGSMITH_API_KEY')))
print("ANTHROPIC_API_KEY:", bool(os.getenv('ANTHROPIC_API_KEY')))
EOF

```text

**Troubleshooting**:
- If keys not loading: Check file is in project root (not subfolder)
- If `load_dotenv` fails: Install with `pip install python-dotenv`
- If wrong keys: Verify from console.anthropic.com and smith.langchain.com


## Activity 5: Create .env.example

**Purpose**: Documentation for team members (template without secrets)

**Location**: Project root (same directory as .env)

**Template** (create file named `.env.example`):

```bash

# LangSmith Configuration
LANGSMITH_API_KEY=your-api-key-here
LANGSMITH_PROJECT=your-project-name
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Anthropic Configuration
ANTHROPIC_API_KEY=your-api-key-here

# Environment
ENVIRONMENT=development

```text

**Purpose for team**:
1. New team member clones repo
2. Copies `.env.example` to `.env`
3. Fills in their own API keys
4. Never needs to ask "what env variables do I need?"

**How to create**:

Using command line:

```bash
cat > .env.example << 'EOF'
LANGSMITH_API_KEY=your-api-key-here
LANGSMITH_PROJECT=your-project-name
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
ANTHROPIC_API_KEY=your-api-key-here
ENVIRONMENT=development
EOF

```text

**Verification**:

```bash

# Check file exists
ls -la .env.example

# Compare with .env
diff .env .env.example

# Should show only differences are actual values vs placeholders

```text

**Important**: `.env.example` IS committed to git (it has no secrets)


## Activity 6: Create requirements.txt

**Purpose**: Lock exact dependency versions for reproducibility

**Location**: Project root

**Command** (with venv activated):

```bash
pip freeze > requirements.txt

```text

**Result** (typical content):

```text

anthropic==0.34.0
langchain==0.1.14
langchain-community==0.0.32
langsmith==0.1.75
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-core==2.14.1
...

```text

**Why this matters**:
- Locks exact versions of all packages
- Team member runs `pip install -r requirements.txt` → exact same versions
- Prevents "works on my machine" problems

**For team onboarding**:

```bash

# New team member setup
python -m venv venv
source venv/bin/activate  # or Windows equivalent
pip install -r requirements.txt

# Now they have exact same environment as you

```text

**Verification**:

```bash

# Check file exists and has content
ls -la requirements.txt
wc -l requirements.txt

```text

**Important**: Commit `requirements.txt` to git (no secrets, safe to share)


## Activity 7: Create .gitignore

**Purpose**: Prevent accidentally committing secrets and unnecessary files

**Location**: Project root

**Minimal template** (copy this):

```text

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

```text

**How to create**:

```bash
cat > .gitignore << 'EOF'

# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF

```text

**Critical files to ignore**:
- `.env` - MUST be ignored (has secrets)
- `venv/` - Don't commit (15GB+, recreate with requirements.txt)
- `__pycache__/` - Generated by Python
- `.vscode/, .idea/` - IDE configuration

**Verification**:

```bash

# Check file exists
ls -la .gitignore

# Simulate git add (won't actually add ignored files)
git add .
git status

# Should NOT show .env or venv/

```text

**Troubleshooting**:
- If .env keeps showing in git: Remove from staging: `git reset .env`
- If too much ignored: Start with minimal, add more as needed


## Activity 8: Test LangSmith Integration

**Purpose**: Verify observability setup works end-to-end

**Create test file** (`test_langsmith.py` in project root):

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic()

# Simple test
print("Testing LangSmith integration...")
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

```text

**Run test** (with venv activated):

```bash
python test_langsmith.py

```text

**Expected output**:

```text

Testing LangSmith integration...
✅ LangSmith integration working!
Response: Hello! How can I help you today?
Check your traces at: https://smith.langchain.com

```text

**Verify in LangSmith**:
1. Go to smith.langchain.com
2. Login
3. Click on your project
4. Should see trace of your API call
5. Shows: input, output, latency, tokens used

**Troubleshooting**:
- If connection fails: Check LANGSMITH_API_KEY is correct
- If 401 error: API key revoked, create new one at smith.langchain.com
- If timeout: Check internet connection
- If "module not found": `pip install anthropic langsmith`


## Quick Command Checklist

```bash

# 1. Create venv
python -m venv venv

# 2. Activate (Linux/macOS)
source venv/bin/activate

# 3. Install dependencies
pip install langchain anthropic langsmith python-dotenv

# 4-5. Create .env and .env.example (use editor or cat command above)

# 6. Create requirements.txt
pip freeze > requirements.txt

# 7. Create .gitignore (use editor or cat command above)

# 8. Test
python test_langsmith.py

```text

All activities complete when you see ✅ output and traces appear in smith.langchain.com!
````
