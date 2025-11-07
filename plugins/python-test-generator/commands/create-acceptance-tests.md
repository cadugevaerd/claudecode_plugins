---
description: Cria testes de aceitação validando features/slices completas com BDD patterns
allowed-tools: Read, Write, Grep, Glob, Skill, Bash
model: claude-sonnet-4-5
argument-hint: '[TARGET_PATH] [--framework behave|pytest-bdd|pytest]'
---

# Create Acceptance Tests

Especialista em criar testes de aceitação para validar features/slices completas, usando BDD patterns (Given-When-Then) e frameworks Python apropriados.

## 🎯 Objetivo

- Criar acceptance tests que validam comportamento end-to-end de features/slices
- Aplicar padrões BDD (Given-When-Then) para testes compreensíveis
- Escolher framework apropriado (behave, pytest-bdd ou pytest puro)
- Estruturar testes baseados em acceptance criteria e user stories
- Garantir testes independentes, determinísticos e focados em comportamento

## ⚠️ RESTRIÇÕES CRÍTICAS

**❌ NUNCA modificar código de produção** (arquivos em `src/`, `app/`, etc.)
**✅ APENAS criar/modificar:**

- Arquivos de teste em `tests/acceptance/`
- Features files `.feature` (se behave ou pytest-bdd)
- Step definitions e fixtures em `tests/`
- Configuração em `pyproject.toml` ou `pytest.ini`

**Se precisar de mudanças no código de produção:**

- ❌ NÃO modificar diretamente
- ✅ Reportar ao usuário quais mudanças são necessárias
- ✅ Deixar usuário decidir se implementa

## 🔧 Instruções

### 1. **Consultar Skills (OBRIGATÓRIO)**

1.1 **Consultar Skill create-acceptance-tests (OBRIGATÓRIO)**

- **SEMPRE** usar `Skill` tool para consultar `create-acceptance-tests` antes de gerar testes
- Extrair princípios: BDD, Given-When-Then, frameworks (behave, pytest-bdd, pytest)
- Identificar acceptance criteria SMART (Specific, Measurable, Achievable, Relevant, Testable)
- Verificar best practices: black-box testing, user perspective, business-focused

1.2 **Consultar Skill langchain-test-specialist (SE APLICÁVEL)**

- Se projeto usa LangChain/LangGraph: consultar `langchain-test-specialist`
- Extrair padrões de mock para chains/graphs (GenericFakeChatModel)
- Adaptar acceptance tests para testar agentic workflows

### 2. **Analisar Projeto e Escolher Framework**

2.1 **Detectar Framework Existente**

- Verificar se projeto já usa behave, pytest-bdd ou pytest
- Verificar arquivos existentes: `.feature`, `conftest.py`, `pyproject.toml`
- Se framework já definido: usar o mesmo

2.2 **Escolher Framework (se novo projeto)**

Usar guia de seleção da skill:

- **behave**: Se stakeholders não-técnicos envolvidos, documentação viva prioritária
- **pytest-bdd**: Se já usa pytest, quer BDD com flexibilidade pytest
- **pytest puro**: Se equipe técnica, máxima flexibilidade, sem stakeholders não-técnicos

2.3 **Identificar Features/Slices a Testar**

- Se `TARGET_PATH` fornecido: focar nesse módulo/feature
- Se não fornecido: analisar projeto para identificar features principais
- Priorizar features críticas de negócio

### 3. **Definir Acceptance Criteria**

3.1 **Extrair User Stories**

- Analisar README, BACKLOG, ou documentação para user stories
- Se não disponível: inferir user stories do código (docstrings, comments)

3.2 **Estruturar Acceptance Criteria (SMART)**

- **S**pecific: Bem definidos e precisos
- **M**easurable: Verificáveis automaticamente
- **A**chievable: Implementáveis com recursos disponíveis
- **R**elevant: Alinhados com requisitos de negócio
- **T**estable: Automatizáveis com framework escolhido

### 4. **Gerar Acceptance Tests**

4.1 **Estrutura Given-When-Then**

Todos os testes devem seguir padrão:

```python
# Given - Setup inicial / pré-condições
# When - Ação/evento que ocorre
# Then - Resultado esperado / pós-condições
```

