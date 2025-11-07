# Acceptance Testing Reference - Frameworks and Methodologies

Documentação técnica detalhada sobre frameworks de acceptance testing em Python, configuração, comparações e best practices.

## 📦 Framework Ecosystem

### 1. Behave - BDD Framework

**Características**:

- Pure BDD framework usando Gherkin syntax
- Standalone framework (não requer pytest/unittest)
- Ideal para envolver stakeholders não-técnicos
- Forte foco em web application testing

**Quando usar**:

- ✅ Stakeholders escrevem/revisam acceptance criteria
- ✅ Documentação viva é crítica
- ✅ Web testing com Selenium/Playwright
- ✅ Equipe familiarizada com Cucumber/SpecFlow

**Instalação**:

```bash
uv pip install behave selenium
```

**Estrutura de Projeto**:

```
project/
├── features/
│   ├── environment.py       # Hooks (before/after scenario, feature, etc)
│   ├── steps/
│   │   ├── authentication_steps.py
│   │   └── common_steps.py
│   ├── login.feature
│   └── checkout.feature
└── behave.ini               # Configuration
```

**Configuration** (`behave.ini`):

```ini
[behave]
show_skipped = false
show_timings = true
color = true
format = pretty
junit = true
junit_directory = test-reports

[behave.userdata]
browser = chrome
base_url = http://localhost:8000
```

**Limitações**:

- ❌ Sem suporte nativo para parallel execution (behave-parallel descontinuado)
- ❌ Fixtures menos flexíveis que pytest
- ❌ Comunidade menor que pytest

### 2. Pytest-BDD - BDD com Pytest

**Características**:

- BDD layer em cima do pytest
- Usa Gherkin features + pytest fixtures
- Integração total com ecossistema pytest
- Melhor de dois mundos: BDD + pytest power

**Quando usar**:

- ✅ Já usa pytest para outros testes
- ✅ Quer BDD mas com flexibilidade pytest
- ✅ Precisa de pytest plugins (xdist, cov, html)
- ✅ Equipe técnica prefere Python

**Instalação**:

```bash
uv pip install pytest pytest-bdd selenium
```

**Estrutura de Projeto**:

```
tests/
├── acceptance/
│   ├── features/
│   │   ├── login.feature
│   │   └── checkout.feature
│   ├── test_login.py        # Step implementations + test binding
│   └── test_checkout.py
└── conftest.py              # Shared fixtures
```

**Key Differences from Behave**:

- Features files separados de step implementations
- `scenarios()` function para vincular features a test files
- Usa pytest fixtures em steps
- Roda com `pytest` command

**Configuration** (`pytest.ini`):

```ini
[pytest]
testpaths = tests/acceptance
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    -v
    --tb=short
    --bdd-features-base-dir=tests/acceptance/features
```

### 3. Pytest (Pure) - Code-Based Acceptance Tests

**Características**:

- Sem Gherkin, testes puramente em Python
- Total flexibilidade e controle
- Menos overhead, mais direto
- Ideal para equipes 100% técnicas

**Quando usar**:

- ✅ Stakeholders não envolvidos em especificação
- ✅ Máxima flexibilidade necessária
- ✅ Equipe prefere código explícito
- ✅ Não precisa de documentação viva em Gherkin

**Instalação**:

```bash
uv pip install pytest pytest-html pytest-cov
```

**Estrutura de Projeto**:

```
tests/
├── acceptance/
│   ├── conftest.py
│   ├── test_user_authentication.py
│   ├── test_product_checkout.py
│   └── fixtures/
│       ├── users.py
│       └── products.py
└── pytest.ini
```

**Best Practice - Docstring Given-When-Then**:

```python
def test_user_can_complete_checkout(app, logged_in_user, product_in_cart):
    """
    Given a logged-in user with a product in their cart
    When the user proceeds to checkout and completes payment
    Then the order should be created and confirmation email sent
    """
    # Test implementation
```

### 4. Robot Framework - Keyword-Driven

**Características**:

- Keyword-driven approach
- Tabular test format
- Extensível via libraries (Python, Java)
- Forte em automação complexa

**Quando usar**:

- ✅ Non-developers participam de automação
- ✅ Keyword libraries reutilizáveis
- ✅ Test automation complexo (RPA + Testing)
- ✅ Relatórios visuais ricos

**Instalação**:

```bash
uv pip install robotframework robotframework-seleniumlibrary
```

**Example** (`login.robot`):

```robot
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Valid Login
    Open Browser    http://localhost/login    chrome
    Input Text    id:username    john@example.com
    Input Password    id:password    SecurePass123
    Click Button    id:submit
    Page Should Contain    Welcome, John
    Close Browser
```

