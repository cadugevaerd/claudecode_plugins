# CI/CD Integration for Smoke Tests

Complete guide to integrating smoke tests into CI/CD pipelines with GitHub Actions, GitLab CI, CircleCI, and Jenkins.

## Core Integration Principles

### 1. Run Smoke Tests First

**Always** run smoke tests before any other test category:

```
Build → Smoke Tests → Integration Tests → Full Test Suite
         ↓ FAIL
         Stop Pipeline
```

**Why**: No point running 1000 integration tests if basic functionality is broken.

### 2. Fail Fast

Configure pipelines to **halt immediately** on smoke test failure:

- Don't waste CI minutes
- Get faster feedback
- Alert team to critical breakage

### 3. Optimize for Speed

Target: **\<2 minutes from commit to smoke test results**

- Use caching for dependencies
- Run smoke tests in parallel if possible
- Minimal setup/teardown

## GitHub Actions

### Basic Setup

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  smoke-tests:
    name: Smoke Tests
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -e .[test]

      - name: Run smoke tests
        run: |
          pytest -m smoke \
            --verbose \
            --tb=short \
            -x \
            --maxfail=1

  full-test-suite:
    name: Full Test Suite
    runs-on: ubuntu-latest
    needs: smoke-tests  # Only run if smoke tests pass

    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -e .[test]

      - name: Run full test suite
        run: pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Advanced: Matrix Strategy

Run smoke tests across multiple Python versions:

```yaml
jobs:
  smoke-tests:
    name: Smoke Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest

    strategy:
      fail-fast: true  # Stop all jobs if one fails
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run smoke tests
        run: pytest -m smoke -x --tb=short
```

### With Service Containers

For tests requiring database:

```yaml
jobs:
  smoke-tests:
    name: Smoke Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run smoke tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: pytest -m smoke -x
```

### Notifications on Failure

```yaml
jobs:
  smoke-tests:
    name: Smoke Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run smoke tests
        id: smoke
        run: pytest -m smoke -x --tb=short
        continue-on-error: true

      - name: Notify on Slack if failed
        if: steps.smoke.outcome == 'failure'
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "🚨 Smoke tests FAILED on ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Smoke Tests Failed*\nRepo: ${{ github.repository }}\nBranch: ${{ github.ref }}\nCommit: ${{ github.sha }}"
                  }
                }
              ]
            }

      - name: Fail job if smoke tests failed
        if: steps.smoke.outcome == 'failure'
        run: exit 1
```

## GitLab CI

### Basic Setup

```yaml
# .gitlab-ci.yml

stages:
  - smoke
  - test
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip

smoke-tests:
  stage: smoke
  image: python:3.11
  before_script:
    - pip install --upgrade pip
    - pip install -e .[test]
  script:
    - pytest -m smoke -x --tb=short --junit-xml=smoke-report.xml
  artifacts:
    reports:
      junit: smoke-report.xml
    when: always

full-tests:
  stage: test
  image: python:3.11
  needs: [smoke-tests]  # Only run after smoke passes
  before_script:
    - pip install --upgrade pip
    - pip install -e .[test]
  script:
    - pytest --cov=myapp --cov-report=xml
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### With Docker Services

```yaml
smoke-tests:
  stage: smoke
  image: python:3.11
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test_db
  script:
    - pip install -e .[test]
    - pytest -m smoke -x
```

### Parallel Execution

```yaml
smoke-tests:
  stage: smoke
  image: python:3.11
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.9", "3.10", "3.11", "3.12"]
  script:
    - apt-get update && apt-get install -y python${PYTHON_VERSION}
    - python${PYTHON_VERSION} -m pip install -e .[test]
    - python${PYTHON_VERSION} -m pytest -m smoke -x
```

## CircleCI

### Basic Setup

```yaml
# .circleci/config.yml

version: 2.1

orbs:
  python: circleci/python@2.1.1

jobs:
  smoke-tests:
    executor: python/default
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          args: -e .[test]
      - run:
          name: Run smoke tests
          command: |
            pytest -m smoke \
              -x \
              --tb=short \
              --junit-xml=test-results/smoke.xml
      - store_test_results:
          path: test-results

  full-tests:
    executor: python/default
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          args: -e .[test]
      - run:
          name: Run full test suite
          command: pytest --cov=myapp --cov-report=xml
      - store_artifacts:
          path: coverage.xml

workflows:
  test-workflow:
    jobs:
      - smoke-tests
      - full-tests:
          requires:
            - smoke-tests  # Wait for smoke to pass
```

### With Database

```yaml
jobs:
  smoke-tests:
    docker:
      - image: cimg/python:3.11
      - image: cimg/postgres:15.0
        environment:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres

    environment:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db

    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          args: -e .[test]
      - run:
          name: Wait for DB
          command: |
            dockerize -wait tcp://localhost:5432 -timeout 1m
      - run:
          name: Run smoke tests
          command: pytest -m smoke -x
