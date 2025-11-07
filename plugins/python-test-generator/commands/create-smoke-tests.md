---
description: Cria smoke tests focados em Happy Paths para validação rápida de funcionalidades críticas
allowed-tools: Read, Write, Grep, Glob, Skill
model: claude-sonnet-4-5
argument-hint: '[TARGET_PATH] [--framework pytest|unittest]'
---

# Create Smoke Tests

Especialista em criar smoke tests **apenas para Happy Paths**, garantindo validação rápida das funcionalidades críticas sem cobrir edge cases ou cenários de erro.

## 🎯 Objetivo

- Gerar smoke tests focados em cenários de sucesso (Happy Paths)
- Validar funcionalidades críticas rapidamente (execução < 30s)
- Usar padrões de teste detectados automaticamente no projeto
- Pesquisar em skills existentes para conhecimento sobre testes
- Integrar com fixtures e mocks já configurados

## 🔧 Instruções

### 1. **Buscar Conhecimento em Skills**

Antes de gerar testes, consultar skills relevantes:

1.1 **Verificar Skills de Teste Disponíveis**

- Usar `Skill` tool para buscar conhecimento sobre testes Python
- Priorizar: `langchain-test-specialist` se projeto usa LangChain/LangGraph
- Extrair padrões de mock, fixtures e estrutura AAA

1.2 **Analisar Projeto**

- Identificar framework de teste (pytest, unittest)
- Detectar fixtures existentes em `conftest.py`
- Verificar padrões de mock já utilizados

### 2. **Identificar Funcionalidades Críticas**

2.1 **Analisar Código-Fonte**

- Se `TARGET_PATH` fornecido: focar nesse módulo/diretório
- Se não fornecido: analisar projeto inteiro
- Usar `Grep` para encontrar funções/classes públicas

2.2 **Priorizar por Criticidade**

- Funções em `__init__.py` (API pública)
- Classes principais do domínio
- Endpoints de API (FastAPI, Flask, Django)
- Chains/Graphs do LangChain/LangGraph
- Funções com docstrings indicando uso principal

### 3. **Gerar Smoke Tests (Happy Path Apenas)**

3.1 **Estrutura AAA (Arrange-Act-Assert)**

```python
def test_feature_happy_path():
    """Smoke test: Valida cenário de sucesso básico"""
    # Arrange - Setup mínimo para sucesso
    ...

    # Act - Executar funcionalidade
    ...

    # Assert - Validar resultado esperado
    ...
```

3.2 **Características dos Smoke Tests**

- ✅ **Apenas Happy Paths**: Cenários onde tudo funciona
- ✅ **Execução rápida**: < 5 segundos por teste
- ✅ **Mocks simples**: GenericFakeChatModel, unittest.mock
- ✅ **Sem edge cases**: Não cobrir erros, exceções, limites
- ✅ **Fixtures mínimos**: Usar apenas fixtures essenciais
- ❌ **Não testar**: Validações de erro, timeouts, casos extremos

3.3 **Padrões de Mock para Smoke Tests**

**LangChain/LangGraph (se aplicável)**:

```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

mock_llm = GenericFakeChatModel(messages=iter([
    AIMessage(content="Success response")
]))
```

**APIs HTTP (se aplicável)**:

```python
from unittest.mock import Mock, patch

@patch("module.requests.get")
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"status": "ok"}
```

### 4. **Organizar e Salvar Testes**

4.1 **Estrutura de Arquivos**

- Criar em `tests/smoke/` ou `tests/`
- Nomear: `test_smoke_<module>.py`
- Um arquivo por módulo principal

4.2 **Adicionar Markers pytest**

```python
import pytest

@pytest.mark.smoke
def test_critical_feature():
    """Smoke test: Valida funcionalidade crítica"""
    ...
```

### 5. **Validar e Reportar**

5.1 **Executar Testes Gerados**

- Rodar: `pytest tests/smoke/ -m smoke -v`
- Validar que todos passam
- Medir tempo de execução total

5.2 **Reportar Resultados**

- Listar testes criados
- Mostrar tempo de execução
- Indicar próximos passos (commit, CI/CD)

## 📊 Formato de Saída

**Durante execução:**

```text
🔍 Consultando skills de teste...
✅ Skill langchain-test-specialist encontrada
✅ Padrões de mock identificados

📂 Analisando projeto em: src/my_module
✅ Framework detectado: pytest
✅ 3 funcionalidades críticas identificadas

🧪 Gerando smoke tests (Happy Paths apenas):
  ✅ test_smoke_main.py (2 testes)
  ✅ test_smoke_api.py (3 testes)
  ✅ test_smoke_agent.py (2 testes)

⚡ Executando testes gerados...
  ✅ 7/7 testes passaram
  ⏱️ Tempo total: 12.4s
```

**Saída final:**

