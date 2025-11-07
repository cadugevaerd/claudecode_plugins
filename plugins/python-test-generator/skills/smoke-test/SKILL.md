---
name: smoke-test
description: Smoke testing expertise - critical functionality validation, test design patterns, pytest markers and CI integration. Use when designing smoke tests, validating builds, implementing quick validation suites, or setting up early-stage testing. Covers smoke vs integration tests, pytest-smoke plugin, and best practices for fast feedback loops.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Smoke Test - Build Verification Testing Expertise

Conhecimento especializado em smoke testing: o que é, quando usar, como implementar e melhores práticas para validação rápida de funcionalidades críticas.

## 📋 When to Use Me

Invoke this skill when you need to:

- **Design smoke test suites** - Determine what to test and how
- **Validate builds quickly** - Verify critical paths work
- **Implement pytest markers** - Set up `@pytest.mark.smoke` patterns
- **Configure CI pipelines** - Add smoke tests to PR validation
- **Choose test strategy** - Decide smoke vs integration vs unit
- **Debug failing builds** - Identify if core functionality broke
- **Optimize test execution** - Run smoke tests before expensive integration tests
- **Set up fail-fast mechanisms** - Halt on smoke test failures

**Trigger terms**: "smoke test", "build verification", "critical functionality", "quick validation", "sanity check", "basic integration test"

## 🎓 Core Knowledge

### What is Smoke Testing?

**Definition**: Smoke testing (Build Verification Testing) is a minimal set of tests that verify the most critical functions of an application work correctly. The term comes from hardware testing - if the device doesn't catch fire when turned on, it passes the "smoke test."

**Purpose**:

- ✅ Catch show-stopping defects early
- ✅ Verify build stability before running expensive tests
- ✅ Provide fast feedback (seconds to minutes, not hours)
- ✅ Validate deployment success in production
- ✅ Save resources by avoiding extensive testing on broken builds

### Smoke Tests vs Other Test Types

| Aspect | Smoke Tests | Integration Tests | Unit Tests |
|--------|-------------|-------------------|------------|
| **Scope** | Broad but shallow | Focused and deep | Isolated components |
| **Speed** | Very fast (\<1s/test) | Moderate (1-10s/test) | Fastest (\<0.1s/test) |
| **When** | After build/deploy | After smoke passes | During development |
| **Coverage** | Critical paths only | Module interactions | Individual functions |
| **Failure** | Build is broken | Feature may be broken | Unit logic error |

**Key insight**: Run smoke → integration → regression in sequence. If smoke fails, stop immediately.

### Core Principles

1. **Test critical paths only** - Login, homepage, core API endpoints
1. **Keep tests fast** - Each test should complete in \<1 second
1. **Fail fast** - Halt entire suite if any smoke test fails
1. **Run early and often** - Every build, every deployment
1. **Shallow validation** - Does it work? Not "does it work perfectly?"

### Pytest Marker Pattern

```python
import pytest

@pytest.mark.smoke
def test_critical_api_responds():
    """Verify API is reachable and returns 200."""
    response = requests.get("http://api.example.com/health")
    assert response.status_code == 200

@pytest.mark.smoke
def test_database_connection():
    """Verify database is accessible."""
    conn = get_db_connection()
    assert conn.is_connected()

@pytest.mark.smoke
def test_core_import():
    """Verify main module can be imported."""
    from myapp import core
    assert core is not None
```

**Execution**:

```bash
# Run only smoke tests
pytest -m smoke

# Run smoke tests with fail-fast
pytest -m smoke -x

# Run smoke tests first, then others
pytest -m smoke && pytest -m "not smoke"
```

### What to Include in Smoke Tests

✅ **Include**:

- Application starts without crashing
- Core imports don't fail
- Database/cache/external service connectivity
- Health check endpoints return 200
- Critical user flows complete (login, main action)
- Configuration loads correctly

❌ **Exclude**:

- Edge cases and error handling
- Detailed business logic validation
- Performance benchmarks
- Complex multi-step workflows
- UI/UX details

### Common Smoke Test Scenarios

**Web Applications**:

- Homepage loads (status 200)
- Login page accessible
- User can authenticate
- Main dashboard renders
- API health endpoint responds

**APIs**:

- Server responds to health check
- Authentication endpoints work
- Core CRUD operations return expected status codes
- Database connection established

**Data Pipelines**:

- Pipeline runs on empty/synthetic data
- All transformation steps execute
- Output schema matches expected structure

**CLI Tools**:

- Binary executes without error
- `--help` flag works
- Basic command completes successfully

## 📚 Reference Files

For detailed implementation patterns and examples:

- **PYTEST_PATTERNS.md** - Complete pytest-smoke plugin usage, markers, and CI integration
- **TEST_DESIGN.md** - How to design effective smoke test suites for different project types
- **CI_INTEGRATION.md** - GitHub Actions, GitLab CI, and other CI/CD smoke test workflows
- **EXAMPLES.md** - Real-world smoke test examples for web apps, APIs, and data pipelines

## 💡 Quick Examples

### Example 1: Basic Smoke Test Suite

```python
import pytest
from myapp import app, db

@pytest.mark.smoke
class TestSmoke:
    """Critical functionality validation."""

    def test_app_starts(self):
        """Application initializes without errors."""
        assert app is not None
        assert app.config['ENV'] == 'test'

    def test_db_connection(self):
        """Database is reachable."""
        assert db.session.execute("SELECT 1").scalar() == 1

    def test_health_endpoint(self, client):
        """Health check returns 200."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'ok'
```

### Example 2: pytest.ini Configuration

```ini
[pytest]
markers =
    smoke: Quick validation of critical functionality (run first)
    integration: Tests requiring external services
    slow: Tests that take >5 seconds

# Run smoke tests first by default
addopts = -m smoke --strict-markers
```

### Example 3: CI Integration (GitHub Actions)

```yaml
name: Test

on: [push, pull_request]

jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest

      # Run smoke tests first - fail fast if critical issues
      - name: Run smoke tests
        run: pytest -m smoke -x --tb=short

      # Only run full suite if smoke passes
      - name: Run full test suite
        if: success()
        run: pytest -m "not smoke"
```

## ✅ Quick Checklist

**Designing Smoke Tests**:

- [ ] Identified 5-10 critical functionality areas
- [ ] Each test completes in \<1 second
- [ ] Tests focus on "does it work?" not "is it perfect?"
- [ ] No complex setup or extensive mocking
- [ ] Tests are deterministic (no flakiness)

**Pytest Implementation**:

- [ ] Markers defined in `pytest.ini` or `pyproject.toml`
- [ ] `@pytest.mark.smoke` applied to critical tests
- [ ] Can run via `pytest -m smoke`
- [ ] Configured to fail fast (`-x` flag)

**CI Integration**:

- [ ] Smoke tests run before full suite
- [ ] Pipeline halts if smoke tests fail
- [ ] Fast feedback (\<2 minutes to results)
- [ ] Clear error messages on failure

## 🎯 Golden Rules

1. **5-10 tests maximum** - More than that, you're testing too much
1. **\<1 second per test** - Smoke tests must be fast
1. **Critical paths only** - Can the app do its main job?
1. **Run first, always** - Before any other test category
1. **Fail fast** - One failure = stop everything

______________________________________________________________________

**For detailed patterns and examples**, consult the reference files in this skill directory.
