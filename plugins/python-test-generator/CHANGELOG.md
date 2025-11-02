# Changelog

Todas as mudanças notáveis neste plugin serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.1.0] - 2025-11-02

### ⚡ FEATURE CRÍTICA

- **Loop automático de cobertura até atingir 80%**: `/py-test` agora NUNCA finaliza sem entregar cobertura ≥80%
  - Implementado `validate_and_iterate_coverage()` no agent `test-assistant` (Passo 8.1)
  - Máximo de 5 iterações por segurança (previne loop infinito)
  - Cria testes adicionais automaticamente em paralelo a cada iteração
  - Re-executa análise de cobertura após cada iteração
  - Identifica gaps remanescentes e prioriza por maior deficiência
  - Finaliza apenas quando: coverage ≥80% OU max iterations atingido OU sem mais gaps detectados

### Adicionado

- Função `validate_and_iterate_coverage(threshold=80, max_iterations=5)` no agent
- Função `identify_remaining_gaps(coverage_data, threshold)` para detectar módulos abaixo do threshold
- Função `create_additional_tests_parallel(gaps)` para criar testes focados nas linhas faltantes
- Output iterativo visual com box drawing:
  ```
  ╔═══════════════════════════════════════════════════════════════╗
  ║ 🔄 ITERATION 1/5 - Coverage: 72.0%
  ╚═══════════════════════════════════════════════════════════════╝
  ```
- Mensagens informativas sobre gap de cobertura e progresso
- Proteção contra loop infinito (max 5 iterações)
- Detecção de situações sem saída (código irracessível, branches complexos)

### Modificado

- Agent `test-assistant` agora executa Passo 8.1 (Loop Automático) após criação inicial de testes
- Relatório final (Passo 9) agora inclui histórico de iterações se loop foi executado
- Descrição do comando `/py-test` atualizada para mencionar loop automático
- Descrição do plugin no marketplace.json destaca garantia de 80%
- Version bump: 2.0.2 → 2.1.0 (MINOR - nova funcionalidade)

### Benefícios

- 🎯 **Garantia de qualidade**: NUNCA entrega cobertura abaixo de 80%
- 🤖 **Totalmente automático**: Zero intervenção do usuário durante iterações
- ⚡ **Performance otimizada**: Testes criados em paralelo a cada iteração
- 🛡️ **Seguro**: Proteção contra loops infinitos e situações sem saída
- 📊 **Transparente**: Progresso visível com coverage atual e gap restante

### Exemplo de Output

```
╔═══════════════════════════════════════════════════════════════╗
║ 🔄 ITERATION 1/5 - Coverage: 72.0%
╚═══════════════════════════════════════════════════════════════╝

⚠️  Coverage is 72.0% - Still below 80% threshold
📊 Gap to close: 8.0%

🔄 AUTOMATICALLY creating additional tests to improve coverage...

📝 Creating tests for 3 modules with insufficient coverage:
   - src/calculator.py (65.0% → target: 80%)
   - src/validator.py (70.0% → target: 80%)
   - src/formatter.py (75.0% → target: 80%)

🚀 Creating 3 test files in PARALLEL...
✅ Created additional tests (10 new tests)
🧪 Running newly created tests...
✅ All new tests passed

╔═══════════════════════════════════════════════════════════════╗
║ 🔄 ITERATION 2/5 - Coverage: 82.0%
╚═══════════════════════════════════════════════════════════════╝

✅ TARGET ACHIEVED: Coverage is now 82.0% (≥80%)

Test generation completed successfully.
```

## [2.0.2] - 2025-11-02

### Modificado

- **Model Optimization**: Agent `test-assistant` now uses Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) for optimal performance and cost-efficiency
- Added explicit model specification in agent YAML frontmatter
- Enhanced agent documentation with model optimization note
- Updated marketplace description to highlight Haiku 4.5 optimization
- Added performance-related tags to plugin keywords

### Benefícios

- ⚡ **Melhor performance**: Haiku 4.5 oferece tempo de resposta mais rápido na geração de testes
- 💰 **Custo-benefício**: Redução de custos mantendo alta qualidade na geração de testes
- 🎯 **Otimizado para task**: Haiku 4.5 é ideal para tarefas estruturadas como geração de testes unitários

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
