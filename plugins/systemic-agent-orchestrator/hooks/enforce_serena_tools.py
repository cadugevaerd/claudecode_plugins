#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Hook to block native tools for .py and .tf files, enforcing Serena MCP tools."""

import json
import re
import sys

# File extensions that MUST use Serena tools
ENFORCED_EXTENSIONS = {".py", ".tf"}

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


def is_enforced_file(file_path: str) -> bool:
    """Check if file extension requires Serena tools."""
    if not file_path:
        return False
    return any(file_path.endswith(ext) for ext in ENFORCED_EXTENSIONS)


def extract_file_from_bash(command: str) -> str | None:
    """Extract target file from Bash write command."""
    # Match patterns like: > file.py, >> file.tf, tee file.py
    patterns = [
        r">\s*(\S+\.(?:py|tf))",      # > file.py or >> file.tf
        r"tee\s+(\S+\.(?:py|tf))",    # tee file.py
        r"cat\s*>\s*(\S+\.(?:py|tf))", # cat > file.py
    ]
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def main() -> None:
    """Block native tools for .py/.tf files, suggest Serena alternatives."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Allow if we can't parse input
        print(json.dumps({}))
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Extract file path from tool input
    file_path = tool_input.get("file_path", "") or tool_input.get("pattern", "")

    # Tools that operate on files
    file_tools = {"Read", "Write", "Edit", "MultiEdit"}
    
    # Search tools - only block if pattern explicitly targets .py/.tf
    search_tools = {"Search", "Glob", "Grep"}

    # Check file-based tools
    if tool_name in file_tools:
        if is_enforced_file(file_path):
            block_with_message(
                f"Tool '{tool_name}' bloqueada para arquivos .py/.tf!",
                f"Arquivo: {file_path}"
            )
            return
        # Allow for non-.py/.tf files
        print(json.dumps({}))
        return

    # Check search tools - only block if pattern explicitly targets .py/.tf
    if tool_name in search_tools:
        # Check if pattern explicitly targets .py or .tf files
        pattern = tool_input.get("pattern", "")
        if pattern.endswith(".py") or pattern.endswith(".tf") or \
           "*.py" in pattern or "*.tf" in pattern:
            block_with_message(
                f"Tool '{tool_name}' bloqueada para busca de arquivos .py/.tf!",
                f"Pattern: {pattern}"
            )
            return
        # Allow general searches
        print(json.dumps({}))
        return

    # Check Bash commands writing to .py/.tf files
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if BASH_WRITE_REGEX.search(command):
            target_file = extract_file_from_bash(command)
            if target_file and is_enforced_file(target_file):
                block_with_message(
                    "Comando Bash de escrita bloqueado para arquivos .py/.tf!",
                    f"Comando: {command[:100]}..."
                )
                return
        # Allow other Bash commands
        print(json.dumps({}))
        return

    # Allow all other tools
    print(json.dumps({}))


def block_with_message(title: str, context: str) -> None:
    """Print block message with proper hook format and exit."""
    serena_alternatives = """
**Alternativas Serena MCP (para .py e .tf):**

| Operacao | Tool Serena |
|----------|-------------|
| Ler arquivo | `mcp__plugin_serena_serena__read_file` |
| Overview simbolos | `mcp__plugin_serena_serena__get_symbols_overview` |
| Buscar simbolo | `mcp__plugin_serena_serena__find_symbol` |
| Buscar padrao/regex | `mcp__plugin_serena_serena__search_for_pattern` |
| Buscar arquivos | `mcp__plugin_serena_serena__find_file` |
| Listar diretorio | `mcp__plugin_serena_serena__list_dir` |
| Criar arquivo | `mcp__plugin_serena_serena__create_text_file` |
| Substituir conteudo | `mcp__plugin_serena_serena__replace_content` |
| Substituir simbolo | `mcp__plugin_serena_serena__replace_symbol_body` |
| Inserir apos simbolo | `mcp__plugin_serena_serena__insert_after_symbol` |
| Inserir antes simbolo | `mcp__plugin_serena_serena__insert_before_symbol` |

**Por que usar Serena para .py/.tf?**
- Busca semantica baseada em simbolos (funcoes, classes, metodos)
- Melhor controle de contexto e menos tokens
- Refatoracao precisa com edicao por simbolo
- Rename automatico com `rename_symbol`
"""

    reason = f"{title}\n\n{context}\n{serena_alternatives}"
    
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
