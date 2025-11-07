# Real-World Smoke Test Examples

Complete smoke test suites for common project types with production-ready patterns.

## Example 1: FastAPI REST API

### Project Structure

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routers/
│   └── dependencies.py
└── tests/
    ├── conftest.py
    └── test_smoke.py
```

### conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Use in-memory SQLite for speed
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    """Session-scoped database for smoke tests."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(db):
    """Session-scoped test client."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def auth_token(client):
    """Session-scoped auth token."""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    return response.json()["access_token"]
```

### test_smoke.py

```python
import pytest

@pytest.mark.smoke
class TestAPISmoke:
    """Critical API functionality validation."""

    def test_app_starts(self):
        """FastAPI app imports and initializes."""
        from app.main import app
        assert app is not None
        assert app.title == "My API"

    def test_health_endpoint(self, client):
        """Health check endpoint responds."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_openapi_schema(self, client):
        """OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()

    def test_authentication_works(self, client):
        """User can authenticate."""
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_protected_endpoint_requires_auth(self, client):
        """Protected endpoints reject unauthenticated requests."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

    def test_protected_endpoint_accepts_token(self, client, auth_token):
        """Protected endpoints accept valid tokens."""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200

    def test_list_endpoint(self, client, auth_token):
        """Core list endpoint works."""
        response = client.get(
            "/api/v1/items",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_endpoint(self, client, auth_token):
        """Core create endpoint works."""
        response = client.post(
            "/api/v1/items",
            json={"name": "test item", "description": "test"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code in [200, 201]
```

## Example 2: Django Web Application

### conftest.py

```python
import pytest
from django.conf import settings
from django.test import Client

@pytest.fixture(scope="session")
def django_db_setup():
    """Configure Django test database."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture(scope="session")
def client():
    """Session-scoped Django test client."""
    return Client()


@pytest.fixture(scope="session")
def test_user(django_db_blocker):
    """Session-scoped test user."""
    from django.contrib.auth.models import User

    with django_db_blocker.unblock():
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        yield user
```

### test_smoke.py

```python
import pytest
from django.urls import reverse

@pytest.mark.smoke
@pytest.mark.django_db
class TestDjangoSmoke:
    """Critical Django app functionality."""

    def test_app_imports(self):
        """Django app modules load."""
        from myapp import views, models, forms
        assert views and models and forms

    def test_homepage_loads(self, client):
        """Homepage is accessible."""
        response = client.get('/')
        assert response.status_code == 200

    def test_login_page_loads(self, client):
        """Login page is accessible."""
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_user_can_login(self, client, test_user):
        """Authentication system works."""
        logged_in = client.login(
            username='testuser',
            password='testpass123'
        )
        assert logged_in is True

    def test_dashboard_requires_auth(self, client):
        """Protected views require authentication."""
        response = client.get(reverse('dashboard'))
        assert response.status_code in [302, 403]  # Redirect or forbidden

    def test_dashboard_loads_when_authenticated(self, client, test_user):
        """Dashboard loads for authenticated users."""
        client.force_login(test_user)
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200

    def test_database_connection(self, db):
        """Database is accessible."""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0] == 1
```

## Example 3: Data Pipeline (Apache Airflow DAG)

### test_smoke.py

