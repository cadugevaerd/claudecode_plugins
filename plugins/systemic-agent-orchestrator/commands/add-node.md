---
description: Add a new LangGraph node with proper patterns to an existing agent project
argument-hint: "<node-name> <type:llm|defined> <purpose>"
allowed-tools:
  - mcp__plugin_serena_serena__read_file
  - mcp__plugin_serena_serena__replace_content
  - mcp__plugin_serena_serena__create_text_file
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__insert_after_symbol
  - mcp__plugin_serena_serena__get_symbols_overview
---

# Add LangGraph Node

Add a new node to an existing LangGraph agent project following the systemic pattern.

## Arguments

- `node-name`: Required. Name of the node (snake_case)
- `type`: Required. Either `llm` (uses model) or `defined` (no LLM, deterministic)
- `purpose`: Required. Brief description of what the node does

## Instructions

1. **Verify project structure** exists:
   - Check for `src/state.py`
   - Check for `src/graph.py`
   - Check for `config/models.yaml`

2. **If type is `llm`**:
   
   a. Add entry to `config/models.yaml`:
   ```yaml
   # ---------------------------------------------------------------------------
   # Node: {node_name}
   # {purpose}
   # ---------------------------------------------------------------------------
   {node_name}:
     model: "anthropic:claude-3-5-sonnet-20241022"
     temperature: 0.3
     max_tokens: 2048
   ```
   
   b. Create node file `src/nodes/{node_name}.py`:
   ```python
   """Node: {node_name} - {purpose}"""
   from langsmith import Client
   from ..state import AgentState
   from ..config import get_model_for_node

   client = Client()

   def {node_name}_node(state: AgentState) -> dict:
       """{purpose}"""
       model = get_model_for_node("{node_name}")
       prompt = client.pull_prompt("my-org/{node_name}-prompt")
       
       formatted = prompt.format(
           messages=state['messages'],
           context=state.get('context', {})
       )
       response = model.invoke(formatted)
       
       return {"messages": [response]}
   ```

3. **If type is `defined`**:
   
   Create node file `src/nodes/{node_name}.py`:
   ```python
   """Node: {node_name} - {purpose} (deterministic, no LLM)"""
   from ..state import AgentState

   def {node_name}_node(state: AgentState) -> dict:
       """{purpose} - deterministic step."""
       # Deterministic logic here
       result = process_data(state)
       
       return {"result": result}
   ```

4. **Update `src/nodes/__init__.py`**:
   - Add import for new node
   - Add to `__all__` list

5. **Update `src/graph.py`**:
   - Import the new node function
   - Add node to graph: `graph.add_node("{node_name}", {node_name}_node)`
   - Add appropriate edges (ask user where to connect)

6. **Update `src/state.py`** if new state fields are needed

7. **Create test** `tests/test_{node_name}.py`:
   ```python
   """Tests for {node_name} node."""
   import pytest
   from src.nodes.{node_name} import {node_name}_node
   from src.state import AgentState

   def test_{node_name}_node():
       state: AgentState = {
           "messages": [],
           "current_step": "",
           "context": {},
           "errors": []
       }
       result = {node_name}_node(state)
       assert "messages" in result or "result" in result
   ```

## Questions to Ask User

Before adding edges, ask:
1. Which node should come BEFORE this new node?
2. Which node should come AFTER this new node?
3. Is this node part of a conditional route? If so, what condition?

## Validation

Before completing:
- [ ] models.yaml updated (if LLM node)
- [ ] Node file created in `src/nodes/`
- [ ] Node exported in `src/nodes/__init__.py`
- [ ] Graph updated with new node and edges
- [ ] Test file created
- [ ] No Functional API patterns used
- [ ] Node file under 100 lines
