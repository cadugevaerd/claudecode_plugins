---
name: uv-python-runner
description: Detecta e usa uv automaticamente para executar comandos Python. Use quando executar testes, linters, type checkers, scripts Python ou qualquer comando Python em projetos que possuem uv.lock ou pyproject.toml com [tool.uv].
allowed-tools: Read, Bash, Grep
---

name: uv-python-runner
description: Detecta e usa uv automaticamente para executar comandos Python. Use quando executar testes, linters, type checkers, scripts Python ou qualquer comando Python em projetos que possuem uv.lock ou pyproject.toml com [tool.uv].
allowed-tools: Read, Bash, Grep

# UV Python Runner Skill

Esta skill detecta automaticamente se um projeto Python utiliza **uv** (gerenciador de pacotes e projetos Python da Astral) e executa comandos usando `uv run` quando apropriado.

## 🎯 Objetivo

Garantir que comandos Python sejam executados corretamente em projetos que usam uv, sem necessidade de ativação manual de virtualenv e com sincronização automática de dependências.

## 🔍 Quando Usar

Esta skill é **invocada automaticamente** quando Claude detecta necessidade de executar comandos Python em um projeto que:

- Possui arquivo `pyproject.toml` com seção `[tool.uv]`
- Possui arquivo `uv.lock` (lockfile do uv)
- Possui diretório `.venv` criado por uv

## 📋 Como Funciona

### 1. Detecção de Ambiente UV

A skill verifica a presença de indicadores de uso do uv:

````bash

# Verificar se pyproject.toml tem configuração uv
grep -q "\[tool.uv\]" pyproject.toml

# Verificar se uv.lock existe
test -f uv.lock

# Verificar se .venv foi criado por uv
test -d .venv && test -f .venv/pyvenv.cfg

```text

### 2. Transformação de Comandos

Quando uv é detectado, a skill transforma comandos Python:

**Antes (sem uv)**:

```bash
pytest
python script.py
black . --check
mypy .
flake8 .

```text

**Depois (com uv)**:

```bash
uv run pytest
uv run python script.py
uv run black . --check
uv run mypy .
uv run flake8 .

```text

### 3. Benefícios do UV Run

O comando `uv run` automaticamente:

✅ **Sincroniza dependências** - Verifica e atualiza lockfile antes de executar
✅ **Isola ambiente** - Executa em virtualenv isolado sem ativação manual
✅ **Garante consistência** - Usa versões exatas do lockfile
✅ **Extremamente rápido** - 80x mais rápido que python -m venv
✅ **Multi-plataforma** - Resoluções de dependências funcionam em qualquer OS

## 🔧 Padrões de Detecção

### Indicador 1: pyproject.toml com [tool.uv]

```toml
[project]
name = "my-project"
version = "0.1.0"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
]

```text

### Indicador 2: Arquivo uv.lock

Presença de `uv.lock` na raiz do projeto indica que o projeto usa uv para gerenciamento de dependências.

### Indicador 3: Virtualenv criado por uv

O diretório `.venv` com estrutura criada por uv (contém `pyvenv.cfg` com referência ao uv).

## 📝 Exemplos de Uso

### Exemplo 1: Executar Testes

**Projeto sem uv**:

```bash
$ pytest --cov

# Pode falhar se virtualenv não estiver ativado

```text

**Projeto com uv (skill aplicada automaticamente)**:

```bash
$ uv run pytest --cov

# ✅ Sincroniza dependências automaticamente

# ✅ Executa em ambiente isolado

# ✅ Garante versões corretas

```text

### Exemplo 2: Executar Scripts Python

**Antes**:

```bash
$ source .venv/bin/activate  # Ativação manual necessária
$ python scripts/validate.py

```text

**Depois (com uv)**:

```bash
$ uv run python scripts/validate.py

# ✅ Sem necessidade de ativação manual

# ✅ Dependências sincronizadas automaticamente

```text

### Exemplo 3: Ferramentas de Desenvolvimento

**Antes**:

```bash
$ source .venv/bin/activate
$ black . --check
$ mypy .
$ flake8 .

```text

**Depois (com uv)**:

```bash
$ uv run black . --check
$ uv run mypy .
$ uv run flake8 .

# ✅ Cada comando em ambiente consistente

# ✅ Sem ativação manual

```text

## 🎨 Integração com Git Commit Helper

Esta skill se integra perfeitamente com o plugin git-commit-helper:

### Durante Execução de Testes

Quando o commit-assistant detecta que precisa executar testes em projeto Python com uv:

```bash

# Sem skill (pode falhar)
pytest --cov

# Com skill (sempre funciona)
uv run pytest --cov

```text

### Durante Validação de Código

```bash

# Linting
uv run black . --check
uv run flake8 .

# Type checking
uv run mypy .

# Security audit
uv run pip-audit

```text

### Durante Build/CI

```bash

# Executar script CI customizado
uv run python ci.py

# Executar script de validação
uv run python scripts/validate.py

