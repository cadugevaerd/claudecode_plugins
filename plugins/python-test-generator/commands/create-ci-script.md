---
description: Create CI.py script with auto-fix, lint, type check, tests and Docker build
allowed-tools: Write, Read, Bash, Grep, Glob
model: claude-sonnet-4-5
argument-hint: '[PROJECT_PATH]'
---

# Create CI Script

Create a comprehensive CI.py script that automates code quality checks with auto-fix, testing, and Docker build process with full logging.

## 🎯 Objetivo

- Create `CI.py` script with complete CI/CD automation
- **Auto-fix code with Black formatting** (executa fix automático)
- **Auto-fix lint issues with Ruff** (executa `--fix` quando possível)
- Run MyPy type checking validation (apenas reporta, sem fix)
- Validate pyproject.toml configuration
- Execute automated test suite
- Build Docker image if Dockerfile exists
- Display detailed logs for all operations

## 🔧 Instruções

### 1. Create CI Script Structure

1.1 Create `CI.py` file in project root or specified path
1.2 Add shebang and imports for subprocess, sys, pathlib
1.3 Define main function with step orchestration
1.4 Add colored output utilities for better readability
1.5 Implement exit code handling for CI/CD pipelines

### 2. Implement Code Quality Checks with Auto-Fix

2.1 **Black Formatting with Auto-Fix**

- **Run `uv run black .` to automatically format code** (NÃO usar `--check`)
- Log output showing files that were reformatted
- Return exit code 0 (Black sempre fixa automaticamente)
- Display list of files modified by Black
- **IMPORTANTE**: Black sempre aplica fixes, nunca apenas checa

2.2 **Ruff Linting with Auto-Fix**

- **Run `uv run ruff check --fix .` to auto-fix lint issues**
- Show detailed lint errors that were auto-fixed
- Show lint errors that require manual intervention
- Return exit code 1 if unfixable lint errors remain
- Display summary: fixed vs. manual intervention needed
- **IMPORTANTE**: Use `--fix` para aplicar correções automáticas

2.3 **MyPy Type Checking (Report Only)**

- Run `uv run mypy .` for type checking
- Display type errors with file locations
- Return exit code 1 if type errors found
- Show summary of type issues by category
- **IMPORTANTE**: MyPy não tem auto-fix, apenas reporta

### 3. Validate pyproject.toml

3.1 Check if `pyproject.toml` exists in project root
3.2 Validate TOML syntax using Python's `tomllib` (Python 3.11+) or `tomli`
3.3 Verify required sections exist:

- `[tool.black]` configuration
- `[tool.ruff]` configuration
- `[tool.mypy]` configuration
- `[tool.pytest.ini_options]` configuration
  3.4 Log validation results with clear success/failure messages
  3.5 Return exit code 1 if validation fails

### 4. Execute Test Suite

4.1 Run `uv run pytest` with verbose output
4.2 Display test execution logs in real-time
4.3 Show test summary with pass/fail counts
4.4 Generate coverage report if configured
4.5 Return exit code 1 if any tests fail
4.6 Log test execution time

### 5. Docker Build Process

5.1 Check if `Dockerfile` exists in project root
5.2 Only execute if all previous steps passed successfully
5.3 Run `docker build -t <image-name> .` with build logs
5.4 Stream build output showing each layer
5.5 Display final image size and build time
5.6 Return exit code 1 if build fails
5.7 Skip silently if no Dockerfile present

### 6. Logging Implementation

6.1 Use structured logging with timestamps
6.2 Color-code output: GREEN for success, RED for errors, YELLOW for warnings
6.3 Print section headers for each CI step
6.4 Stream subprocess output in real-time (not buffered)
6.5 Log final summary with pass/fail status for each step
6.6 Include execution time for each major step

### 7. Error Handling and Exit Codes

7.1 Fail fast: Stop execution if critical step fails
7.2 Return appropriate exit codes:

- 0: All checks passed
- 1: One or more checks failed
  7.3 Log stack traces for unexpected errors
  7.4 Provide actionable error messages with fix suggestions

