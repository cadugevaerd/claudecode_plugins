# Serena MCP Helper

A Claude Code plugin that integrates [Serena MCP](https://github.com/oraios/serena) for symbolic code operations and persistent memory management.

## Features

- **Symbolic Code Navigation** - Work with functions, classes, and methods instead of full files
- **Token Savings** - Up to 70% reduction by reading only what you need
- **Persistent Memory** - Store and retrieve knowledge across sessions
- **Semantic Analysis** - LSP-powered code understanding
- **Enforcement Hooks** - Optionally block native tools for .py/.tf files

## Installation

1. Clone this plugin to your Claude Code plugins directory:
   ```bash
   cd ~/.claude/plugins
   git clone <repository-url> serena-mcp-helper
   ```

2. Ensure `uv` is installed (required for Serena):
   ```bash
   pip install uv
   # or
   pipx install uv
   ```

3. Restart Claude Code

## Commands

### `/serena-mcp-helper:init`
Initialize Serena for a new project. Runs onboarding and creates initial memories.

### `/serena-mcp-helper:memories`
List and manage project memories.

## Available Tools

Once the plugin is active, you have access to Serena MCP tools:

### Memory Operations

| Tool | Description |
|------|-------------|
| `initial_instructions` | Load Serena Instructions Manual (run first!) |
| `onboarding` | Auto-analyze project and create memories |
| `check_onboarding_performed` | Check if project was onboarded |
| `list_memories` | List all stored memories |
| `read_memory` | Read a specific memory |
| `write_memory` | Create/update a memory |
| `edit_memory` | Edit content in a memory |
| `delete_memory` | Delete a memory |

### Code Navigation

| Tool | Description |
|------|-------------|
| `get_symbols_overview` | Get symbols in a file (classes, functions) |
| `find_symbol` | Find a specific symbol by name |
| `find_referencing_symbols` | Find all usages of a symbol |
| `search_for_pattern` | Search with regex pattern |
| `list_dir` | List directory contents |
| `find_file` | Find files by name pattern |
| `read_file` | Read file content |

### Code Editing

| Tool | Description |
|------|-------------|
| `replace_symbol_body` | Replace entire function/method body |
| `insert_after_symbol` | Insert code after a symbol |
| `insert_before_symbol` | Insert code before a symbol |
| `replace_content` | Replace content using needle/replacement |
| `create_text_file` | Create a new file |
| `rename_symbol` | Rename a symbol across the codebase |

## Hook Enforcement (Optional)

The plugin includes hooks that can enforce Serena tool usage for Python and Terraform files:

- **SessionStart**: Reminds to load Serena Instructions Manual
- **PreToolUse**: Blocks native tools for .py/.tf files (suggests Serena alternatives)

To disable enforcement hooks, remove or rename the `hooks/hooks.json` file.

## Memory Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| API docs | `api_{service}_integration.md` | `api_stripe_integration.md` |
| Architecture | `arch_{component}_design.md` | `arch_state_machine.md` |
| Patterns | `pattern_{name}.md` | `pattern_retry_backoff.md` |
| Progress | `progress_{feature}.md` | `progress_auth_flow.md` |

## Quick Start

1. **Initialize Serena** (first time):
   ```
   /serena-mcp-helper:init
   ```

2. **Check memories**:
   ```
   list_memories()
   ```

3. **Store external API docs**:
   ```python
   write_memory("api_stripe_integration.md", """
   # Stripe Integration

   ## Endpoints
   - POST /v1/customers
   - POST /v1/payment_intents

   ## Authentication
   - Bearer token from SSM Parameter Store
   """)
   ```

4. **Navigate code symbolically**:
   ```python
   # Get overview
   get_symbols_overview("src/graph.py", depth=1)

   # Find specific function
   find_symbol("planner_node", include_body=True)

   # Replace implementation
   replace_symbol_body("planner_node", "src/nodes/planner.py", new_body)
   ```

## Integration with CLAUDE.md

After creating memories, add references to your project's CLAUDE.md:

```markdown
## Project Memories (Serena MCP)

### API Integrations
- `api_stripe_integration` - Payment API docs
  Use: `read_memory('api_stripe_integration')`

### Architecture
- `arch_state_machine` - Agent state design
  Use: `read_memory('arch_state_machine')`
```

## Requirements

- Python 3.10+
- `uv` package manager
- Claude Code with plugin support

## License

MIT
