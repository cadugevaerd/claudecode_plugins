---
description: Configura pytest.ini ou pyproject.toml com configurações otimizadas para testes Python
---

# Setup Pytest Configuration

Este comando cria ou atualiza a configuração do pytest, priorizando `pyproject.toml` (moderno) ou criando `pytest.ini` (fallback).

## 🎯 Objetivo

Configurar pytest automaticamente com:
- Coverage habilitado
- Testes paralelos (pytest-xdist)
- Markers customizados
- Configuração async (se detectado)
- Paths e patterns otimizados

## 📋 Como usar

```bash
# Configuração automática
/setup-pytest-config

# Com customização de coverage threshold
/setup-pytest-config --coverage 90

# Forçar pytest.ini mesmo se pyproject.toml existe
/setup-pytest-config --force-ini
```

## 🔍 Processo de Execução

### 1. Detecção de Ambiente

```
═══════════════════════════════════════════
⚙️  CONFIGURAÇÃO PYTEST
═══════════════════════════════════════════

🔍 Detectando ambiente do projeto...
```

**Verificar existência de arquivos**:

1. **pyproject.toml** existe?
   - ✅ SIM → Usar pyproject.toml (PREFERENCIAL)
   - ❌ NÃO → Criar pytest.ini (FALLBACK)

2. **Configuração pytest já existe?**
   - Em `pyproject.toml` → seção `[tool.pytest.ini_options]`
   - Em `pytest.ini` → arquivo completo
   - Em `setup.cfg` → seção `[tool:pytest]`

**Se configuração já existe**:
```
⚠️  Configuração pytest já existe em [arquivo]

Deseja atualizar/sobrescrever? (s/n/ver)
- s: Atualizar com novas configurações
- n: Cancelar
- ver: Mostrar configuração atual
```

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
```

**Output**:
```
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
```

### 3. Escolher Formato de Configuração

**Se pyproject.toml existe**:
```
📝 pyproject.toml encontrado

✅ Recomendação: Usar pyproject.toml
   Padrão moderno Python (PEP 518)
   Centralize todas as configurações do projeto

Usar pyproject.toml? (s/n)
```

**Se pyproject.toml NÃO existe**:
```
📝 pyproject.toml não encontrado

Opções:
1. Criar pytest.ini (simples, específico para pytest)
2. Criar pyproject.toml (recomendado, centraliza configs)

Escolha (1/2):
```

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
    "--cov-fail-under=80",

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
    "slow: Slow tests (skip in CI with -m 'not slow')",
    "e2e: End-to-end tests",
]

# Async (se detectado pytest-asyncio)
asyncio_mode = "auto"

# Django (se detectado pytest-django)
DJANGO_SETTINGS_MODULE = "config.settings.test"

# Timeout (se detectado pytest-timeout)
timeout = 300
```

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
```

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
    --cov-fail-under=80

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
    slow: Slow tests (skip in CI with -m 'not slow')
    e2e: End-to-end tests

# Async
asyncio_mode = auto

# Timeout
timeout = 300
```

### 5. Preview da Configuração

Mostrar preview COMPLETO antes de aplicar:

```
═══════════════════════════════════════════
📄 PREVIEW DA CONFIGURAÇÃO
═══════════════════════════════════════════

Arquivo: pyproject.toml
Seção: [tool.pytest.ini_options]

Configuração gerada:

---
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
    "-v",
    "--tb=short",
    "-n auto",
    "--strict-markers",
]

markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

asyncio_mode = "auto"
---

Características:
✅ Coverage habilitado (≥80%)
✅ Testes paralelos (pytest-xdist)
✅ Async support (pytest-asyncio)
✅ Markers customizados (3)
✅ Warnings configurados

═══════════════════════════════════════════

Aplicar configuração? (s/n/editar)
- s: Aplicar
- n: Cancelar
- editar: Ajustar configuração
```

**Se usuário escolher "editar"**:

```
O que deseja ajustar?

1. Coverage threshold (atual: 80%)
2. Adicionar/remover markers
3. Ajustar addopts
4. Mudar testpaths
5. Cancelar edição

Escolha (1-5):
```

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
```

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
```

#### Se pytest.ini (criar arquivo novo):

```python
# Pseudocódigo

1. Criar pytest.ini na raiz do projeto
2. Escrever template completo
3. Validar sintaxe INI
```

### 7. Confirmação de Sucesso

```
═══════════════════════════════════════════
✅ CONFIGURAÇÃO PYTEST APLICADA
═══════════════════════════════════════════

Arquivo: pyproject.toml
Seção: [tool.pytest.ini_options]

Configurações:
✓ Coverage: ≥80%
✓ Parallel: pytest-xdist (-n auto)
✓ Async: pytest-asyncio (auto mode)
✓ Markers: 4 customizados

═══════════════════════════════════════════

🚀 Próximos Passos

1. Validar configuração:
   pytest --version
   pytest --markers

2. Executar testes:
   pytest

3. Ver cobertura:
   pytest --cov

4. Executar apenas testes rápidos:
   pytest -m "not slow"

5. Gerar testes automaticamente:
   /py-test

═══════════════════════════════════════════
```

