# Designing Effective Smoke Test Suites

Step-by-step guide to designing smoke tests for different project types with real-world examples.

## Design Principles

### The 5-10 Rule

**Maximum 5-10 smoke tests per project**

- More than 10 = you're testing too much detail
- Fewer than 5 = you're missing critical paths
- Sweet spot: 7 tests covering core functionality

### The 1-Second Rule

**Each smoke test should complete in \<1 second**

- Fast feedback is critical
- If test takes >1s, it's not a smoke test
- Total suite should run in \<10 seconds

### The Critical Path Rule

**Only test what would make the app unusable if broken**

- Can users log in?
- Can the app start?
- Can it talk to critical services?
- Can it perform its primary function?

## Design Process

### Step 1: Identify Critical Functionality

Ask: "If this breaks, is the app completely unusable?"

**Web Application Example**:

- ✅ YES: User authentication
- ✅ YES: Homepage loads
- ✅ YES: Database connection
- ❌ NO: Profile picture upload
- ❌ NO: Email notifications
- ❌ NO: Advanced search filters

**API Example**:

- ✅ YES: Server responds to health check
- ✅ YES: Authentication works
- ✅ YES: Core CRUD endpoints return 200
- ❌ NO: Pagination works correctly
- ❌ NO: Advanced filtering
- ❌ NO: Rate limiting

### Step 2: Map to User Journeys

Identify the absolute minimum path users must complete:

**E-commerce**:

1. User can view homepage
1. User can search for products
1. User can add to cart
1. User can checkout (without payment processing details)

**SaaS Dashboard**:

1. User can log in
1. Dashboard loads with data
1. Primary action works (create project, send message, etc)

### Step 3: Create Test Inventory

**Template**:

```
Functionality: [What it tests]
Critical: [Yes/No]
Speed: [<1s, 1-3s, >3s]
Dependencies: [None, DB, External API, etc]
Include: [Yes/No in smoke suite]
```

**Example Inventory**:

```
| Functionality | Critical | Speed | Dependencies | Include |
|---------------|----------|-------|--------------|---------|
| App imports   | Yes      | <1s   | None         | ✅ Yes  |
| DB connection | Yes      | <1s   | DB           | ✅ Yes  |
| API health    | Yes      | <1s   | None         | ✅ Yes  |
| User login    | Yes      | <1s   | DB, Auth     | ✅ Yes  |
| Homepage      | Yes      | <1s   | DB           | ✅ Yes  |
| Profile edit  | No       | 2s    | DB, Storage  | ❌ No   |
| Email send    | No       | 3s    | External API | ❌ No   |
```

### Step 4: Implement Tests

Start with simplest tests first:

**Priority 1: No external dependencies**

```python
@pytest.mark.smoke
def test_app_imports():
    """Can import main modules?"""
    from myapp import core, utils
    assert core and utils
```

**Priority 2: Local dependencies (DB, cache)**

```python
@pytest.mark.smoke
def test_db_connection(db):
    """Can connect to database?"""
    assert db.execute("SELECT 1").scalar() == 1
```

**Priority 3: HTTP endpoints**

```python
@pytest.mark.smoke
def test_health_endpoint(client):
    """Health check responds?"""
    assert client.get("/health").status_code == 200
```

## Project Type Templates

### Web Application (Flask/Django)

```python
import pytest

@pytest.mark.smoke
class TestWebAppSmoke:
    """Critical functionality for web app."""

    def test_app_starts(self, app):
        """Application initializes."""
        assert app is not None
        assert app.config is not None

    def test_db_connection(self, db):
        """Database is accessible."""
        assert db.session.execute("SELECT 1").scalar() == 1

    def test_homepage_loads(self, client):
        """Homepage returns 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_login_page_loads(self, client):
        """Login page accessible."""
        response = client.get("/login")
        assert response.status_code == 200

    def test_user_can_authenticate(self, client, test_user):
        """Authentication system works."""
        response = client.post("/login", data={
            "username": test_user.username,
            "password": "password",
        })
        assert response.status_code in [200, 302]  # Success or redirect

    def test_api_health(self, client):
        """API health endpoint works."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json["status"] == "ok"
```

### REST API

```python
import pytest

@pytest.mark.smoke
class TestAPISmoke:
    """Critical API functionality."""

    def test_server_responds(self, api_client):
        """Server is reachable."""
        response = api_client.get("/")
        assert response.status_code in [200, 404]  # Responds, even if not found

    def test_health_check(self, api_client):
        """Health endpoint works."""
        response = api_client.get("/health")
        assert response.status_code == 200

    def test_authentication(self, api_client, auth_token):
        """Auth system functional."""
        response = api_client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200

    def test_core_list_endpoint(self, api_client, auth_token):
        """Main resource list works."""
        response = api_client.get(
            "/api/v1/items",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_core_create_endpoint(self, api_client, auth_token):
        """Can create main resource."""
        response = api_client.post(
            "/api/v1/items",
            json={"name": "test"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code in [200, 201]
```

### Data Pipeline

```python
import pytest

@pytest.mark.smoke
class TestPipelineSmoke:
    """Critical pipeline functionality."""

    def test_pipeline_imports(self):
        """Pipeline modules load."""
        from pipeline import extract, transform, load
        assert extract and transform and load

    def test_database_connection(self, db):
        """Source database accessible."""
        assert db.is_connected()

    def test_warehouse_connection(self, warehouse):
        """Data warehouse accessible."""
        assert warehouse.is_connected()

    def test_pipeline_runs_on_empty_data(self, pipeline):
        """Pipeline handles empty dataset."""
        result = pipeline.run(data=[])
        assert result.status == "success"

    def test_schema_validation(self, pipeline):
        """Output schema is correct."""
        result = pipeline.run(data=[{"id": 1}])
        assert "id" in result.schema
        assert result.schema["id"] == "integer"

    def test_critical_transformation(self, transformer):
        """Core transformation works."""
        input_data = [{"value": 10}]
        output = transformer.transform(input_data)
        assert len(output) > 0
```

