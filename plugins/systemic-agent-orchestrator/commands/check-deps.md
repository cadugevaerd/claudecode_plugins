---
description: Check and verify MCP dependencies required by this plugin
argument-hint: ""
allowed-tools:
  - mcp__plugin_serena_serena__execute_shell_command
  - mcp__plugin_serena_serena__list_dir
---

# Check Plugin Dependencies

Verify all required MCP-enabled plugins and tools are installed and functional.

## Instructions

### 1. Check uv Installation
```bash
uv --version
```
If not found, display installation instructions:
```
Install uv:
  curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Check Python Version
```bash
python3 --version
```
Require Python 3.11+

### 3. Check Required MCP Plugins

List available MCP tools and check for:

**langchain-ecosystem-helper**:
- Tools: `mcp__langchain-docs__SearchDocsByLangChain`
- Purpose: LangGraph and LangChain documentation
- Install: `claude mcp add langchain-ecosystem-helper`

**aws-documentation-helper** (Phase 2):
- Tools: `mcp__aws-knowledge-mcp-server__aws___search_documentation`
- Purpose: AWS documentation and best practices
- Install: `claude mcp add aws-documentation-helper`

**serena**:
- Tools: `mcp__plugin_serena_serena__*`
- Purpose: Semantic code analysis and memories
- Install: Configure in settings.json

### 4. Check Langsmith Configuration
Check environment variables:
```bash
echo $LANGCHAIN_API_KEY
echo $LANGCHAIN_PROJECT
```

If not set, display:
```
Configure Langsmith:
  export LANGCHAIN_API_KEY="lsv2_..."
  export LANGCHAIN_PROJECT="my-project"
  export LANGCHAIN_TRACING_V2="true"
```

### 5. Check Ruff Installation
```bash
uv run ruff --version
```
If not found: `uv add ruff --dev`

## Output Format

```
=== Dependency Check ===

RUNTIME:
[OK] uv: 0.5.11
[OK] Python: 3.12.0

MCP PLUGINS:
[OK] langchain-ecosystem-helper
     Tools: SearchDocsByLangChain
     
[OK] serena
     Tools: read_file, create_text_file, find_symbol, ...

[MISSING] aws-documentation-helper
     Install: claude mcp add aws-documentation-helper
     Purpose: AWS documentation (needed for Phase 2)

ENVIRONMENT:
[OK] LANGCHAIN_API_KEY: Configured
[OK] LANGCHAIN_PROJECT: my-project

DEV TOOLS:
[OK] ruff: 0.8.4

=== Summary ===
Required: 3/3 OK
Optional: 1/2 OK

All core dependencies are available.
Phase 2 features require: aws-documentation-helper
```

## Recommendations

Based on missing dependencies:

1. **Missing MCP plugins**: Provide installation commands
2. **Missing env vars**: Provide export commands
3. **Missing dev tools**: Provide uv add commands
4. **All present**: Confirm ready status

## Notes

- This command is non-blocking (informational only)
- Run at session start via hook
- Run manually anytime with `/check-deps`
