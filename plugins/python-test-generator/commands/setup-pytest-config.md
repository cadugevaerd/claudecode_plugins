---
description: Configura pyproject.toml com pytest, mypy, ruff e black otimizados
model: claude-sonnet-4-5
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: '[--coverage THRESHOLD] [--tools pytest,mypy,ruff,black]'
---

# Setup Python Development Tools Configuration

Este comando cria ou atualiza a configuração de ferramentas Python de desenvolvimento em `pyproject.toml`:

- **pytest**: Framework de testes
- **mypy**: Type checker estático
- **ruff**: Linter rápido (substitui flake8, isort, etc)
- **black**: Code formatter

## 🎯 Objetivo

Configurar ferramentas Python modernas em `pyproject.toml`:

**pytest**:

- Coverage habilitado
- Testes paralelos (pytest-xdist)
- Markers customizados
- Configuração async (se detectado)
- Paths e patterns otimizados

**mypy**:

- Type checking estrito
- Suporte para pytest e testes
- Overrides por módulo

**ruff**:

- Linting rápido (substitui flake8, isort, etc)
- Line-length consistente com black
- Regras selecionadas (E, F, I, N, W)

**black**:

- Code formatting automático
- Line-length = 88 (padrão)

## 📋 Como usar

````bash

# Configuração automática (todas as ferramentas)
/setup-pytest-config

# Apenas pytest
/setup-pytest-config --tools pytest

# Pytest + mypy + ruff + black
/setup-pytest-config --tools pytest,mypy,ruff,black

# Com customização de coverage threshold
/setup-pytest-config --coverage 90

# Apenas mypy e ruff
/setup-pytest-config --tools mypy,ruff

```text

## 🔍 Processo de Execução

### 1. Detecção de Ambiente

```text

═══════════════════════════════════════════
⚙️  CONFIGURAÇÃO PYTEST
═══════════════════════════════════════════

🔍 Detectando ambiente do projeto...

```text

**Verificar existência de arquivos**:

1. **pyproject.toml** existe?
   - ✅ SIM → Usar pyproject.toml (PREFERENCIAL)
   - ❌ NÃO → Criar pytest.ini (FALLBACK)

2. **Configuração pytest já existe?**
   - Em `pyproject.toml` → seção `[tool.pytest.ini_options]`
   - Em `pytest.ini` → arquivo completo
   - Em `setup.cfg` → seção `[tool:pytest]`

**Se configuração já existe**:

```text

⚠️  Configuração pytest já existe em [arquivo]

Deseja atualizar/sobrescrever? (s/n/ver)
- s: Atualizar com novas configurações
- n: Cancelar
- ver: Mostrar configuração atual

```text

### 2. Detectar Stack Python

**Verificar dependências** (requirements.txt, pyproject.toml, Pipfile):

```python

# Detectar frameworks async
pytest-asyncio → asyncio_mode = "auto"
anyio → anyio_mode = "auto"

# Detectar pytest plugins
pytest-xdist → -n auto (parallel)
pytest-cov → --cov flags
pytest-django → DJANGO_SETTINGS_MODULE
pytest-flask → configuração Flask

# Detectar estrutura
src/ layout → --cov=src
flat layout → --cov=.

# Detectar markers comuns
@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.unit

```text

**Output**:

```text

✅ Stack detectada:

Gerenciador: poetry
Framework de testes: pytest
Plugins detectados:
  - pytest-cov (coverage)
  - pytest-xdist (parallel)
  - pytest-asyncio (async support)

Estrutura do projeto:
  - Layout: src/
  - Diretório de testes: tests/
  - Código fonte: src/

Markers detectados:
  - @pytest.mark.slow (2 usos)
  - @pytest.mark.integration (5 usos)
  - @pytest.mark.unit (15 usos)

```text

### 3. Escolher Formato de Configuração

**Se pyproject.toml existe**:

```text

📝 pyproject.toml encontrado

✅ Recomendação: Usar pyproject.toml
   Padrão moderno Python (PEP 518)
   Centralize todas as configurações do projeto

Usar pyproject.toml? (s/n)

```text

**Se pyproject.toml NÃO existe**:

```text

📝 pyproject.toml não encontrado

Opções:
1. Criar pytest.ini (simples, específico para pytest)
2. Criar pyproject.toml (recomendado, centraliza configs)

Escolha (1/2):

```text

### 4. Gerar Configuração

#### Opção A: pyproject.toml (PREFERENCIAL)

**Template base**:

```toml
[tool.pytest.ini_options]