## 🔍 Framework Comparison Matrix

| Feature | Behave | Pytest-BDD | Pytest Pure | Robot |
|---------|--------|------------|-------------|-------|
| **Gherkin Syntax** | ✅ Native | ✅ Via features | ❌ No | ❌ Keywords |
| **Readability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Flexibility** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Pytest Integration** | ❌ No | ✅ Full | ✅ Native | ❌ No |
| **Parallel Execution** | ❌ Limited | ✅ pytest-xdist | ✅ pytest-xdist | ✅ pabot |
| **Fixtures** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Learning Curve** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Community** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Reporting** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🛠️ Setup and Configuration Best Practices

### Environment Management with Hooks

**Behave** (`features/environment.py`):

```python
from selenium import webdriver

def before_all(context):
    """Setup once before all features"""
    context.config.setup_logging()

def before_scenario(context, scenario):
    """Setup before each scenario"""
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(10)

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    context.browser.quit()

def after_step(context, step):
    """Screenshot on failure"""
    if step.status == 'failed':
        context.browser.save_screenshot(f'screenshots/{step.name}.png')
```

**Pytest-BDD/Pytest** (`conftest.py`):

```python
import pytest
from selenium import webdriver

@pytest.fixture(scope='session')
def browser_config():
    """Browser configuration for all tests"""
    return {
        'browser': 'chrome',
        'headless': False,
        'implicit_wait': 10
    }

@pytest.fixture(scope='function')
def browser(browser_config):
    """Browser instance per test"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(browser_config['implicit_wait'])
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def base_url():
    """Base URL for application"""
    return 'http://localhost:8000'

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        browser = item.funcargs.get('browser')
        if browser:
            browser.save_screenshot(f'screenshots/{item.name}.png')
```

### Test Data Management

**Using Fixtures**:

```python
# conftest.py
import pytest

@pytest.fixture
def valid_user():
    """Valid user credentials"""
    return {
        'username': 'john@example.com',
        'password': 'SecurePass123',
        'expected_name': 'John Doe'
    }

@pytest.fixture
def invalid_users():
    """Invalid user scenarios"""
    return [
        {'username': 'invalid@example.com', 'password': 'wrong', 'error': 'Invalid credentials'},
        {'username': '', 'password': 'pass', 'error': 'Username required'},
        {'username': 'user@example.com', 'password': '', 'error': 'Password required'},
    ]

@pytest.fixture
def test_database(db_session):
    """Populate test database"""
    from models import User
    user = User(username='john@example.com', password_hash='hashed')
    db_session.add(user)
    db_session.commit()
    yield db_session
    db_session.rollback()
```

**Using Context Tables (Behave)**:

```gherkin
Scenario Outline: Login with different credentials
  Given I am on the login page
  When I enter username "<username>"
  And I enter password "<password>"
  Then I should see "<result>"

  Examples:
    | username           | password    | result                |
    | john@example.com   | SecurePass  | Welcome, John         |
    | invalid@email.com  | wrong       | Invalid credentials   |
    | user@test.com      |             | Password required     |
```

## 🎯 BDD Methodology Deep Dive

### The Three Amigos Meeting

**Who**: Developer + QA + Business Analyst/Product Owner

**When**: Before implementing user story

**Goal**: Define acceptance criteria collaboratively

**Process**:

1. **Example Mapping**: Identificar regras e exemplos
1. **Write Scenarios**: Converter exemplos em Given-When-Then
1. **Clarify Ambiguities**: Resolver dúvidas antes de desenvolvimento
1. **Agree on Scope**: O que está in/out of scope

### Writing Effective Scenarios

**Good Scenario**:

```gherkin
Scenario: Free shipping for orders over $50
  Given I have added items worth $60 to my cart
  When I proceed to checkout
  Then I should see "Free Shipping" in the shipping options
  And the shipping cost should be $0.00
```

**Bad Scenario** (Too coupled to UI):

```gherkin
Scenario: Free shipping
  Given I click on product ID "12345"
  And I click the "Add to Cart" button with class "btn-primary"
  And I navigate to "/cart" URL
  When I click element with xpath "//button[@data-action='checkout']"
  Then element with CSS selector ".shipping-label" should contain text "Free Shipping"
```

**Why bad?**: Tied to implementation (IDs, classes, XPath), fragile to UI changes.

### Scenario Organization Principles

**1. Feature Cohesion**: Agrupe scenarios por feature

```
features/
├── user_authentication.feature
├── product_catalog.feature
└── shopping_cart.feature
```

**2. Scenario Independence**: Cada scenario roda isolado