4.2 **Características dos Acceptance Tests**

- ✅ **Black-box**: Testa comportamento observável (não implementação)
- ✅ **User perspective**: Do ponto de vista do usuário final
- ✅ **Business-focused**: Baseado em acceptance criteria
- ✅ **End-to-end**: Testa fluxos completos (não unidades)
- ✅ **Independent**: Cada teste roda isolado
- ✅ **Deterministic**: Sem flakiness
- ✅ **Readable**: Compreensível por stakeholders
- ❌ **Não testa**: Detalhes de implementação, código interno

4.3 **Padrões por Framework**

**behave (BDD Gherkin)**:

```gherkin
Feature: User Authentication
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid credentials
    Then I should be redirected to dashboard
```

**pytest-bdd**:

```python
from pytest_bdd import scenarios, given, when, then

scenarios('login.feature')

@given('the login page is displayed')
def login_page(browser):
    browser.get('/login')
```

**pytest puro**:

```python
def test_successful_login_redirects_to_dashboard(app_client, valid_user):
    """
    Given a registered user with valid credentials
    When the user submits the login form
    Then the user should be redirected to dashboard
    """
    # Given
    username, password = valid_user

    # When
    response = app_client.post('/login', data={...})

    # Then
    assert response.status_code == 200
    assert b'Dashboard' in response.data
```

### 5. **Organizar e Salvar Testes**

5.1 **Estrutura de Diretórios**

```
tests/acceptance/
├── features/              # behave
│   ├── steps/
│   │   └── feature_steps.py
│   └── feature.feature
├── test_acceptance/       # pytest-bdd or pytest
│   ├── conftest.py
│   └── test_feature.py
└── fixtures/
    └── test_data.py
```

5.2 **Naming Conventions**

- **behave**: `features/feature_name.feature`, `steps/feature_steps.py`
- **pytest-bdd**: `test_acceptance/feature.feature`, `test_acceptance/test_feature.py`
- **pytest**: `test_acceptance/test_feature_acceptance.py`

5.3 **Configurar Framework**

- Instalar dependências: `behave`, `pytest-bdd`, ou apenas `pytest`
- Configurar `pyproject.toml` ou `pytest.ini`
- Criar fixtures base em `conftest.py`

### 6. **Validar e Reportar**

6.1 **Executar Testes Gerados**

- **behave**: `behave tests/acceptance/features/`
- **pytest-bdd/pytest**: `pytest tests/acceptance/ -v`
- Validar que todos passam
- Medir tempo de execução total

6.2 **Reportar Resultados**

- Listar testes criados
- Mostrar framework usado
- Mostrar features/scenarios cobertos
- Indicar próximos passos (commit, CI/CD)

## 📊 Formato de Saída

**Durante execução:**

```text
🔍 Consultando skill create-acceptance-tests (OBRIGATÓRIO)...
✅ Princípios de acceptance testing carregados
✅ Padrões identificados: BDD, Given-When-Then, SMART criteria

🔍 Verificando skills complementares...
✅ Skill langchain-test-specialist encontrada (projeto usa LangChain)

📂 Analisando projeto em: src/features/authentication
✅ Framework detectado: pytest (ou behave/pytest-bdd)
✅ 2 features identificadas: login, logout

🧪 Gerando acceptance tests:
  ✅ test_acceptance_auth.py (4 scenarios)
     • test_successful_login_redirects_to_dashboard()
     • test_invalid_credentials_show_error()
     • test_logout_clears_session()
     • test_unauthorized_access_redirects_to_login()

⚡ Executando testes gerados...
  ✅ 4/4 testes passaram
  ⏱️ Tempo total: 18.2s
```

**Saída final:**