# Paths
testpaths = ["tests"]

# Patterns
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Options
addopts = [
    # Coverage
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=70",

    # Verbosity
    "-v",
    "--tb=short",

    # Parallel (se pytest-xdist detectado)
    "-n auto",

    # Warnings
    "--strict-markers",
    "-W ignore::DeprecationWarning",
]

# Markers
markers = [
    "unit: Unit tests (fast, isolated)",
    "integration: Integration tests (slower, external deps)",
    "smoke: Smoke tests for Happy Path validations",
    "slow: Slow tests (skip in CI with -m 'not slow')",
    "e2e: End-to-end tests",
]

# Async (se detectado pytest-asyncio)
asyncio_mode = "auto"

# Django (se detectado pytest-django)
DJANGO_SETTINGS_MODULE = "config.settings.test"

# Timeout (se detectado pytest-timeout)
timeout = 300

# =========================
# Mypy Configuration
# =========================
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
strict_equality = true

# Relaxar para testes
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
ignore_errors = false

# =========================
# Ruff Configuration
# =========================
[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# =========================
# Black Configuration
# =========================
[tool.black]
line-length = 88
target-version = ["py313"]
include = '\.pyi?$'

```text

**Customização por stack detectada**:

```python

# Se FastAPI detectado
markers += ["api: API endpoint tests"]

# Se LangChain detectado
markers += [
    "llm: Tests that call LLMs (expensive)",
    "trajectory: Trajectory validation tests",
]

# Se banco de dados detectado
markers += ["db: Tests requiring database"]

# Se coverage threshold fornecido
addopts = [..., f"--cov-fail-under={coverage_threshold}"]

```text

#### Opção B: pytest.ini (FALLBACK)

**Template base**:

```ini
[pytest]

# Paths
testpaths = tests

# Patterns
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Options
addopts =
    # Coverage
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=70

    # Verbosity
    -v
    --tb=short

    # Parallel
    -n auto

    # Warnings
    --strict-markers
    -W ignore::DeprecationWarning

# Markers
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, external deps)
    smoke: Smoke tests for Happy Path validations
    slow: Slow tests (skip in CI with -m 'not slow')
    e2e: End-to-end tests

# Async
asyncio_mode = auto

# Timeout
timeout = 300

```text

### 5. Preview da Configuração

Mostrar preview COMPLETO antes de aplicar:

```text

═══════════════════════════════════════════
📄 PREVIEW DA CONFIGURAÇÃO
═══════════════════════════════════════════

Arquivo: pyproject.toml
Seção: [tool.pytest.ini_options]

Configuração gerada:


[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=70",
    "-v",
    "--tb=short",
    "-n auto",
    "--strict-markers",
]

markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "smoke: Smoke tests for Happy Path validations",
    "slow: Slow tests",
]

asyncio_mode = "auto"

Características:
✅ Coverage habilitado (≥70%)
✅ Testes paralelos (pytest-xdist)
✅ Async support (pytest-asyncio)
✅ Markers customizados (4: unit, integration, smoke, slow)
✅ Warnings configurados

═══════════════════════════════════════════

Aplicar configuração? (s/n/editar)
- s: Aplicar
- n: Cancelar
- editar: Ajustar configuração

```text

**Se usuário escolher "editar"**:

```text

O que deseja ajustar?

1. Coverage threshold (atual: 70%)
2. Adicionar/remover markers
3. Ajustar addopts
4. Mudar testpaths
5. Cancelar edição

Escolha (1-5):

```text

### 6. Aplicar Configuração

#### Se pyproject.toml (atualizar arquivo existente):

```python

# Pseudocódigo do processo

1. Ler pyproject.toml atual
2. Parsear TOML para dict
3. Adicionar/atualizar seção [tool.pytest.ini_options]
4. Preservar TODAS as outras seções
5. Escrever de volta com formatação correta
6. Validar sintaxe TOML

```text

**CRÍTICO**:
- ❌ NUNCA sobrescrever outras seções do pyproject.toml
- ✅ SEMPRE preservar formatação existente
- ✅ SEMPRE adicionar comentários explicativos

**Exemplo de atualização segura**:

```toml

# pyproject.toml ANTES
[tool.poetry]
name = "my-project"
version = "1.0.0"

[tool.black]
line-length = 100

# pyproject.toml DEPOIS (seção pytest adicionada)
[tool.poetry]
name = "my-project"
version = "1.0.0"

