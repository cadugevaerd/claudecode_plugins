---
name: create-acceptance-tests
description: Conhecimento de testes de aceitação em Python - BDD, frameworks (pytest, behave, pytest-bdd), padrões Given-When-Then, acceptance criteria e melhores práticas. Use quando criar acceptance tests, implementar BDD, validar user stories, testar end-to-end behaviors, ou estruturar test suites de aceitação.
version: 1.0.0
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Acceptance Testing in Python

Especialização em testes de aceitação, Behavior-Driven Development (BDD) e validação de requisitos de negócio em Python.

## 📋 When to Use Me

Invoque esta skill quando:

- **Criar acceptance tests** para validar user stories e requisitos
- **Implementar BDD** com Given-When-Then patterns
- **Escolher framework** para acceptance testing (pytest vs behave vs pytest-bdd)
- **Estruturar test suites** de aceitação end-to-end
- **Validar acceptance criteria** de forma automatizada
- **Integrar testes** com stakeholders não-técnicos
- **Converter user stories** em testes executáveis
- **Revisar ou refatorar** acceptance tests existentes
- **Definir estratégia** de testes de aceitação para projeto

**Trigger Keywords**: acceptance tests, BDD, behave, Given-When-Then, Gherkin, user stories, acceptance criteria, end-to-end testing, pytest-bdd, behavioral testing

## 🎓 Core Knowledge

### O Que São Acceptance Tests?

**Acceptance Testing** valida se o sistema atende aos requisitos de negócio e às expectativas dos stakeholders. Características:

- ✅ **Black-box testing**: Testa comportamento observável (não implementação)
- ✅ **User perspective**: Valida do ponto de vista do usuário final
- ✅ **Business-focused**: Baseado em acceptance criteria e user stories
- ✅ **End-to-end**: Testa fluxos completos (não unidades isoladas)
- ✅ **Readable**: Compreensível por stakeholders não-técnicos

**Diferenças de outros testes**:

- **Unit tests**: Testam unidades isoladas (funções, classes)
- **Integration tests**: Testam interação entre componentes
- **Acceptance tests**: Testam comportamento completo do sistema

### Behavior-Driven Development (BDD)

BDD é uma metodologia que aproxima testes de especificações de negócio usando linguagem natural estruturada.

**Estrutura Given-When-Then**:

```gherkin
Given [contexto inicial / pré-condições]
When [ação/evento que ocorre]
Then [resultado esperado / pós-condições]
```

**Benefícios**:

- Testes servem como documentação viva
- Colaboração entre dev, QA e stakeholders
- Especificações executáveis
- Reduz ambiguidade nos requisitos

### Frameworks Python para Acceptance Testing

| Framework | Abordagem | Melhor Para |
|-----------|-----------|-------------|
| **behave** | BDD puro, Gherkin sintax | Stakeholders não-técnicos, web apps |
| **pytest-bdd** | BDD com pytest integration | Equipes técnicas, integração com test suite |
| **pytest** | Code-based, flexible | Total controle, devs confortáveis com Python |
| **Robot Framework** | Keyword-driven | Automação complexa, non-developers |

**Recomendação Geral**:

- **Stakeholders não-técnicos envolvidos**: behave ou Robot Framework
- **Equipe técnica com pytest existente**: pytest-bdd
- **Máxima flexibilidade e controle**: pytest puro

### Acceptance Criteria Structure

Acceptance criteria devem ser **SMART**:

- **S**pecific: Bem definidos e precisos
- **M**easurable: Mensuráveis e verificáveis
- **A**chievable: Implementáveis
- **R**elevant: Alinhados com requisitos
- **T**estable: Automatizáveis

**Formato Given-When-Then** (recomendado):

```gherkin
Scenario: User login with valid credentials
  Given the user is on the login page
  When the user enters valid username and password
  Then the user should be redirected to dashboard
  And a welcome message should be displayed
```

### Best Practices Essenciais

1. **Write tests BEFORE implementation** (TDD/BDD cycle)
1. **One scenario = One behavior**: Evite cenários complexos
1. **Use meaningful scenario names**: Descreva o comportamento claramente
1. **Avoid implementation details**: Foque no comportamento observável
1. **Keep scenarios independent**: Cada teste deve rodar isolado
1. **Use fixtures/backgrounds**: Reutilize setup comum
1. **Organize by features**: Agrupe testes por funcionalidade
1. **Test environment should mimic production**: Realismo

### Test Organization Pattern

```
tests/acceptance/
├── features/                 # behave (BDD)
│   ├── steps/
│   │   └── login_steps.py
│   └── login.feature
├── test_acceptance/          # pytest-bdd or pytest
│   ├── conftest.py
│   └── test_user_login.py
└── fixtures/
    └── test_data.py
```

### Common Anti-Patterns

❌ **Testing implementation details** instead of behavior
❌ **Overly complex scenarios** with many Given/When/Then steps
❌ **Dependent tests** that require specific execution order
❌ **Vague or generic test names**
❌ **Missing negative test cases**
❌ **Hard-coded test data** without fixtures
❌ **Not involving stakeholders** in acceptance criteria definition

