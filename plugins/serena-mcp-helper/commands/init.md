---
description: "Initialize Serena MCP for a new project - runs onboarding and creates initial memories"
allowed-tools:
  - mcp__plugin_serena-mcp-helper_serena__initial_instructions
  - mcp__plugin_serena-mcp-helper_serena__check_onboarding_performed
  - mcp__plugin_serena-mcp-helper_serena__onboarding
  - mcp__plugin_serena-mcp-helper_serena__list_memories
  - Write
  - Read
---

# Initialize Serena MCP

## Objective
Set up Serena MCP for this project, running onboarding and creating initial memories.

## Steps

### 1. Load Serena Instructions Manual
Call `mcp__plugin_serena-mcp-helper_serena__initial_instructions` first.

### 2. Check Onboarding Status
```python
check_onboarding_performed()
```

### 3. Run Onboarding (if needed)
If not onboarded:
```python
onboarding()
```

### 4. Verify Memories
```python
list_memories()
```

### 5. Update CLAUDE.md
Add memory references to project's CLAUDE.md:

```markdown
## Project Memories (Serena MCP)

Use Serena MCP for persistent knowledge:
- `list_memories()` - See all stored memories
- `read_memory("name")` - Read specific memory
- `write_memory("name.md", content)` - Store new knowledge
```

## Success Criteria
- Serena onboarding completed
- Initial memories created
- CLAUDE.md updated with memory references
