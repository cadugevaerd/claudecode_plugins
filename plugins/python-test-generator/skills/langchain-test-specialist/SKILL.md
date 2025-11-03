---
name: langchain-test-specialist
language: en
description: Creates unit and integration tests for LangChain and LangGraph applications with advanced mocking patterns. Use when testing LCEL chains, LangGraph workflows, agents, or validating LLM integrations with mocking and trajectory evaluation.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# LangChain Test Specialist

Expert in creating comprehensive unit and integration tests for **LangChain** and **LangGraph** applications with advanced patterns for LCEL chains, graph workflows, LLM mocking, and trajectory validation.

## What This Skill Does

Creates production-quality tests for LangChain/LangGraph applications including:

- LCEL chain testing with pipe operators (`|`)
- LangGraph state management and workflow testing
- Individual node-level testing and partial execution
- Advanced LLM mocking with `GenericFakeChatModel`
- Agent trajectory validation with `agentevals`
- LLM-as-judge evaluation for response quality
- HTTP recording/replay with VCR for deterministic integration tests

## When Claude Should Auto-Invoke This

✅ **Auto-invoke when you detect trigger terms**:

- User shows code with `from langchain` or `from langgraph` imports
- Mentions: "test", "unit test", "integration test", "coverage", "mock", "LLM"
- Specific triggers: "test chain", "test graph", "mock LLM", "write tests for agent", "validate trajectory"
- Technical terms: "LCEL", "pipe operator", "StateGraph", "LangGraph nodes", "GenericFakeChatModel"

✅ **Auto-invoke when user asks**:

- "How do I test this LangChain chain?"
- "Generate unit tests for my LangGraph workflow"
- "Write tests for LLM agent with trajectory validation"
- "Mock LLM calls in my tests"
- "Create integration tests with VCR recording"

## Instructions

### 1. Detect LangChain/LangGraph Context

When you detect code using:

- `from langchain...` or `from langgraph...` imports
- Classes: `StateGraph`, `MessageGraph`, `CompiledGraph`, `ChatOpenAI`, `ChatAnthropic`
- LCEL chains with pipe operator (`|`)
- Concepts: Nodes, edges, checkpointers, threads, trajectories

**Action**: Immediately select the most appropriate test pattern from the 7 patterns below.

### 2. Choose Appropriate Test Pattern

**For LangGraph workflows**:

- **Pattern 1 (State-based)**: Test full graph execution with state transformations
- **Pattern 2 (Node-level)**: Test individual nodes in isolation
- **Pattern 3 (Partial execution)**: Test interrupts and state injection for human-in-the-loop

**For LangChain chains**:

- **Pattern 4 (Mocking)**: Unit test chains with `GenericFakeChatModel` for determinism
- **Pattern 5 (Trajectory match)**: Validate agent action sequences with `agentevals`
- **Pattern 6 (LLM-as-judge)**: Use LLM to evaluate response quality

**For integration tests**:

- **Pattern 7 (VCR recording)**: Record real API calls on first run, replay in subsequent tests

### 3. Create Tests Following AAA (Arrange-Act-Assert)

All tests must follow this pattern for clarity:

````python
def test_feature():
    """Test: Clear scenario description"""
    # Arrange - Set up state, mocks, fixtures
    ...

    # Act - Execute function/chain/graph
    ...

    # Assert - Validate output
    ...

```text

### 4. Use Correct Pattern for Scenario

Analyze the code and user request, then apply one of the 7 patterns below.

## When to Use (Full Context)

Apply this skill automatically when you encounter:

- Code containing `langchain` or `langgraph` imports
- Requests to test conversational AI, chatbots, agents, workflows
- Questions about mocking LLMs or testing chains
- Mentions of LCEL, pipe operators, graphs, state management
- Trajectory validation or agent testing scenarios
- Integration testing with real LLM APIs

## Test Patterns

### Pattern 1: Basic LangGraph Test (State-based)

**When to use**: Test full graph execution with state transformations and checkpointing.

```python
import pytest
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict


def create_graph() -> StateGraph:
    """Factory para criar grafo de teste"""
    class MyState(TypedDict):
        my_key: str

    graph = StateGraph(MyState)
    graph.add_node("node1", lambda state: {"my_key": "hello"})
    graph.add_edge(START, "node1")
    graph.add_edge("node1", END)
    return graph


