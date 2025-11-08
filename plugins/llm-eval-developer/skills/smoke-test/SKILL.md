---
name: smoke-test
description: Smoke testing expertise - critical functionality validation, test design patterns, pytest markers and CI integration. Use when designing smoke tests, validating builds, implementing quick validation suites, or setting up early-stage testing for fast feedback loops.
version: 1.0.0
allowed-tools: Task, Write, Read, Bash
---

# Smoke Test

Especializada em smoke testing - validação rápida de funcionalidade crítica com pytest e CI/CD integration.

## 📋 When to Use Me

Use this skill when you need to:

- **Design smoke test suites** for quick validation
- **Setup pytest markers** for test categorization
- **Implement fast feedback loops** in CI/CD
- **Validate builds** before full test suite
- **Create quick validation tests** for critical paths
- **Setup CI/CD with smoke tests** for speed

Gatilhos para auto-invocação:

- "smoke test"
- "quick validation"
- "fast test suite"
- "CI smoke tests"
- "build validation"

## 🎓 Core Knowledge

### Smoke Testing Fundamentals

**Purpose**: Validate that critical functionality works without running full test suite.

**Characteristics**:

- ✅ Fast execution (< 1 minute for suite)
- ✅ Tests critical happy paths
- ✅ Broad coverage, not deep
- ✅ Early warning for major issues
- ✅ Suitable for pre-commit and CI gates

### Smoke vs Integration Tests

| Aspect | Smoke | Integration |
|--------|-------|-------------|
| **Speed** | Very fast | Slower |
| **Scope** | Critical paths | Full workflows |
| **Execution** | Quick gates | Full validation |
| **Frequency** | Every commit | Post-merge |
| **Example** | Can chain start? | Full request/response cycle |

### Test Design for Speed

**Fast Test Patterns**:

1. **Mock External Calls** - No API calls, no DB waits
1. **In-Memory Testing** - Use fixtures, not real resources
1. **Minimal Data** - Small datasets, focused scenarios
1. **Parallel Execution** - Run tests in parallel with pytest-xdist

**Slow Test Patterns to Avoid**:

- ❌ Real database calls
- ❌ Real API calls (use mocks)
- ❌ Large file operations
- ❌ Sleep/wait statements

### Pytest Markers for Organization

Standard markers for categorization:

```python
@pytest.mark.smoke          # Critical path validation
@pytest.mark.slow          # Long-running tests
@pytest.mark.integration   # Integration tests
@pytest.mark.unit          # Unit tests
@pytest.mark.skip_ci       # Skip in CI
```

### CI/CD Integration Strategy

**Stage 1: Pre-commit Smoke Tests**

- Run on developer machine
- Tests basic functionality
- Fast feedback (< 30 seconds)

**Stage 2: CI Smoke Tests**

- Run on every PR
- Validates basic build
- Gates for full test suite

**Stage 3: Full Test Suite**

- Run on merge to main
- Complete validation
- Full coverage check

## 📚 Reference Files

For detailed smoke test patterns and CI/CD setup, see:

- `SMOKE_TEST_PATTERNS.md` - Smoke test design patterns
- `PYTEST_MARKERS.md` - Pytest marker configuration
- `CI_WORKFLOW_SETUP.md` - GitHub Actions and CI/CD integration
- `PERFORMANCE_TUNING.md` - Optimizing test execution speed

## 💡 Quick Examples

### Example 1: Basic Smoke Test Suite

```python
import pytest
from my_app import create_chain

@pytest.mark.smoke
class TestChainSmoke:
    def test_chain_initializes(self):
        chain = create_chain()
        assert chain is not None

    def test_chain_basic_invocation(self):
        chain = create_chain()
        result = chain.invoke("test")
        assert result is not None

    def test_critical_tool_available(self):
        chain = create_chain()
        assert "search_tool" in chain.tools
```

### Example 2: CI/CD Smoke Test Configuration

```yaml
# .github/workflows/smoke-tests.yml
name: Smoke Tests

on: [pull_request, push]

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - run: pip install -r requirements.txt

      - name: Run smoke tests
        run: pytest -m smoke --timeout=10 -v

      - name: Report results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: smoke-test-results
          path: reports/
```

### Example 3: Pytest Marker Configuration

```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: critical path validation"
    )
    config.addinivalue_line(
        "markers", "slow: long-running tests"
    )

# Usage:
@pytest.mark.smoke
def test_critical_feature():
    pass

# Run only smoke tests:
# pytest -m smoke
```

### Example 4: Fast Mock-Based Test

```python
from unittest.mock import patch

@pytest.mark.smoke
@patch('my_app.expensive_api_call')
def test_with_mocked_external_call(mock_api):
    mock_api.return_value = {"status": "ok"}

    result = my_function()

    assert result["status"] == "ok"
    # Fast! No real API call
```

## 🔧 Key Concepts

### Smoke Test Checklist

✅ **What to Test**:

- Application startup
- Critical happy paths
- Main feature availability
- Error handling basics
- Core integrations (with mocks)

❌ **What NOT to Test**:

- Edge cases (save for integration tests)
- Complex workflows
- Performance characteristics
- Error recovery paths

### Performance Targets

```
Single smoke test:     < 500ms
Smoke suite (10 tests): < 5 seconds
CI smoke stage:        < 30 seconds
```

### Fixture Strategy for Speed

```python
@pytest.fixture
def fast_chain():
    """In-memory chain for smoke tests"""
    return MockChain()

@pytest.fixture(scope="session")
def shared_data():
    """Session-level fixture for reuse"""
    return load_minimal_dataset()
```

### Parallel Test Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -m smoke -n auto
```

______________________________________________________________________

**Integration**: Works with CI/CD pipelines and `/create-eval-suite` command