```python
import pytest
from datetime import datetime
from airflow.models import DagBag

@pytest.mark.smoke
class TestPipelineSmoke:
    """Critical data pipeline functionality."""

    def test_dag_imports(self):
        """DAG module can be imported."""
        from dags import my_pipeline
        assert my_pipeline is not None

    def test_dag_bag_import(self):
        """All DAGs load without errors."""
        dag_bag = DagBag(dag_folder='dags/', include_examples=False)
        assert len(dag_bag.import_errors) == 0

    def test_dag_structure(self):
        """Critical DAG is present and valid."""
        dag_bag = DagBag(dag_folder='dags/', include_examples=False)
        assert 'my_pipeline' in dag_bag.dags

        dag = dag_bag.get_dag('my_pipeline')
        assert dag is not None
        assert len(dag.tasks) > 0

    def test_dag_has_required_tasks(self):
        """Critical tasks are defined."""
        dag_bag = DagBag(dag_folder='dags/')
        dag = dag_bag.get_dag('my_pipeline')

        task_ids = [task.task_id for task in dag.tasks]
        assert 'extract' in task_ids
        assert 'transform' in task_ids
        assert 'load' in task_ids

    def test_database_connection(self):
        """Source database is reachable."""
        from airflow.hooks.postgres_hook import PostgresHook

        hook = PostgresHook(postgres_conn_id='source_db')
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        assert cursor.fetchone()[0] == 1

    def test_warehouse_connection(self):
        """Data warehouse is reachable."""
        from airflow.hooks.postgres_hook import PostgresHook

        hook = PostgresHook(postgres_conn_id='warehouse')
        conn = hook.get_conn()
        assert conn is not None

    def test_transform_function_on_empty_data(self):
        """Transform handles empty dataset."""
        from dags.my_pipeline import transform_data

        result = transform_data(data=[])
        assert isinstance(result, list)
        assert len(result) == 0
```

## Example 4: CLI Application (Click)

### test_smoke.py

```python
import pytest
from click.testing import CliRunner

@pytest.fixture(scope="session")
def cli_runner():
    """Session-scoped CLI runner."""
    return CliRunner()


@pytest.mark.smoke
class TestCLISmoke:
    """Critical CLI functionality."""

    def test_cli_imports(self):
        """CLI module loads."""
        from myapp import cli
        assert cli is not None

    def test_help_command(self, cli_runner):
        """--help flag works."""
        from myapp.cli import cli

        result = cli_runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Usage:' in result.output

    def test_version_command(self, cli_runner):
        """--version flag works."""
        from myapp.cli import cli

        result = cli_runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '1.0' in result.output  # Check version is displayed

    def test_config_command(self, cli_runner):
        """Config command works."""
        from myapp.cli import cli

        result = cli_runner.invoke(cli, ['config', 'show'])
        assert result.exit_code == 0

    def test_main_command_dry_run(self, cli_runner):
        """Main command executes in dry-run mode."""
        from myapp.cli import cli

        result = cli_runner.invoke(cli, ['process', '--dry-run'])
        assert result.exit_code == 0

    def test_invalid_command_fails_gracefully(self, cli_runner):
        """Invalid commands show helpful error."""
        from myapp.cli import cli

        result = cli_runner.invoke(cli, ['nonexistent'])
        assert result.exit_code != 0
        assert 'Error' in result.output or 'No such command' in result.output
```

## Example 5: Microservice with gRPC

### test_smoke.py

```python
import pytest
import grpc

from myservice.protos import service_pb2, service_pb2_grpc


@pytest.fixture(scope="session")
def grpc_channel():
    """Session-scoped gRPC channel."""
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()


@pytest.fixture(scope="session")
def grpc_stub(grpc_channel):
    """Session-scoped gRPC stub."""
    return service_pb2_grpc.MyServiceStub(grpc_channel)


@pytest.mark.smoke
class TestMicroserviceSmoke:
    """Critical microservice functionality."""

    def test_service_imports(self):
        """Service modules load."""
        from myservice import server, handlers
        assert server and handlers

    def test_grpc_server_responds(self, grpc_stub):
        """gRPC server is reachable."""
        request = service_pb2.HealthCheckRequest()
        response = grpc_stub.HealthCheck(request)
        assert response.status == service_pb2.HealthCheckResponse.SERVING

    def test_database_connection(self, grpc_stub):
        """Database connectivity check."""
        request = service_pb2.HealthCheckRequest()
        response = grpc_stub.HealthCheck(request)
        assert response.database_connected is True

    def test_cache_connection(self, grpc_stub):
        """Cache connectivity check."""
        request = service_pb2.HealthCheckRequest()
        response = grpc_stub.HealthCheck(request)
        assert response.cache_connected is True

    def test_core_rpc_method(self, grpc_stub):
        """Core RPC method works."""
        request = service_pb2.GetItemRequest(id=1)
        response = grpc_stub.GetItem(request)
        assert response is not None

    def test_list_rpc_method(self, grpc_stub):
        """List RPC method works."""
        request = service_pb2.ListItemsRequest()
        response = grpc_stub.ListItems(request)
        assert hasattr(response, 'items')
```

