#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Block LangGraph Functional API usage.
Only Graph API (StateGraph) is allowed in this project.
"""
import json
import re
import sys

BLOCKED_PATTERNS = [
    (r'@entrypoint\b', 'Functional API @entrypoint decorator'),
    (r'@task\b', 'Functional API @task decorator'),
    (r'from\s+langgraph\.func\s+import', 'Functional API import'),
    (r'langgraph\.func\.entrypoint', 'Functional API entrypoint reference'),
    (r'langgraph\.func\.task', 'Functional API task reference'),
    (r'from\s+langgraph\.prebuilt\s+import\s+.*\bentrypoint\b', 'Functional API entrypoint import'),
]


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        # Get content being written
        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

        # Only check Python files
        if not file_path.endswith('.py'):
            print(json.dumps({}))
            return

        violations = []
        for pattern, description in BLOCKED_PATTERNS:
            if re.search(pattern, content):
                violations.append(description)

        if violations:
            reason = f"""BLOCKED: LangGraph Functional API usage detected.

Violations found:
{chr(10).join(f'  - {v}' for v in violations)}

This project ONLY allows Graph API (StateGraph). The Functional API is PROHIBITED.

CORRECT PATTERN - Use StateGraph:
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]

def my_node(state: AgentState) -> dict:
    # Node logic here
    return {{"messages": [...]}}

graph = StateGraph(AgentState)
graph.add_node("my_node", my_node)
graph.add_edge(START, "my_node")
graph.add_edge("my_node", END)
app = graph.compile()
```

WHY Graph API instead of Functional API:
- Full time-travel debugging support
- Explicit, predictable state management
- Battle-tested in production environments
- Better tooling and visualization support

Please rewrite using StateGraph instead of @entrypoint/@task decorators."""

            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason
                }
            }
            print(json.dumps(result))
            sys.exit(0)

        print(json.dumps({}))

    except Exception as e:
        # Non-blocking on error - allow operation to proceed
        print(json.dumps({}))


if __name__ == "__main__":
    main()
