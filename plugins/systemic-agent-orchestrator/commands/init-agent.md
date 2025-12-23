---
description: Initialize a new LangGraph agent project with correct structure and configurations
argument-hint: "<agent-name> [nodes]"
allowed-tools:
  - mcp__plugin_serena_serena__create_text_file
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__read_file
---

# Initialize Agent Project

Create a new LangGraph agent project following the systemic pattern with Graph API, models.yaml, and Langsmith integration.

## Arguments

- `agent-name`: Required. Name of the agent project (kebab-case)
- `nodes`: Optional. Comma-separated list of node names (default: planner,executor)

## Instructions

1. **Create directory structure**:
   ```
   {agent-name}/
   ├── config/
   │   └── models.yaml
   ├── src/
   │   ├── __init__.py
   │   ├── state.py
   │   ├── config.py
   │   ├── nodes/
   │   │   ├── __init__.py
   │   │   └── {node_name}.py  # for each node
   │   └── graph.py
   ├── tests/
   │   ├── __init__.py
   │   └── test_nodes.py
   ├── pyproject.toml
   └── README.md
   ```

2. **Create models.yaml** with entries for each specified node:
   - Use `anthropic:claude-3-5-sonnet-20241022` as default model
   - Set temperature 0.0 for planner/router nodes, 0.3 for others
   - Add comments explaining each node's purpose

3. **Create state.py** with AgentState TypedDict:
   - Include `messages: Annotated[list, add]`
   - Include `current_step: str`
   - Include `context: dict`
   - Include `errors: list[str]`

4. **Create config.py** with:
   - `load_models_config()` function
   - `get_model_for_node(node_name)` function
   - Support for all providers (anthropic, anthropic_bedrock, openai, google_genai, xai)

5. **Create node files** for each specified node:
   - Use models.yaml for configuration
   - Reference Langsmith prompts with placeholder names
   - Follow Graph API patterns
   - Keep under 50 lines per node

6. **Create graph.py** with StateGraph builder:
   - Import all nodes
   - Create graph with proper edges
   - Export compiled app

7. **Create pyproject.toml** with dependencies:
   ```toml
   [project]
   name = "{agent-name}"
   version = "0.1.0"
   requires-python = ">=3.11"
   dependencies = [
       "langgraph>=0.3",
       "langchain-anthropic>=0.3",
       "langchain-openai>=0.2",
       "langchain-google-genai>=2",
       "langchain-aws>=0.2",
       "langsmith>=0.2",
       "pyyaml>=6",
   ]

   [project.optional-dependencies]
   dev = ["ruff>=0.8", "pytest>=8", "pytest-cov>=6"]

   [tool.ruff]
   line-length = 100
   ```

8. **Create basic tests** for node functions

9. **Create README.md** with:
   - Project description
   - Setup instructions
   - How to run locally with `langgraph dev`
   - How to configure Langsmith prompts

## Output

After creation, display:
- Project structure tree
- Next steps checklist:
  - [ ] Create prompts in Langsmith for each node
  - [ ] Configure .env with API keys
  - [ ] Run `uv sync` to install dependencies
  - [ ] Run `langgraph dev` to test locally

## Validation

Before completing:
- [ ] No Functional API usage (@entrypoint, @task)
- [ ] No local prompts (all reference Langsmith)
- [ ] models.yaml is valid with all nodes
- [ ] All files under 500 lines
- [ ] All nodes have corresponding config in models.yaml
