#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Verify that uv is installed and functioning.
This hook runs at session start to ensure the environment is properly configured.
"""
import json
import shutil
import subprocess
import sys


def main():
    try:
        # Check if uv is in PATH
        uv_path = shutil.which("uv")

        if not uv_path:
            result = {
                "systemMessage": """WARNING: uv is not installed or not in PATH.

The Systemic Agent Orchestrator plugin requires uv for Python dependency management.

INSTALL uv:
  curl -LsSf https://astral.sh/uv/install.sh | sh

Or with pipx:
  pipx install uv

After installation, restart your terminal and Claude Code session.

More info: https://docs.astral.sh/uv/"""
            }
            print(json.dumps(result))
            return

        # Verify uv works by getting version
        version_result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if version_result.returncode != 0:
            result = {
                "systemMessage": f"""WARNING: uv is installed but not functioning properly.

Error: {version_result.stderr}

Try reinstalling uv:
  curl -LsSf https://astral.sh/uv/install.sh | sh"""
            }
            print(json.dumps(result))
            return

        uv_version = version_result.stdout.strip()

        # Success - uv is installed and working
        result = {
            "systemMessage": f"""Systemic Agent Orchestrator initialized.
  Runtime: {uv_version}
  Guardrails: Graph API, Langsmith Prompts, models.yaml, 500-line limit"""
        }
        print(json.dumps(result))

    except subprocess.TimeoutExpired:
        print(json.dumps({
            "systemMessage": "Warning: uv version check timed out. Plugin may not function correctly."
        }))
    except Exception as e:
        print(json.dumps({
            "systemMessage": f"Warning: uv check error: {str(e)}"
        }))


if __name__ == "__main__":
    main()
