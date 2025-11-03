---
name: py-test
description: Executes autonomous test generation for Python projects, automatically iterating to 80% coverage without user prompts.
---

name: py-test
description: Executes autonomous test generation for Python projects, automatically iterating to 80% coverage without user prompts.

# Python Test Executor

**AUTONOMOUS EXECUTION MODE - NO USER QUESTIONS**

This command invokes the test-assistant agent to automatically generate unit tests for your Python project. The agent works independently, analyzing the codebase and creating tests with intelligent iteration to reach 80% coverage.

**Key Behavior**:

- Executes test generation without pausing for confirmations
- Agent determines strategy internally (mocks, patterns, fixtures)
- Iterates automatically until 80% coverage is reached
- Only shows final results to user

## What Happens When You Run This

1. **Agent analyzes** your Python project structure and current test coverage
1. **Agent determines strategy** for creating tests (no prompts to user)
1. **Agent creates tests in parallel** for maximum performance
1. **Agent executes and validates** all tests automatically
1. **Agent iterates internally** until 80% coverage is reached
1. **Reports final results** with complete test suite ready

## Usage

````bash

# Analyze entire Python project and generate tests
/py-test

# Analyze specific module/directory
/py-test src/my_module

# Set custom coverage threshold
/py-test --threshold 85

```text

## Three-Phase Intelligent Strategy (v3.0+)

1. **PHASE 1**: Analyze existing tests (quality, relevance)
2. **PHASE 2**: Maintain existing tests (remove/fix/improve before creating)
3. **PHASE 3**: Create new tests for gaps + auto-detect fixtures from conftest.py

**Fixtures (v3.1.0)**: Automatically detects and reuses existing fixtures.
See README.md "Fixtures Architecture" for details.

## Supported Patterns

- **Frameworks**: pytest, unittest, nose, unittest2
- **Mocking**: unittest.mock, pytest-mock, responses
- **Coverage**: coverage.py, pytest-cov
- **Async**: pytest-asyncio, asyncio
- **Web**: LangChain, FastAPI, Django, Flask, Starlette
- **Databases**: SQLAlchemy, Django ORM, Pynamodb
- **HTTP**: requests, httpx, aiohttp

## Coverage Threshold

- **Default**: 80%
- **Ideal**: 85-90%
- **Critical modules**: 90%+

Respects existing configuration in `pytest.ini`, `pyproject.toml`, `setup.cfg`, `.coveragerc`

## After Generation

Generated tests are saved to disk but **NOT committed**.

**Next steps**:
1. Review the generated tests
2. Run tests locally: `pytest`
3. Commit when satisfied: `git add tests/ && git commit -m "test: add tests for X"`

Tests are ready for immediate use - no configuration needed.

## Agent Invocation

This command delegates to the **test-assistant agent**:

- Working directory: `{{WORKING_DIRECTORY}}`
- Coverage threshold: `{{COVERAGE_THRESHOLD:80}}`
- Framework detection: AUTO
- Mode: AUTONOMOUS (no prompts, fully autonomous)

The agent handles all complexity internally.
````