## 📊 Formato de Saída

### CI.py Script Structure

```python
#!/usr/bin/env python3
"""
CI/CD automation script for Python projects.
Runs linting, type checking, tests, and Docker builds.
"""
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def run_command(cmd: List[str], step_name: str) -> bool:
    """Execute command and stream output with logging."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Running: {step_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    # Implementation here
    pass

def check_black() -> bool:
    """Run Black formatting with auto-fix."""
    # Run: uv run black .
    # Always returns True (Black auto-fixes)
    pass

def check_ruff() -> bool:
    """Run Ruff linting with auto-fix."""
    # Run: uv run ruff check --fix .
    # Returns False if unfixable errors remain
    pass

def check_mypy() -> bool:
    """Run MyPy type checking."""
    pass

def validate_pyproject() -> bool:
    """Validate pyproject.toml configuration."""
    pass

def run_tests() -> bool:
    """Execute pytest test suite."""
    pass

def build_docker() -> bool:
    """Build Docker image if Dockerfile exists."""
    pass

def main() -> int:
    """Main CI pipeline orchestration."""
    steps = [
        ("Black Formatting (Auto-Fix)", check_black),
        ("Ruff Linting (Auto-Fix)", check_ruff),
        ("MyPy Type Checking", check_mypy),
        ("pyproject.toml Validation", validate_pyproject),
        ("Test Suite", run_tests),
        ("Docker Build", build_docker),
    ]

    # Execute steps and collect results
    # Return 0 if all passed, 1 if any failed
    pass

if __name__ == "__main__":
    sys.exit(main())
```

### Expected Console Output

```text
============================================================
Running: Black Formatting (Auto-Fix)
============================================================

Reformatted 3 files:
  - src/main.py
  - src/utils.py
  - tests/test_example.py

✓ All files formatted

============================================================
Running: Ruff Linting (Auto-Fix)
============================================================

Fixed 5 issues automatically:
  - F401: Unused import removed (3 files)
  - E501: Line too long fixed (2 files)

⚠️  1 issue requires manual fix:
  - E711: Comparison to None should be 'if cond is None:' (src/main.py:42)

✓ Auto-fixable issues resolved

============================================================
Running: MyPy Type Checking
============================================================

✓ Type checking passed

============================================================
Running: pyproject.toml Validation
============================================================

✓ Configuration valid
  - [tool.black] ✓
  - [tool.ruff] ✓
  - [tool.mypy] ✓
  - [tool.pytest.ini_options] ✓

============================================================
Running: Test Suite
============================================================

============================= test session starts ==============================
collected 42 items

tests/test_example.py::test_function PASSED                              [ 2%]
...

============================== 42 passed in 2.31s ==============================

✓ All tests passed

============================================================
Running: Docker Build
============================================================

Step 1/8 : FROM python:3.11-slim
 ---> abc123def456
...
Successfully built image-name:latest

✓ Docker build successful

============================================================
CI PIPELINE SUMMARY
============================================================

✓ Black Formatting (Auto-Fix)     PASSED (3 files reformatted)
✓ Ruff Linting (Auto-Fix)        PASSED (5 issues auto-fixed)
✓ MyPy Type Checking             PASSED
✓ pyproject.toml                 PASSED
✓ Test Suite                     PASSED
✓ Docker Build                   PASSED

All checks passed! ✨
```

## ✅ Critérios de Sucesso

- [ ] CI.py script created with proper structure
- [ ] **Black auto-fix implemented** (executa `black .` sem `--check`)
- [ ] **Ruff auto-fix implemented** (executa `ruff check --fix .`)
- [ ] **Auto-fix summary logged** (quantos issues foram corrigidos)
- [ ] MyPy type checking implemented with issue reporting (report only)
- [ ] pyproject.toml validation implemented
- [ ] Pytest test suite execution implemented
- [ ] Docker build process implemented (conditional)
- [ ] All subprocess outputs logged in real-time
- [ ] Color-coded output for better readability
- [ ] Proper exit codes returned (0 for success, 1 for failure)
- [ ] Fail-fast behavior on critical errors
- [ ] Execution time logged for each step
- [ ] Final summary report generated with auto-fix stats
- [ ] Script is executable and uses uv run for Python commands