```text
═══════════════════════════════════════════
✅ ACCEPTANCE TESTS CRIADOS COM SUCESSO
═══════════════════════════════════════════

📊 RESUMO:
├─ Framework: pytest (ou behave/pytest-bdd)
├─ Testes criados: 4 scenarios
├─ Features cobertas: 2 (login, logout)
├─ Padrão: Given-When-Then
├─ Tempo de execução: 18.2s
└─ Localização: tests/acceptance/

🧪 TESTES GERADOS:
  📄 test_acceptance_auth.py
     • test_successful_login_redirects_to_dashboard()
       Given: User with valid credentials
       When: User submits login form
       Then: Redirected to dashboard

     • test_invalid_credentials_show_error()
       Given: User on login page
       When: User submits invalid credentials
       Then: Error message displayed

📝 PRÓXIMOS PASSOS:
1. Executar: pytest tests/acceptance/ -v
2. Revisar acceptance criteria cobertos
3. Commit: git add tests/acceptance/ && git commit -m "test: add acceptance tests for auth feature"
4. Integrar no CI/CD (feature validation)

═══════════════════════════════════════════
```

## ✅ Critérios de Sucesso

**Restrições Respeitadas:**

- [ ] ❌ NENHUM arquivo de código de produção modificado (`src/`, `app/`, etc.)
- [ ] ✅ Apenas arquivos em `tests/acceptance/` criados/modificados
- [ ] ✅ Apenas configuração (`pyproject.toml`, `pytest.ini`) atualizada
- [ ] ✅ Se mudanças em código de produção necessárias: reportado ao usuário

**Consulta de Skills:**

- [ ] Skill `create-acceptance-tests` consultada OBRIGATORIAMENTE
- [ ] Princípios BDD e Given-When-Then aplicados
- [ ] Skill `langchain-test-specialist` consultada se projeto usa LangChain/LangGraph

**Geração de Testes:**

- [ ] Framework apropriado escolhido ou detectado (behave, pytest-bdd, pytest)
- [ ] Testes baseados em acceptance criteria SMART
- [ ] Estrutura Given-When-Then clara em todos os testes
- [ ] Testes focam em comportamento observável (black-box)
- [ ] User perspective aplicada (ponto de vista do usuário final)
- [ ] Testes independentes (sem dependências entre eles)
- [ ] Scenarios com nomes descritivos
- [ ] Fixtures em `conftest.py` (não hard-coded)
- [ ] Positive e negative test cases cobertos
- [ ] Todos os testes gerados passam
- [ ] Testes determinísticos (sem flakiness)
- [ ] Documentação das features testadas

## 📝 Exemplos

**Exemplo 1 - Projeto inteiro:**

```bash
/create-acceptance-tests
```

Analisa projeto completo, detecta framework, gera acceptance tests para features principais.

**Exemplo 2 - Feature específica:**

```bash
/create-acceptance-tests src/features/authentication
```

Gera acceptance tests apenas para feature de autenticação.

**Exemplo 3 - Framework específico (behave):**

```bash
/create-acceptance-tests --framework behave
```

Força uso de behave (BDD Gherkin) com `.feature` files.

**Exemplo 4 - LangChain/LangGraph:**

```bash
/create-acceptance-tests src/agent
```

Detecta LangChain/LangGraph, consulta `langchain-test-specialist`, gera acceptance tests para agentic workflows.

## ❌ Anti-Patterns

### ❌ Erro 0: Modificar Código de Produção (CRÍTICO)

**NUNCA** modifique código de produção ao gerar acceptance tests:

```python
# ❌ CRÍTICO - NUNCA modificar código em src/
# Arquivo: src/auth/login.py
def login_user(username, password):
    # ... código existente ...
    pass  # ❌ NÃO adicionar logs, prints, ou mudanças aqui!

# ✅ CORRETO - Apenas criar testes
# Arquivo: tests/acceptance/test_auth.py
def test_successful_login():
    """Acceptance test: User can login with valid credentials"""
    # Given, When, Then
    ...
```

### ❌ Erro 1: Não Consultar Skill create-acceptance-tests (CRÍTICO)

**NUNCA** gere acceptance tests sem consultar a skill `create-acceptance-tests`:

