# 🐍 Python Test Generator

Plugin de geração automática de testes unitários Python com análise de cobertura e **criação paralela** de arquivos para máxima performance.

## 📋 Descrição

O **Python Test Generator** é um plugin especializado que analisa a cobertura de testes do seu projeto Python e **cria automaticamente múltiplos testes em paralelo**, gerando testes unitários completos, bem estruturados e com alta qualidade, seguindo os padrões e frameworks já utilizados no projeto.

### 🎯 Principais Recursos

- ⚡ **Criação Paralela**: Gera múltiplos arquivos de teste simultaneamente (até 80% mais rápido)
- ✅ **Detecção Automática Python**: Identifica frameworks, estrutura e padrões do projeto Python
- ✅ **Análise de Cobertura**: Executa e analisa cobertura atual automaticamente
- ✅ **Criação Inteligente**: Gera testes Python seguindo AAA pattern e padrões do projeto
- ✅ **Suporte Multi-Framework Python**: pytest, unittest, nose, FastAPI, Django, LangChain, etc.
- ✅ **Mocks Automáticos Python**: Cria mocks corretos de APIs, DB, LLM e outras dependências
- ✅ **Modo Empírico**: Executa sem perguntas, totalmente automatizado
- ✅ **Reutilização**: Aproveita fixtures e factories Python existentes
- ✅ **Validação**: Executa testes criados e valida cobertura alcançada

---

## 🚀 Instalação

Este plugin faz parte do repositório **claudecode_plugins**. Para usá-lo:

```bash
# 1. Clone ou atualize o repositório
git pull origin main

# 2. Recarregue plugins no Claude Code
/plugin refresh

# 3. Verifique se o plugin está disponível
/plugin list
```

---

## 📖 Uso

### `/setup-project-tests`

**Configura CLAUDE.md do projeto** com padrões de testes Python.

**O que faz**:
- ✅ Cria ou atualiza `CLAUDE.md` na raiz do projeto
- ✅ Adiciona padrões de testes Python (AAA pattern, mocks, fixtures)
- ✅ Configura frameworks detectados (pytest, unittest, nose)
- ✅ Documenta padrões de mock (LangChain, FastAPI, Django, AWS)
- ✅ Orienta sobre fixtures reutilizáveis (conftest.py)
- ✅ Preserva conteúdo existente (não sobrescreve)
- ✅ Detecta stack Python automaticamente

**Uso**:
```bash
# Setup básico (detecta stack automaticamente)
/setup-project-tests

# Ou com descrição da stack
/setup-project-tests "API FastAPI com LangChain + PostgreSQL"
```

**Resultado**:
Claude ficará automaticamente orientado a:
- Gerar testes Python seguindo padrões do projeto
- Reutilizar fixtures existentes (conftest.py)
- Criar mocks adequados (LangChain chains, FastAPI, AWS boto3)
- Aplicar AAA pattern consistentemente
- Garantir testes paralelos seguros (pytest-xdist)

**Quando usar**:
- ✅ No início de novos projetos Python
- ✅ Ao adicionar este plugin em projetos existentes
- ✅ Quando quiser padronizar testes no time

---

### Comando Principal: `/py-test`

Analisa cobertura e **cria testes Python em paralelo** automaticamente:

```bash
# Analisar projeto Python inteiro (padrão)
/py-test

# Analisar diretório específico
/py-test src/meu_modulo

# Definir threshold customizado (padrão: 80%)
/py-test --threshold 85
```

### O que acontece automaticamente:

1. **Detecta** framework de testes Python (pytest/unittest/nose)
2. **Identifica** gerenciador de pacotes Python (poetry/pipenv/uv/pip)
3. **Analisa** cobertura atual do projeto Python
4. **Identifica** módulos Python com cobertura < 80%
5. **Lê** fixtures e padrões Python existentes (conftest.py)
6. **Cria testes em PARALELO** - múltiplos arquivos simultaneamente (⚡ até 80% mais rápido)
7. **Executa** testes criados e valida cobertura
8. **Reporta** resultados detalhados

### ⚡ Performance com Paralelização

O plugin cria **múltiplos arquivos de teste simultaneamente**:
- **5 módulos sem testes** → Cria 5 arquivos em paralelo
- **10 módulos sem testes** → Cria 10 arquivos em paralelo
- **Redução de tempo**: Até 80% mais rápido que criação sequencial

