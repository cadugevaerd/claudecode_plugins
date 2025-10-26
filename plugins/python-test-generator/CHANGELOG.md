# Changelog

Todas as mudanças notáveis neste plugin serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
