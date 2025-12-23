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
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny"
                },
                "systemMessage": f"""BLOCKED: File exceeds {MAX_LINES}-line limit.

File: {file_path}
Current lines: {line_count}
Maximum allowed: {MAX_LINES}

RECOMMENDATIONS - Split into smaller modules:

1. **Separate by concern:**
   - state.py - State definitions (TypedDict, Annotated fields)
   - nodes/ - Directory with individual node files
     - nodes/__init__.py
     - nodes/planner.py
     - nodes/executor.py
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

EXAMPLE structure:
```
src/
├── __init__.py
├── state.py          # ~30-50 lines
├── config.py         # ~50-80 lines
├── graph.py          # ~50-100 lines
├── nodes/
│   ├── __init__.py   # exports all nodes
│   ├── planner.py    # ~50-100 lines
│   ├── executor.py   # ~50-100 lines
│   └── reviewer.py   # ~50-100 lines
└── utils/
    ├── __init__.py
    └── helpers.py
```

Smaller files = better maintainability, testing, and code review."""
            }
            print(json.dumps(result))
            sys.exit(0)

        # Warning when approaching limit
        if line_count > WARNING_THRESHOLD:
            print(json.dumps({
                "systemMessage": f"Note: {file_path} has {line_count} lines (limit: {MAX_LINES}). Consider splitting soon."
            }))
        else:
            print(json.dumps({}))

    except Exception as e:
        print(json.dumps({
            "systemMessage": f"Warning: File size validation skipped: {str(e)}"
        }))


if __name__ == "__main__":
    main()