---

## 🎯 Casos de Uso

### Caso 1: Projeto Simples com Pytest

**Cenário**: Projeto Python com pytest, cobertura atual de 65%

```bash
/test-coverage
```

**Resultado**:
```
═══════════════════════════════════════════
✅ ANÁLISE DE TESTES CONCLUÍDA
═══════════════════════════════════════════

📊 COBERTURA GERAL:
Antes:  65.0%
Depois: 85.0%
Delta:  +20.0%

📁 ARQUIVOS DE TESTE CRIADOS:
├─ tests/unit/test_calculator.py (8 testes)
├─ tests/unit/test_validator.py (12 testes)
└─ tests/unit/test_parser.py (6 testes)

Total: 26 novos testes

📈 MÓDULOS COM COBERTURA 80%+:
✅ src/calculator.py - 90.0% (antes: 60.0%)
✅ src/validator.py - 85.0% (antes: 55.0%)
✅ src/parser.py - 82.0% (antes: 70.0%)
```

### Caso 2: Projeto LangChain com Poetry

**Cenário**: Projeto usando LangChain, LangGraph, Poetry, cobertura 50%

```bash
/test-coverage
```

**O plugin detecta automaticamente**:
- Framework: pytest com poetry
- Bibliotecas: langchain, langgraph
- Padrão: Nodes, Chains, Agents com LLM

**Cria testes específicos**:
```python
@patch("workflow.nodes.node_processar.ChatOpenAI")
@patch("workflow.nodes.node_processar.ChatPromptTemplate.from_template")
def test_node_processar_com_sucesso(
    self,
    mock_prompt,
    mock_chat,
    sample_state,  # Fixture do conftest.py
):
    """Teste: Node processa conversa com LLM mockado"""
    # Arrange
    mock_llm = Mock()
    mock_chain = Mock()
    mock_chain.invoke.return_value = {"resultado": "processado"}
    mock_prompt.return_value.__or__ = Mock(return_value=mock_chain)
    mock_chat.return_value = mock_llm

    # Act
    result = node_processar(sample_state)

    # Assert
    assert result is not None
    assert "resultado" in result
    mock_chat.assert_called_once()
```

### Caso 3: Projeto FastAPI

**Cenário**: API REST com FastAPI, endpoints sem testes

```bash
/test-coverage
```

**Cria testes de API**:
```python
from fastapi.testclient import TestClient

class TestUserAPI:
    """Testes para endpoints de usuários"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_get_users_success(self, client):
        """Teste: GET /users retorna lista de usuários"""
        # Act
        response = client.get("/api/users")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch("api.routes.users.get_current_user")
    def test_create_user_authenticated(self, mock_auth, client):
        """Teste: POST /users requer autenticação"""
        # Arrange
        mock_auth.return_value = {"user_id": "123"}

        # Act
        response = client.post(
            "/api/users",
            json={"name": "Test", "email": "test@example.com"},
            headers={"Authorization": "Bearer token"}
        )

        # Assert
        assert response.status_code == 201
```

### Caso 4: Projeto Django

**Cenário**: Aplicação Django com models e views sem testes

```bash
/test-coverage
```

**Cria testes Django**:
```python
import pytest
from django.test import Client

class TestBlogViews:
    """Testes para views do blog"""

    @pytest.mark.django_db
    def test_post_list_view(self, client):
        """Teste: Listagem de posts funciona corretamente"""
        # Arrange
        Post.objects.create(title="Test", content="Content")

        # Act
        response = client.get("/blog/")

        # Assert
        assert response.status_code == 200
        assert "Test" in response.content.decode()

    @pytest.mark.django_db
    def test_create_post_model(self):
        """Teste: Model Post é criado corretamente"""
        # Arrange & Act
        post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            author_id=1
        )

        # Assert
        assert post.pk is not None
        assert post.title == "Test Post"
```

### Caso 5: AWS Lambda

**Cenário**: Lambda handlers sem testes

```bash
/test-coverage
```

