# Pytest Patterns for Smoke Testing

Comprehensive guide to implementing smoke tests using pytest markers, plugins, and best practices.

## Pytest Marker Basics

### Defining Markers

**Method 1: pytest.ini**

```ini
[pytest]
markers =
    smoke: Quick validation of critical functionality (run first)
    integration: Tests requiring external services
    slow: Tests that take >5 seconds
    regression: Full regression suite

# Optional: Run smoke by default
addopts = -m smoke
```

**Method 2: pyproject.toml**

```toml
[tool.pytest.ini_options]
markers = [
    "smoke: Quick validation of critical functionality",
    "integration: Tests requiring external services",
    "slow: Tests that take >5 seconds",
]
```

### Applying Markers

**Single marker**:

```python
import pytest

@pytest.mark.smoke
def test_api_health():
    response = requests.get("http://api/health")
    assert response.status_code == 200
```

**Multiple markers**:

```python
@pytest.mark.smoke
@pytest.mark.integration
def test_critical_external_service():
    """Both a smoke test AND integration test."""
    result = external_service.ping()
    assert result.is_ok()
```

**Class-level markers**:

```python
@pytest.mark.smoke
class TestCriticalFunctionality:
    """All tests in this class are smoke tests."""

    def test_app_starts(self):
        assert app is not None

    def test_db_connection(self):
        assert db.is_connected()
```

## Running Smoke Tests

### Basic Execution

```bash
# Run only smoke tests
pytest -m smoke

# Run everything EXCEPT smoke tests
pytest -m "not smoke"

# Run smoke OR integration
pytest -m "smoke or integration"

# Run smoke AND integration (tests with both markers)
pytest -m "smoke and integration"
```

### Advanced Options

```bash
# Fail fast - stop on first failure
pytest -m smoke -x

# Stop after N failures
pytest -m smoke --maxfail=3

# Verbose output
pytest -m smoke -v

# Show short traceback
pytest -m smoke --tb=short

# Run smoke tests in parallel (requires pytest-xdist)
pytest -m smoke -n auto
```

## pytest-smoke Plugin

The `pytest-smoke` plugin provides advanced smoke test selection strategies.

### Installation

```bash
pip install pytest-smoke
```

### Usage Modes

**First N tests**:

```bash
# Run first 10 tests (quick sanity check)
pytest --smoke-first 10
```

**Last N tests**:

```bash
# Run last 5 tests (recently added)
pytest --smoke-last 5
```

**Random N tests**:

```bash
# Run 10 random tests (sample validation)
pytest --smoke-random 10
```

**Marked tests**:

```bash
# Run tests marked as @pytest.mark.smoke
pytest --smoke-marked

# Halt on smoke test failure
pytest --smoke-marked --halt-on-smoke-test-failure
```

### Configuration

**pytest.ini**:

```ini
[pytest]
smoke_first = 10
smoke_last = 5
smoke_random = 15
halt_on_smoke_test_failure = true
```

## Combining with Fixtures

### Minimal Fixtures for Smoke Tests

```python
import pytest

@pytest.fixture(scope="session")
def app():
    """Minimal app instance for smoke tests."""
    from myapp import create_app
    return create_app(config="testing")

@pytest.fixture(scope="session")
def db_connection():
    """Shared DB connection for smoke tests."""
    conn = connect_to_db()
    yield conn
    conn.close()

@pytest.mark.smoke
def test_app_configured(app):
    """Smoke test using session-scoped fixture."""
    assert app.config['TESTING'] is True
```

### Skip Expensive Fixtures

```python
@pytest.fixture
def expensive_setup():
    """This fixture takes 10 seconds to set up."""
    pytest.skip("Skipping expensive setup for smoke tests")

@pytest.mark.smoke
def test_without_expensive_setup(expensive_setup):
    """This test will be skipped in smoke runs."""
    pass
```

## Organizing Smoke Tests

### Pattern 1: Dedicated Smoke Test File

```
tests/
├── test_smoke.py          # All smoke tests here
├── test_integration.py    # Integration tests
└── test_unit.py           # Unit tests
```

```python
# test_smoke.py
import pytest

@pytest.mark.smoke
class TestSmoke:
    def test_app_starts(self):
        ...

    def test_db_connection(self):
        ...

    def test_api_health(self):
        ...
```

### Pattern 2: Mixed Files with Markers

```
tests/
├── test_api.py            # Contains smoke + integration tests
├── test_database.py       # Contains smoke + unit tests
└── test_auth.py           # Contains smoke + integration tests
```

```python
# test_api.py
import pytest

@pytest.mark.smoke
def test_api_responds():
    """Quick smoke test."""
    ...

@pytest.mark.integration
def test_api_full_workflow():
    """Detailed integration test."""
    ...
```

