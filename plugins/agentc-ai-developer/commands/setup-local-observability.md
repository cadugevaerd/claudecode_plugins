---
description: Interactive guide through Microprocesso 1.2 (Setup Local + Observability) - Python venv, dependencies, .env configuration, LangSmith integration. Continues from /brief with 3 operating modes. ~1.5 hours to complete environment setup.
allowed-tools: Read, Bash, Write
---

# Microprocesso 1.2: Setup Local + Observability

Interactive setup for reproducible Python environment with LangSmith observability.

## Prerequisites

Verify before starting:

- Completed `/brief` (Microprocesso 1.1)
- README.md with Brief Minimo specification exists
- Python 3.8+ installed
- LangSmith account created (smith.langchain.com)
- Anthropic API key available (console.anthropic.com)
- 1.5 hours available

## Execution

1. **Choose Operating Mode**

   - Ask user: "Select mode - [G]uiado, [A]utomático, or [M]isto?"
   - Guiado: Explain each step, user executes manually (~2h)
   - Automático: Execute all commands automatically (~20min)
   - Misto: Ask per activity: manual or automatic? (~1.5h)

1. **Execute 8 Activities** (in sequence)

   - Activity 1: Create Python venv
   - Activity 2: Activate venv
   - Activity 3: Install dependencies (langchain, anthropic, langsmith, python-dotenv)
   - Activity 4: Create .env file with API keys
   - Activity 5: Create .env.example template
   - Activity 6: Create requirements.txt
   - Activity 7: Create/update .gitignore
   - Activity 8: Test LangSmith integration

1. **Validate Each Activity**

   - Verify files created correctly
   - Check dependencies installed
   - Test environment variables loaded
   - Confirm LangSmith connection works

1. **Create Validation Script**

   - Generate validate_setup.py
   - Run validation
   - Report results

## Operating Mode Details

**Guiado (Guided)**:

- Explain each activity step-by-step
- Provide commands for user to execute
- Wait for confirmation before proceeding

**Automático (Automatic)**:

- Execute all commands without intervention
- Show progress for each activity
- Report final status

**Misto (Mixed)**:

- Before each activity, ask: "Manual or Automatic?"
- Execute accordingly
- Combine flexibility with speed

## Validation Criteria

After completion, verify:

- venv directory exists and is activated
- All dependencies listed in requirements.txt
- .env contains LANGSMITH_API_KEY and ANTHROPIC_API_KEY
- .env.example exists (no secrets)
- .gitignore protects .env
- validate_setup.py runs successfully
- LangSmith traces visible at smith.langchain.com

## Next Steps

After successful setup:

- Run `/update-claude-md` to integrate guidance
- Proceed to `/spike-agentic` (Microprocesso 1.3)
- Share requirements.txt with team for reproducibility

## Detailed Knowledge

For step-by-step instructions, templates, and troubleshooting, see skill `microprocesso-1-2`.