**Cria testes de Lambda**:
```python
@patch("main.boto3.client")
@patch("main.os.getenv")
def test_lambda_handler_processa_s3_event(self, mock_env, mock_boto):
    """Teste: Lambda processa evento S3 corretamente"""
    # Arrange
    mock_env.return_value = "test-bucket"
    mock_s3 = Mock()
    mock_s3.get_object.return_value = {
        "Body": Mock(read=lambda: b'{"data": "test"}')
    }
    mock_boto.return_value = mock_s3

    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": "test-bucket"},
                "object": {"key": "test-key"}
            }
        }]
    }
    context = Mock()

    # Act
    response = lambda_handler(event, context)

    # Assert
    assert response["statusCode"] == 200
    mock_s3.get_object.assert_called_once()
```

---

## 🔧 Frameworks e Bibliotecas Suportados

### Testing Frameworks
- ✅ **pytest** (recomendado)
- ✅ **unittest**
- ✅ **nose**

### Package Managers
- ✅ **poetry**
- ✅ **pipenv**
- ✅ **uv**
- ✅ **pip**

### Web Frameworks
- ✅ **FastAPI**
- ✅ **Django**
- ✅ **Flask**

### LLM & AI Frameworks
- ✅ **LangChain**
- ✅ **LangGraph**
- ✅ **LangSmith**

### Cloud & Serverless
- ✅ **AWS Lambda**
- ✅ **boto3 (AWS SDK)**

### Databases
- ✅ **SQLAlchemy**
- ✅ **Django ORM**
- ✅ **Pynamodb**

### HTTP Clients
- ✅ **requests**
- ✅ **httpx**
- ✅ **aiohttp**

### Mock Libraries
- ✅ **unittest.mock**
- ✅ **pytest-mock**
- ✅ **responses**
- ✅ **httpx-mock**

### Async
- ✅ **pytest-asyncio**
- ✅ **asyncio**
- ✅ **AsyncMock**

---

## 🎯 Skills Especializadas

### LangChain Test Specialist

**Nova em v1.3.0**: Skill especializada para criar testes unitários e de integração para aplicações LangChain e LangGraph.

#### Recursos da Skill

Esta skill detecta automaticamente código LangChain/LangGraph e aplica **7 padrões de teste especializados**:

1. **Basic LangGraph Test**: Testes state-based com `MemorySaver` checkpointer
2. **Individual Node Testing**: Testar nodes isoladamente via `graph.nodes["node_name"]`
3. **Partial Execution**: Uso de `update_state()` e `interrupt_after` para testes parciais
4. **Mocking LLM**: `GenericFakeChatModel` para testes unitários sem API calls
5. **Trajectory Match**: Validação de sequência de ações com `agentevals`
6. **LLM-as-Judge**: Avaliação de qualidade usando LLM como juiz
7. **VCR Recording**: Gravar/replay HTTP calls com `pytest-recording`

#### Quando a Skill é Ativada

A skill é invocada automaticamente pelo Claude quando detecta:
- Imports de `langchain`, `langgraph`, ou `langchain_core`
- Uso de `StateGraph`, `MessageGraph`, chains LCEL
- LLM calls (`ChatOpenAI`, `ChatAnthropic`, etc.)
- Agents, tools, ou trajectories
- Pedidos como: "testar chain", "testar grafo", "mock LLM", "trajectory validation"

#### Exemplos de Testes Criados

**Teste de Grafo LangGraph**:
```python
def test_basic_graph_execution():
    """Teste: Grafo executa corretamente com estado inicial"""
    # Arrange
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)

    # Act
    result = compiled_graph.invoke(
        {"my_key": "initial"},
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert
    assert result["my_key"] == "expected_value"
```

**Teste com Mocked LLM**:
```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

def test_node_with_mocked_llm():
    """Teste: Node com LLM mockado retorna respostas esperadas"""
    # Arrange
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(content="Primeira resposta"),
        AIMessage(content="Segunda resposta")
    ]))

    # Act
    result = node_with_llm({"messages": [...]})

    # Assert
    assert result["response"] == "Primeira resposta"
```

**Trajectory Validation com AgentEvals**:
```python
from agentevals.trajectory.match import create_trajectory_match_evaluator

def test_trajectory_strict_match():
    """Teste: Trajectory corresponde exatamente à esperada"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="strict"
    )

    # Act
    evaluation = evaluator(
        outputs=actual_trajectory,
        reference_outputs=reference_trajectory
    )

    # Assert
    assert evaluation["score"] is True
```

