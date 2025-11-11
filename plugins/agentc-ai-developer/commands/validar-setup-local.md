---
description: Validate local setup completion before Microprocesso 1.3 - checks git, uv, .env, LangSmith, README, and backlog
allowed-tools: Read, Bash, Glob, AskUserQuestion
model: claude-haiku-4-5
argument-hint: ''
---

# Validar Setup Local

⚠️ **PARADA OBRIGATÓRIA** - Validate BEFORE continuing to Microprocesso 1.3 (Spike Agentic).

Validates that all Microprocesso 1.1 (Brief) and 1.2 (Setup Local + Observability) steps are completed correctly.

## 🎯 Objective

Perform comprehensive validation of:

- ✅ Git repository initialized and functional
- ✅ UV package manager installed and synced
- ✅ .env file created with API keys (not committed)
- ✅ LangSmith account registered and working
- ✅ README.md updated with Quick Start guide
- ✅ BACKLOG.md created with user stories

**Decision Gate:**

- ALL checks pass → Proceed to `/spike-agentic` (Microprocesso 1.3) 🚀
- ANY check fails → Stop and fix issues before continuing ⚠️

## 🔧 Instructions

### 1. Validate Git Repository

1.1 **Check Git Initialization**

Execute:

```bash
git status
```

**Pass criteria:**

- Command succeeds (exit code 0)
- Shows branch name (e.g., "On branch main")
- No error: "not a git repository"

**If fails:**

- Run `git init` to initialize repository
- Create initial commit: `git add . && git commit -m "feat: initial commit"`

1.2 **Verify Initial Commit**

Execute:

```bash
git log --oneline -1
```

**Pass criteria:**

- Shows at least 1 commit
- Commit message exists

**If fails:**

- No commits yet: Inform user to create initial commit

### 2. Validate UV Installation and Sync

2.1 **Check UV Installed**

Execute:

```bash
uv --version
```

**Pass criteria:**

- Command succeeds
- Shows version (e.g., "uv 0.4.x")

**If fails:**

- UV not installed
- Provide installation command: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2.2 **Verify UV Sync Executed**

Check for indicators of uv sync:

- `.venv/` directory exists
- `uv.lock` file exists
- `pyproject.toml` has dependencies

Execute:

```bash
ls -la .venv uv.lock 2>/dev/null && echo "UV synced" || echo "UV not synced"
```

**Pass criteria:**

- `.venv/` directory exists
- `uv.lock` exists (lockfile)

**If fails:**

- Run `uv sync` to install dependencies

### 3. Validate .env File (Secrets)

3.1 **Check .env Exists**

Execute:

```bash
test -f .env && echo "EXISTS" || echo "MISSING"
```

**Pass criteria:**

- .env file exists

**If fails:**

- File missing: Create `.env` from `.env.example` template
- Add required keys: LANGSMITH_API_KEY, OPENAI_API_KEY (or LLM provider)

3.2 **Verify .env Has API Keys**

Read `.env` file and check for required keys:

```bash
grep -E "LANGSMITH_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY" .env
```

**Pass criteria:**

- At least 2 keys present (LangSmith + LLM provider)
- Keys have values (not empty)

**If fails:**

- Missing keys: Guide user to add them
- LangSmith key: Get from smith.langchain.com
- LLM key: Get from provider (OpenAI, Anthropic, etc.)

3.3 **Verify .env is NOT Committed (Security Check)**

Execute:

```bash
git status --porcelain .env 2>/dev/null
```

**Pass criteria:**

- .env does NOT appear in `git status` output
- OR shows as "??" (untracked - acceptable if .gitignore works)

**If fails (CRITICAL SECURITY ISSUE):**

- .env appears in git status as staged/modified
- Check `.gitignore` contains `.env`
- If .env was committed: Immediately run `git rm --cached .env`
- Warn user: "⚠️ SECURITY: .env must NEVER be committed!"

3.4 **Verify .gitignore Protects .env**

Execute:

```bash
grep -q "^\.env$" .gitignore && echo "PROTECTED" || echo "NOT_PROTECTED"
```

**Pass criteria:**

- `.gitignore` contains `.env` entry