```gherkin
# ❌ Bad: Depends on previous scenario
Scenario: Add item to cart
  When I add Product A to cart
  Then cart should have 1 item

Scenario: Checkout
  # Assumes cart has item from previous scenario!
  When I proceed to checkout
  Then order should be created

# ✅ Good: Independent scenarios
Scenario: Add item to cart
  Given the cart is empty
  When I add Product A to cart
  Then cart should have 1 item

Scenario: Checkout with item in cart
  Given I have Product A in my cart
  When I proceed to checkout
  Then order should be created
```

**3. Background for Common Setup**:

```gherkin
Feature: Shopping Cart

  Background:
    Given I am logged in as a registered user
    And the product catalog is available

  Scenario: Add single item to cart
    When I add "Product A" to cart
    Then cart should contain 1 item

  Scenario: Add multiple items to cart
    When I add "Product A" to cart
    And I add "Product B" to cart
    Then cart should contain 2 items
```

## 🔬 Testing Patterns

### Page Object Pattern (for Web Testing)

**Why**: Encapsulate page interactions, reduce duplication, improve maintainability

**Implementation**:

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.url = '/login'

    def navigate(self):
        self.browser.get(self.url)

    def enter_username(self, username):
        self.browser.find_element_by_id('username').send_keys(username)

    def enter_password(self, password):
        self.browser.find_element_by_id('password').send_keys(password)

    def click_submit(self):
        self.browser.find_element_by_id('submit').click()

    def get_error_message(self):
        return self.browser.find_element_by_class('error-message').text

# steps/login_steps.py (behave)
from behave import given, when, then
from pages.login_page import LoginPage

@given('I am on the login page')
def step_impl(context):
    context.login_page = LoginPage(context.browser)
    context.login_page.navigate()

@when('I enter username "{username}"')
def step_impl(context, username):
    context.login_page.enter_username(username)
```

### API Testing Pattern

**REST API Acceptance Tests**:

```python
import pytest
import requests

class TestUserAPI:
    """Acceptance tests for User API endpoints"""

    def test_create_user_returns_201_with_user_data(self, api_base_url):
        """
        Given valid user registration data
        When POST request is sent to /api/users
        Then response status should be 201 Created
        And response should contain user ID and email
        """
        # Given
        user_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePassword123',
            'name': 'New User'
        }

        # When
        response = requests.post(f'{api_base_url}/api/users', json=user_data)

        # Then
        assert response.status_code == 201
        response_data = response.json()
        assert 'id' in response_data
        assert response_data['email'] == user_data['email']
        assert 'password' not in response_data  # Should not expose password

    def test_get_user_by_id_returns_user_details(self, api_base_url, existing_user):
        """
        Given a user exists in the database
        When GET request is sent to /api/users/{id}
        Then response should return user details
        And status code should be 200 OK
        """
        # When
        response = requests.get(f'{api_base_url}/api/users/{existing_user.id}')

        # Then
        assert response.status_code == 200
        user_data = response.json()
        assert user_data['id'] == existing_user.id
        assert user_data['email'] == existing_user.email
```

## 📊 Reporting and CI/CD Integration

### JUnit XML Reports

**Behave**:

```bash
behave --junit --junit-directory=test-reports/
```

**Pytest**:

```bash
pytest --junitxml=test-reports/junit.xml
```

### HTML Reports

**Pytest-HTML**:

```bash
uv pip install pytest-html
pytest --html=test-reports/report.html --self-contained-html
```

### CI/CD Integration (GitHub Actions Example)

```yaml
name: Acceptance Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -r requirements-test.txt

      - name: Run acceptance tests
        run: |
          pytest tests/acceptance/ \
            --junitxml=test-reports/junit.xml \
            --html=test-reports/report.html

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: test-reports/
```

## 🚀 Performance and Parallel Execution

### Pytest with pytest-xdist

```bash
uv pip install pytest-xdist
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 workers
```

**Configuration** (`pytest.ini`):

```ini
[pytest]
addopts = -n auto --dist loadscope
```

### Behave Workarounds for Parallel

Since behave doesn't support parallel natively:

1. **Split by features**:

```bash
# Terminal 1
behave features/login.feature

# Terminal 2
behave features/checkout.feature
```

2. **Use test orchestrators** (e.g., Jenkins, GitLab CI parallel jobs)

## 📚 Additional Resources

- **Behave Documentation**: https://behave.readthedocs.io/
- **Pytest-BDD Documentation**: https://pytest-bdd.readthedocs.io/
- **Pytest Documentation**: https://docs.pytest.org/
- **BDD Best Practices**: https://cucumber.io/docs/bdd/
- **Page Object Pattern**: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/

______________________________________________________________________

**Next**: See PATTERNS.md for advanced patterns and EXAMPLES.md for complete project examples.
