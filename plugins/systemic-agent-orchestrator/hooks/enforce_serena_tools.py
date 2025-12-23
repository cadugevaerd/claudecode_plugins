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
    tool_input = os.environ.get("TOOL_INPUT", "{}")
    tool_name = os.environ.get("TOOL_NAME", "")

    # Tools to block completely
    blocked_tools = {"Write", "Edit", "Read", "MultiEdit", "Search", "Glob", "Grep"}

    try:
        input_data = json.loads(tool_input)
    except json.JSONDecodeError:
        input_data = {}

    # Check if it's a blocked native tool
    if tool_name in blocked_tools:
        file_path = input_data.get("file_path", "unknown")
        block_with_message(f"Tool '{tool_name}' bloqueada!", f"Arquivo: {file_path}")
        return

    # Check if it's a Bash command trying to write files
    if tool_name == "Bash":
        command = input_data.get("command", "")
        if BASH_WRITE_REGEX.search(command):
            block_with_message(
                "Comando Bash de escrita bloqueado!",
                f"Comando: {command[:100]}..."
            )
            return

    # Allow other tools/commands
    return


def block_with_message(title: str, context: str) -> None:
    """Print block message and exit."""
    serena_alternatives = """
**Alternativas Serena MCP:**

| Operacao | Tool Serena |
|----------|-------------|
| Ler arquivo | `mcp__plugin_serena_serena__read_file` |
| Criar/sobrescrever | `mcp__plugin_serena_serena__create_text_file` |
| Substituir texto | `mcp__plugin_serena_serena__replace_content` |
| Substituir simbolo | `mcp__plugin_serena_serena__replace_symbol_body` |
| Inserir apos simbolo | `mcp__plugin_serena_serena__insert_after_symbol` |
| Inserir antes simbolo | `mcp__plugin_serena_serena__insert_before_symbol` |
| Buscar simbolo | `mcp__plugin_serena_serena__find_symbol` |
| Overview simbolos | `mcp__plugin_serena_serena__get_symbols_overview` |
| Buscar arquivos | `mcp__plugin_serena_serena__find_file` |
| Buscar padrao/regex | `mcp__plugin_serena_serena__search_for_pattern` |
| Listar diretorio | `mcp__plugin_serena_serena__list_dir` |

**Por que usar Serena?**
- Edicao semantica baseada em simbolos (funcoes, classes, metodos)
- Melhor controle de contexto e menos tokens
- Refatoracao mais precisa com `replace_content` (suporta regex)
- Rename automatico com `rename_symbol`
"""

    result = {
        "decision": "block",
        "reason": f"{title}\n\n{context}\n{serena_alternatives}",
    }

    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