**VCR Recording para Integration Tests**:
```python
@pytest.mark.vcr()
def test_agent_with_real_llm_vcr():
    """Teste: Grava chamadas LLM reais na primeira execução, replay depois"""
    # PRIMEIRA EXECUÇÃO: Faz chamadas reais e grava
    # PRÓXIMAS EXECUÇÕES: Replay sem API calls (100% determinístico)

    agent = create_agent()
    result = agent.invoke({"input": "What's the capital of France?"})

    assert "Paris" in result["output"]
```

#### Dependencies Adicionais

Para usar os padrões LangChain/LangGraph, certifique-se de ter:

```bash
# Principais
pip install langchain langchain-core langgraph

# Testing
pip install pytest pytest-asyncio agentevals vcrpy pytest-recording
```

Ou com poetry:
```toml
[tool.poetry.group.test.dependencies]
agentevals = "^0.1.0"      # Trajectory validation
vcrpy = "^6.0.0"            # HTTP recording
pytest-recording = "^0.13.0"  # pytest-vcr integration
```

#### Modos de Trajectory Matching

- **strict**: Ordem e conteúdo idênticos
- **unordered**: Mesmo conteúdo, ordem irrelevante
- **subset**: Trajectory real contém pelo menos as ações esperadas
- **superset**: Trajectory real é subconjunto das ações esperadas

#### LLM-as-Judge Models

Suportados:
- `openai:gpt-4o-mini`, `openai:o3-mini`
- `anthropic:claude-3-5-sonnet`, `anthropic:claude-3-5-haiku`

---

## 📝 Padrões de Teste Criados

### AAA Pattern (Arrange-Act-Assert)

Todos os testes seguem o padrão AAA:

```python
def test_exemplo(self):
    """Teste: Descrição clara do cenário"""
    # Arrange - Preparar dados e mocks
    data = {"key": "value"}
    mock_api.return_value = {"result": "ok"}

    # Act - Executar a função/método
    result = function_under_test(data)

    # Assert - Validar resultado
    assert result is not None
    assert result["status"] == "ok"
    mock_api.assert_called_once()
```

### Happy Path + Erros + Edge Cases

Cada função recebe pelo menos 3 tipos de testes:

```python
# 1. Happy path - Cenário de sucesso
def test_process_data_success(self):
    """Teste: Processa dados válidos com sucesso"""
    ...

# 2. Error handling - Tratamento de erros
def test_process_data_invalid_input(self):
    """Teste: Lida corretamente com entrada inválida"""
    with pytest.raises(ValueError):
        ...

# 3. Edge cases - Casos extremos
@pytest.mark.parametrize("input,expected", [
    (None, False),
    ("", False),
    ([], False),
    ({}, False),
])
def test_process_data_edge_cases(self, input, expected):
    """Teste: Lida com casos extremos"""
    ...
```

### Mocks de Dependências Externas

Todas as dependências externas são mockadas:

```python
@patch("module.requests.get")  # HTTP
@patch("module.boto3.client")  # AWS
@patch("module.ChatOpenAI")    # LLM
@patch("module.db.session")    # Database
def test_with_all_mocks(self, mock_db, mock_llm, mock_aws, mock_http):
    """Teste: Todas as dependências externas mockadas"""
    ...
```

---

## 🎓 Recursos Avançados

### Detecção Automática de Fixtures

O plugin lê automaticamente `conftest.py` e reutiliza fixtures:

```python
# conftest.py
@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Test User"}

# Teste criado automaticamente usa a fixture
def test_get_user(self, sample_user):
    """Teste: Buscar usuário usa fixture existente"""
    result = get_user(sample_user["id"])
    assert result["name"] == sample_user["name"]
```

### Parametrização Inteligente

Cria testes parametrizados quando identifica múltiplos casos:

```python
@pytest.mark.parametrize("input_value,expected_output", [
    ("valid@email.com", True),
    ("invalid-email", False),
    ("", False),
    (None, False),
    ("test@", False),
    ("@test.com", False),
])
def test_validate_email_parametrized(self, input_value, expected_output):
    """Teste: Validação de email com múltiplos casos"""
    result = validate_email(input_value)
    assert result == expected_output
```

### Suporte a Código Assíncrono

Detecta e cria testes assíncronos corretamente:

```python
@pytest.mark.asyncio
@patch("module.async_http_client")
async def test_fetch_data_async(self, mock_client):
    """Teste: Função assíncrona funciona corretamente"""
    # Arrange
    mock_client.get.return_value = AsyncMock(
        return_value={"data": "test"}
    )

    # Act
    result = await fetch_data_async()

    # Assert
    assert result == {"data": "test"}
```