## ❌ Anti-Patterns

### ❌ Erro 1: Buffered Output

Do not buffer subprocess output - stream in real-time:

```python
# ❌ Errado - output só aparece no final
result = subprocess.run(cmd, capture_output=True)
print(result.stdout)

# ✅ Correto - output em tempo real
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)
for line in process.stdout:
    print(line, end='')
```

### ❌ Erro 2: Using --check Instead of Auto-Fix

Do not just check - always apply auto-fix when available:

```python
# ❌ Errado - apenas checa, não corrige
def check_black() -> bool:
    result = subprocess.run(["uv", "run", "black", "--check", "."])
    if result.returncode != 0:
        print("Black formatting needed")
        return False
    return True

# ✅ Correto - aplica auto-fix automaticamente
def check_black() -> bool:
    result = subprocess.run(["uv", "run", "black", "."], capture_output=True, text=True)

    # Parse output para contar arquivos reformatados
    reformatted_files = []
    for line in result.stdout.splitlines():
        if "reformatted" in line.lower():
            # Extract filename
            reformatted_files.append(line)

    if reformatted_files:
        print(f"{GREEN}✓ Black formatted {len(reformatted_files)} files{RESET}")
        for file in reformatted_files:
            print(f"  - {file}")
    else:
        print(f"{GREEN}✓ All files already formatted{RESET}")

    return True  # Black always succeeds (auto-fixes)
```

### ❌ Erro 3: Ignoring pyproject.toml Validation

Do not skip configuration validation:

```python
# ❌ Errado - assume pyproject.toml está correto
def validate_pyproject() -> bool:
    return True  # Não valida nada

# ✅ Correto - valida estrutura e conteúdo
def validate_pyproject() -> bool:
    import tomllib

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print(f"{RED}✗ pyproject.toml not found{RESET}")
        return False

    try:
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)

        required_sections = [
            "tool.black",
            "tool.ruff",
            "tool.mypy",
            "tool.pytest.ini_options"
        ]

        for section in required_sections:
            keys = section.split(".")
            current = config
            for key in keys:
                if key not in current:
                    print(f"{RED}✗ Missing [{section}] section{RESET}")
                    return False
                current = current[key]
            print(f"{GREEN}✓ [{section}] found{RESET}")

        return True
    except Exception as e:
        print(f"{RED}✗ Invalid TOML: {e}{RESET}")
        return False
```

### ❌ Erro 4: Running Docker Build Even If Tests Fail

Do not build Docker image if previous steps failed:

```python
# ❌ Errado - sempre tenta build
def main() -> int:
    check_black()
    check_ruff()
    check_mypy()
    validate_pyproject()
    run_tests()
    build_docker()  # Roda mesmo se testes falharam

# ✅ Correto - só build se tudo passou
def main() -> int:
    results = []
    results.append(("Black", check_black()))
    results.append(("Ruff", check_ruff()))
    results.append(("MyPy", check_mypy()))
    results.append(("pyproject.toml", validate_pyproject()))
    results.append(("Tests", run_tests()))

    # Só executa build se tudo passou
    if all(passed for _, passed in results):
        results.append(("Docker Build", build_docker()))

    # Retorna 1 se qualquer etapa falhou
    return 0 if all(passed for _, passed in results) else 1
```

## 📝 Exemplo

### Uso Básico

```bash
/create-ci-script
```

Cria `CI.py` no diretório raiz do projeto atual.

### Com Caminho Customizado

```bash
/create-ci-script /path/to/project
```

Cria `CI.py` no caminho especificado.

### Executando o Script Criado

```bash
# Tornar executável
chmod +x CI.py

# Executar
./CI.py

# Ou via Python
uv run python CI.py
```

### Integração com GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Run CI checks
        run: uv run python CI.py
```
