---
name: py-test
description: Gera testes unitários Python automaticamente com análise de cobertura
---

# 🐍 Gerador Automático de Testes Unitários Python

**MODO EMPÍRICO - EXECUÇÃO DIRETA SEM PERGUNTAS**

Este comando analisa a cobertura de testes do seu projeto Python e cria automaticamente testes unitários completos seguindo os padrões e frameworks detectados, com **criação paralela de arquivos** para máxima performance.

---

## 🎯 O que este comando faz:

1. **Invoca o agente test-assistant** especializado em testes Python
2. **Analisa cobertura atual** do projeto Python
3. **Identifica gaps de cobertura** (< 80%)
4. **Cria testes em PARALELO** para máxima performance
5. **Gera testes completos** seguindo padrões do projeto
6. **Executa e valida** os testes criados
7. **Reporta resultados** detalhados

---

## 📋 Uso

```bash
# Analisar projeto Python inteiro
/py-test

# Analisar diretório específico
/py-test src/meu_modulo

# Definir threshold customizado
/py-test --threshold 85
```

---

## 🤖 Agente Especializado Python

Este comando invoca o **test-assistant agent** que:

- ✅ **Cria testes em PARALELO** - máxima performance e eficiência
- ✅ Detecta automaticamente frameworks Python (pytest, unittest, nose)
- ✅ Identifica padrões do projeto (fixtures, mocks, factories)
- ✅ Cria testes Python seguindo AAA pattern
- ✅ Cobre happy path + erros + edge cases
- ✅ Mock de dependências externas (API, DB, LLM)
- ✅ Suporta código Python assíncrono
- ✅ Frameworks Python específicos (LangChain, FastAPI, Django, etc.)

---

## 🎓 Padrões Suportados

- **Testing Frameworks**: pytest, unittest, nose
- **Mock Libraries**: unittest.mock, pytest-mock, responses
- **Coverage Tools**: coverage.py, pytest-cov
- **Async**: pytest-asyncio, asyncio
- **Frameworks**: LangChain, FastAPI, Django, Flask, AWS Lambda
- **Databases**: SQLAlchemy, Django ORM, Pynamodb
- **HTTP**: requests, httpx, aiohttp

---

## ⚡ MODO EMPÍRICO + PARALELIZAÇÃO

**Este comando NÃO faz perguntas e cria testes em PARALELO.**

Executa automaticamente:
1. ✅ Detecta ambiente Python
2. ✅ Analisa cobertura
3. ✅ **Cria MÚLTIPLOS testes EM PARALELO** (reduz tempo em até 80%)
4. ✅ Executa testes
5. ✅ Reporta resultados

### 🚀 Performance Otimizada

O agente cria **todos os arquivos de teste simultaneamente** usando paralelização:
- 5 módulos sem testes = **5 arquivos criados em paralelo**
- 10 módulos sem testes = **10 arquivos criados em paralelo**
- Redução de tempo: **até 80% mais rápido**

---

## 📊 Meta de Cobertura

- **Padrão**: 80%
- **Ideal**: 85-90%
- **Críticos**: 90%+

Respeita configurações em `pytest.ini`, `pyproject.toml`, `setup.cfg`, `.coveragerc`

---

**Invocação do agente test-assistant**:

Use o agente especializado `test-coverage-analyzer:test-assistant` para executar esta tarefa.

**Parâmetros**:
- Diretório de trabalho: {{WORKING_DIRECTORY}}
- Threshold de cobertura: {{COVERAGE_THRESHOLD:80}}
- Framework detectado: AUTO
- Modo: EMPIRICO (sem perguntas)

**Tarefas do agente**:
1. Detectar ambiente e frameworks
2. Executar análise de cobertura
3. Identificar módulos < threshold
4. Ler padrões existentes (conftest.py, fixtures)
5. Criar testes completos
6. Executar testes e validar
7. Reportar resultados