def test_basic_graph_execution():
    """Teste: Grafo executa corretamente com estado inicial"""
    # Arrange
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)

    # Act
    result = compiled_graph.invoke(
        {"my_key": "initial"},
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert
    assert result["my_key"] == "hello"

```text

**Apply when**:
- Testing full graph workflow end-to-end
- Validating state transformations across graph execution
- Verifying checkpointing and thread management

### Pattern 2: Individual Node Testing

**When to use**: Test individual nodes in isolation without full graph execution.

```python
def test_individual_node():
    """Teste: Node individual funciona sem dependências do grafo"""
    # Arrange
    graph = create_graph()
    compiled_graph = graph.compile()

    # Act
    result = compiled_graph.nodes["node1"].invoke({"my_key": "test"})

    # Assert
    assert result["my_key"] == "hello"


def test_node_with_dependencies():
    """Teste: Node processa dependências corretamente"""
    # Arrange
    def node_with_deps(state):
        return {"result": state["input"] * 2}

    graph = StateGraph(TypedDict("State", {"input": int, "result": int}))
    graph.add_node("processor", node_with_deps)
    compiled = graph.compile()

    # Act
    result = compiled.nodes["processor"].invoke({"input": 5})

    # Assert
    assert result["result"] == 10

```text

**Apply when**:
- Testing node-level logic in isolation
- Validating individual data transformations
- Debugging specific node issues without full graph context

### Pattern 3: Partial Execution (Interrupts)

**When to use**: Test graph interruption points and state injection for human-in-the-loop workflows.

```python
def test_partial_execution_with_interrupt():
    """Test: Graph execution stops at interrupt point"""
    # Arrange
    checkpointer = MemorySaver()

    class State(TypedDict):
        value: int

    def increment(state):
        return {"value": state["value"] + 1}

    graph = StateGraph(State)
    graph.add_node("node1", increment)
    graph.add_node("node2", increment)
    graph.add_node("node3", increment)
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", "node3")
    graph.add_edge("node3", END)

    compiled = graph.compile(checkpointer=checkpointer)

    # Act - Execute up to node2 (interrupt point)
    result = compiled.invoke(
        {"value": 0},
        config={"configurable": {"thread_id": "1"}},
        interrupt_after=["node2"]
    )

    # Assert - Stopped at node2, node3 not executed
    assert result["value"] == 2

    # Act - Resume execution
    final_result = compiled.invoke(
        None,
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert - Now node3 executed
    assert final_result["value"] == 3


def test_update_state_mid_execution():
    """Test: State can be modified during execution"""
    # Arrange
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled = graph.compile(checkpointer=checkpointer)

    # Act - Inject state as if executed by specific node
    compiled.update_state(
        config={"configurable": {"thread_id": "1"}},
        values={"my_key": "injected_value"},
        as_node="node1"
    )

    # Resume execution
    result = compiled.invoke(
        None,
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert
    assert result["my_key"] == "injected_value"

```text

**Apply when**:
- Testing human-in-the-loop workflows with user input
- Simulating workflow pauses and resumptions
- Injecting state to test specific execution paths

### Pattern 4: Mocking LLM (GenericFakeChatModel)

**When to use**: Unit test chains and nodes with LLMs without making actual API calls. Guarantees deterministic, fast tests with zero cost.

```python
from unittest.mock import Mock
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, ToolCall


def test_node_with_mocked_llm():
    """Test: Node with mocked LLM returns expected responses"""
    # Arrange - Mock LLM with predefined responses
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(content="Primeira resposta"),
        AIMessage(content="Segunda resposta")
    ]))

    def node_with_llm(state):
        response = mock_llm.invoke(state["messages"])
        return {"response": response.content}

    # Act
    result = node_with_llm({"messages": [{"role": "user", "content": "test"}]})

    # Assert
    assert result["response"] == "Primeira resposta"

    # Act - Segunda chamada
    result2 = node_with_llm({"messages": [{"role": "user", "content": "test2"}]})

    # Assert
    assert result2["response"] == "Segunda resposta"