**If fails:**

- Add `.env` to `.gitignore`
- Re-test with `git status .env`

### 4. Validate LangSmith Registration

4.1 **Check LangSmith API Key Format**

Extract LANGSMITH_API_KEY from .env:

```bash
grep "LANGSMITH_API_KEY" .env | cut -d= -f2
```

**Pass criteria:**

- Key starts with "lsv2\_" or "ls\_\_" (LangSmith key format)
- Key is not empty
- Key length > 20 characters

**If fails:**

- Invalid format: Ask user to get valid key from smith.langchain.com

4.2 **Test LangSmith Connection (Optional)**

Execute simple test to verify LangSmith works:

```bash
python -c "from langsmith import Client; c = Client(); print('Connected:', c.info())" 2>&1
```

**Pass criteria:**

- Command succeeds
- Shows "Connected:" with info

**If fails:**

- Connection error: Verify API key is correct
- Network error: Check internet connection
- Import error: Verify langsmith installed (`uv add langsmith`)

### 5. Validate README.md with Quick Start

5.1 **Check README.md Exists**

Execute:

```bash
test -f README.md && echo "EXISTS" || echo "MISSING"
```

**Pass criteria:**

- README.md file exists

**If fails:**

- Create basic README.md with project description

5.2 **Verify Quick Start Section**

Read README.md and search for Quick Start section:

```bash
grep -i "quick start\|getting started\|how to run" README.md
```

**Pass criteria:**

- README contains Quick Start, Getting Started, or How to Run section
- Section includes installation/setup steps

**If fails:**

- Missing Quick Start: Add section with:
  1. Clone repository
  1. Install dependencies (`uv sync`)
  1. Copy `.env.example` to `.env` and add keys
  1. Run application

5.3 **Reproducibility Test (Conceptual)**

Ask user validation question:

**Question:** "Can another developer clone this repo and run it following README steps?"

**Pass criteria:**

- User confirms YES

**If fails:**

- README incomplete: Add missing setup steps
- Dependencies not documented: Update README

### 6. Validate BACKLOG.md Created

6.1 **Check BACKLOG.md Exists**

Execute:

```bash
test -f BACKLOG.md && echo "EXISTS" || echo "MISSING"
```

**Pass criteria:**

- BACKLOG.md file exists

**If fails:**

- File missing: Must run `/backlog` command first
- Or create manually with user stories from `/create-user-histories`

6.2 **Verify BACKLOG Has User Stories**

Read BACKLOG.md and check structure:

```bash
grep -E "US-[0-9]+|Story [0-9]+|\- \[" BACKLOG.md | wc -l
```

**Pass criteria:**

- BACKLOG contains at least 3 user stories
- Stories follow format (US-ID or checkboxes)

**If fails:**

- Empty backlog: Run `/create-user-histories` then `/backlog`
- Incomplete: Add missing user stories

### 7. Generate Validation Report

7.1 **Calculate Overall Score**

Count passed checks:

- Git initialized: 10 pts
- Git has commits: 5 pts
- UV installed: 10 pts
- UV synced: 10 pts
- .env exists: 10 pts
- .env has keys: 10 pts
- .env not committed: 15 pts (CRITICAL)
- .gitignore protects .env: 10 pts
- LangSmith key valid: 10 pts
- README exists: 5 pts
- README has Quick Start: 5 pts
- BACKLOG exists: 5 pts
- BACKLOG has stories: 5 pts

**Total: 100 points**

7.2 **Determine Go/No-Go Decision**

**GREEN (100/100):** All checks passed ✅

- **Decision:** Proceed to `/spike-agentic` (Microprocesso 1.3) 🚀

**YELLOW (85-99/100):** Minor issues ⚠️

- **Decision:** Fix minor issues before proceeding
- List what needs fixing

**RED (\<85/100):** Blocking issues ❌

- **Decision:** STOP - Fix critical issues before continuing
- Prioritize security issues (.env protection)

7.3 **Present Validation Report**

Show structured report with:

- Overall score: X/100
- Passed checks (✅)
- Failed checks (❌)
- Go/No-Go decision
- Next steps

## 📊 Output Format