```text

## 🚀 Comandos Suportados

A skill reconhece e transforma automaticamente:

### Frameworks de Teste
- `pytest` → `uv run pytest`
- `pytest --cov` → `uv run pytest --cov`
- `python -m pytest` → `uv run python -m pytest`
- `unittest` → `uv run python -m unittest`

### Ferramentas de Qualidade
- `black` → `uv run black`
- `flake8` → `uv run flake8`
- `mypy` → `uv run mypy`
- `pylint` → `uv run pylint`
- `ruff` → `uv run ruff`

### Ferramentas de Segurança
- `pip-audit` → `uv run pip-audit`
- `bandit` → `uv run bandit`
- `safety` → `uv run safety`

### Scripts Customizados
- `python script.py` → `uv run python script.py`
- `python -m module` → `uv run python -m module`

### Build e Deploy
- `python setup.py` → `uv run python setup.py`
- `python -m build` → `uv run python -m build`

## ⚙️ Configuração

### Nenhuma Configuração Necessária!

A skill funciona automaticamente quando detecta ambiente uv. Não requer configuração manual.

### Fallback para Comandos Tradicionais

Se uv não estiver instalado ou não for detectado, a skill não interfere e permite execução de comandos tradicionais.

## 🔍 Verificação de Status

Para verificar se a skill detectou uv corretamente:

```bash

# Verificar se uv está instalado
uv --version

# Verificar estado do projeto
uv run --version  # Deve funcionar se projeto usa uv

# Verificar sincronização
uv sync  # Sincroniza dependências manualmente

```text

## 📚 Boas Práticas

### 1. Manter Lockfile Atualizado

```bash

# Atualizar dependências
uv lock

# Sincronizar ambiente com lockfile
uv sync

```text

### 2. Usar uv.lock no Controle de Versão

✅ **Sempre commitar** `uv.lock`:

```bash
git add uv.lock
git commit -m "chore: update dependencies lockfile"

```text

### 3. Especificar Dependências no pyproject.toml

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]

```text

### 4. Usar uv run para Scripts CI/CD

Em scripts de CI, sempre use `uv run`:

```bash
#!/bin/bash

# ci.sh

set -e

echo "Running tests..."
uv run pytest --cov

echo "Running linter..."
uv run black . --check
uv run flake8 .

echo "Running type checker..."
uv run mypy .

echo "✅ All checks passed!"

```text

## 🐛 Troubleshooting

### Problema: Comando não usa uv run

**Sintoma**: Comando Python executado sem uv run mesmo com uv.lock presente

**Solução**:
1. Verificar se `pyproject.toml` tem seção `[tool.uv]`
2. Verificar se `uv.lock` existe na raiz do projeto
3. Executar `uv sync` para garantir sincronização

### Problema: uv não encontrado

**Sintoma**: `command not found: uv`

**Solução**:

```bash

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou via pip
pip install uv

```text

### Problema: Dependências desatualizadas

**Sintoma**: Testes falham por versão incorreta de dependência

**Solução**:

```bash

# Sincronizar dependências
uv sync

# Ou forçar atualização
uv lock --upgrade
uv sync

```text

## 📖 Referências

### Documentação Oficial
- [uv Documentation](https://docs.astral.sh/uv/)
- [Running Commands with uv](https://docs.astral.sh/uv/concepts/projects/run/)
- [Working on Projects](https://docs.astral.sh/uv/guides/projects/)

### Recursos Adicionais
- [GitHub - astral-sh/uv](https://github.com/astral-sh/uv)
- [uv: Python packaging in Rust](https://astral.sh/blog/uv)
- [Real Python - Managing Python Projects With uv](https://realpython.com/python-uv/)

### Características Principais do UV

**Performance**:
- 🚀 80x mais rápido que `python -m venv`
- 🚀 7x mais rápido que `virtualenv`
- 🚀 10-100x mais rápido que pip

**Compatibilidade**:
- ✅ Standards-compliant virtual environments
- ✅ Funciona com pip, poetry, virtualenv
- ✅ Sem vendor lock-in

**Funcionalidades**:
- 🔒 Lockfiles cross-platform
- 🔄 Sincronização automática de dependências
- 🎯 Resolução determinística
- 🌍 Suporte multi-plataforma

## 💡 Quando Esta Skill É Invocada

A skill é **automaticamente invocada** quando:

1. Claude detecta necessidade de executar comando Python
2. Projeto tem indicadores de uso do uv (pyproject.toml + uv.lock)
3. Comando será executado como parte do workflow de commit

**Não requer invocação manual** - funciona transparentemente em background.

## ✅ Checklist de Integração

Para projetos que usam uv, a skill garante:

- [x] Detecção automática de ambiente uv
- [x] Transformação de comandos Python para `uv run`
- [x] Sincronização automática de dependências
- [x] Execução em ambiente isolado
- [x] Compatibilidade com git-commit-helper
- [x] Fallback para comandos tradicionais se uv não disponível
- [x] Zero configuração necessária


**Desenvolvido para git-commit-helper plugin** 🚀

Integração perfeita com uv para execução consistente e rápida de comandos Python!
````