[tool.black]
line-length = 100

[tool.pytest.ini_options]  # ← ADICIONADO
testpaths = ["tests"]

# ... resto da config

```text

#### Se pytest.ini (criar arquivo novo):

```python

# Pseudocódigo

1. Criar pytest.ini na raiz do projeto
2. Escrever template completo
3. Validar sintaxe INI

```text

### 7. Confirmação de Sucesso

```text

═══════════════════════════════════════════
✅ FERRAMENTAS PYTHON CONFIGURADAS
═══════════════════════════════════════════

Arquivo: pyproject.toml

**pytest** [tool.pytest.ini_options]:
✓ Coverage: ≥70%
✓ Parallel: pytest-xdist (-n auto)
✓ Async: pytest-asyncio (auto mode)
✓ Markers: 5 customizados (unit, integration, smoke, slow, e2e)

**mypy** [tool.mypy]:
✓ Type checking estrito habilitado
✓ Python version: 3.13
✓ Overrides para tests.*

**ruff** [tool.ruff]:
✓ Line-length: 88 (consistente com black)
✓ Regras: E, F, I, N, W
✓ Target version: py313

**black** [tool.black]:
✓ Line-length: 88
✓ Target version: py313

═══════════════════════════════════════════

🚀 Próximos Passos

1. Validar pytest:
   pytest --version
   pytest --markers

2. Executar testes com coverage:
   pytest --cov

3. Type check com mypy:
   mypy src/

4. Lint com ruff:
   ruff check .
   ruff format --check .

5. Format com black:
   black .

6. Gerar testes automaticamente:
   /py-test

═══════════════════════════════════════════

```text

### 8. Dicas e Troubleshooting

**Se erro ao parsear TOML**:

```text

❌ Erro ao ler pyproject.toml

Sintaxe TOML inválida detectada.
Possíveis causas:
- Aspas não fechadas
- Vírgulas faltando em arrays
- Seções duplicadas

Deseja ver detalhes do erro? (s/n)

```text

**Se conflito de configuração**:

```text

⚠️  Múltiplas configurações pytest detectadas

Encontrado em:
- pyproject.toml [tool.pytest.ini_options]
- pytest.ini

Recomendação: Manter apenas UMA configuração
Pytest usa ordem de prioridade:
1. pytest.ini
2. pyproject.toml
3. setup.cfg

Remover pytest.ini e manter pyproject.toml? (s/n)

```text

## 📚 Exemplos de Uso

### Exemplo 1: Projeto Novo (Sem pyproject.toml)

```bash
/setup-pytest-config

```text

**Resultado**:

```text

⚙️  Detectando ambiente...

✓ Estrutura: src/ layout
✓ Plugins: pytest-cov detectado

📝 pyproject.toml não encontrado

Opções:
1. Criar pytest.ini
2. Criar pyproject.toml (recomendado)

Escolha: 2

✅ pyproject.toml criado com configuração pytest

```text

### Exemplo 2: Projeto com pyproject.toml Existente

```bash
/setup-pytest-config

```text

**Resultado**:

```text

⚙️  Detectando ambiente...

✓ pyproject.toml encontrado
✓ Stack: FastAPI + pytest-asyncio + pytest-xdist

📝 Adicionando [tool.pytest.ini_options]

Preview:
[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = ["-n auto", "--cov=src", ...]

Aplicar? s

✅ pyproject.toml atualizado

```text

### Exemplo 3: Coverage Customizado

```bash
/setup-pytest-config --coverage 90

```text

**Resultado**:

```text

⚙️  Configurando com coverage ≥90%

✅ Configuração aplicada
   --cov-fail-under=90

```text

### Exemplo 4: Forçar pytest.ini

```bash
/setup-pytest-config --force-ini

```text

**Resultado**:

```text

⚙️  Criando pytest.ini (forçado)

✅ pytest.ini criado (pyproject.toml ignorado)

```text

## 🎯 Configurações Recomendadas por Stack

### FastAPI

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=app",
    "--cov-fail-under=70",
    "-v",
]
markers = [
    "api: API endpoint tests",
    "unit: Unit tests",
    "smoke: Smoke tests for Happy Path validations",
]

```text

### LangChain / LangGraph

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=src",
    "--cov-fail-under=70",
    "-v",
]
markers = [
    "llm: Tests that call LLMs",
    "trajectory: Trajectory validation",
    "unit: Unit tests with mocks",
    "smoke: Smoke tests for Happy Path validations",
]
asyncio_mode = "auto"