def test_node_with_tool_calls():
    """Teste: Node com LLM que invoca tools"""
    # Arrange - Mock LLM retornando tool call
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(
            content="",
            tool_calls=[
                ToolCall(
                    name="search_tool",
                    args={"query": "test query"},
                    id="call_123"
                )
            ]
        ),
        AIMessage(content="Final response based on tool")
    ]))

    def agent_node(state):
        response = mock_llm.invoke(state["messages"])
        return {"tool_calls": response.tool_calls, "response": response.content}

    # Act - First call returns tool call
    result = agent_node({"messages": []})

    # Assert
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0].name == "search_tool"
    assert result["tool_calls"][0].args == {"query": "test query"}

    # Act - Second call returns final response
    result2 = agent_node({"messages": []})

    # Assert
    assert result2["response"] == "Final response based on tool"

```text

**Apply when**:
- Unit testing chains and graphs with LLMs
- Avoiding API costs in tests
- Guaranteeing deterministic responses
- Testing tool calling behavior

### Pattern 5: Trajectory Match Evaluator (AgentEvals)

**When to use**: Validate agent action sequences and tool calls match expected trajectory patterns.

```python
import pytest
from agentevals.trajectory.match import create_trajectory_match_evaluator
from langchain_core.messages import HumanMessage, AIMessage, ToolCall, ToolMessage


def test_trajectory_strict_match():
    """Test: Trajectory matches expected sequence exactly (strict mode)"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="strict"
    )

    # Expected trajectory
    reference_trajectory = [
        HumanMessage(content="What's the weather?"),
        AIMessage(content="", tool_calls=[
            ToolCall(name="weather_tool", args={"location": "NYC"}, id="1")
        ]),
        ToolMessage(content="Sunny, 75F", tool_call_id="1"),
        AIMessage(content="It's sunny and 75F in NYC")
    ]

    # Actual trajectory (identical)
    actual_trajectory = [
        HumanMessage(content="What's the weather?"),
        AIMessage(content="", tool_calls=[
            ToolCall(name="weather_tool", args={"location": "NYC"}, id="1")
        ]),
        ToolMessage(content="Sunny, 75F", tool_call_id="1"),
        AIMessage(content="It's sunny and 75F in NYC")
    ]

    # Act
    evaluation = evaluator(
        outputs=actual_trajectory,
        reference_outputs=reference_trajectory
    )

    # Assert
    assert evaluation["score"] is True


def test_trajectory_unordered_match():
    """Test: Trajectory contains same actions but different order (unordered mode)"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="unordered"
    )

    reference = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_a", args={}, id="1"),
            ToolCall(name="tool_b", args={}, id="2")
        ])
    ]

    # Different order
    actual = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_b", args={}, id="2"),
            ToolCall(name="tool_a", args={}, id="1")
        ])
    ]

    # Act
    evaluation = evaluator(outputs=actual, reference_outputs=reference)

    # Assert
    assert evaluation["score"] is True


