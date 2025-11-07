---
description: Generate integration tests with VCR recording for Python projects
allowed-tools: [Read, Grep, Glob, Write, Edit, Bash]
model: claude-sonnet-4-5
argument-hint: TARGET_PATH [--coverage-threshold PERCENT]
---

# Create Integration Tests

Generate comprehensive integration tests for Python projects with VCR HTTP recording/replay, real API integration validation, and automated coverage tracking.

## 🎯 Objective

- Generate integration tests that validate real component interactions
- Implement VCR (pytest-recording) for deterministic HTTP replay
- Create fixtures and test configuration following project patterns
- Support LangChain/LangGraph integration testing with real LLM APIs
- Achieve specified coverage threshold (default: 80%)
- Ensure tests are CI/CD friendly (cassette validation)

## 🔧 Instructions

### 1. Analyze Target Code and Project Structure

1.1 **Read Target File/Module**

- Use `Read` to analyze the target code structure
- Identify functions, classes, and external dependencies
- Detect HTTP calls, LLM integrations, database connections
- Map external services requiring mocking or VCR recording

1.2 **Detect Test Framework Configuration**

- Use `Glob` to find `pytest.ini`, `pyproject.toml`, or `conftest.py`
- Use `Read` to analyze existing test patterns and fixtures
- Identify coverage configuration and thresholds
- Check for existing VCR configuration

1.3 **Validate Dependencies**

- Use `Grep` to search for imports: `pytest`, `pytest-recording`, `vcrpy`
- Check `pyproject.toml` or `requirements.txt` for test dependencies
- If missing: Add to TODO list to install dependencies

### 2. Classify Integration Test Patterns

Based on code analysis, select appropriate test patterns:

**Pattern A: VCR Recording for HTTP/LLM APIs**

- Use when: Code makes HTTP calls to external APIs (OpenAI, Anthropic, REST APIs)
- Benefits: Deterministic tests, no API costs in CI/CD, fast execution
- Record modes: `once`, `new_episodes`, `none`, `all`

**Pattern B: Database Integration Testing**

- Use when: Code interacts with databases (PostgreSQL, MongoDB, Redis)
- Strategies: In-memory databases, Docker containers, fixtures

**Pattern C: Multi-Service Integration**

- Use when: Code orchestrates multiple services
- Strategies: Test containers, mocking boundaries, partial integration

**Pattern D: LangChain/LangGraph Integration**

- Use when: Code uses LangChain chains or LangGraph workflows
- Strategies: VCR for LLM calls, trajectory validation, state persistence

### 3. Generate VCR Configuration (if needed)

3.1 **Create/Update conftest.py**

- Check if `conftest.py` exists in test directory
- Add VCR fixture configuration:

```python
import pytest

@pytest.fixture(scope="module")
def vcr_config():
    """Default VCR configuration for integration tests"""
    return {
        "filter_headers": ["authorization", "api-key", "x-api-key"],
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "cassette_library_dir": "tests/cassettes",
    }
```

3.2 **Configure Cassette Directory**

- Create `tests/cassettes/` directory if not exists
- Add `.gitignore` entry if cassettes should not be committed (sensitive data)
- Or commit cassettes for deterministic CI/CD

### 4. Generate Integration Test File

4.1 **Create Test File Structure**

- Name: `test_integration_[module_name].py`
- Location: `tests/integration/` or `tests/`
- Follow AAA pattern (Arrange-Act-Assert)

4.2 **Generate Test Cases**

For each integration point, create:

**Basic VCR Test:**

```python
import pytest

@pytest.mark.vcr()
def test_api_integration_basic():
    """Test: API call recorded and replayed correctly"""
    # Arrange
    from my_module import api_function

    # Act
    result = api_function(param="test")

    # Assert
    assert result["status"] == "success"
    assert "data" in result
```

**LangChain/LangGraph VCR Test:**

```python
@pytest.mark.vcr()
def test_langchain_agent_integration():
    """Test: LangChain agent with real LLM (VCR replay)"""
    # Arrange
    from my_agent import create_agent
    agent = create_agent()

    # Act
    result = agent.invoke({"input": "What's the capital of France?"})

    # Assert
    assert "Paris" in result["output"]
```

**Database Integration Test:**

