---
description: Configura CLAUDE.md do projeto com padrões de testes Python, frameworks, mocks e estrutura de diretórios
---

# Setup Project for Python Testing

Este comando configura o arquivo `CLAUDE.md` do projeto atual com instruções sobre testes Python, padrões de mock, fixtures e convenções de teste.

## 🎯 Objetivo

Adicionar ao `CLAUDE.md` do projeto instruções claras para que Claude:
- Gere testes Python seguindo padrões do projeto
- Utilize frameworks de teste corretos (pytest, unittest, nose)
- Crie mocks adequados (LangChain, FastAPI, Django, AWS, etc.)
- Reutilize fixtures existentes (conftest.py)
- Siga estrutura de diretórios de testes do projeto
- Aplique AAA pattern (Arrange-Act-Assert)
- Garanta testes paralelos seguros (pytest-xdist)

## 📋 Como usar

```bash
/setup-project-tests
```

Ou com descrição da stack Python:

```bash
/setup-project-tests "API FastAPI com LangChain + PostgreSQL"
```

## 🔍 Processo de Execução

### 1. Detectar ou Criar CLAUDE.md

**Se CLAUDE.md existe**:
- Ler arquivo atual
- Adicionar seção "Python Testing Standards" ao final
- Preservar conteúdo existente

**Se CLAUDE.md NÃO existe**:
- Criar arquivo na raiz do projeto
- Adicionar template completo de padrões de testes Python

### 2. Adicionar Instruções de Testes Python

O comando deve adicionar a seguinte seção ao `CLAUDE.md`:

```markdown
# Python Testing Standards

**IMPORTANTE**: Este projeto utiliza o plugin `python-test-generator` para criação automática de testes Python com padrões consistentes.

## 📋 Padrões de Testes

### ✅ Framework de Testes

**Framework Principal**: [pytest/unittest/nose - detectado automaticamente]

**Bibliotecas de Teste**:
- Testing framework: pytest/unittest
- Mocking: pytest-mock, unittest.mock
- Coverage: pytest-cov
- Async: pytest-asyncio (se aplicável)
- Parallel: pytest-xdist (se aplicável)

### 📁 Estrutura de Diretórios

```
projeto/
├── src/                    # Código fonte
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/                  # Testes
│   ├── __init__.py
│   ├── conftest.py        # Fixtures globais
│   ├── unit/              # Testes unitários
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/       # Testes de integração
│   └── e2e/              # Testes end-to-end
└── pytest.ini            # Configuração pytest
```

### 🎯 Convenções de Nomenclatura

**Arquivos de Teste**:
- Pattern: `test_*.py` ou `*_test.py`
- Espelhar estrutura do código: `src/services/user.py` → `tests/unit/test_services_user.py`

**Funções de Teste**:
- Pattern: `test_<funcao>_<cenario>()`
- Exemplos:
  - `test_calculate_discount_valid_input()`
  - `test_calculate_discount_invalid_percentage()`
  - `test_calculate_discount_zero_price()`

**Classes de Teste**:
- Pattern: `Test<NomeDaClasse>`
- Exemplo: `TestUserService`, `TestOrderModel`

### 📝 AAA Pattern (Arrange-Act-Assert)

**Sempre seguir AAA pattern**:

```python
def test_process_order_with_valid_data():
    """Deve processar pedido válido com sucesso"""
    # Arrange - Preparar dados e mocks
    order_data = {"id": 1, "total": 100}
    mock_db = MagicMock()
    mock_db.save.return_value = True

    # Act - Executar ação
    result = process_order(order_data, db=mock_db)

    # Assert - Validar resultado
    assert result.status == "success"
    assert result.order_id == 1
    mock_db.save.assert_called_once_with(order_data)
```

### 🎭 Padrões de Mock

#### Mock de APIs Externas

```python
@pytest.fixture
def mock_external_api(mocker):
    """Mock de API externa"""
    mock = mocker.patch('module.external_api.call')
    mock.return_value = {"status": "ok", "data": []}
    return mock

def test_fetch_data_from_api(mock_external_api):
    """Deve buscar dados da API mockada"""
    # Arrange
    mock_external_api.return_value = {"data": [1, 2, 3]}

    # Act
    result = fetch_data()

    # Assert
    assert len(result) == 3
    mock_external_api.assert_called_once()
```

#### Mock de Banco de Dados

```python
@pytest.fixture
def mock_db_session(mocker):
    """Mock de sessão de banco de dados"""
    mock_session = mocker.MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    return mock_session

def test_create_user_new_email(mock_db_session):
    """Deve criar usuário com email novo"""
    # Arrange
    user_data = {"email": "test@example.com", "name": "Test"}

    # Act
    result = create_user(user_data, db=mock_db_session)

    # Assert
    assert result.email == "test@example.com"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
