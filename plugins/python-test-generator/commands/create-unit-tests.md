---
description: Creates isolated unit tests for Python functions and classes with 70% coverage target
allowed-tools: Read, Write, Grep, Glob, Skill, Task
model: sonnet
argument-hint: '[TARGET_PATH] [--coverage-target 70]'
---

# Create Unit Tests

**SPECIALIZED IN UNIT TESTS ONLY - NOT INTEGRATION OR E2E**

This command focuses exclusively on creating **isolated unit tests** for Python functions, methods, and classes. It generates tests with proper mocking and fixtures to achieve 70% code coverage by default.

**Key Behavior**:

- Generates **unit tests only** (functions, methods, classes in isolation)
- Uses mocks and stubs to isolate dependencies
- Follows AAA pattern (Arrange-Act-Assert) consistently
- Targets **70% code coverage** by default
- Consults existing skills for testing patterns (e.g., langchain-test-specialist)
- Works autonomously without user prompts

## What Happens When You Run This

1. **Consults skills** for testing patterns and best practices
1. **Analyzes codebase** to identify functions and classes to test
1. **Detects framework** (pytest, unittest) and existing fixtures
1. **Generates unit tests** with proper isolation (mocks, stubs)
1. **Validates tests** by running them and checking coverage
1. **Iterates** until 70% coverage target is reached
1. **Reports results** with coverage metrics

## Usage

````bash

# Generate unit tests for entire project (70% coverage target)
/py-test

# Generate unit tests for specific module
/py-test src/my_module

# Set custom coverage target
/py-test --coverage-target 80

# Generate tests for specific file
/py-test src/services/user_service.py

```text

## Unit Test Generation Strategy

1. **PHASE 1**: Consult skills for testing patterns (langchain-test-specialist if applicable)
2. **PHASE 2**: Analyze existing unit tests and fixtures (conftest.py)
3. **PHASE 3**: Identify functions/classes needing unit tests
4. **PHASE 4**: Generate isolated tests with mocks for dependencies
5. **PHASE 5**: Validate and iterate until 70% coverage reached

**Focus**: Only unit tests (isolated, fast, deterministic). No integration or E2E tests.

## Unit Test Patterns

- **Test Structure**: AAA pattern (Arrange-Act-Assert)
- **Frameworks**: pytest (preferred), unittest
- **Mocking**: unittest.mock, pytest-mock, GenericFakeChatModel (LangChain)
- **Fixtures**: Auto-detects and reuses from conftest.py
- **Isolation**: Mocks for databases, APIs, external services, LLMs
- **Coverage**: coverage.py, pytest-cov

## Mocking Strategies

- **External APIs**: Mock with unittest.mock.patch
- **Databases**: Mock connections and queries
- **LLMs** (LangChain): GenericFakeChatModel for deterministic tests
- **HTTP requests**: responses, httpx.MockTransport
- **File I/O**: tempfile, mock open()

## Coverage Target

- **Default**: 70% (configurable via --coverage-target)
- **Recommendation**: 70-80% for unit tests
- **Focus**: Functions with business logic, complex branches

Respects existing configuration in `pytest.ini`, `pyproject.toml`, `setup.cfg`, `.coveragerc`

## After Generation

Generated tests are saved to disk but **NOT committed**.

**Next steps**:
1. Review the generated tests
2. Run tests locally: `pytest`
3. Commit when satisfied: `git add tests/ && git commit -m "test: add tests for X"`

Tests are ready for immediate use - no configuration needed.

## Agent Invocation

This command delegates to the **test-assistant agent** with unit test specialization:

- **Test Type**: Unit tests only (isolated, mocked dependencies)
- **Working Directory**: `{{WORKING_DIRECTORY}}`
- **Coverage Target**: `{{COVERAGE_THRESHOLD:70}}`
- **Framework**: Auto-detected (pytest preferred)
- **Mode**: AUTONOMOUS (no user prompts)
- **Skills Consulted**: langchain-test-specialist (if applicable)

The agent handles all complexity internally, including:
- Analyzing code structure
- Detecting dependencies to mock
- Generating AAA-pattern tests
- Creating fixtures when needed
- Iterating until coverage target reached
````
