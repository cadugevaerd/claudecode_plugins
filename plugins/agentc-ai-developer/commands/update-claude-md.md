---
description: Integrates Agentc AI Developer guidance into project's CLAUDE.md (≤40 lines). Reads README.md from /brief, extracts Brief Minimo specification, creates focused section with commands and next steps. Progressive disclosure pattern with links to full documentation.
allowed-tools: Read, Write
argument-hint: '[silent|verbose]'
---

# Update Project CLAUDE.md

Automatically integrate Agentc AI Developer guidance into your project's CLAUDE.md file.

## Prerequisites

Verify before execution:

1. Completed `/brief` command (Microprocesso 1.1)
1. README.md exists with Brief Minimo specification
1. Project's CLAUDE.md exists or will be created automatically

## Execution

1. ## **Read project context**

   - Extract Brief Minimo spLocate README.md (from `/brief` command)ecification (agent name, purpose)
   - Validate Microprocesso 1.1 completion

1. **Generate CLAUDE.md section**

   - Create concise guidance section (≤40 lines)
   - Include available Agentc commands: `/brief`, `/setup-local-observability`, `/spike-agentic`, `/backlog`
   - Add usage context: when to use each command
   - Link to `plugins/agentc-ai-developer/README.md` for details

1. **Update or create CLAUDE.md**

   - If CLAUDE.md exists: Add Agentc section (update if already present)
   - If CLAUDE.md missing: Create with Agentc section only
   - Preserve existing content, never remove

1. **Report completion**

   - Confirm CLAUDE.md location and updated section
   - Show generated content
   - Display execution time (\<1 minute)

## Generated Section Example

```markdown
## Agentc AI Developer (Microprocesso 1.1-1.4)

Commands for AI agent planning, environment setup, architecture validation, and incremental development:

- **`/brief`**: Create or review Brief Minimo specification
- **`/setup-local-observability`**: Configure Python venv, dependencies, .env, LangSmith
- **`/spike-agentic`**: Validate agent architecture with agentic loop
- **`/backlog`**: Generate incremental development backlog

**Documentation**: See `plugins/agentc-ai-developer/README.md`
```

## Troubleshooting

### README.md not found

- Execute `/brief` first to create Brief Minimo specification

### CLAUDE.md doesn't exist

- Command creates CLAUDE.md automatically with Agentc section only

### Section already exists

- Command updates existing section (no duplication)
- All other CLAUDE.md content preserved
