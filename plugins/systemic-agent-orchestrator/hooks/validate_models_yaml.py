#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Hook: Validate models.yaml structure and content.
Ensures all LLM configurations follow the required format.
"""
import json
import re
import sys

VALID_PROVIDERS = ['anthropic', 'anthropic_bedrock', 'openai', 'google_genai', 'xai']


def validate_models_yaml(content: str) -> tuple[bool, list[str], list[str]]:
    """Validate models.yaml content. Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    try:
        import yaml
        data = yaml.safe_load(content)
    except ImportError:
        return True, [], ["PyYAML not available, skipping validation"]
    except Exception as e:
        return False, [f"Invalid YAML syntax: {str(e)}"], []

    if not isinstance(data, dict):
        return False, ["models.yaml must be a YAML dictionary"], []

    if 'nodes' not in data:
        return False, ["Missing required 'nodes' top-level key"], []

    nodes = data.get('nodes', {})
    if not isinstance(nodes, dict):
        return False, ["'nodes' must be a dictionary"], []

    if len(nodes) == 0:
        return False, ["'nodes' dictionary is empty - add at least one node configuration"], []

    for node_name, config in nodes.items():
        if not isinstance(config, dict):
            errors.append(f"Node '{node_name}': config must be a dictionary")
            continue

        # Required: model
        if 'model' not in config:
            errors.append(f"Node '{node_name}': missing required 'model' field")
        else:
            model = config['model']
            if not isinstance(model, str):
                errors.append(f"Node '{node_name}': model must be a string")
            elif ':' not in model:
                errors.append(f"Node '{node_name}': model must be 'provider:model_name' format (got '{model}')")
            else:
                provider = model.split(':')[0]
                if provider not in VALID_PROVIDERS:
                    errors.append(f"Node '{node_name}': invalid provider '{provider}'. Valid providers: {', '.join(VALID_PROVIDERS)}")

        # Required: temperature
        if 'temperature' not in config:
            errors.append(f"Node '{node_name}': missing required 'temperature' field")
        else:
            temp = config['temperature']
            try:
                temp_val = float(temp)
                if not 0.0 <= temp_val <= 1.0:
                    errors.append(f"Node '{node_name}': temperature must be between 0.0 and 1.0 (got {temp_val})")
            except (ValueError, TypeError):
                errors.append(f"Node '{node_name}': temperature must be a number (got '{temp}')")

        # Optional: max_tokens (must be positive int if present)
        if 'max_tokens' in config:
            max_tokens = config['max_tokens']
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                errors.append(f"Node '{node_name}': max_tokens must be a positive integer")

        # Optional: timeout (must be positive int if present)
        if 'timeout' in config:
            timeout = config['timeout']
            if not isinstance(timeout, int) or timeout <= 0:
                errors.append(f"Node '{node_name}': timeout must be a positive integer")

    # Check for comments (warning only)
    if '#' not in content:
        warnings.append("Consider adding comments to explain each node's purpose")

    return len(errors) == 0, errors, warnings


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

        # Only validate models.yaml files
        if not file_path.endswith('models.yaml'):
            print(json.dumps({}))
            return

        is_valid, errors, warnings = validate_models_yaml(content)

        if not is_valid:
            providers_list = ', '.join(VALID_PROVIDERS)
            reason = f"""BLOCKED: Invalid models.yaml configuration.

Errors:
{chr(10).join(f'  - {e}' for e in errors)}

CORRECT FORMAT:
```yaml
# LLM Configuration for Agent Nodes
nodes:
  planner:
    model: "anthropic:claude-3-5-sonnet-20241022"
    temperature: 0.0
    max_tokens: 2048

  executor:
    model: "anthropic_bedrock:anthropic.claude-3-sonnet-20240229-v1:0"
    temperature: 0.3
    max_tokens: 4096
    timeout: 60
```

VALID PROVIDERS: {providers_list}
TEMPERATURE RANGE: 0.0 to 1.0

REQUIRED FIELDS per node:
  - model: "provider:model_name"
  - temperature: 0.0-1.0

OPTIONAL FIELDS:
  - max_tokens: positive integer
  - timeout: positive integer (seconds)
  - top_p: 0.0-1.0"""

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
        print(json.dumps({}))


if __name__ == "__main__":
    main()