## Example 6: Machine Learning Pipeline

### test_smoke.py

```python
import pytest
import numpy as np

@pytest.mark.smoke
class TestMLPipelineSmoke:
    """Critical ML pipeline functionality."""

    def test_model_imports(self):
        """Model modules load."""
        from mlpipeline import preprocessing, model, inference
        assert preprocessing and model and inference

    def test_model_file_exists(self):
        """Trained model file exists."""
        import os
        assert os.path.exists('models/trained_model.pkl')

    def test_model_loads(self):
        """Model can be loaded."""
        from mlpipeline.model import load_model

        model = load_model('models/trained_model.pkl')
        assert model is not None

    def test_preprocessing_on_empty_data(self):
        """Preprocessing handles empty input."""
        from mlpipeline.preprocessing import preprocess

        result = preprocess(data=np.array([]))
        assert isinstance(result, np.ndarray)

    def test_model_inference_on_sample(self):
        """Model can make predictions."""
        from mlpipeline.model import load_model
        from mlpipeline.inference import predict

        model = load_model('models/trained_model.pkl')
        sample = np.array([[1.0, 2.0, 3.0]])

        prediction = predict(model, sample)
        assert prediction is not None
        assert len(prediction) > 0

    def test_feature_extraction(self):
        """Feature extraction works."""
        from mlpipeline.preprocessing import extract_features

        raw_data = {"text": "sample input"}
        features = extract_features(raw_data)
        assert features is not None

    def test_data_loader(self):
        """Data loader can load training data."""
        from mlpipeline.data import DataLoader

        loader = DataLoader(batch_size=32)
        batch = next(iter(loader))
        assert batch is not None
```

## Example 7: Celery Task Queue

### test_smoke.py

```python
import pytest
from celery import Celery

@pytest.fixture(scope="session")
def celery_app():
    """Session-scoped Celery app."""
    from myapp.celery import app
    return app


@pytest.mark.smoke
class TestCelerySmoke:
    """Critical Celery functionality."""

    def test_celery_app_imports(self):
        """Celery app loads."""
        from myapp.celery import app
        assert app is not None

    def test_celery_config(self, celery_app):
        """Celery configuration is valid."""
        assert celery_app.conf.broker_url is not None
        assert celery_app.conf.result_backend is not None

    def test_broker_connection(self, celery_app):
        """Message broker is reachable."""
        inspector = celery_app.control.inspect()
        assert inspector is not None

    def test_critical_task_registered(self, celery_app):
        """Critical tasks are registered."""
        assert 'myapp.tasks.process_data' in celery_app.tasks

    def test_task_can_be_called_sync(self):
        """Task can be called synchronously."""
        from myapp.tasks import process_data

        result = process_data.apply(args=[{'test': 'data'}])
        assert result.successful()

    def test_task_can_be_queued(self):
        """Task can be queued for async execution."""
        from myapp.tasks import process_data

        # Queue task (don't wait for result in smoke test)
        async_result = process_data.delay({'test': 'data'})
        assert async_result.id is not None
```

## Running These Examples

### Run All Smoke Tests

```bash
pytest -m smoke -v
```

### Run Smoke Tests for Specific Project

```bash
pytest tests/test_smoke.py -v
```

### Run with Fail-Fast

```bash
pytest -m smoke -x
```

### Generate Report

```bash
pytest -m smoke --html=smoke-report.html --self-contained-html
```

## Common Patterns Summary

All examples follow these patterns:

1. **Session-scoped fixtures** - Minimize setup/teardown
1. **Minimal mocking** - Test real functionality where possible
1. **Happy path only** - No edge cases in smoke tests
1. **Fast execution** - Each test \<1 second
1. **Clear assertions** - Simple pass/fail checks
1. **Organized in classes** - Group related tests

______________________________________________________________________

**Back to main skill**: See SKILL.md for smoke testing overview.
