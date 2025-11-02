---
name: py-test
description: Gera testes unitários Python automaticamente com análise de cobertura (RESPEITA THRESHOLD DE 80%)
---

# 🐍 Gerador Automático de Testes Unitários Python

**MODO EMPÍRICO - EXECUÇÃO DIRETA SEM PERGUNTAS**

Este comando analisa a cobertura de testes do seu projeto Python e cria automaticamente testes unitários completos seguindo os padrões e frameworks detectados, com **criação paralela de arquivos** para máxima performance.

**⚠️ BREAKING CHANGE (v2.0.0)**: Este comando **RESPEITA threshold de 80% de cobertura**. Se o projeto já tem ≥80% de cobertura, PARA e pergunta se o usuário realmente quer criar novos testes.

---

## 🎯 O que este comando faz:

1. **Invoca o agente test-assistant** especializado em testes Python
2. **Analisa cobertura atual** do projeto Python
3. **✅ NOVO v2.0: Verifica se cobertura ≥80%**
   - Se ≥80%: PARA e pergunta ao usuário
   - Se <80%: Prossegue automaticamente
4. **🆕 NOVO v2.0: Detecta testes falhando**
   - Executa pytest e identifica testes com falhas
   - Calcula impacto na cobertura se removidos
5. **🆕 NOVO v2.0: Remove testes falhando (se cobertura ≥80%)**
   - SE cobertura pós-remoção ≥80%: oferece remoção
   - SE cobertura pós-remoção <80%: avisa e mantém testes
6. **🆕 NOVO v2.0: Detecta e remove testes obsoletos**
   - Identifica testes desnecessários ou obsoletos
   - Pergunta confirmação antes de remover
   - Remove automaticamente com Edit tool
7. **Identifica gaps de cobertura** (< 80%)
8. **Cria testes em PARALELO** para máxima performance
9. **Gera testes completos** seguindo padrões do projeto
10. **Executa e valida** os testes criados
11. **Reporta resultados** detalhados

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

## ⚡ MODO EMPÍRICO + PARALELIZAÇÃO (v2.0)

**Este comando RESPEITA threshold de 80% de cobertura.**

**Fluxo automático**:
1. ✅ Detecta ambiente Python
2. ✅ Analisa cobertura
3. ✅ **✨ NOVO v2.0: Verifica threshold de 80%**
   - Se cobertura ≥80%:
     ```
     ✅ Coverage is already at X% (≥80%)

     New tests will only be created if explicitly requested.
     Do you want to create tests anyway? (y/n)
     ```
   - Se usuário responde "n": PARA e não cria testes
   - Se usuário responde "y": Prossegue normalmente
   - Se cobertura <80%: Prossegue automaticamente
4. ✅ **🆕 NOVO v2.0: Detecta testes falhando**
   - Executa pytest e identifica testes com falhas
   - Calcula cobertura antes da remoção
   - Estima cobertura após remoção dos testes falhando
5. ✅ **🆕 NOVO v2.0: Remove testes falhando (CONDICIONAL)**
   - **SE cobertura pós-remoção ≥80%**:
     ```
     ⚠️  FAILING TESTS DETECTED (N tests)

     Coverage Analysis:
     - Current coverage: 85%
     - Estimated coverage after removal: 82%

     ✅ Coverage will remain ≥80% (82%) after removal.

     Remove failing tests? (y/n)
     ```
   - **SE cobertura pós-remoção <80%**:
     ```
     ⚠️  FAILING TESTS DETECTED (N tests)

     Coverage Analysis:
     - Current coverage: 83%
     - Estimated coverage after removal: 76%

     ❌ Cannot remove failing tests automatically.

     Reason: Coverage would drop below 80% threshold (76% < 80%).

     ⚠️  Action Required: Fix failing tests manually.
     ```
   - Se "y": Remove usando Edit tool
   - Se "n" ou cobertura <80%: Mantém testes e avisa
6. ✅ **🆕 NOVO v2.0: Detecta e remove testes obsoletos**
   - Analisa arquivos de teste existentes
   - Identifica testes desnecessários:
     * Função testada não existe mais
     * Teste duplicado
     * Sem asserções reais
     * Mock de função inexistente
   - Lista testes obsoletos com justificativa
   - Pergunta: "Remove obsolete tests? (y/n)"
   - Se "y": Remove usando Edit tool
   - Se "n": Mantém testes existentes
7. ✅ **Cria MÚLTIPLOS testes EM PARALELO** (reduz tempo em até 80%)
8. ✅ Executa testes
9. ✅ Reporta resultados

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

## 📝 After Test Generation

Tests are generated and saved to disk, but **NOT committed**.

**Next steps**:
1. Review generated tests
2. Run tests to verify they work: `pytest`
3. Commit when satisfied: `git add tests/ && git commit -m "test: add tests for X"`

**Agent does NOT create commits** - you control when to commit.

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