### Validation Report Structure

````markdown
# 🔍 Setup Validation Report

**Overall Score**: X/100 [🟢|🟡|🔴]
**Validation Date**: [YYYY-MM-DD HH:MM]

---

## ✅ Passed Checks (X/13)

- ✅ Git repository initialized
- ✅ Initial commit created
- ✅ UV package manager installed (version X.X.X)
- ✅ UV sync completed (.venv and uv.lock exist)
- ✅ .env file created with API keys
- ✅ .env contains LANGSMITH_API_KEY and LLM key
- ✅ .env NOT committed (security validated)
- ✅ .gitignore protects .env
- ✅ LangSmith API key format valid
- ✅ README.md exists with Quick Start section
- ✅ README reproducible (confirmed by user)
- ✅ BACKLOG.md exists
- ✅ BACKLOG.md contains user stories

---

## ❌ Failed Checks (X/13)

[List any failed checks with remediation steps]

Example:
- ❌ .env not protected by .gitignore
  **Fix:** Add `.env` to .gitignore file
  **Command:** `echo ".env" >> .gitignore`

---

## 🎯 Decision Gate

[If score = 100]
✅ **GO**: All validations passed!
🚀 **Next Step**: Run `/spike-agentic` to start Microprocesso 1.3

[If score 85-99]
⚠️ **CONDITIONAL GO**: Minor issues detected
🔧 **Action Required**: Fix listed issues, then re-run validation
📋 **Estimated Time**: X minutes

[If score < 85]
❌ **NO-GO**: Critical issues must be resolved
⛔ **STOP**: Do NOT proceed to Microprocesso 1.3
🔧 **Action Required**: Fix all critical issues before continuing
🔴 **Priority**: Security issues (if any)

---

## 📋 Detailed Results

### 1. Git Repository (15 pts)
- ✅ Initialized: YES
- ✅ Commits: 1 commit ("feat: initial commit")

### 2. UV Package Manager (20 pts)
- ✅ Installed: YES (version 0.4.18)
- ✅ Synced: YES (.venv and uv.lock present)

### 3. Environment Variables (45 pts) ⚠️ CRITICAL
- ✅ .env exists: YES
- ✅ API keys present: YES (2 keys found)
- ✅ Not committed: YES (security check passed)
- ✅ .gitignore protection: YES

### 4. LangSmith Integration (10 pts)
- ✅ API key format: VALID (lsv2_xxxx...)
- [Optional] Connection test: [PASSED|SKIPPED]

### 5. Documentation (10 pts)
- ✅ README.md exists: YES
- ✅ Quick Start section: YES
- ✅ Reproducible setup: CONFIRMED

### 6. Backlog (10 pts)
- ✅ BACKLOG.md exists: YES
- ✅ User stories: 5 stories found

---

## 🔧 Remediation Steps (if needed)

[Only show if there are failed checks]

**To fix issue X:**
```bash
[command to fix]
````

**To re-run validation:**

```bash
/validar-setup-local
```

______________________________________________________________________

## 📚 Reference

This validation covers:

- **Microprocesso 1.1**: Brief Minimo → BACKLOG.md
- **Microprocesso 1.2**: Setup Local + Observability → .env, UV, LangSmith

**Next Microprocesso:**

- **1.3**: Spike Agentic (`/spike-agentic`)
  - Prerequisites: ALL validations above must pass
  - Duration: ~3-4 hours
  - Output: Working agent with agentic loop

````

## ✅ Success Criteria

- [ ] Git status executed successfully
- [ ] Git commit history checked
- [ ] UV version command executed
- [ ] UV sync artifacts (.venv, uv.lock) verified
- [ ] .env file existence confirmed
- [ ] .env API keys presence validated
- [ ] .env NOT in git status (security check)
- [ ] .gitignore contains .env entry
- [ ] LANGSMITH_API_KEY format validated
- [ ] README.md existence confirmed
- [ ] README Quick Start section verified
- [ ] BACKLOG.md existence confirmed
- [ ] BACKLOG user stories counted
- [ ] Overall score calculated (0-100)
- [ ] Go/No-Go decision determined
- [ ] Validation report presented to user
- [ ] Remediation steps provided (if needed)

## 📝 Examples

### Example 1: Perfect Setup (All Passed)

**Command:**
```bash
/validar-setup-local
````