```text

### Django

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
DJANGO_SETTINGS_MODULE = "config.settings.test"
addopts = [
    "--cov=apps",
    "--cov-fail-under=70",
    "--reuse-db",
    "-v",
]
markers = [
    "db: Database tests",
    "views: View tests",
    "models: Model tests",
    "smoke: Smoke tests for Happy Path validations",
]

```text

## ⚠️ Importante

### Ordem de Prioridade do Pytest

Pytest usa esta ordem para carregar configuração:

1. **pytest.ini** (maior prioridade)
2. **pyproject.toml**
3. **setup.cfg**
4. **tox.ini**

**Recomendação**: Manter APENAS UMA configuração para evitar conflitos.

### Preservar Configurações Existentes

- ✅ SEMPRE ler arquivo antes de modificar
- ✅ SEMPRE preservar outras seções (tool.poetry, tool.black, etc.)
- ✅ SEMPRE fazer backup antes de sobrescrever
- ❌ NUNCA sobrescrever sem confirmação

### Validar Sintaxe

Após criar/atualizar:

```bash

# Validar TOML
python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"

# Validar pytest config
pytest --version
pytest --markers
pytest --collect-only

```text

## 🚀 Integração com Outros Comandos

### Usar com /setup-project-tests

```bash

# 1. Configurar CLAUDE.md com padrões de testes
/setup-project-tests

# 2. Configurar pytest
/setup-pytest-config

# 3. Gerar testes automaticamente
/py-test

```text

### Usar com /py-test

O comando `/py-test` automaticamente:

- Detecta configuração pytest
- Respeita testpaths
- Usa addopts configurados
- Aplica markers

## 💡 Dicas

### Coverage por Módulo

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=src/models",
    "--cov=src/services",
    "--cov=src/utils",
    "--cov-report=term-missing:skip-covered",
]

```text

### Executar Apenas Testes Rápidos

```toml

# Adicionar marker slow
markers = ["slow: Slow tests"]

# No CI, skip slow tests
addopts = ["-m", "not slow"]

```text

### Parallel com Número Fixo de Workers

```toml

# Auto (recomendado)
addopts = ["-n auto"]

# Fixo (4 workers)
addopts = ["-n 4"]

# Desabilitar parallel

# Remover -n auto

```text

### Relatórios Customizados

```toml
addopts = [
    "--cov-report=term-missing",  # Terminal com linhas faltantes
    "--cov-report=html",           # HTML report em htmlcov/
    "--cov-report=xml",            # XML para CI/CD
    "--cov-report=json",           # JSON para análise
]

```text

## 🔧 Troubleshooting

### "No module named tomli"

```bash

# Instalar tomli (Python < 3.11)
pip install tomli

# Ou usar tomllib (Python 3.11+, incluído no Python 3.13)

# tomllib já incluído no Python 3.11+

```text

### Conflito entre pytest.ini e pyproject.toml

```bash

# Remover pytest.ini
rm pytest.ini

# Manter apenas pyproject.toml

# Pytest usará automaticamente

```text

### Markers não reconhecidos

```bash

# Adicionar --strict-markers
addopts = ["--strict-markers"]

# Declarar todos os markers usados
markers = [
    "slow: ...",
    "integration: ...",
    # ... todos os markers
]

```text

### Coverage não encontra módulos

```bash

# Verificar source paths
addopts = ["--cov=src"]  # Se usa src/ layout
addopts = ["--cov=."]    # Se flat layout

# Adicionar source root
addopts = ["--cov=.", "--cov-config=.coveragerc"]

```text

## 📖 Referências

**pytest**:
- [pytest docs](https://docs.pytest.org/)
- [pytest.ini reference](https://docs.pytest.org/en/stable/reference/customize.html)
- [pyproject.toml spec (PEP 518)](https://peps.python.org/pep-0518/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/)

**mypy**:
- [mypy docs](https://mypy.readthedocs.io/)
- [mypy configuration](https://mypy.readthedocs.io/en/stable/config_file.html)

**ruff**:
- [ruff docs](https://docs.astral.sh/ruff/)
- [ruff configuration](https://docs.astral.sh/ruff/configuration/)
- [ruff rules](https://docs.astral.sh/ruff/rules/)

**black**:
- [black docs](https://black.readthedocs.io/)
- [black configuration](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)

**Desenvolvido por Carlos Araujo para python-test-generator** 🧪
````