```python
@pytest.fixture
def test_db():
    """Fixture: In-memory test database"""
    # Setup
    db = create_test_database()
    yield db
    # Teardown
    db.close()

def test_database_integration(test_db):
    """Test: Database operations work correctly"""
    # Arrange
    from my_module import save_data

    # Act
    result = save_data(test_db, {"key": "value"})

    # Assert
    assert result.id is not None
    assert test_db.query(...).count() == 1
```

4.3 **Add Docstrings**

- Every test: Clear description of scenario
- Format: `"""Test: [What is being tested]"""`

### 5. Generate Test Fixtures

5.1 **Create Reusable Fixtures**

- Identify common setup patterns
- Create fixtures in `conftest.py` for reuse
- Use appropriate scopes: `function`, `module`, `session`

```python
@pytest.fixture(scope="module")
def integration_config():
    """Shared configuration for integration tests"""
    return {
        "api_url": "https://api.example.com",
        "timeout": 30
    }
```

5.2 **Create Mock Data Fixtures**

- Generate realistic test data
- Use factories or builders for complex objects

### 6. Add Coverage Configuration

6.1 **Update pytest.ini or pyproject.toml**

```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "integration: Integration tests (deselect with '-m \"not integration\"')",
]
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]
```

6.2 **Add Coverage Thresholds**

- Use `--coverage-threshold` argument or default 80%
- Configure per-module thresholds if needed

### 7. Validate and Run Tests

7.1 **Validate Syntax**

- Use `Bash` to run: `uv run python -m pytest --collect-only tests/integration/`
- Check all tests are discovered correctly

7.2 **Run Tests (First Time - Record)**

- Use `Bash`: `uv run python -m pytest tests/integration/ --record-mode=once -v`
- This records HTTP cassettes on first run
- Verify cassettes created in `tests/cassettes/`

7.3 **Run Tests (Replay)**

- Use `Bash`: `uv run python -m pytest tests/integration/ -v`
- Tests use recorded cassettes (fast, deterministic)

7.4 **Check Coverage**

- Use `Bash`: `uv run python -m pytest tests/integration/ --cov --cov-report=term-missing`
- Verify coverage meets threshold

### 8. Generate CI/CD Recommendations

8.1 **Add CI/CD Instructions**

- Document how to run in CI: `pytest --record-mode=none`
- Ensure cassettes are committed or API keys available
- Add to test output as comments

## 📊 Formato de Saída

### Test File Created

```text
✅ Integration tests created successfully!

📁 Test file: tests/integration/test_integration_[module].py
🧪 Test cases: [X] generated
📼 VCR configuration: [ENABLED|DISABLED]
📊 Coverage target: [X]%

🔧 Test Patterns Used:
- [✓] VCR Recording for HTTP/LLM APIs
- [✓] Database integration with fixtures
- [ ] Multi-service integration

📝 Next Steps:
1. Install dependencies: uv add --dev pytest pytest-recording vcrpy
2. Run tests (record): uv run pytest tests/integration/ --record-mode=once -v
3. Run tests (replay): uv run pytest tests/integration/ -v
4. Check coverage: uv run pytest tests/integration/ --cov

💡 CI/CD Usage:
   pytest tests/integration/ --record-mode=none -v
```

### Coverage Report

```text
📊 Coverage Report:
---------- coverage: platform linux, python 3.12 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/module.py             45      5    89%   12-15, 34
tests/integration/...     30      0   100%
-----------------------------------------------------
TOTAL                     75      5    93%

✅ Coverage threshold met: 93% >= 80%
```

## ✅ Critérios de Sucesso

- [ ] Target code analyzed and integration points identified
- [ ] Appropriate test patterns selected (VCR, DB, multi-service)
- [ ] VCR configuration created in `conftest.py` (if needed)
- [ ] Integration test file generated with AAA pattern
- [ ] All test cases have clear docstrings
- [ ] Fixtures created for reusable setup
- [ ] Coverage configuration added/updated
- [ ] Tests validated with `--collect-only`
- [ ] First run executed with `--record-mode=once` (if VCR)
- [ ] Cassettes recorded in `tests/cassettes/` (if VCR)
- [ ] Replay run successful (deterministic)
- [ ] Coverage threshold achieved
- [ ] CI/CD instructions documented