```text
═══════════════════════════════════════════
✅ SMOKE TESTS CRIADOS COM SUCESSO
═══════════════════════════════════════════

📊 RESUMO:
├─ Testes criados: 7
├─ Módulos cobertos: 3
├─ Framework: pytest
├─ Markers: @pytest.mark.smoke
├─ Tempo de execução: 12.4s
└─ Localização: tests/smoke/

🧪 TESTES GERADOS:
  📄 test_smoke_main.py
     • test_process_data_happy_path()
     • test_validate_input_happy_path()

  📄 test_smoke_api.py
     • test_get_users_success()
     • test_create_user_success()
     • test_health_check_success()

  📄 test_smoke_agent.py
     • test_agent_basic_query()
     • test_chain_execution()

📝 PRÓXIMOS PASSOS:
1. Executar: pytest tests/smoke/ -m smoke -v
2. Revisar testes gerados
3. Commit: git add tests/smoke/ && git commit -m "test: add smoke tests for happy paths"
4. Integrar no CI/CD (workflow rápido)

═══════════════════════════════════════════
```

## ✅ Critérios de Sucesso

- [ ] Skills de teste consultadas antes de gerar
- [ ] Framework de teste detectado automaticamente
- [ ] Fixtures existentes identificados e reutilizados
- [ ] Apenas Happy Paths cobertos (sem edge cases)
- [ ] Testes seguem padrão AAA (Arrange-Act-Assert)
- [ ] Mocks simples e determinísticos
- [ ] Markers `@pytest.mark.smoke` aplicados
- [ ] Todos os testes gerados passam
- [ ] Tempo de execução total < 30 segundos
- [ ] Arquivos salvos em `tests/smoke/`
- [ ] Relatório final com próximos passos

## 📝 Exemplos

**Exemplo 1 - Projeto inteiro:**

```bash
/create-smoke-tests
```

Analisa projeto completo e gera smoke tests para módulos principais.

**Exemplo 2 - Módulo específico:**

```bash
/create-smoke-tests src/api
```

Gera smoke tests apenas para módulo `src/api`.

**Exemplo 3 - Framework específico:**

```bash
/create-smoke-tests --framework unittest
```

Força uso de `unittest` em vez de detecção automática.

**Exemplo 4 - LangChain/LangGraph:**

```bash
/create-smoke-tests src/agent
```

Detecta LangChain/LangGraph, consulta `langchain-test-specialist`, usa GenericFakeChatModel.

## ❌ Anti-Patterns

### ❌ Erro 1: Incluir Edge Cases

Não crie testes para cenários de erro em smoke tests:

```python
# ❌ ERRADO - Smoke test não deve cobrir erros
def test_invalid_input_raises_error():
    with pytest.raises(ValueError):
        process_data(None)

# ✅ CORRETO - Apenas Happy Path
def test_process_data_success():
    """Smoke test: Processa dados válidos com sucesso"""
    result = process_data({"id": 1, "name": "Test"})
    assert result["status"] == "processed"
```

### ❌ Erro 2: Testes Lentos

Não faça smoke tests que demoram muito:

```python
# ❌ ERRADO - Teste lento (chamada real de API)
def test_api_integration():
    response = requests.get("https://real-api.com/data")
    assert response.status_code == 200

# ✅ CORRETO - Mock rápido
@patch("module.requests.get")
def test_api_integration(mock_get):
    mock_get.return_value.status_code = 200
    result = fetch_data()
    assert result is not None
```

### ❌ Erro 3: Não Usar Skills Disponíveis

Não ignore skills de teste existentes:

```python
# ❌ ERRADO - Criar mocks sem consultar skills
def test_langchain_chain():
    # Mock incorreto ou sub-ótimo
    mock_llm = Mock()
    ...

# ✅ CORRETO - Consultar langchain-test-specialist primeiro
# Usar GenericFakeChatModel conforme skill recomenda
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

def test_langchain_chain():
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(content="Test response")
    ]))
```

### ❌ Erro 4: Não Usar Markers pytest

Não deixe de marcar smoke tests:

```python
# ❌ ERRADO - Sem marker
def test_critical_feature():
    assert feature() == "ok"

# ✅ CORRETO - Com marker @pytest.mark.smoke
@pytest.mark.smoke
def test_critical_feature():
    """Smoke test: Valida funcionalidade crítica"""
    assert feature() == "ok"
```

### ❌ Erro 5: Cobertura Excessiva

Não tente cobrir tudo em smoke tests:

```python
# ❌ ERRADO - Smoke test muito detalhado
def test_all_edge_cases():
    assert process(None) is None
    assert process("") == ""
    assert process([]) == []
    assert process({}) == {}
    # ... 20 mais casos

# ✅ CORRETO - Apenas cenário principal de sucesso
@pytest.mark.smoke
def test_process_valid_data():
    """Smoke test: Processa dados válidos"""
    result = process({"id": 1, "value": "test"})
    assert result["status"] == "success"
```