## 📚 Reference Files

Para conhecimento detalhado, consulte:

- **REFERENCE.md** - Frameworks detalhados (behave, pytest-bdd, pytest), comparações, setup e configuração
- **PATTERNS.md** - Padrões Given-When-Then, estruturas de features, page object pattern, step organization
- **EXAMPLES.md** - Exemplos completos com behave, pytest-bdd e pytest puro para diferentes cenários

## 💡 Quick Examples

### Example 1: Behave (BDD Gherkin)

**Feature file** (`features/login.feature`):

```gherkin
Feature: User Authentication
  As a registered user
  I want to log in to the system
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter username "john@example.com"
    And I enter password "SecurePass123"
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see "Welcome, John"
```

**Step definitions** (`features/steps/login_steps.py`):

```python
from behave import given, when, then

@given('I am on the login page')
def step_impl(context):
    context.browser.get('http://localhost/login')

@when('I enter username "{username}"')
def step_impl(context, username):
    context.browser.find_element_by_id('username').send_keys(username)
```

### Example 2: Pytest-BDD

**Feature file** (`tests/acceptance/login.feature`):

```gherkin
Feature: User login
  Scenario: Login with valid credentials
    Given the login page is displayed
    When I submit valid credentials
    Then I should see the dashboard
```

**Test file** (`tests/acceptance/test_login.py`):

```python
from pytest_bdd import scenarios, given, when, then

scenarios('login.feature')

@given('the login page is displayed')
def login_page(browser):
    browser.get('/login')
    assert 'Login' in browser.title

@when('I submit valid credentials')
def submit_credentials(browser, user_credentials):
    browser.find_element_by_id('username').send_keys(user_credentials['username'])
    browser.find_element_by_id('password').send_keys(user_credentials['password'])
    browser.find_element_by_id('submit').click()

@then('I should see the dashboard')
def verify_dashboard(browser):
    assert browser.current_url.endswith('/dashboard')
```

### Example 3: Pytest Pure (Code-based)

```python
import pytest

class TestUserAuthentication:
    """Acceptance tests for user authentication feature"""

    def test_successful_login_redirects_to_dashboard(self, app_client, valid_user):
        """
        Given a registered user with valid credentials
        When the user submits the login form with correct username and password
        Then the user should be redirected to the dashboard page
        """
        # Given
        username, password = valid_user

        # When
        response = app_client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

        # Then
        assert response.status_code == 200
        assert b'Dashboard' in response.data
        assert b'Welcome' in response.data

    def test_invalid_credentials_show_error_message(self, app_client):
        """
        Given a user on the login page
        When the user submits invalid credentials
        Then an error message should be displayed
        And the user should remain on the login page
        """
        # When
        response = app_client.post('/login', data={
            'username': 'invalid@example.com',
            'password': 'wrongpassword'
        })

        # Then
        assert response.status_code == 200
        assert b'Invalid credentials' in response.data
        assert b'Login' in response.data
```

## ✅ Quick Checklist

Ao criar acceptance tests, verifique:

- [ ] **Testes baseados em user stories** e acceptance criteria
- [ ] **Cenários independentes** (sem dependências entre testes)
- [ ] **Given-When-Then structure** clara e legível
- [ ] **Nomes descritivos** que explicam o comportamento
- [ ] **Test data em fixtures** (não hard-coded)
- [ ] **Positive e negative test cases** cobertos
- [ ] **Environment mimics production** (realismo)
- [ ] **Stakeholders podem compreender** (se usando BDD)
- [ ] **Testes são determinísticos** (sem flakiness)
- [ ] **Documentação das features** testadas

## 🎯 Framework Selection Guide

**Escolha behave se**:

- Stakeholders não-técnicos escrevem/revisam acceptance criteria
- Documentação viva é prioridade
- Web application testing com Selenium
- Gherkin syntax é familiar à equipe

**Escolha pytest-bdd se**:

- Já usa pytest para unit/integration tests
- Quer BDD mas com flexibilidade de pytest
- Equipe técnica prefere Python sobre Gherkin puro
- Precisa de plugins pytest (fixtures, parametrize, etc)

**Escolha pytest puro se**:

- Equipe totalmente técnica
- Máxima flexibilidade e controle
- Não precisa envolver stakeholders não-técnicos
- Prefere código Python explícito

## 📖 Next Steps

1. **Consulte REFERENCE.md** para setup detalhado de frameworks
1. **Veja PATTERNS.md** para padrões avançados de organização
1. **Explore EXAMPLES.md** para casos de uso completos
1. **Escolha framework** baseado no guide acima
1. **Defina acceptance criteria** com stakeholders
1. **Implemente testes** seguindo BDD cycle

______________________________________________________________________

**Lembre-se**: Acceptance tests validam **O QUE** o sistema faz (comportamento), não **COMO** faz (implementação).