```

#### Mock de Variáveis Module-Level

```python
# ⚠️ IMPORTANTE: Variáveis module-level requerem patch especial

# src/config.py
MAX_RETRIES = 3  # Variável module-level

# tests/test_config.py
@patch("src.config.MAX_RETRIES", 5)  # ✅ Correto
def test_with_custom_retries():
    from src.config import MAX_RETRIES
    assert MAX_RETRIES == 5

# ❌ ERRADO: Não funciona com variáveis module-level
@patch.dict(os.environ, {"MAX_RETRIES": "5"})
def test_wrong_approach():
    # Isso NÃO altera a variável module-level
    pass
```

### 🔗 Padrões Específicos por Framework

#### LangChain / LangGraph

**Mock de Chains com Pipe Operators**:

```python
# ⚠️ CRÍTICO: Cada | requer um __or__ mock

def test_langchain_chain_with_pipes(mocker):
    """Deve executar chain com múltiplos pipes"""
    # Arrange - Mock CADA componente
    mock_prompt = mocker.MagicMock()
    mock_llm = mocker.MagicMock()
    mock_parser = mocker.MagicMock()

    # Mock do pipe operator (|)
    mock_prompt.__or__ = mocker.MagicMock(return_value=mock_llm)
    mock_llm.__or__ = mocker.MagicMock(return_value=mock_parser)

    # Mock do invoke
    mock_parser.invoke.return_value = {"output": "result"}

    # Act
    chain = mock_prompt | mock_llm | mock_parser
    result = chain.invoke({"input": "test"})

    # Assert
    assert result["output"] == "result"
```

**Mock de LangGraph StateGraph**:

```python
@pytest.fixture
def mock_state_graph(mocker):
    """Mock de StateGraph do LangGraph"""
    mock_graph = mocker.MagicMock()
    mock_graph.invoke.return_value = {"final_state": "completed"}
    return mock_graph

def test_graph_execution(mock_state_graph):
    """Deve executar graph com sucesso"""
    result = mock_state_graph.invoke({"initial_state": "start"})
    assert result["final_state"] == "completed"
```

#### FastAPI

**Mock de Dependências**:

```python
from fastapi.testclient import TestClient

def override_get_db():
    """Override de dependência de DB"""
    db = MagicMock()
    yield db

app.dependency_overrides[get_db] = override_get_db

def test_create_item_endpoint():
    """Deve criar item via endpoint"""
    client = TestClient(app)
    response = client.post("/items", json={"name": "test"})
    assert response.status_code == 201
```

#### AWS / Boto3

**Mock de Serviços AWS**:

```python
@pytest.fixture
def mock_s3_client(mocker):
    """Mock de cliente S3"""
    mock_client = mocker.MagicMock()
    mock_client.upload_file.return_value = None
    mock_client.download_file.return_value = None
    mocker.patch('boto3.client', return_value=mock_client)
    return mock_client

def test_upload_to_s3(mock_s3_client):
    """Deve fazer upload para S3"""
    upload_to_s3("file.txt", "bucket", "key")
    mock_s3_client.upload_file.assert_called_once()
```

### 🧪 Fixtures e Reutilização

**conftest.py - Fixtures Globais**:

```python
# tests/conftest.py

import pytest

@pytest.fixture
def sample_user():
    """Usuário de exemplo para testes"""
    return {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User"
    }

@pytest.fixture
def mock_db_session(mocker):
    """Mock de sessão de banco de dados"""
    return mocker.MagicMock()