```python
# ❌ CRÍTICO - Criar testes sem consultar skill
def test_login():
    # Implementação sem BDD patterns
    # Pode resultar em testes que testam implementação, não comportamento
    ...

# ✅ CORRETO - Consultar skill primeiro
# 1. Usar Skill tool: Skill(skill="create-acceptance-tests")
# 2. Extrair princípios: BDD, Given-When-Then, SMART criteria
# 3. Aplicar padrões identificados
def test_successful_login():
    """
    Acceptance Test: User can login with valid credentials

    Given a registered user with valid credentials
    When the user submits the login form
    Then the user should be redirected to dashboard
    """
    # Given
    user = create_valid_user()

    # When
    response = login(user.username, user.password)

    # Then
    assert response.status_code == 200
    assert response.redirected_to == '/dashboard'
```

### ❌ Erro 2: Testar Detalhes de Implementação

Não teste como o sistema funciona internamente, teste o comportamento:

```python
# ❌ ERRADO - Testa implementação (white-box)
def test_login_calls_database():
    with mock.patch('auth.db.query') as mock_query:
        login('user', 'pass')
        assert mock_query.called  # Detalhes internos!

# ✅ CORRETO - Testa comportamento (black-box)
def test_successful_login_shows_welcome_message():
    """
    Given: User with valid credentials
    When: User logs in
    Then: Welcome message is displayed
    """
    response = login('user@example.com', 'password123')
    assert 'Welcome' in response.text
```

### ❌ Erro 3: Scenarios Dependentes

Não crie testes que dependem da execução de outros:

```python
# ❌ ERRADO - Testes dependentes
def test_1_create_user():
    user = create_user('john@example.com')
    assert user.id == 1  # Assume que é o primeiro!

def test_2_login_user():
    # Depende de test_1_create_user ter rodado!
    response = login('john@example.com', 'pass')
    assert response.status_code == 200

# ✅ CORRETO - Testes independentes
def test_user_can_login_after_registration(app_client):
    """
    Given: A newly registered user
    When: User attempts to login
    Then: Login is successful
    """
    # Given - Setup completo neste teste
    user = app_client.post('/register', data={...})

    # When
    response = app_client.post('/login', data={...})

    # Then
    assert response.status_code == 200
```

### ❌ Erro 4: Nomes Vagos

Não use nomes genéricos que não descrevem o comportamento:

```python
# ❌ ERRADO - Nome vago
def test_login():
    ...

def test_login_2():
    ...

# ✅ CORRETO - Nomes descritivos
def test_successful_login_with_valid_credentials_redirects_to_dashboard():
    """
    Given: User with valid username and password
    When: User submits login form
    Then: User is redirected to dashboard page
    """
    ...

def test_login_with_invalid_password_shows_error_message():
    """
    Given: User enters valid username but wrong password
    When: User submits login form
    Then: Error message "Invalid credentials" is displayed
    """
    ...
```

### ❌ Erro 5: Hard-Coded Test Data

Não use dados hard-coded diretamente nos testes:

```python
# ❌ ERRADO - Hard-coded data
def test_user_registration():
    response = register('john@example.com', 'SecurePass123')
    assert response.status_code == 201

# ✅ CORRETO - Fixtures reutilizáveis
@pytest.fixture
def valid_user_data():
    return {
        'email': 'john@example.com',
        'password': 'SecurePass123'
    }

def test_user_registration(app_client, valid_user_data):
    """
    Given: Valid user registration data
    When: User submits registration form
    Then: User account is created successfully
    """
    response = app_client.post('/register', data=valid_user_data)
    assert response.status_code == 201
```

### ❌ Erro 6: Ignorar Negative Test Cases

Não teste apenas cenários de sucesso (happy paths):

```python
# ❌ ERRADO - Apenas happy path
def test_successful_login():
    response = login('user@example.com', 'password')
    assert response.status_code == 200

# ✅ CORRETO - Positive e negative cases
def test_successful_login_with_valid_credentials():
    """Positive: User can login with valid credentials"""
    response = login('user@example.com', 'password')
    assert response.status_code == 200

def test_login_with_invalid_password_fails():
    """Negative: Login fails with wrong password"""
    response = login('user@example.com', 'wrong_password')
    assert response.status_code == 401
    assert 'Invalid credentials' in response.text

def test_login_with_nonexistent_user_fails():
    """Negative: Login fails for non-registered user"""
    response = login('nonexistent@example.com', 'password')
    assert response.status_code == 404
```