**Result:**

```
🔍 Setup Validation Report
Overall Score: 100/100 🟢

✅ All 13 checks passed!

🎯 Decision: GO ✅
🚀 Next Step: Run /spike-agentic (Microprocesso 1.3)

You're ready to start building your agentic spike! 🚀
```

### Example 2: Minor Issues (85-99 pts)

**Command:**

```bash
/validar-setup-local
```

**Result:**

```
🔍 Setup Validation Report
Overall Score: 90/100 🟡

✅ Passed: 12/13 checks

❌ Failed Checks:
- README Quick Start section missing

🎯 Decision: CONDITIONAL GO ⚠️
🔧 Fix: Add Quick Start section to README.md
📋 Estimated Time: 5 minutes

After fixing, re-run: /validar-setup-local
```

### Example 3: Critical Issues (\<85 pts)

**Command:**

```bash
/validar-setup-local
```

**Result:**

```
🔍 Setup Validation Report
Overall Score: 70/100 🔴

✅ Passed: 9/13 checks

❌ Failed Checks (CRITICAL):
1. ❌ .env is COMMITTED (git status shows it) 🔴 SECURITY RISK
   Fix: git rm --cached .env && git commit -m "Remove .env from git"

2. ❌ .gitignore does NOT protect .env
   Fix: echo ".env" >> .gitignore

3. ❌ UV not synced (no .venv directory)
   Fix: uv sync

4. ❌ BACKLOG.md missing
   Fix: Run /create-user-histories then /backlog

🎯 Decision: NO-GO ❌
⛔ STOP: Do NOT proceed to Microprocesso 1.3
🔴 Priority 1: Fix security issue (.env exposure)
🔧 Fix all issues above, then re-run validation
```

## ❌ Anti-Patterns

### ❌ Error 1: Skipping Security Validation

Don't proceed if .env is exposed:

```markdown
# ❌ Wrong - Ignore .env in git
Score: 85/100 (missing .env protection)
Decision: Proceed anyway

# ✅ Correct - Block on security issues
Score: 85/100
❌ CRITICAL: .env not protected
⛔ NO-GO: Fix security issue before continuing
```

### ❌ Error 2: Not Checking UV Sync

Don't assume UV is synced without verification:

```markdown
# ❌ Wrong - Assume synced
UV installed? YES → Mark as complete

# ✅ Correct - Verify sync artifacts
UV installed? YES
UV synced? Check for .venv and uv.lock
```

### ❌ Error 3: Accepting Empty BACKLOG

Don't pass validation with empty backlog:

```markdown
# ❌ Wrong - File exists = Pass
BACKLOG.md exists? YES ✅

# ✅ Correct - Verify content
BACKLOG.md exists? YES
BACKLOG has stories? Check for US-XX or checkboxes
Minimum: 3 user stories
```

### ❌ Error 4: Not Testing .gitignore Protection

Don't trust .gitignore without testing:

```markdown
# ❌ Wrong - Assume .gitignore works
.gitignore contains .env? YES ✅

# ✅ Correct - Test with git status
.gitignore contains .env? YES
Test: git status .env
Result: File not shown = Protected ✅
```

### ❌ Error 5: Ignoring LangSmith Key Format

Don't accept any string as LangSmith key:

```markdown
# ❌ Wrong - Any value is OK
LANGSMITH_API_KEY=my-secret-key ✅

# ✅ Correct - Validate format
LANGSMITH_API_KEY must start with "lsv2_" or "ls__"
Length must be >20 characters
Example: lsv2_pt_abc123xyz...
```

### ❌ Error 6: Proceeding with Low Score

Don't allow progression with critical failures:

```markdown
# ❌ Wrong - Soft validation
Score: 65/100
"You have some issues, but you can continue"

# ✅ Correct - Hard gate
Score: 65/100 (< 85 threshold)
❌ NO-GO: Critical issues must be fixed
⛔ STOP: Do NOT proceed to Microprocesso 1.3
```
