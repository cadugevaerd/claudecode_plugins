---
description: "List and manage Serena project memories"
allowed-tools:
  - mcp__plugin_serena-mcp-helper_serena__list_memories
  - mcp__plugin_serena-mcp-helper_serena__read_memory
  - mcp__plugin_serena-mcp-helper_serena__write_memory
  - mcp__plugin_serena-mcp-helper_serena__edit_memory
  - mcp__plugin_serena-mcp-helper_serena__delete_memory
---

# Serena Memories Management

## Objective
List, read, create, and manage project memories.

## Available Operations

### List All Memories
```python
list_memories()
```

### Read a Memory
```python
read_memory("memory_name")  # without .md extension
```

### Create/Update Memory
```python
write_memory("memory_name.md", """
# Memory Title

Content here...
""")
```

### Edit Memory Content
```python
edit_memory(
    memory_file_name="memory_name.md",
    needle="text to find",
    repl="replacement text",
    mode="literal"  # or "regex"
)
```

### Delete Memory (only when explicitly requested)
```python
delete_memory("memory_name.md")
```

## Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| API docs | `api_{service}_integration.md` | `api_stripe_integration.md` |
| Architecture | `arch_{component}_design.md` | `arch_state_machine.md` |
| Patterns | `pattern_{name}.md` | `pattern_retry_backoff.md` |
| Progress | `progress_{feature}.md` | `progress_auth_flow.md` |

## Workflow

1. List existing memories to see available knowledge
2. Read relevant memories before starting work
3. Create new memories for external API documentation
4. Update CLAUDE.md with memory references
