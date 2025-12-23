---
description: "This skill activates when the user asks about Serena MCP integration, project memories, onboarding new projects, storing knowledge, or persisting context across sessions. Trigger on: 'setup Serena', 'create memory', 'store project knowledge', 'onboard project', 'read memory', 'list memories', 'persist context'."
---

# Serena MCP Integration Guide

## Why Serena MCP?

Serena MCP provides:
- **Symbol-level code navigation** - Functions, classes, methods (not just full files)
- **Token savings up to 70%** - Read only what you need
- **Persistent memory** - Knowledge survives across sessions
- **Semantic code analysis** - LSP-powered understanding

---

## Onboarding New Projects

### Step 1: Check Onboarding Status

```python
# First, check if project was already onboarded
check_onboarding_performed()

# If not performed, run onboarding
onboarding()
```

### Step 2: Automatic Memory Generation

Serena's onboarding automatically creates memories for:
- Project overview and structure
- Tech stack detection
- Coding patterns and standards
- Development commands

### Step 3: Verify Memory Creation

```python
# List all memories to verify
list_memories()

# Expected output:
# - project_overview.md
# - coding_standards.md
# - development_commands.md
```

---

## Memory Operations

### Creating Memories

Use memories to store:
- API integration documentation
- Architecture decisions (ADRs)
- Reusable patterns
- Feature implementation progress

```python
# Create a new memory
write_memory(
    memory_file_name="api_stripe_integration.md",
    content="""
# Stripe API Integration

## Authentication
- API Key stored in SSM Parameter Store
- Path: /prod/agent/stripe_api_key

## Endpoints Used
- POST /v1/customers
- POST /v1/payment_intents
- GET /v1/payment_intents/{id}

## Webhook Events
- payment_intent.succeeded
- payment_intent.failed
- customer.created

## Error Handling
All Stripe errors return:
{
  "error": {
    "type": "...",
    "message": "...",
    "code": "..."
  }
}

## Rate Limits
- 100 requests/second (test mode)
- Contact Stripe for production limits
"""
)
```

### Reading Memories

```python
# Read a specific memory
read_memory("api_stripe_integration")

# Content is returned as markdown
```

### Listing Memories

```python
# List all available memories
list_memories()

# Returns list of memory filenames
```

### Editing Memories

```python
# Update content in a memory
edit_memory(
    memory_file_name="api_stripe_integration.md",
    needle="## Rate Limits",
    repl="## Rate Limits (Updated Dec 2024)",
    mode="literal"
)
```

### Deleting Memories

```python
# Only when user explicitly requests
delete_memory("outdated_memory.md")
```

---

## Memory Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| API docs | `api_{service}_integration.md` | `api_stripe_integration.md` |
| Architecture | `arch_{component}_design.md` | `arch_agent_state_machine.md` |
| Patterns | `pattern_{name}.md` | `pattern_retry_with_backoff.md` |
| Progress | `progress_{feature}.md` | `progress_payment_flow.md` |
| Agent overview | `agent_overview.md` | - |

---

## CLAUDE.md Integration

**CRITICAL**: After creating memories, always add references to CLAUDE.md!

```markdown
## Project Memories (Serena MCP)

### API Integrations
- `api_stripe_integration` - Stripe payment API docs, auth, webhooks
  Use: `read_memory('api_stripe_integration')`

### Architecture Decisions
- `arch_agent_state_machine` - LangGraph state design
  Use: `read_memory('arch_agent_state_machine')`

### Patterns
- `pattern_retry_with_backoff` - Retry logic for external APIs
  Use: `read_memory('pattern_retry_with_backoff')`
```

This enables future sessions to quickly access relevant knowledge.

---

## Workflow: External API Integration

When integrating a new external API:

1. **Research** - Use WebSearch to find API documentation
2. **Document** - Create memory with findings
3. **Reference** - Add to CLAUDE.md
4. **Evaluate MCP** - Check if MCP server exists for this API

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  Research  │───▶│  Document  │───▶│ Reference  │───▶│ Evaluate   │
│  (WebSearch)│    │ (write_    │    │ (CLAUDE.md)│    │   MCP      │
│            │    │  memory)   │    │            │    │            │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
```

---

## Symbolic Code Operations

Serena provides powerful code analysis:

### Get File Overview

```python
# Get symbols in a file (classes, functions, methods)
get_symbols_overview("src/graph.py", depth=1)
```

### Find Specific Symbols

```python
# Find a class or function
find_symbol("AgentState", include_body=True)

# Find method in class
find_symbol("AgentState/messages", include_body=True)
```

### Find References

```python
# Find all usages of a symbol
find_referencing_symbols("planner_node", relative_path="src/nodes/planner.py")
```

### Replace Symbol Body

```python
# Replace entire function/method
replace_symbol_body(
    name_path="planner_node",
    relative_path="src/nodes/planner.py",
    body="""def planner_node(state: AgentState) -> dict:
    \"\"\"Updated planner node.\"\"\"
    model = get_model_for_node("planner")
    # ... new implementation
    return {"messages": [response]}"""
)
```

### Insert Code

```python
# Insert after a symbol
insert_after_symbol(
    name_path="planner_node",
    relative_path="src/nodes/planner.py",
    body="""

def helper_function():
    \"\"\"New helper.\"\"\"
    pass
"""
)
```

---

## Best Practices

### DO:
- Run onboarding for new projects
- Create memories for external API integrations
- Add memory references to CLAUDE.md
- Use symbolic operations instead of full file reads
- Name memories descriptively

### DON'T:
- Skip CLAUDE.md references
- Use generic memory names
- Read entire files when symbols suffice
- Delete memories without user request
- Forget to list memories when context needed

---

## Quick Reference

```python
# Onboarding
check_onboarding_performed()
onboarding()

# Memories
write_memory("name.md", content)
read_memory("name")
list_memories()
edit_memory("name.md", needle, repl, mode)
delete_memory("name.md")

# Code Analysis
get_symbols_overview(path, depth)
find_symbol(pattern, include_body)
find_referencing_symbols(name_path, relative_path)

# Code Editing
replace_symbol_body(name_path, relative_path, body)
insert_after_symbol(name_path, relative_path, body)
insert_before_symbol(name_path, relative_path, body)
replace_content(relative_path, needle, repl, mode)
```
