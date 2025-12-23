---
description: "This skill activates when the user asks about models.yaml configuration, LLM configuration, model selection, temperature settings, provider configuration, or how to configure models for LangGraph nodes. Trigger on: 'configure model', 'models.yaml format', 'change temperature', 'add new model provider', 'model configuration'."
---

# models.yaml Configuration Guide

## Purpose

The `models.yaml` file centralizes ALL LLM configurations for your agent. This enables:
- Single source of truth for model configs
- Easy switching between providers
- Environment-specific configurations
- Clear documentation of node purposes
- No hardcoded model names in code

---

## File Location

Place `models.yaml` in your project root or `config/` directory:

```
my-agent/
├── config/
│   └── models.yaml
├── src/
│   └── graph.py
```

---

## Required Structure

```yaml
# models.yaml - LLM Configuration
# Each node that uses an LLM MUST be configured here

nodes:
  # ---------------------------------------------------------------------------
  # Node: planner
  # Orchestrates workflow decisions with deterministic routing
  # ---------------------------------------------------------------------------
  planner:
    model: "anthropic:claude-3-5-sonnet-20241022"
    temperature: 0.0
    max_tokens: 2048
    
  # ---------------------------------------------------------------------------
  # Node: executor
  # Performs actions and tool calls
  # ---------------------------------------------------------------------------
  executor:
    model: "anthropic_bedrock:anthropic.claude-3-sonnet-20240229-v1:0"
    temperature: 0.3
    max_tokens: 4096
    timeout: 60
    
  # ---------------------------------------------------------------------------
  # Node: reviewer
  # Validates and critiques outputs
  # ---------------------------------------------------------------------------
  reviewer:
    model: "openai:gpt-4o"
    temperature: 0.0
    max_tokens: 2048
```

---

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Format: `provider:model_name` |
| `temperature` | float | 0.0 to 1.0 |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_tokens` | int | Model default | Max output tokens |
| `top_p` | float | 1.0 | Nucleus sampling |
| `timeout` | int | 30 | Request timeout (seconds) |

---

## Valid Providers

| Provider | Example Model | Use Case |
|----------|---------------|----------|
| `anthropic` | `claude-3-5-sonnet-20241022` | Direct Anthropic API |
| `anthropic_bedrock` | `anthropic.claude-3-sonnet-20240229-v1:0` | AWS Bedrock |
| `openai` | `gpt-4o`, `gpt-4o-mini` | OpenAI API |
| `google_genai` | `gemini-1.5-pro` | Google AI |
| `xai` | `grok-beta` | xAI Grok |

---

## Loading Configuration

```python
import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_models_config() -> dict:
    """Load and cache models.yaml configuration."""
    config_path = Path(__file__).parent.parent / "config" / "models.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def get_model_for_node(node_name: str):
    """Get configured model for a specific node."""
    config = load_models_config()
    node_config = config['nodes'][node_name]
    
    provider, model_name = node_config['model'].split(':')
    temperature = node_config['temperature']
    max_tokens = node_config.get('max_tokens')
    
    if provider == 'anthropic':
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == 'anthropic_bedrock':
        from langchain_aws import ChatBedrockConverse
        return ChatBedrockConverse(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == 'openai':
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == 'google_genai':
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
    elif provider == 'xai':
        from langchain_xai import ChatXAI
        return ChatXAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
```

---

## Temperature Guidelines

| Temperature | Use Case | Example Nodes |
|-------------|----------|---------------|
| `0.0` | Deterministic, routing, classification | planner, router, validator |
| `0.1-0.3` | Structured outputs, code generation | executor, data_extractor |
| `0.4-0.7` | Creative tasks, writing | summarizer, content_writer |
| `0.8-1.0` | Highly creative (rarely used) | brainstormer |

---

## Environment Variations

For different environments, use separate files:

```
config/
├── models.yaml           # Default/development
├── models.prod.yaml      # Production
├── models.test.yaml      # Testing (cheaper models)
```

Load based on environment:

```python
import os
from pathlib import Path

def get_config_path() -> Path:
    env = os.getenv('ENVIRONMENT', 'development')
    base = Path(__file__).parent.parent / "config"
    
    if env == 'production':
        return base / "models.prod.yaml"
    elif env == 'test':
        return base / "models.test.yaml"
    return base / "models.yaml"
```

---

## Usage in Nodes

```python
from config import get_model_for_node
from langsmith import Client

client = Client()

def planner_node(state: AgentState) -> dict:
    """Planner node using models.yaml config."""
    # Model loaded from configuration
    model = get_model_for_node("planner")
    
    # Prompt from Langsmith
    prompt = client.pull_prompt("my-org/planner-prompt")
    
    formatted = prompt.format(
        messages=state['messages'],
        context=state.get('context', {})
    )
    
    response = model.invoke(formatted)
    return {"messages": [response]}
```

---

## Validation Rules (Enforced by Hooks)

1. **YAML syntax must be valid**
2. **Every node needs `model` and `temperature`**
3. **Model format must be `provider:model_name`**
4. **Provider must be valid** (anthropic, anthropic_bedrock, openai, google_genai, xai)
5. **Temperature must be 0.0-1.0**
6. **Comments required** for each node (description of purpose)

---

## DO and DON'T

### DO:
- Configure ALL nodes in models.yaml
- Add comments explaining each node's purpose
- Use appropriate temperature for the task
- Create environment-specific configs

### DON'T:
- Hardcode model names in Python code
- Hardcode temperature values
- Skip the models.yaml file
- Use models without configuration