def test_trajectory_subset_match():
    """Teste: Trajectory contém pelo menos as ações esperadas (subset mode)"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="subset"
    )

    # Esperado: pelo menos tool_a
    reference = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_a", args={}, id="1")
        ])
    ]

    # Actual: tool_a + tool_b (superset)
    actual = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_a", args={}, id="1"),
            ToolCall(name="tool_b", args={}, id="2")
        ])
    ]

    # Act
    evaluation = evaluator(outputs=actual, reference_outputs=reference)

    # Assert
    assert evaluation["score"] is True

```text

**Apply when**:
- Validating agent executed correct actions
- Testing tool call sequences
- Verifying agent behavior is deterministic
- Validating multi-step reasoning patterns

**Available modes**:
- `strict`: Order and content must match exactly
- `unordered`: Same content, order doesn't matter
- `subset`: Actual trajectory contains at least expected actions
- `superset`: Actual trajectory is subset of expected actions

### Pattern 6: LLM-as-Judge Evaluator

**When to use**: Use another LLM to evaluate response quality when exact matches aren't possible.

```python
from agentevals.trajectory.llm import (
    create_trajectory_llm_as_judge,
    TRAJECTORY_ACCURACY_PROMPT
)


def test_trajectory_accuracy_with_llm_judge():
    """Test: LLM evaluates if trajectory achieved goal correctly"""
    # Arrange
    evaluator = create_trajectory_llm_as_judge(
        model="openai:gpt-4o-mini",  # ou "anthropic:claude-3-5-sonnet"
        prompt=TRAJECTORY_ACCURACY_PROMPT
    )

    # Trajectory of agent that searched information correctly
    trajectory = [
        HumanMessage(content="Who won the 2023 World Series?"),
        AIMessage(content="", tool_calls=[
            ToolCall(name="search", args={"query": "2023 World Series winner"}, id="1")
        ]),
        ToolMessage(content="Texas Rangers won 2023 World Series", tool_call_id="1"),
        AIMessage(content="The Texas Rangers won the 2023 World Series")
    ]

    # Act
    evaluation = evaluator(outputs=trajectory)

    # Assert - LLM julga se resposta foi precisa
    assert evaluation["score"] is True
    assert "reasoning" in evaluation  # LLM explica decisão


@pytest.mark.asyncio
async def test_async_llm_judge():
    """Teste: LLM judge com execução assíncrona"""
    # Arrange
    evaluator = create_trajectory_llm_as_judge(
        model="openai:gpt-4o-mini",
        prompt=TRAJECTORY_ACCURACY_PROMPT
    )

    trajectory = [
        HumanMessage(content="What's 2+2?"),
        AIMessage(content="2+2 equals 4")
    ]

    # Act
    evaluation = await evaluator.ainvoke(outputs=trajectory)

    # Assert
    assert evaluation["score"] is True

```text

**Available prompts**:
- `TRAJECTORY_ACCURACY_PROMPT`: Evaluates if agent answered correctly
- Custom prompts: Define your own evaluation criteria

**Supported models**:
- `openai:gpt-4o-mini`, `openai:o3-mini`
- `anthropic:claude-3-5-sonnet`, `anthropic:claude-3-5-haiku`

**Apply when**:
- Evaluating agent response quality
- Validating agent achieved objective
- Tests where exact match isn't feasible
- Evaluating conversational quality or creativity

### Pattern 7: VCR Recording (HTTP Replay)

**When to use**: Record real LLM API calls on first run, replay in subsequent test runs for determinism without API costs.

```python
import pytest


@pytest.mark.vcr()
def test_agent_with_real_llm_vcr():
    """Test: Record real LLM calls on first run, replay in subsequent runs"""
    # FIRST EXECUTION:
    # - Makes real calls to LLM API
    # - Records requests/responses in cassette YAML
    #
    # SUBSEQUENT EXECUTIONS:
    # - Reads recorded cassette
    # - Replays responses without calling API
    # - Tests are 100% deterministic and fast

    # Arrange
    from my_agent import create_agent
    agent = create_agent()

    # Act
    result = agent.invoke({"input": "What's the capital of France?"})

    # Assert
    assert "Paris" in result["output"]


@pytest.mark.vcr(record_mode="once")
def test_agent_record_once():
    """Test: Record cassette once, fail if it doesn't exist in CI"""
    # record_mode="once": Records first time, error if cassette missing later
    # Useful for CI/CD - ensures cassettes are committed

    from my_agent import create_agent
    agent = create_agent()

    result = agent.invoke({"input": "Who wrote Hamlet?"})

    assert "Shakespeare" in result["output"]


@pytest.mark.vcr(record_mode="new_episodes")
def test_agent_record_new_episodes():
    """Test: Add new interactions to existing cassette"""
    # record_mode="new_episodes":
    # - Uses existing cassette for known interactions
    # - Records new interactions not yet in cassette
    # Useful when expanding tests

    from my_agent import create_agent
    agent = create_agent()

    # This call might already be in cassette
    result1 = agent.invoke({"input": "What's 2+2?"})
    assert result1["output"] == "4"

    # This is new, will be recorded
    result2 = agent.invoke({"input": "What's 3+3?"})
    assert "6" in result2["output"]

```text

**pytest-recording configuration**:

```python

# conftest.py
import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """Default VCR configuration"""
    return {
        "filter_headers": ["authorization", "api-key"],  # Remove sensitive headers
        "record_mode": "once",  # Default: record only once
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "cassette_library_dir": "tests/cassettes",  # Where to save cassettes
    }

```text

**Record modes**:
- `once`: Record once, error if cassette missing later
- `new_episodes`: Add new interactions to existing cassette
- `none`: Never record, replay only (fails if cassette missing)
- `all`: Always re-record cassette (useful for updates)

**Apply when**:
- Integration testing with real LLMs without CI/CD API costs
- Guaranteeing determinism in agent tests
- Debugging issues with specific API calls
- Testing different LLM models without API keys in CI

**Managing cassettes**:

```bash