## ❌ Anti-Patterns

### ❌ Erro 1: Not filtering sensitive headers in VCR

Do NOT record sensitive data in cassettes:

```python
# ❌ WRONG - API keys recorded in cassettes
@pytest.mark.vcr()  # No header filtering!
def test_api():
    response = requests.get("https://api.com", headers={"Authorization": "secret"})
```

```python
# ✅ CORRECT - Filter sensitive headers
@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization", "api-key", "x-api-key"],
        "record_mode": "once",
    }

@pytest.mark.vcr()
def test_api():
    response = requests.get("https://api.com", headers={"Authorization": "secret"})
```

### ❌ Erro 2: Using real databases without cleanup

Do NOT leave test data in production databases:

```python
# ❌ WRONG - No cleanup, pollutes database
def test_save_user():
    db = connect_to_production_db()  # Dangerous!
    user = create_user(db, "test@example.com")
    assert user.id is not None
    # No cleanup!
```

```python
# ✅ CORRECT - Use test database with cleanup
@pytest.fixture
def test_db():
    db = create_in_memory_db()  # Or test container
    yield db
    db.drop_all()  # Cleanup

def test_save_user(test_db):
    user = create_user(test_db, "test@example.com")
    assert user.id is not None
```

### ❌ Erro 3: Incorrect VCR record mode in CI/CD

Do NOT use `record_mode=all` in CI/CD:

```bash
# ❌ WRONG - CI tries to record, fails without API keys
pytest tests/integration/ --record-mode=all
```

```bash
# ✅ CORRECT - CI uses existing cassettes only
pytest tests/integration/ --record-mode=none
```

### ❌ Erro 4: Testing too many components at once

Do NOT create mega-integration tests:

```python
# ❌ WRONG - Tests entire system, hard to debug
def test_entire_application():
    # 50 lines of setup
    # Tests database + API + cache + queue + email
    # If fails, which component broke?
```

```python
# ✅ CORRECT - Test specific integration points
def test_api_to_database_integration():
    """Test: API correctly saves to database"""
    # Focused integration test

def test_queue_to_email_integration():
    """Test: Queue triggers email correctly"""
    # Another focused integration test
```

### ❌ Erro 5: Not using AAA pattern

Do NOT write unstructured tests:

```python
# ❌ WRONG - No structure, hard to understand
def test_something():
    x = create_agent()
    result = x.invoke({"input": "test"})
    y = result["output"]
    assert "Paris" in y
```

```python
# ✅ CORRECT - Clear AAA structure
def test_agent_answers_question():
    """Test: Agent answers geography question correctly"""
    # Arrange
    agent = create_agent()
    question = {"input": "What's the capital of France?"}

    # Act
    result = agent.invoke(question)

    # Assert
    assert "Paris" in result["output"]
```

## 📝 Exemplos

### Exemplo 1: Generate integration tests for LangChain module

```bash
/create-integration-test src/agents/rag_agent.py
```

**O que acontece:**

1. Analisa `rag_agent.py` e detecta LangChain/LLM calls
1. Cria `tests/integration/test_integration_rag_agent.py`
1. Configura VCR para gravar chamadas LLM
1. Gera testes com `@pytest.mark.vcr()`
1. Cria fixtures em `conftest.py`
1. Executa testes (primeira vez grava cassettes)
1. Valida coverage >= 80%

### Exemplo 2: Integration tests with custom coverage threshold

```bash
/create-integration-test src/services/api_client.py --coverage-threshold 90
```

**O que acontece:**

1. Analisa `api_client.py` (HTTP client)
1. Detecta chamadas HTTP externas
1. Configura VCR com filtros de headers sensíveis
1. Gera testes com diferentes record modes
1. Define threshold de 90% (ao invés de 80%)
1. Valida coverage >= 90%

### Exemplo 3: Database integration tests

```bash
/create-integration-test src/repositories/user_repo.py
```

**O que acontece:**

1. Analisa `user_repo.py` e detecta database calls
1. Cria fixtures para database de teste
1. Gera testes com setup/teardown
1. Usa in-memory database ou test containers
1. Valida transações e rollback
1. Verifica coverage >= 80%