### Pattern 3: Nested Structure

```
tests/
├── smoke/
│   ├── test_core.py
│   ├── test_api.py
│   └── test_database.py
└── integration/
    ├── test_workflows.py
    └── test_external_services.py
```

## Parameterized Smoke Tests

```python
import pytest

@pytest.mark.smoke
@pytest.mark.parametrize("endpoint", [
    "/health",
    "/api/v1/status",
    "/api/v1/ping",
])
def test_critical_endpoints(client, endpoint):
    """Smoke test for multiple critical endpoints."""
    response = client.get(endpoint)
    assert response.status_code == 200
```

## Smoke Test Best Practices

### ✅ DO

```python
@pytest.mark.smoke
def test_app_imports():
    """Quick import test - no external dependencies."""
    from myapp import core, utils, models
    assert core and utils and models

@pytest.mark.smoke
def test_config_loads():
    """Verify configuration is valid."""
    from myapp import config
    assert config.DATABASE_URL is not None
    assert config.SECRET_KEY is not None

@pytest.mark.smoke
def test_db_ping(db_connection):
    """Minimal database validation."""
    result = db_connection.execute("SELECT 1").scalar()
    assert result == 1
```

### ❌ DON'T

```python
@pytest.mark.smoke
def test_complex_business_logic():
    """Too complex for smoke test."""
    # Creating 50 records
    # Running complex calculations
    # Validating edge cases
    # This should be an integration or unit test
    pass

@pytest.mark.smoke
def test_slow_external_api():
    """Too slow for smoke test (takes 5 seconds)."""
    response = requests.get("http://slow-api.com/data")
    # Process large response...
    # This should be integration test, not smoke
```

## CI/CD Integration Patterns

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run smoke tests
        run: |
          pytest -m smoke \
            -x \
            --tb=short \
            --maxfail=1 \
            --timeout=2

  full-suite:
    needs: smoke  # Only run if smoke passes
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run full test suite
        run: pytest
```

### GitLab CI

```yaml
stages:
  - smoke
  - test

smoke-tests:
  stage: smoke
  script:
    - pip install -e .[test]
    - pytest -m smoke -x --tb=short
  artifacts:
    reports:
      junit: smoke-report.xml

full-tests:
  stage: test
  needs: [smoke-tests]  # Depends on smoke passing
  script:
    - pip install -e .[test]
    - pytest --cov=myapp
```

## Reporting and Monitoring

### JUnit XML Output

```bash
# Generate JUnit report for CI
pytest -m smoke --junit-xml=smoke-report.xml
```

### HTML Report

```bash
# Requires pytest-html
pip install pytest-html

pytest -m smoke --html=smoke-report.html --self-contained-html
```

### Integration with Test Monitoring Tools

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: Quick validation of critical functionality"
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Log smoke test failures to monitoring service."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "smoke" in item.keywords:
            # Send alert - critical smoke test failed
            alert_monitoring_service(
                test_name=item.nodeid,
                error=str(report.longrepr),
            )
```

## Debugging Failed Smoke Tests

### Verbose Failure Output

```bash
# Show full traceback
pytest -m smoke -vv --tb=long

# Show local variables in traceback
pytest -m smoke -vv --tb=long --showlocals

# Drop into debugger on failure
pytest -m smoke --pdb
```

### Selective Re-runs

```bash
# Re-run only failed smoke tests
pytest -m smoke --lf  # last-failed

# Re-run failed, then all
pytest -m smoke --ff  # failed-first
```

## Performance Tuning

### Parallel Execution

```bash
# Requires pytest-xdist
pip install pytest-xdist

# Run smoke tests in parallel
pytest -m smoke -n auto
```

### Timeout Control

```bash
# Requires pytest-timeout
pip install pytest-timeout

# Fail tests that take >2 seconds
pytest -m smoke --timeout=2
```

### Minimal Output

```bash
# Quiet mode - only show failures
pytest -m smoke -q

# Ultra-minimal - just pass/fail counts
pytest -m smoke --quiet --no-header --no-summary
```

## Common Patterns Summary

| Pattern | Command | Use Case |
|---------|---------|----------|
| Basic smoke | `pytest -m smoke` | Run all smoke tests |
| Fail fast | `pytest -m smoke -x` | Stop on first failure |
| First N | `pytest --smoke-first 10` | Quick sanity check |
| With coverage | `pytest -m smoke --cov` | Measure smoke coverage |
| Parallel | `pytest -m smoke -n auto` | Speed up execution |
| CI report | `pytest -m smoke --junit-xml=report.xml` | CI integration |

______________________________________________________________________

**Next**: See TEST_DESIGN.md for designing effective smoke test suites.