### Mocks Específicos de LangChain

Cria mocks corretos para LangChain patterns:

```python
@patch("module.ChatPromptTemplate.from_template")
@patch("module.ChatOpenAI")
def test_langchain_chain(self, mock_chat, mock_prompt):
    """Teste: Chain LangChain funciona corretamente"""
    # Arrange - Mock de chain com pipe operator
    mock_llm = Mock()
    mock_chain = Mock()
    mock_chain.invoke.return_value = {"output": "result"}
    mock_prompt.return_value.__or__ = Mock(return_value=mock_chain)
    mock_chat.return_value = mock_llm

    # Act
    result = process_with_chain(data)

    # Assert
    assert result["output"] == "result"
    mock_chain.invoke.assert_called_once()
```

---

## 📊 Configuração de Cobertura

### Threshold Padrão

- **Cobertura mínima global**: 80%
- **Cobertura ideal**: 85-90%
- **Arquivos críticos**: 90%+

### Customização via Arquivos de Configuração

O plugin respeita configurações existentes:

**pytest.ini**:
```ini
[pytest]
addopts = --cov=src --cov-report=term-missing --cov-fail-under=80
```

**pyproject.toml**:
```toml
[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

**setup.cfg**:
```cfg
[coverage:report]
fail_under = 80
```

**.coveragerc**:
```ini
[report]
fail_under = 80
omit =
    */tests/*
    */migrations/*
```

---

## ⚡ Modo Empírico

Este plugin opera em **modo empírico** - executa automaticamente sem perguntas.

### O que NÃO faz:
- ❌ Não pergunta qual framework usar
- ❌ Não pergunta quais módulos testar
- ❌ Não pergunta se deve criar testes
- ❌ Não pergunta se deve executar testes

### O que FAZ:
- ✅ Detecta automaticamente todo o ambiente
- ✅ Analisa cobertura imediatamente
- ✅ Cria testes diretamente
- ✅ Executa testes automaticamente
- ✅ Reporta resultados ao final

---

## 🐛 Troubleshooting

### Problema: Import errors em testes criados

**Causa**: Estrutura de imports ou `sys.path` incorreta

**Solução automática**: O plugin ajusta imports e adiciona `__init__.py` quando necessário

### Problema: Mocks não funcionam

**Causa**: Path de mocking incorreto

**Solução automática**: O plugin corrige paths de mocking e adiciona `spec` quando necessário

### Problema: Testes assíncronos não executam

**Causa**: Falta `@pytest.mark.asyncio`

**Solução automática**: O plugin adiciona markers e instala `pytest-asyncio` se necessário

### Problema: Fixtures não encontradas

**Causa**: `conftest.py` ausente ou mal localizado

**Solução automática**: O plugin move fixtures para local correto

---

## 📚 Componentes do Plugin

### Command: `/test-coverage`
Comando principal que invoca o agente especializado

**Localização**: `commands/test-coverage.md`

### Agent: `test-assistant`
Agente especializado em análise e criação de testes

**Localização**: `agents/test-assistant.md`

**Especialidades**:
- Detecção de ambiente e frameworks
- Análise de cobertura
- Criação de testes seguindo padrões
- Mocks inteligentes
- Validação de qualidade

---

## 🚀 Roadmap

Funcionalidades planejadas para versões futuras:

- [ ] Suporte a mais frameworks de teste (Robot Framework, Behave)
- [ ] Testes de integração automáticos
- [ ] Testes E2E com Playwright/Selenium
- [ ] Mutation testing
- [ ] Performance testing
- [ ] Geração de relatórios HTML customizados
- [ ] Integração com CI/CD (GitHub Actions, GitLab CI)
- [ ] Suporte a TypeScript/JavaScript
- [ ] Dashboard de cobertura

---

## 📄 Licença

MIT License - Carlos Araujo

---

## 👤 Autor

**Carlos Araujo**
- Email: cadu.gevaerd@gmail.com
- GitHub: [@cadugevaerd](https://github.com/cadugevaerd)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/cadugevaerd/claudecode_plugins/issues)
- **Documentação**: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins)

---

**Desenvolvido com ❤️ para Claude Code Community**