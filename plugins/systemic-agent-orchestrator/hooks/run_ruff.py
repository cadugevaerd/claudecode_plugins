#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Run ruff linting after Python file writes.
Non-blocking - reports issues but doesn't prevent writes.
"""
import json
import os
import shutil
import subprocess
import sys


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

        if not file_path.endswith('.py'):
            print(json.dumps({}))
            return

        # Check if file exists (it should after PostToolUse)
        if not os.path.exists(file_path):
            print(json.dumps({}))
            return

        # Check if ruff is available
        ruff_path = shutil.which("ruff")
        if not ruff_path:
            # Try with uv run
            try:
                result = subprocess.run(
                    ["uv", "run", "ruff", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    print(json.dumps({
                        "systemMessage": "Note: ruff not installed. Run 'uv add ruff --dev' for linting support."
                    }))
                    return
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(json.dumps({
                    "systemMessage": "Note: ruff not available. Run 'uv add ruff --dev' for linting."
                }))
                return

        # Run ruff check
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", file_path, "--output-format=concise"],
                capture_output=True,
                text=True,
                timeout=30
            )
        except FileNotFoundError:
            # Fallback to direct ruff call
            result = subprocess.run(
                ["ruff", "check", file_path, "--output-format=concise"],
                capture_output=True,
                text=True,
                timeout=30
            )

        if result.returncode != 0 and result.stdout.strip():
            issues = result.stdout.strip()
            issue_count = len(issues.split('\n'))

            output = {
                "systemMessage": f"""Ruff found {issue_count} issue(s) in {os.path.basename(file_path)}:

{issues}

Quick fixes:
  uv run ruff check --fix {file_path}

Or to fix all:
  uv run ruff check --fix ."""
            }
            print(json.dumps(output))
        else:
            print(json.dumps({}))

    except subprocess.TimeoutExpired:
        print(json.dumps({
            "systemMessage": "Warning: ruff check timed out."
        }))
    except Exception as e:
        print(json.dumps({
            "systemMessage": f"Warning: ruff check skipped: {str(e)}"
        }))


if __name__ == "__main__":
    main()
