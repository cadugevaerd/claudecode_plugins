#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Hook to validate Python LSP (Pyright) is installed on SessionStart.

Blocks if Pyright is not installed, providing installation instructions.
"""

import json
import shutil
import subprocess
import sys


def check_pyright_installed() -> tuple[bool, str]:
    """Check if Pyright is installed and get version."""
    # Check if pyright command exists
    pyright_path = shutil.which("pyright")
    if pyright_path:
        try:
            result = subprocess.run(
                ["pyright", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, version
        except Exception:
            pass

    # Check if pyright is available via npx
    npx_path = shutil.which("npx")
    if npx_path:
        try:
            result = subprocess.run(
                ["npx", "pyright", "--version"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"{version} (via npx)"
        except Exception:
            pass

    return False, ""


def main() -> None:
    """Validate Pyright LSP on SessionStart."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    # Only run on SessionStart event
    hook_event = input_data.get("hook_event_name", "")
    if hook_event != "SessionStart":
        print(json.dumps({}))
        return

    is_installed, version = check_pyright_installed()

    if not is_installed:
        reason = """=== Python LSP (Pyright) NOT INSTALLED ===

[ERROR] Pyright is required for Python code intelligence.

The LSP tool provides:
- Go to definition
- Find references
- Hover documentation
- Type checking
- Code navigation

INSTALLATION OPTIONS:

1. Via pipx (recommended):
   pipx install pyright

2. Via pip:
   pip install pyright

3. Via npm:
   npm install -g pyright

4. Via uv:
   uv tool install pyright

After installation, restart Claude Code to enable LSP features.

Run /systemic-agent-orchestrator:setup to auto-install."""

        result = {
            "decision": "block",
            "reason": reason
        }
        print(json.dumps(result))
        return

    # Pyright installed - pass silently
    print(json.dumps({}))


if __name__ == "__main__":
    main()