```

## Jenkins

### Declarative Pipeline

```groovy
// Jenkinsfile

pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -e .[test]'
            }
        }

        stage('Smoke Tests') {
            steps {
                script {
                    def smokeResult = sh(
                        script: 'venv/bin/pytest -m smoke -x --tb=short --junit-xml=smoke-results.xml',
                        returnStatus: true
                    )

                    if (smokeResult != 0) {
                        currentBuild.result = 'FAILURE'
                        error('Smoke tests failed - stopping pipeline')
                    }
                }
            }
            post {
                always {
                    junit 'smoke-results.xml'
                }
            }
        }

        stage('Full Test Suite') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh 'venv/bin/pytest --cov=myapp --cov-report=xml --junit-xml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }
    }

    post {
        failure {
            emailext(
                subject: "Smoke Tests Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Smoke tests failed. Check console output at ${env.BUILD_URL}",
                to: 'team@example.com'
            )
        }
    }
}
```

## Docker Compose for Local CI Testing

Test your CI setup locally:

```yaml
# docker-compose.ci.yml

version: '3.8'

services:
  smoke-tests:
    build: .
    command: pytest -m smoke -x --tb=short
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/test_db
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

Run locally:

```bash
docker-compose -f docker-compose.ci.yml up --abort-on-container-exit
```

## Monitoring and Alerts

### Track Smoke Test Metrics

```yaml
# GitHub Actions with metrics

- name: Run smoke tests with timing
  id: smoke
  run: |
    START_TIME=$(date +%s)
    pytest -m smoke -x --tb=short
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    echo "duration=$DURATION" >> $GITHUB_OUTPUT

- name: Send metrics to monitoring
  run: |
    curl -X POST https://metrics.example.com/api/metrics \
      -H "Content-Type: application/json" \
      -d '{
        "test_suite": "smoke",
        "duration": ${{ steps.smoke.outputs.duration }},
        "status": "success",
        "commit": "${{ github.sha }}"
      }'
```

### Track Flaky Tests

```python
# conftest.py

import pytest
import json

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Track smoke test failures."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and "smoke" in item.keywords:
        result = {
            "test": item.nodeid,
            "outcome": report.outcome,
            "duration": report.duration,
        }

        with open("smoke-results.json", "a") as f:
            f.write(json.dumps(result) + "\n")
```

## Troubleshooting CI Issues

### Issue: Smoke Tests Pass Locally, Fail in CI

**Common causes**:

1. **Environment differences**

   ```yaml
   # Add debug step
   - name: Debug environment
     run: |
       python --version
       pip list
       env | sort
   ```

1. **Timing issues**

   ```python
   # Add explicit waits
   @pytest.mark.smoke
   def test_db_ready(db):
       import time
       for _ in range(5):
           try:
               assert db.ping()
               break
           except:
               time.sleep(1)
   ```

1. **Missing dependencies**

   ```yaml
   # Install system dependencies
   - name: Install system deps
     run: |
       apt-get update
       apt-get install -y libpq-dev
   ```

### Issue: Smoke Tests Too Slow in CI

**Solutions**:

1. **Use caching**:

   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
   ```

1. **Minimize setup**:

   ```python
   # Use session-scoped fixtures
   @pytest.fixture(scope="session")
   def db():
       """Shared DB for all smoke tests."""
       return create_db_connection()
   ```

1. **Parallelize**:

   ```yaml
   - name: Run smoke tests in parallel
     run: pytest -m smoke -n auto
   ```

## Best Practices Summary

### ✅ DO

- Run smoke tests first in pipeline
- Fail fast on smoke test failure
- Cache dependencies
- Use minimal, fast fixtures
- Track smoke test metrics
- Alert team on failures

### ❌ DON'T

- Run full suite before smoke tests
- Continue pipeline if smoke fails
- Use slow, heavy fixtures
- Skip smoke tests for "speed"
- Ignore flaky smoke tests

## Example: Complete GitHub Actions Workflow

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  smoke-tests:
    name: Smoke Tests
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -e .[test]

      - name: Run smoke tests
        run: |
          pytest -m smoke \
            -x \
            --tb=short \
            --junit-xml=smoke-report.xml \
            --maxfail=1

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: smoke-test-results
          path: smoke-report.xml

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: smoke-tests
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -e .[test]

      - name: Run integration tests
        run: pytest -m integration --cov=myapp

  deploy:
    name: Deploy
    needs: [smoke-tests, integration-tests]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - name: Deploy to production
        run: echo "Deploying..."
```

______________________________________________________________________

**Next**: See EXAMPLES.md for real-world smoke test examples.
