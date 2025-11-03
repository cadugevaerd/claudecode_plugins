---
description: Interactive guide through Microprocesso 1.2 (Setup Local + Observability) - Python venv, dependencies, .env configuration, LangSmith integration. Continues from /brief with 3 operating modes. ~1.5 hours to complete environment setup.
---

# Microprocesso 1.2: Setup Local + Observability

**INTERACTIVE**: Guides you through setting up a reproducible local development environment with complete observability.

This command continues directly from `/brief`, skipping Git setup (already done) and walking you through 8 structured activities to create your production-ready local environment.

## TL;DR

`/setup-local-observability` → Choose mode → 1.5 hours → Reproducible environment ready

**Time**: ~1.5 hours
**Result**: Python venv + dependencies + .env + LangSmith integration

---

## ⚠️ Prerequisites

- ✅ Completed `/brief` (Microprocesso 1.1)
- ✅ README.md with Brief Minimo specification
- ✅ Python 3.8+ installed
- ✅ LangSmith account (free at smith.langchain.com)
- ✅ 1.5 hours available

---

## What This Command Does

After running `/setup-local-observability`, you'll have:

1. **Python Virtual Environment** - Isolated Python environment for your project
2. **Core Dependencies** - langchain, anthropic, langsmith, python-dotenv installed
3. **.env Configuration** - Secure API keys and environment variables
4. **.env.example** - Template for team members
5. **requirements.txt** - Locked dependency versions
6. **.gitignore** - Protects .env from being committed
7. **LangSmith Integration** - Full observability and tracing
8. **Validation Scripts** - Automated environment testing

---

## 🎯 Three Operating Modes

Choose the mode that fits your style:

| Mode | Best For | What Happens | Time |
|------|----------|-------------|------|
| **Guiado (Guided)** | Learning, full control | I explain each step, you execute commands manually | ~2 hours |
| **Automático (Automatic)** | Speed, reproducibility | I execute all commands automatically | ~20 minutes |
| **Misto (Mixed)** | Flexibility | You choose manual or automatic per activity | ~1.5 hours |

---

## 🚀 Quick Start

### Run the Command

```bash
/setup-local-observability
```

The command will ask you:
1. **Choose your mode**: Guiado, Automático, or Misto?
2. **LangSmith API Key**: Get from smith.langchain.com
3. **Anthropic API Key**: Get from console.anthropic.com
4. **For each activity** (if Misto mode): Manual or Automatic?

### Example Flow

```
/setup-local-observability
→ "Which mode? [G]uiado [A]utomatico [M]isto?"
→ Your response: A (Automático)
→ "Installing dependencies..."
→ [command executes: pip install langchain anthropic ...]
→ "✅ Dependencies installed"
→ [continue through all 8 activities]
→ "✅ Environment ready! Run: python validate_setup.py"
```

---

## The 8 Activities (Overview)

1. **Create Python venv** - Isolated Python environment
2. **Activate venv** - Load the environment
3. **Install dependencies** - Core LLM packages
4. **Create .env** - Store API keys securely
5. **Create .env.example** - Team template
6. **Create requirements.txt** - Dependency lock
7. **Create .gitignore** - Protect secrets
8. **Test LangSmith** - Verify observability works

Each activity has templates and validation.

---

## 💡 Key Features

**Progressive Disclosure**: Command guides overview, detailed knowledge in [skill: microprocesso-1-2]

**Validation at Each Step**: Every activity is validated before proceeding

**Templates Provided**: Copy/paste .env, .gitignore, validation script

**Troubleshooting Built-in**: If something fails, get immediate guidance

**Reproducible**: Team can use requirements.txt to recreate environment

---

## 📚 For Detailed Guidance

For detailed information about any activity:
- **Step-by-step instructions** → See skill `microprocesso-1-2`
- **Template files** → See skill `microprocesso-1-2`
- **Troubleshooting common issues** → See skill `microprocesso-1-2`
- **Validation scripts** → See skill `microprocesso-1-2`

The skill contains all the knowledge needed for each activity.

---

## What Happens Next

After successful setup:

✅ Your environment is reproducible (requirements.txt can recreate it)
✅ All traces go to LangSmith automatically
✅ You're ready for Microprocesso 1.3 (Spike Agentic)
✅ Team can onboard quickly with requirements.txt

---

## See Also

- `/brief` - Microprocesso 1.1 (agent planning)
- Skill `microprocesso-1-2` - Complete knowledge base for all 8 activities
- Full documentation: `README.md` in plugin directory

---

**Next**: After completing setup, run `/update-claude-md` to integrate guidance into your project's CLAUDE.md