# Re-record all cassettes
pytest --record-mode=all

# Re-record specific cassettes
pytest tests/test_agent.py --record-mode=all

# Validate cassettes exist (CI/CD)
pytest --record-mode=none

```text

## Dependencies

To use these patterns, ensure your project has:

```toml

# pyproject.toml
[tool.poetry.dependencies]
langchain = "^0.3.0"
langchain-core = "^0.3.0"
langgraph = "^0.2.0"

[tool.poetry.group.test.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
agentevals = "^0.1.0"  # For trajectory validation
vcrpy = "^6.0.0"  # For HTTP recording/replay
pytest-recording = "^0.13.0"  # pytest-vcr integration

```text

```bash

# pip/uv installation
pip install langchain langchain-core langgraph pytest pytest-asyncio agentevals vcrpy pytest-recording

```text

## Real-World Examples

### Example 1: Complete LangGraph Test Suite

```python
import pytest
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage


class AgentState(TypedDict):
    messages: Annotated[list, "Messages in conversation"]
    next_action: str


def create_agent_graph():
    """Factory: Cria grafo de agent"""
    graph = StateGraph(AgentState)

    def router(state):
        if len(state["messages"]) > 3:
            return {"next_action": "end"}
        return {"next_action": "continue"}

    def responder(state):
        return {
            "messages": state["messages"] + [
                AIMessage(content="Response")
            ]
        }

    graph.add_node("router", router)
    graph.add_node("responder", responder)
    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", lambda s: s["next_action"])
    graph.add_edge("responder", END)

    return graph


class TestAgentGraph:
    """Test suite for agent graph"""

    def test_graph_basic_execution(self):
        """Test: Graph executes basic flow"""
        # Arrange
        checkpointer = MemorySaver()
        graph = create_agent_graph()
        compiled = graph.compile(checkpointer=checkpointer)

        # Act
        result = compiled.invoke(
            {"messages": [HumanMessage(content="Hi")], "next_action": ""},
            config={"configurable": {"thread_id": "1"}}
        )

        # Assert
        assert result["next_action"] == "continue"

    def test_router_node_individually(self):
        """Test: Router node decides correctly"""
        # Arrange
        graph = create_agent_graph()
        compiled = graph.compile()

        # Act - Few messages
        result1 = compiled.nodes["router"].invoke({
            "messages": [HumanMessage(content="Test")],
            "next_action": ""
        })

        # Assert
        assert result1["next_action"] == "continue"

        # Act - Many messages
        result2 = compiled.nodes["router"].invoke({
            "messages": [HumanMessage(content=f"Msg {i}") for i in range(5)],
            "next_action": ""
        })

        # Assert
        assert result2["next_action"] == "end"

    def test_partial_execution_with_interrupt(self):
        """Test: Partial execution up to router"""
        # Arrange
        checkpointer = MemorySaver()
        graph = create_agent_graph()
        compiled = graph.compile(checkpointer=checkpointer)

        # Act
        result = compiled.invoke(
            {"messages": [HumanMessage(content="Test")], "next_action": ""},
            config={"configurable": {"thread_id": "1"}},
            interrupt_after=["router"]
        )

        # Assert - Stopped at router
        assert result["next_action"] == "continue"

```text

### Example 2: LangChain Chain with Mocked LLM

```python
from unittest.mock import Mock, patch
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate


def test_chain_with_pipe_operator_mocked():
    """Test: LCEL chain with pipe operator and mocked LLM"""
    # Arrange
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(content="Mocked response")
    ]))

    prompt = ChatPromptTemplate.from_template("Answer: {question}")
    chain = prompt | mock_llm

    # Act
    result = chain.invoke({"question": "What's 2+2?"})

    # Assert
    assert result.content == "Mocked response"


@patch("my_module.ChatOpenAI")
@patch("my_module.ChatPromptTemplate.from_template")
def test_chain_with_patch_mocking(mock_prompt, mock_chat):
    """Test: Chain with @patch mocking"""
    # Arrange - Mock chain com pipe operator
    mock_llm = Mock()
    mock_chain = Mock()
    mock_chain.invoke.return_value = AIMessage(content="Patched response")

    # Mock do pipe operator (|)
    mock_prompt.return_value.__or__ = Mock(return_value=mock_chain)
    mock_chat.return_value = mock_llm

    # Importar DEPOIS do patch
    from my_module import process_question

    # Act
    result = process_question("What's the weather?")

    # Assert
    assert "Patched response" in result
    mock_chain.invoke.assert_called_once()

