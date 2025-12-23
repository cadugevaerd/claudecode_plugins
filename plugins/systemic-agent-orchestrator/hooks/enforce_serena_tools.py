#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Hook to block native Write/Edit/Read tools and Bash file writes, enforcing Serena MCP tools."""

import json
import os
import re
import sys

# Patterns that indicate Bash is being used to write files
BASH_WRITE_PATTERNS = [
    r"cat\s*>",           # cat > file
    r"cat\s+<<",          # cat << 'EOF' (heredoc)
    r"echo\s*>",          # echo > file
    r"printf\s*>",        # printf > file
    r"tee\s+",            # tee file
    r">\s*\S+",           # > file (redirect)
    r">>\s*\S+",          # >> file (append)
    r"sed\s+-i",          # sed -i (in-place edit)
    r"awk\s+-i",          # awk -i (in-place edit)
]

BASH_WRITE_REGEX = re.compile("|".join(BASH_WRITE_PATTERNS), re.IGNORECASE)


def main() -> None:
    """Block native file tools and Bash file writes, suggest Serena alternatives."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Allow if we can't parse input
        print(json.dumps({}))
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Tools to block for reading (force Serena semantic search)
    read_tools = {"Read", "Search", "Glob", "Grep"}
    
    # Tools to block for writing (force Serena symbolic editing)
    write_tools = {"Edit", "MultiEdit"}
    
    # Write tool - allow for new files, block for existing
    # (Serena can't create new files, only edit symbols)
    
    # Whitelisted file patterns for Write (documentation, config, etc.)
    write_whitelist = [
        "CLAUDE.md", "README.md", "LICENSE", 
        ".md", ".json", ".yaml", ".yml", ".toml",
        ".gitignore", ".env.example", "Makefile",
        "pyproject.toml", "requirements.txt"
    ]

    file_path = tool_input.get("file_path", "") or tool_input.get("pattern", "")

    # Check Write tool - allow whitelisted files
    if tool_name == "Write":
        if any(file_path.endswith(ext) for ext in write_whitelist):
            print(json.dumps({}))  # Allow
            return
        block_with_message(
            f"Tool 'Write' bloqueada para arquivos .py!",
            f"Arquivo: {file_path}\nUse Serena para edição semântica de código Python."
        )
        return

    # Check if it's a blocked read tool
    if tool_name in read_tools:
        block_with_message(
            f"Tool '{tool_name}' bloqueada para forçar busca semântica!",
            f"Arquivo/Pattern: {file_path}"
        )
        return

    # Check if it's a blocked write/edit tool
    if tool_name in write_tools:
        block_with_message(
            f"Tool '{tool_name}' bloqueada para forçar edição semântica!",
            f"Arquivo: {file_path}"
        )
        return

    # Check if it's a Bash command trying to write files
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if BASH_WRITE_REGEX.search(command):
            block_with_message(
                "Comando Bash de escrita bloqueado!",
                f"Comando: {command[:100]}..."
            )
            return

    # Allow other tools/commands
    print(json.dumps({}))


def block_with_message(title: str, context: str) -> None:
    """Print block message with proper hook format and exit."""
    serena_alternatives = """
**Alternativas Serena MCP:**

| Operacao | Tool Serena |
|----------|-------------|
| Overview simbolos | `mcp__plugin_systemic-agent-orchestrator_serena__get_symbols_overview` |
| Buscar simbolo | `mcp__plugin_systemic-agent-orchestrator_serena__find_symbol` |
| Buscar padrao/regex | `mcp__plugin_systemic-agent-orchestrator_serena__search_for_pattern` |
| Buscar arquivos | `mcp__plugin_systemic-agent-orchestrator_serena__find_file` |
| Listar diretorio | `mcp__plugin_systemic-agent-orchestrator_serena__list_dir` |
| Substituir simbolo | `mcp__plugin_systemic-agent-orchestrator_serena__replace_symbol_body` |
| Inserir apos simbolo | `mcp__plugin_systemic-agent-orchestrator_serena__insert_after_symbol` |
| Inserir antes simbolo | `mcp__plugin_systemic-agent-orchestrator_serena__insert_before_symbol` |

**Por que usar Serena?**
- Busca semantica baseada em simbolos (funcoes, classes, metodos)
- Melhor controle de contexto e menos tokens
- Refatoracao precisa com edicao por simbolo
- Rename automatico com `rename_symbol`
"""

    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny"
        },
        "systemMessage": f"{title}\n\n{context}\n{serena_alternatives}"
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
