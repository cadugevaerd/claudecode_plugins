#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Enforce 500-line limit per Python file.
Large files should be split into smaller, focused modules.
"""
import json
import sys

MAX_LINES = 500
WARNING_THRESHOLD = 400  # Warn when approaching limit


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

        if not file_path.endswith('.py'):
            print(json.dumps({}))
            return

        # Count lines
        lines = content.split('\n')
        line_count = len(lines)

        if line_count > MAX_LINES:
            reason = f"""BLOCKED: File exceeds {MAX_LINES}-line limit.

File: {file_path}
Current lines: {line_count}
Maximum allowed: {MAX_LINES}

RECOMMENDATIONS - Split into smaller modules:

1. **Separate by concern:**
   - state.py - State definitions (TypedDict, Annotated fields)
   - nodes/ - Directory with individual node files
   - graph.py - Graph builder only
   - utils.py - Utility functions
   - config.py - Configuration loading

2. **Extract shared logic:**
   - validators.py - Validation functions
   - integrations/ - External service clients
   - domain/ - Business logic

3. **Node file structure:**
   Each node file should contain:
   - Imports
   - Node function (< 50 lines ideally)
   - Helper functions if needed

Smaller files = better maintainability, testing, and code review."""

            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason
                }
            }
            print(json.dumps(result))
            sys.exit(0)

        # Warning when approaching limit (non-blocking)
        print(json.dumps({}))

    except Exception as e:
        print(json.dumps({}))


if __name__ == "__main__":
    main()