@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset automático de estado global"""
    # Setup
    yield
    # Teardown
    # Limpar cache, variáveis globais, etc.
```

**Reutilizar Fixtures**:

```python
def test_create_user(sample_user, mock_db_session):
    """Deve criar usuário usando fixtures reutilizáveis"""
    result = create_user(sample_user, db=mock_db_session)
    assert result.email == sample_user["email"]
```

### 🔄 Testes Paralelos (pytest-xdist)

**Garantir segurança em execução paralela**:

```python
# ✅ BOM: Cada teste independente
def test_isolated_function():
    result = pure_function(input_data)
    assert result == expected

# ❌ RUIM: Compartilha estado global
global_counter = 0

def test_with_global_state():
    global global_counter
    global_counter += 1  # ⚠️ Race condition!
    assert global_counter == 1

# ✅ CORRETO: Usar fixtures autouse para isolar
@pytest.fixture(autouse=True)
def reset_counter():
    global global_counter
    global_counter = 0
    yield
    global_counter = 0
```

### 🧹 Cleanup de Recursos

**Sempre fazer cleanup de recursos**:

```python
@pytest.fixture
def db_connection():
    """Conexão de DB com cleanup automático"""
    # Setup
    conn = create_connection()
    yield conn
    # Teardown
    conn.close()  # ✅ SEMPRE fechar

@pytest.fixture
def temp_file():
    """Arquivo temporário com cleanup"""
    # Setup
    file_path = "/tmp/test_file.txt"
    with open(file_path, "w") as f:
        f.write("test")
    yield file_path
    # Teardown
    if os.path.exists(file_path):
        os.remove(file_path)  # ✅ SEMPRE remover
```

### 📊 Cobertura de Testes

**Threshold**: ≥ 80% (configurável)

**Executar com cobertura**:

```bash
# Executar testes com relatório de cobertura
pytest --cov=src --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=src --cov-report=html

# Falhar se cobertura < 80%
pytest --cov=src --cov-fail-under=80
```

**pytest.ini**:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=src
    --cov-report=term-missing
    --cov-fail-under=80
    -v
```

## ⚙️ Configuração Pytest

**RECOMENDAÇÃO**: Após configurar CLAUDE.md, execute `/setup-pytest-config` para configurar pytest automaticamente.

```bash
# Configurar pytest (pyproject.toml ou pytest.ini)
/setup-pytest-config
```

Este comando:
- ✅ Cria/atualiza `[tool.pytest.ini_options]` em pyproject.toml (preferencial)
- ✅ Cria `pytest.ini` se pyproject.toml não existir
- ✅ Configura coverage, parallel, markers automaticamente
- ✅ Detecta stack Python e customiza configuração

**Exemplo de configuração gerada**:

```toml
# pyproject.toml (PREFERENCIAL)
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
    "-n auto",  # Parallel com pytest-xdist
]

markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

asyncio_mode = "auto"  # Se async detectado
```

```ini
# pytest.ini (FALLBACK - só se pyproject.toml não existir)
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    --cov=src
    --cov-report=term-missing
    --cov-fail-under=80
    -v
    -n auto

markers =
    unit: Unit tests
    integration: Integration tests

asyncio_mode = auto
```

**Ordem de Prioridade**:
1. ✅ **pyproject.toml** (recomendado - padrão moderno Python PEP 518)
2. pytest.ini (fallback - só se pyproject.toml não existir)
3. setup.cfg (legado)

## 🎯 Plugin Python Test Generator

Este projeto usa o plugin `python-test-generator` com os seguintes recursos:

**Comandos**:
- `/py-test` - Gera testes Python automaticamente em paralelo
- `/setup-pytest-config` - Configura pytest (pyproject.toml ou pytest.ini)
- `/setup-project-tests` - Configura CLAUDE.md com padrões de testes

**Agente**:
- `test-assistant` - Especialista em testes Python com mocks avançados

**Skill**:
- `langchain-test-specialist` - Expertise em mocks de LangChain/LangGraph

**Padrões Avançados**:
- Mock de chains LangChain com pipe operators (`|`)
- Mock de variáveis module-level
- Fixtures reutilizáveis (conftest.py)
- Testes paralelos seguros (pytest-xdist)
- Cleanup automático de recursos
- AAA pattern (Arrange-Act-Assert)

**Performance**:
- ⚡ Criação paralela de múltiplos arquivos de teste
- 📊 Até 80% mais rápido que criação sequencial
- 🔄 Validação automática de cobertura

---

**Filosofia**: Testes Rápidos > Testes Lentos | Mocks > Chamadas Reais | AAA Pattern > Código Confuso
```

### 3. Adicionar Contexto do Projeto (Se Fornecido)

Se o usuário fornecer descrição da stack, adicionar seção customizada:

```markdown
## 📊 Contexto Deste Projeto

**Stack Python**: [stack fornecida pelo usuário]

**Frameworks de Teste Recomendados**:
- Framework principal: [pytest/unittest]
- Mocking: [pytest-mock/unittest.mock]
- Coverage: [pytest-cov/coverage.py]
- Async: [pytest-asyncio]

**Mocks Específicos da Stack**:
- [LangChain]: Mock de chains, agents, tools
- [FastAPI]: Mock de dependências, TestClient
- [Django]: Mock de ORM, views, middleware
- [AWS]: Mock de boto3, serviços AWS

**Fixtures Recomendadas**:
- Fixtures de banco de dados
- Fixtures de autenticação
- Fixtures de APIs externas
```

### 4. Detectar Stack Python do Projeto

Analisar projeto para customizar instruções:

- Verificar `requirements.txt`, `pyproject.toml`, `Pipfile`
- Detectar frameworks: FastAPI, Django, Flask, LangChain, LangGraph
- Identificar gerenciador de pacotes: pip, poetry, pipenv, uv
- Localizar `conftest.py` e fixtures existentes
- Verificar `pytest.ini` ou `setup.cfg`

**Adicionar ao CLAUDE.md**:

```markdown
## 🔧 Stack Python Detectada

**Gerenciador de Pacotes**: [pip/poetry/pipenv/uv]
**Framework de Testes**: [pytest/unittest/nose]
**Framework Web**: [FastAPI/Django/Flask]
**Bibliotecas Especiais**: [LangChain, boto3, sqlalchemy, etc.]

**Fixtures Existentes** (conftest.py):
- [listar fixtures encontradas]

**Padrões de Mock Detectados**:
- [analisar testes existentes]
```

### 5. Confirmar com Usuário

Mostrar preview do que será adicionado:

```
═══════════════════════════════════════════
📝 SETUP PYTHON TESTING
═══════════════════════════════════════════

Arquivo: CLAUDE.md

Ação: [CRIAR NOVO / ADICIONAR SEÇÃO]

Stack Python Detectada:
- Gerenciador: [poetry/pip/pipenv/uv]
- Framework: [pytest/unittest]
- Web Framework: [FastAPI/Django/Flask]
- Bibliotecas: [LangChain, boto3, etc.]

Fixtures Existentes:
- conftest.py encontrado
- [X] fixtures detectadas

Conteúdo a ser adicionado:
---
[Preview das instruções]
---

Adicionar ao CLAUDE.md? (s/n)
```

### 6. Criar/Atualizar Arquivo

Se usuário confirmar:
- Criar ou atualizar CLAUDE.md
- Adicionar instruções completas
- Preservar conteúdo existente (NUNCA sobrescrever)
- Validar que arquivo foi criado corretamente

```
✅ CLAUDE.md configurado com sucesso!

Instruções de testes Python adicionadas.

Stack Python detectada:
- Gerenciador: poetry
- Framework: pytest
- Web Framework: FastAPI
- Bibliotecas: LangChain, boto3, sqlalchemy

Fixtures encontradas:
- conftest.py com 5 fixtures

Próximos passos:
1. Revisar CLAUDE.md
2. Customizar fixtures (se necessário)
3. Executar: /py-test
4. Validar cobertura: pytest --cov

Claude agora está orientado a:
✓ Gerar testes Python seguindo padrões do projeto
✓ Reutilizar fixtures existentes (conftest.py)
✓ Criar mocks adequados (LangChain, FastAPI, AWS)
✓ Aplicar AAA pattern consistentemente
✓ Garantir testes paralelos seguros
```

## 📚 Exemplos de Uso

### Exemplo 1: Novo Projeto Python

```bash
/setup-project-tests "API FastAPI com PostgreSQL"
```

**Resultado**:
- Cria `CLAUDE.md` na raiz do projeto
- Adiciona padrões pytest + FastAPI
- Configura mocks de banco de dados
- Define estrutura de diretórios de testes
- Orienta sobre TestClient FastAPI

### Exemplo 2: Projeto LangChain Existente

```bash
/setup-project-tests "LangChain + LangGraph com OpenAI"
```

**Resultado**:
- Detecta `CLAUDE.md` existente
- Adiciona seção de testes ao final
- Preserva conteúdo existente
- Inclui padrões de mock LangChain (pipe operators)
- Configura mock de chains e agents

### Exemplo 3: Projeto Django

```bash
/setup-project-tests "Django REST Framework + Celery"
```

**Resultado**:
- Adiciona padrões de teste Django
- Configura fixtures de banco de dados Django
- Orienta sobre mock de tasks Celery
- Define testes de views/serializers/models

## ⚠️ Importante

### Não Sobrescrever Conteúdo Existente

Se `CLAUDE.md` já existe:
- ❌ NUNCA sobrescrever conteúdo
- ✅ SEMPRE adicionar ao final
- ✅ Usar separador claro: `---`

### Detectar Stack Python

Analisar projeto para customizar instruções:
- Verificar `requirements.txt`, `pyproject.toml`, `Pipfile`
- Detectar frameworks de teste em uso
- Identificar bibliotecas que requerem mocks especiais
- Localizar fixtures existentes (conftest.py)

### Validar Sintaxe Markdown

Após criar/atualizar:
- Verificar que markdown está válido
- Headers bem formatados
- Code blocks Python com syntax highlighting
- Links funcionando

## 🚀 Após Executar Este Comando

O usuário terá:

1. ✅ `CLAUDE.md` configurado com padrões de testes Python
2. ✅ Claude orientado a seguir AAA pattern
3. ✅ Mocks adequados para frameworks usados
4. ✅ Reutilização de fixtures existentes
5. ✅ Estrutura de diretórios padronizada

**Próximo passo**: Executar `/py-test` para gerar testes automaticamente!

## 💡 Dica

Após configurar o projeto, sempre valide cobertura de testes:

```bash
# Gerar testes automaticamente
/py-test

# Executar com cobertura
pytest --cov=src --cov-report=term-missing

# Verificar que cobertura ≥ 80%
pytest --cov-fail-under=80
```

Isso garantirá qualidade consistente e detecção precoce de bugs.