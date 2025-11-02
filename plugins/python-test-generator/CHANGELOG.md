# Changelog

Todas as mudanças notáveis neste plugin serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2025-11-01

### ⚠️ BREAKING CHANGES

- **Test generation now respects 80% coverage threshold**: `/py-test` command will NOT generate new tests if project already has ≥80% coverage, unless explicitly requested by user. This prevents unnecessary test creation and maintains focus on untested code.

  **Migration**: If you relied on automatic test generation regardless of coverage, you'll need to explicitly confirm test creation when coverage is already sufficient (≥80%). When prompted:
  - Respond "y" to create tests anyway
  - Respond "n" to abort (tests won't be created)

  **Rationale**: This breaking change aligns with industry best practice (80% coverage target) and prevents test suite bloat.

### Adicionado

- **New command `/update-claude-md`**: Updates project's CLAUDE.md with python-test-generator configuration following best practices (≤40 lines, progressive disclosure, agent documentation)
- **Automatic detection and removal of obsolete tests**: `/py-test` now identifies and removes unnecessary tests (functions no longer exist, duplicates, no assertions, invalid mocks)
- **Conditional removal of failing tests**: `/py-test` detects failing tests and offers removal ONLY if coverage remains ≥80% after removal
  - If coverage ≥80% after removal: offers to remove failing tests
  - If coverage <80% after removal: warns user to fix tests manually instead
  - Automatic coverage impact analysis before removal
- Coverage threshold verification in `/py-test` command
- User prompt when coverage ≥80%: asks if tests should be created anyway
- User prompt before removing obsolete tests: lists all obsolete tests with justification
- User prompt before removing failing tests: shows coverage impact analysis
- Enhanced agent `test-assistant` with coverage threshold logic
- Enhanced agent `test-assistant` with failing test detection (Step 2.5)
- Enhanced agent `test-assistant` with obsolete test detection (Step 2.6)
- Migration guide in README.md for v1.x → v2.0 upgrade
- 5 criteria for obsolete test detection: FUNCTION_NOT_FOUND, DUPLICATE, NO_ASSERTIONS, MOCK_NOT_FOUND, OLD_IMPLEMENTATION

### Modificado

- **Agent no longer creates git commits**: test-assistant now only generates test files without committing. Users have full control over when to commit tests.
- `/py-test` command now checks coverage before generating tests
- Agent `test-assistant` updated to respect coverage threshold
- README.md with breaking changes section and migration guide
- Command `/py-test` description updated to mention threshold enforcement

## [1.4.1] - 2025-10-26

### Adicionado
- Seção "Acionamento Automático de Testes" no comando `/setup-project-tests`
- Claude agora sugere automaticamente atualização de testes após modificações em código Python
- Template de mensagem para sugerir testes (com meta de ≥80% coverage)
- Gatilhos automáticos para detectar: novas funcionalidades, refatorações, bug fixes
- Documentação clara: Claude PERGUNTA antes de executar, nunca executa automaticamente

### Modificado
- Comando `/setup-project-tests` adiciona instruções de acionamento automático ao CLAUDE.md
- Descrição do plugin menciona "sugestão inteligente de atualização de testes"
- Objetivo do comando expandido para incluir sugestão automática de testes

## [1.4.0] - 2025-10-26

### Adicionado
- Comando `/setup-pytest-config` para configuração automática de pytest
- Preferência por `pyproject.toml` para configuração pytest (padrão moderno PEP 518)
- Fallback para `pytest.ini` quando `pyproject.toml` não existe
- Detecção automática de stack Python (async, frameworks, plugins pytest)
- Template completo de configuração pytest com coverage, parallel e markers
- Sugestão automática de `/setup-pytest-config` quando configuração não encontrada
- Keywords: `pytest-config`, `pyproject-toml`

### Modificado
- Agente `test-assistant` agora detecta e respeita configuração pytest existente
- Agente `test-assistant` sugere `/setup-pytest-config` se não houver configuração
- Comando `/setup-project-tests` documenta novo comando e ordem de prioridade
- Descrição do plugin menciona configuração automática de pytest

## [1.3.0] - 2025-10-24

### Adicionado
- Skill `langchain-test-specialist` para testes especializados em LangChain/LangGraph
- Suporte para trajectory validation com agentevals
- Padrões avançados de mock para LangChain chains com pipe operators
- VCR recording para testes de LLMs
- Documentação completa de mocking de chains, graphs e agents
- Keywords: `langchain`, `langgraph`, `agentevals`, `trajectory`, `llm-testing`

### Modificado
- README expandido com exemplos de mocks LangChain/LangGraph
- Agente `test-assistant` com padrões de mock para chains LCEL

## [1.2.0] - 2025-10-22

### Adicionado
- Comando `/setup-project-tests` para configurar CLAUDE.md
- Configuração automática de padrões de testes por framework
- Detecção de fixtures existentes em conftest.py
- Documentação de AAA pattern
- Padrões de cleanup de recursos

### Modificado
- Comando `/py-test` agora respeita configurações do CLAUDE.md
- Agente `test-assistant` reutiliza fixtures detectadas

## [1.1.0] - 2025-10-21

### Adicionado
- Suporte para projetos Python com uv (universal virtualenv)
- Detecção automática de gerenciador de pacotes (pip, poetry, pipenv, uv)
- Comando `/py-test` com argumentos customizáveis
- Keywords: `automation`, `parallel`, `quality`

### Modificado
- Agente `test-assistant` detecta gerenciador de pacotes automaticamente
- Melhorias na detecção de frameworks de teste

## [1.0.0] - 2025-10-20

### Adicionado
- Lançamento inicial do plugin
- Comando `/py-test` para geração automática de testes
- Agente `test-assistant` com criação paralela de arquivos
- Análise de cobertura com pytest-cov
- Suporte para pytest, unittest, nose
- Padrões de mock para FastAPI, Django, Flask, AWS
- Mock de variáveis module-level
- Criação paralela de múltiplos arquivos de teste (até 80% mais rápido)
- AAA pattern (Arrange-Act-Assert)
- Keywords: `python`, `testing`, `unit-tests`, `coverage`, `pytest`, `generator`, `mock`