### CLI Application

```python
import pytest
from click.testing import CliRunner

@pytest.mark.smoke
class TestCLISmoke:
    """Critical CLI functionality."""

    def test_cli_imports(self):
        """CLI module loads."""
        from myapp import cli
        assert cli is not None

    def test_help_command(self, cli_runner):
        """--help flag works."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output

    def test_version_command(self, cli_runner):
        """--version flag works."""
        result = cli_runner.invoke(cli, ["--version"])
        assert result.exit_code == 0

    def test_main_command_executes(self, cli_runner):
        """Primary command runs."""
        result = cli_runner.invoke(cli, ["process", "--dry-run"])
        assert result.exit_code == 0

    def test_config_loads(self, cli_runner):
        """Configuration file loads."""
        result = cli_runner.invoke(cli, ["config", "show"])
        assert result.exit_code == 0
```

### Microservice

```python
import pytest

@pytest.mark.smoke
class TestMicroserviceSmoke:
    """Critical microservice functionality."""

    def test_service_starts(self, service):
        """Service initializes."""
        assert service.is_running()

    def test_health_endpoint(self, client):
        """Health check works."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"

    def test_readiness_check(self, client):
        """Readiness endpoint works."""
        response = client.get("/ready")
        assert response.status_code == 200

    def test_database_connectivity(self, service):
        """Database is reachable."""
        assert service.db.is_connected()

    def test_cache_connectivity(self, service):
        """Cache is reachable."""
        assert service.cache.ping()

    def test_message_queue_connectivity(self, service):
        """Message queue is reachable."""
        assert service.queue.is_connected()

    def test_core_message_processing(self, service):
        """Can process basic message."""
        message = {"type": "test", "data": {}}
        result = service.handle_message(message)
        assert result.success is True
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Testing Too Much Detail

**Bad**:

```python
@pytest.mark.smoke
def test_user_profile_complete_workflow():
    """Too detailed for smoke test."""
    user = create_user()
    login(user)
    update_profile(user, avatar=..., bio=..., social_links=...)
    verify_email(user)
    enable_2fa(user)
    # This is an integration test, not smoke
```

**Good**:

```python
@pytest.mark.smoke
def test_user_can_login():
    """Just verify login works."""
    response = client.post("/login", data={"user": "test", "pass": "test"})
    assert response.status_code in [200, 302]
```

### ❌ Anti-Pattern 2: Slow External Dependencies

**Bad**:

```python
@pytest.mark.smoke
def test_payment_gateway_integration():
    """Too slow - real API call takes 3-5 seconds."""
    payment = PaymentGateway().charge(amount=100)
    assert payment.success
```

**Good**:

```python
@pytest.mark.smoke
def test_payment_module_imports():
    """Just verify module loads."""
    from myapp.payments import PaymentGateway
    assert PaymentGateway is not None
```

### ❌ Anti-Pattern 3: Edge Cases

**Bad**:

```python
@pytest.mark.smoke
def test_api_handles_malformed_json():
    """Edge case - not critical for smoke."""
    response = client.post("/api/items", data="not valid json")
    assert response.status_code == 400
```

**Good**:

```python
@pytest.mark.smoke
def test_api_accepts_valid_request():
    """Happy path only for smoke."""
    response = client.post("/api/items", json={"name": "test"})
    assert response.status_code in [200, 201]
```

## Decision Tree: Is This a Smoke Test?

```
Is this functionality CRITICAL to the app?
├─ No → Not a smoke test
└─ Yes → Does it take <1 second to run?
    ├─ No → Not a smoke test (consider mocking)
    └─ Yes → Does it test a happy path?
        ├─ No → Not a smoke test (edge cases = integration)
        └─ Yes → Does it require complex setup?
            ├─ Yes → Not a smoke test (too complex)
            └─ No → ✅ This is a smoke test!
```

## Maintenance and Evolution

### When to Add Smoke Tests

- New critical feature deployed
- Production incident revealed missing validation
- Core dependency added (new database, cache, etc)

### When to Remove Smoke Tests

- Feature is deprecated
- Test becomes flaky
- Test takes >1 second consistently
- Functionality no longer critical

### Regular Review

**Quarterly review checklist**:

- [ ] All smoke tests still complete in \<1s?
- [ ] All smoke tests still cover critical functionality?
- [ ] Any new critical features need smoke tests?
- [ ] Any tests can be moved to integration suite?

## Summary Template

Use this template to design your smoke suite:

```python
# test_smoke.py
"""
Smoke Test Suite

Critical functionality validation:
1. [Test 1 description] - [Why critical]
2. [Test 2 description] - [Why critical]
3. [Test 3 description] - [Why critical]
...

Total expected runtime: [X seconds]
Last reviewed: [Date]
"""

import pytest

@pytest.mark.smoke
class TestSmoke:
    def test_1(self):
        """[What it validates]."""
        pass

    def test_2(self):
        """[What it validates]."""
        pass

    # ... max 10 tests
```

______________________________________________________________________

**Next**: See CI_INTEGRATION.md for CI/CD pipeline integration patterns.
