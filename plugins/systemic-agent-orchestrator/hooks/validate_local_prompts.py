#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Block local prompt definitions in Python code.
All prompts must be stored in Langsmith, not in code.
"""
import json
import re
import sys

# Patterns that indicate local prompt definitions
PROMPT_PATTERNS = [
    # ChatPromptTemplate with inline content (not just variable references)
    (r'ChatPromptTemplate\.from_template\s*\(\s*["\'](?:[^"\']{30,}|.*\\n.*)["\']',
     'Inline prompt in ChatPromptTemplate.from_template()'),

    # Multi-line system/user prompts in from_messages
    (r'ChatPromptTemplate\.from_messages\s*\(\s*\[\s*\(\s*["\'](?:system|user|assistant)["\'].*?["\'][^)]{50,}',
     'Inline messages in ChatPromptTemplate.from_messages()'),

    # Direct message content with substantial text
    (r'SystemMessage\s*\(\s*content\s*=\s*["\'][^"\']{50,}',
     'Inline SystemMessage content (long hardcoded prompt)'),

    (r'HumanMessage\s*\(\s*content\s*=\s*["\'][^"\']{50,}',
     'Inline HumanMessage content (long hardcoded prompt)'),

    # Prompt string constants
    (r'(?:SYSTEM_PROMPT|USER_PROMPT|PROMPT_TEMPLATE|ASSISTANT_PROMPT)\s*=\s*["\'\[]',
     'Hardcoded prompt constant'),

    # Triple-quoted strings with prompt indicators
    (r'["\'][\'"]{2}[\s\S]*?(?:You are|Your task|Instructions:|Please respond|Answer the|As an AI)[\s\S]*?["\'][\'"]{2}',
     'Multi-line prompt string with instruction keywords'),
]

# Allowed patterns (Langsmith integration)
ALLOWED_PATTERNS = [
    r'hub\.pull\s*\(',           # Langsmith hub pull
    r'client\.pull_prompt\s*\(',  # Langsmith client
    r'get_prompt_from_langsmith',  # Custom getter function
    r'langsmith.*prompt',          # Langsmith imports
    r'from\s+langsmith\s+import',  # Langsmith imports
    r'\.pull_prompt\(',            # Any pull_prompt call
]


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

        if not file_path.endswith('.py'):
            print(json.dumps({}))
            return

        # Check for Langsmith integration (allow if present)
        for allowed in ALLOWED_PATTERNS:
            if re.search(allowed, content, re.IGNORECASE):
                print(json.dumps({}))
                return

        violations = []
        for pattern, description in PROMPT_PATTERNS:
            if re.search(pattern, content, re.DOTALL | re.MULTILINE):
                violations.append(description)

        if violations:
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny"
                },
                "systemMessage": f"""BLOCKED: Local prompt definitions detected.

Violations found:
{chr(10).join(f'  - {v}' for v in violations)}

This project requires ALL prompts to be stored in Langsmith.

CORRECT PATTERN:
```python
from langsmith import Client

client = Client()
prompt = client.pull_prompt("your-org/your-prompt-name")

# Use the prompt
formatted = prompt.format(
    variable1="value1",
    variable2="value2"
)
response = model.invoke(formatted)
```

Or using LangChain Hub:
```python
from langchain import hub

prompt = hub.pull("your-org/your-prompt-name")
```

BENEFITS of Langsmith Prompts:
- Version control for prompts
- A/B testing capability
- Prompt analytics and monitoring
- Team collaboration without code changes
- Easy rollback to previous versions

Please move your prompts to Langsmith and reference them by name."""
            }
            print(json.dumps(result))
            sys.exit(0)

        print(json.dumps({}))

    except Exception as e:
        print(json.dumps({
            "systemMessage": f"Warning: Local prompt validation skipped: {str(e)}"
        }))


if __name__ == "__main__":
    main()