### 8. Dicas e Troubleshooting

**Se erro ao parsear TOML**:
```
❌ Erro ao ler pyproject.toml

Sintaxe TOML inválida detectada.
Possíveis causas:
- Aspas não fechadas
- Vírgulas faltando em arrays
- Seções duplicadas

Deseja ver detalhes do erro? (s/n)
```

**Se conflito de configuração**:
```
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
```

## 📚 Exemplos de Uso

### Exemplo 1: Projeto Novo (Sem pyproject.toml)

```bash
/setup-pytest-config
```

**Resultado**:
```
⚙️  Detectando ambiente...

✓ Estrutura: src/ layout
✓ Plugins: pytest-cov detectado

📝 pyproject.toml não encontrado

Opções:
1. Criar pytest.ini
2. Criar pyproject.toml (recomendado)

Escolha: 2

✅ pyproject.toml criado com configuração pytest
```

### Exemplo 2: Projeto com pyproject.toml Existente

```bash
/setup-pytest-config
```

**Resultado**:
```
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
```

### Exemplo 3: Coverage Customizado

```bash
/setup-pytest-config --coverage 90
```

**Resultado**:
```
⚙️  Configurando com coverage ≥90%

✅ Configuração aplicada
   --cov-fail-under=90
```

### Exemplo 4: Forçar pytest.ini

```bash
/setup-pytest-config --force-ini
```

**Resultado**:
```
⚙️  Criando pytest.ini (forçado)

✅ pytest.ini criado (pyproject.toml ignorado)
```

## 🎯 Configurações Recomendadas por Stack

### FastAPI

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=app",
    "--cov-fail-under=80",
    "-v",
]
markers = [
    "api: API endpoint tests",
    "unit: Unit tests",
]
```

### LangChain / LangGraph

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=src",
    "--cov-fail-under=80",
    "-v",
]
markers = [
    "llm: Tests that call LLMs",
    "trajectory: Trajectory validation",
    "unit: Unit tests with mocks",
]
asyncio_mode = "auto"
```

### Django

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
DJANGO_SETTINGS_MODULE = "config.settings.test"
addopts = [
    "--cov=apps",
    "--cov-fail-under=80",
    "--reuse-db",
    "-v",
]
markers = [
    "db: Database tests",
    "views: View tests",
    "models: Model tests",
]
```

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
```

## 🚀 Integração com Outros Comandos

### Usar com /setup-project-tests

```bash
# 1. Configurar CLAUDE.md com padrões de testes
/setup-project-tests

# 2. Configurar pytest
/setup-pytest-config

# 3. Gerar testes automaticamente
/py-test
```

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
```

### Executar Apenas Testes Rápidos

```toml
# Adicionar marker slow
markers = ["slow: Slow tests"]

# No CI, skip slow tests
addopts = ["-m", "not slow"]
```

### Parallel com Número Fixo de Workers

```toml
# Auto (recomendado)
addopts = ["-n auto"]

# Fixo (4 workers)
addopts = ["-n 4"]

# Desabilitar parallel
# Remover -n auto
```

### Relatórios Customizados

```toml
addopts = [
    "--cov-report=term-missing",  # Terminal com linhas faltantes
    "--cov-report=html",           # HTML report em htmlcov/
    "--cov-report=xml",            # XML para CI/CD
    "--cov-report=json",           # JSON para análise
]
```

## 🔧 Troubleshooting

### "No module named tomli"

```bash
# Instalar tomli (Python < 3.11)
pip install tomli

# Ou usar tomllib (Python 3.11+)
# Já incluído no Python 3.11+
```

### Conflito entre pytest.ini e pyproject.toml

```bash
# Remover pytest.ini
rm pytest.ini

# Manter apenas pyproject.toml
# Pytest usará automaticamente
```

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
```

### Coverage não encontra módulos

```bash
# Verificar source paths
addopts = ["--cov=src"]  # Se usa src/ layout
addopts = ["--cov=."]    # Se flat layout

# Adicionar source root
addopts = ["--cov=.", "--cov-config=.coveragerc"]
```

## 📖 Referências

- [pytest docs](https://docs.pytest.org/)
- [pytest.ini reference](https://docs.pytest.org/en/stable/reference/customize.html)
- [pyproject.toml spec (PEP 518)](https://peps.python.org/pep-0518/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/)

---

**Desenvolvido por Carlos Araujo para python-test-generator** 🧪