```text

## Best Practices

### 1. Always Use Factories for Graphs

```python

# ✅ GOOD - Reusable factory
def create_graph() -> StateGraph:
    graph = StateGraph(MyState)
    # ... configuração
    return graph

def test_feature():
    graph = create_graph()
    compiled = graph.compile()

```text

```python

# ❌ BAD - Global graph
GRAPH = StateGraph(MyState)

# ... can cause shared state between tests

```text

### 2. Use MemorySaver for Checkpointer Tests

```python

# ✅ GOOD - In-memory checkpointer
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
compiled = graph.compile(checkpointer=checkpointer)

```text

```python

# ❌ BAD - Persistent checkpointer in tests
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver("test.db")  # Creates file, slow

```text

### 3. Mock LLMs for Unit Tests

```python

# ✅ GOOD - Deterministic mock
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

mock_llm = GenericFakeChatModel(messages=iter([
    AIMessage(content="Expected response")
]))

```text

```python

# ❌ BAD - Real LLM in unit test
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()  # Costs $$$, not deterministic

```text

### 4. Use VCR for Integration Tests

```python

# ✅ GOOD - Integration test with VCR
@pytest.mark.vcr()
def test_integration_with_real_api():
    # Records first time, replays after
    agent = create_agent()
    result = agent.invoke(...)

```text

### 5. Validate Trajectories with AgentEvals

```python

# ✅ GOOD - Structured validation
from agentevals.trajectory.match import create_trajectory_match_evaluator

evaluator = create_trajectory_match_evaluator(trajectory_match_mode="subset")
evaluation = evaluator(outputs=result, reference_outputs=expected)
assert evaluation["score"] is True

```text

```python

# ❌ BAD - Fragile manual validation
assert len(result["messages"]) == 4
assert result["messages"][1].tool_calls[0].name == "search"

# Fragile, breaks with small changes

```text

### 6. Test Individual Nodes First

```python

# ✅ GOOD - Test nodes in isolation first
def test_individual_node():
    graph = create_graph()
    compiled = graph.compile()
    result = compiled.nodes["my_node"].invoke(state)
    assert result["key"] == "expected"

def test_full_graph():
    # Then test full graph
    ...

```text

## Common Pitfalls

### ❌ Not using thread_id in checkpointer

```python

# ERROR - Missing thread_id
result = compiled.invoke({"key": "value"})

# CORRECT
result = compiled.invoke(
    {"key": "value"},
    config={"configurable": {"thread_id": "1"}}
)

```text

### ❌ Forgetting to compile graph

```python

# ERROR
graph = StateGraph(MyState)
result = graph.invoke(...)  # StateGraph is not invocable

# CORRECT
compiled = graph.compile()
result = compiled.invoke(...)

```text

### ❌ Incorrect pipe operator mocking

```python

# ERROR - Incomplete pipe mock
mock_prompt.return_value | mock_llm  # Doesn't work

# CORRECT
mock_prompt.return_value.__or__ = Mock(return_value=mock_chain)

```text

### ❌ Not installing test dependencies

```bash

# ERROR - Fails to import agentevals
pytest test_agent.py

# ModuleNotFoundError: No module named 'agentevals'

# CORRECT
pip install agentevals pytest-recording
pytest test_agent.py

```text

## Summary

This skill provides **7 complete test patterns** for LangChain/LangGraph:

1. **Basic LangGraph Test**: State-based testing with checkpointer
2. **Individual Node Testing**: Isolate and test individual nodes
3. **Partial Execution**: Graph interrupts and state injection
4. **Mocking LLM**: GenericFakeChatModel for deterministic unit tests
5. **Trajectory Match**: Validate agent action sequences (agentevals)
6. **LLM-as-Judge**: Use LLM to evaluate response quality
7. **VCR Recording**: Record/replay HTTP calls for integration tests

**Auto-invoke when**: Detecting LangChain, LangGraph, LCEL chains, graphs, agents, or requests to test LLMs.
````
