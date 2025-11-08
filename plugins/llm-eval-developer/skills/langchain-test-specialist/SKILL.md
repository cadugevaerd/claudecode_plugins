---
name: langchain-test-specialist
description: Create unit and integration tests for LangChain and LangGraph applications with advanced mocking patterns. Use when testing LCEL chains, LangGraph workflows, agents, or validating LLM integrations with comprehensive mocking strategies.
version: 1.0.0
allowed-tools: Task, Write, Read, Bash
---

# LangChain Test Specialist

Especializada em criar unit e integration tests para aplicações LangChain/LangGraph com padrões avançados de mocking.

## 📋 When to Use Me

Use this skill when you need to:

- **Test LCEL chains** without calling real LLMs
- **Mock LangChain components** effectively
- **Test LangGraph workflows** with state validation
- **Write integration tests** with VCR recording
- **Validate agent behavior** with tool mocking
- **Design test strategies** for LLM applications

Gatilhos para auto-invocação:

- "test langchain"
- "mock LLM"
- "unit test chain"
- "integration test langgraph"
- "test LLM agent"

## 🎓 Core Knowledge

### Testing Strategies for LLM Apps

**1. Unit Testing**

- Mock LLM calls with fake responses
- Test chain logic isolation
- Validate prompt formatting
- Test individual tools/functions

**2. Integration Testing**

- Record/replay with VCR
- Test full chain end-to-end
- Validate tool integration
- Test state management

**3. Behavioral Testing**

- Test agent decision making
- Validate tool selection
- Test error handling
- Validate output format

### Mocking Patterns

**Pattern 1: Mock LLM Response**

```python
from unittest.mock import patch, MagicMock

@patch('langchain_openai.ChatOpenAI')
def test_chain(mock_llm):
    mock_llm.return_value.invoke.return_value.content = "expected response"
    # Test chain behavior
```

**Pattern 2: Mock Tool Execution**

```python
@patch('my_tools.search_web')
def test_agent_with_tools(mock_search):
    mock_search.return_value = "search results"
    # Test agent behavior
```

**Pattern 3: Fixture-Based Testing**

```python
@pytest.fixture
def mock_chain():
    return create_test_chain(
        llm_responses={"query": "response"}
    )
```

### LangGraph Testing

Testing workflow states:

```python
def test_workflow_state_transition():
    # Create test input
    state = {"input": "test", "step": 1}

    # Execute node
    result = node_function(state)

    # Validate output state
    assert result["step"] == 2
    assert "output" in result
```

### VCR Integration Testing

Record HTTP interactions for replay:

```python
import vcr

@vcr.use_cassette('tests/fixtures/search_results.yaml')
def test_with_real_api():
    # First run: records API calls
    # Subsequent runs: replays from cassette
    response = call_external_api()
```

## 📚 Reference Files

For detailed testing patterns and configurations, see:

- `MOCKING_PATTERNS.md` - Advanced mocking strategies
- `LANGRAPH_TESTING.md` - State machine and workflow testing
- `VCR_SETUP.md` - Recording and replaying HTTP interactions
- `TEST_FIXTURES.md` - Creating reusable test fixtures

## 💡 Quick Examples

### Example 1: Simple Chain Test

```python
def test_qa_chain():
    # Mock the LLM
    with patch('langchain_openai.ChatOpenAI') as mock_llm:
        mock_llm.return_value.invoke.return_value = "answer"

        chain = create_qa_chain()
        result = chain.invoke({"question": "What is AI?"})

        assert "answer" in result
```

### Example 2: Agent with Tools Test

```python
@patch('tools.search_web')
@patch('tools.calculate')
def test_agent(mock_calc, mock_search):
    mock_search.return_value = "search results"
    mock_calc.return_value = 42

    result = run_agent("What is 2+2?")

    assert mock_calc.called
    assert result == "42"
```

### Example 3: LangGraph State Test

```python
def test_graph_workflow():
    graph = create_workflow_graph()

    state = {"input": "test", "processed": False}
    result = graph.invoke(state)

    assert result["processed"] is True
    assert "output" in result
```

## 🔧 Key Concepts

### Test Structure

Standard test file organization:

```python
import pytest
from unittest.mock import patch, MagicMock
from my_chain import create_chain

class TestChain:
    @pytest.fixture
    def chain(self):
        return create_chain()

    def test_basic_invocation(self, chain):
        # Test with mocks
        pass

    def test_error_handling(self, chain):
        # Test error scenarios
        pass
```

### Assertion Patterns

Common assertions for LLM apps:

```python
# Mock was called
assert mock_llm.called
assert mock_llm.call_count == 1

# Response format
assert isinstance(result, str)
assert len(result) > 0

# State transitions
assert result["status"] == "complete"
```

### Fixtures for Common Scenarios

```python
@pytest.fixture
def mock_responses():
    return {
        "greeting": "Hello!",
        "answer": "42",
        "error": Exception("API Error")
    }

@pytest.fixture
def test_dataset():
    return [
        {"input": "test", "expected": "output"},
    ]
```

______________________________________________________________________

**Integration**: Works with `/create-eval-suite` command and `evaluation-developer` skill
