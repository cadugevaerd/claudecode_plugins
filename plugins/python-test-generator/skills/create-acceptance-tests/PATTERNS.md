# Acceptance Testing Patterns and Best Practices

Padrões avançados de estruturação, organização e implementação de acceptance tests em Python.

## 🎨 Given-When-Then Pattern Deep Dive

### Anatomia Completa

```gherkin
Scenario: [Brief description of behavior being tested]
  Given [Initial context / Preconditions]
    And [Additional context]
  When [Action or event]
    And [Additional action]
  Then [Expected outcome]
    And [Additional verification]
    But [Negative verification]
```

### Given - Context and Preconditions

**Purpose**: Estabelecer o estado inicial do sistema

**Best Practices**:

- ✅ Descrever estado, não ações para chegar nele
- ✅ Usar linguagem de negócio, não técnica
- ✅ Ser específico mas conciso

**Examples**:

```gherkin
# ✅ Good: Describes state
Given the user "john@example.com" is registered
Given the shopping cart contains 3 items
Given the product "iPhone 15" is in stock

# ❌ Bad: Describes actions
Given I navigate to the registration page
Given I fill the registration form
Given I submit the form
```

**Implementation Pattern** (behave):

```python
from behave import given

@given('the user "{email}" is registered')
def step_impl(context, email):
    # Setup user in database
    context.user = create_user(email=email, password='TestPass123')
    context.db.add(context.user)
    context.db.commit()

@given('the shopping cart contains {count:d} items')
def step_impl(context, count):
    context.cart = ShoppingCart(user=context.user)
    for i in range(count):
        context.cart.add_item(create_test_product(f'Product {i}'))
```

### When - Action or Event

**Purpose**: Descrever a ação sendo testada

**Best Practices**:

- ✅ Usar tempo presente
- ✅ Uma única ação principal por scenario
- ✅ Descrever comportamento do usuário, não cliques/teclas

**Examples**:

```gherkin
# ✅ Good: User behavior
When the user logs in with valid credentials
When the customer completes the checkout process
When the admin approves the order

# ❌ Bad: Technical details
When I click the button with id "submit-btn"
When I send a POST request to "/api/login"
When the login() function is called
```

**Implementation Pattern** (pytest-bdd):

```python
from pytest_bdd import when

@when('the user logs in with valid credentials')
def user_logs_in(browser, valid_user, login_page):
    login_page.navigate()
    login_page.enter_email(valid_user['email'])
    login_page.enter_password(valid_user['password'])
    login_page.submit()

@when('the customer completes the checkout process')
def complete_checkout(browser, checkout_page, payment_info):
    checkout_page.enter_shipping_address(payment_info['address'])
    checkout_page.select_payment_method('credit_card')
    checkout_page.enter_card_details(payment_info['card'])
    checkout_page.confirm_order()
```

### Then - Expected Outcome

**Purpose**: Verificar que o comportamento esperado ocorreu

**Best Practices**:

- ✅ Verificar resultados observáveis
- ✅ Ser específico sobre o que mudou
- ✅ Focar em comportamento, não implementação

**Examples**:

```gherkin
# ✅ Good: Observable outcomes
Then the user should be logged in
Then the order confirmation page should be displayed
Then the user should receive a welcome email

# ❌ Bad: Implementation details
Then the session cookie should be set
Then the database should have 1 new row in orders table
Then the send_email() function should be called
```

**Implementation Pattern** (pytest):

```python
def test_user_can_login(browser, login_page, dashboard_page, valid_user):
    """
    Given a registered user
    When the user logs in with valid credentials
    Then the user should be logged in
    And the dashboard should be displayed
    """
    # Given
    user = create_registered_user(valid_user)

    # When
    login_page.navigate()
    login_page.login(user['email'], user['password'])

    # Then
    assert dashboard_page.is_displayed()
    assert dashboard_page.get_welcome_message() == f"Welcome, {user['name']}"
    assert browser.get_cookie('session_id') is not None
```

## 📁 Test Organization Patterns

### Pattern 1: Feature-Based Organization

**Structure**:

```
tests/acceptance/
├── features/
│   ├── authentication/
│   │   ├── login.feature
│   │   ├── logout.feature
│   │   └── password_reset.feature
│   ├── shopping_cart/
│   │   ├── add_to_cart.feature
│   │   └── remove_from_cart.feature
│   └── checkout/
│       ├── shipping.feature
│       └── payment.feature
└── steps/
    ├── authentication_steps.py
    ├── shopping_cart_steps.py
    └── checkout_steps.py
```

**Benefits**:

- Clear feature boundaries
- Easy to navigate by functionality
- Aligns with user stories/epics

### Pattern 2: User Journey Organization

**Structure**:

```
tests/acceptance/
├── user_journeys/
│   ├── new_user_registration.feature
│   ├── returning_customer_purchase.feature
│   └── guest_checkout.feature
└── steps/
    └── journey_steps.py
```

**Use when**: Testing end-to-end user flows

### Pattern 3: Layer-Based Organization

**Structure**:

```
tests/
├── acceptance/
│   ├── ui/                    # UI-based acceptance tests
│   │   ├── test_login_ui.py
│   │   └── test_checkout_ui.py
│   ├── api/                   # API-based acceptance tests
│   │   ├── test_user_api.py
│   │   └── test_order_api.py
│   └── integration/           # Multi-system acceptance tests
│       └── test_payment_integration.py
└── conftest.py
```

**Benefits**:

- Separation by testing approach
- Different fixtures/configurations per layer
- Parallel execution easier

## 🏗️ Step Definition Patterns

### Pattern 1: Reusable Step Definitions

**Problem**: Duplicated step code across features

**Solution**: Parameterized, generic steps

```python
# ❌ Bad: Specific, duplicated
@given('the user "john@example.com" is logged in')
def step_impl(context):
    login(context, 'john@example.com', 'password')

@given('the user "admin@example.com" is logged in')
def step_impl(context):
    login(context, 'admin@example.com', 'password')

# ✅ Good: Reusable, parameterized
@given('the user "{email}" is logged in')
def step_impl(context, email):
    password = context.test_users[email]['password']
    login(context, email, password)

@given('the {role} user is logged in')
def step_impl(context, role):
    user = context.test_users_by_role[role]
    login(context, user['email'], user['password'])
```

### Pattern 2: Step Helpers

**Problem**: Complex step logic becomes unreadable

**Solution**: Extract helpers

```python
# helpers/authentication_helpers.py
def login_user(browser, email, password):
    """Helper to perform login action"""
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.enter_credentials(email, password)
    login_page.submit()
    return DashboardPage(browser)

def create_test_user(db, email, role='user'):
    """Helper to create user in database"""
    from models import User
    user = User(email=email, role=role)
    user.set_password('TestPass123')
    db.add(user)
    db.commit()
    return user

# steps/authentication_steps.py
from behave import given, when, then
from helpers.authentication_helpers import login_user, create_test_user

@given('the user "{email}" is registered')
def step_impl(context, email):
    context.user = create_test_user(context.db, email)

@when('the user logs in with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.dashboard = login_user(context.browser, email, password)

@then('the user should be on the dashboard')
def step_impl(context):
    assert context.dashboard.is_displayed()
```

**Benefits**:

- Steps remain readable
- Business logic separated from test orchestration
- Helpers reusable across test types

### Pattern 3: Context Table Pattern

**Use case**: Testing multiple variations of same scenario

**Gherkin** (behave):

```gherkin
Scenario Outline: Password validation
  Given the user is on the registration page
  When the user enters password "<password>"
  Then the validation message should be "<message>"

  Examples: Valid passwords
    | password      | message              |
    | SecureP@ss1   | Password accepted    |
    | MyP@ssw0rd    | Password accepted    |

  Examples: Invalid passwords
    | password      | message                           |
    | short         | Password must be at least 8 chars |
    | nodigits      | Password must contain a digit     |
    | NoSpecial1    | Password must contain special char|
```

**Pytest** (parametrize):

```python
import pytest

@pytest.mark.parametrize('password,expected_message', [
    # Valid passwords
    ('SecureP@ss1', 'Password accepted'),
    ('MyP@ssw0rd', 'Password accepted'),
    # Invalid passwords
    ('short', 'Password must be at least 8 chars'),
    ('nodigits', 'Password must contain a digit'),
    ('NoSpecial1', 'Password must contain special char'),
])
def test_password_validation(registration_page, password, expected_message):
    """
    Given the user is on the registration page
    When the user enters a password
    Then appropriate validation message should be displayed
    """
    registration_page.navigate()
    registration_page.enter_password(password)
    actual_message = registration_page.get_validation_message()
    assert actual_message == expected_message
```

## 🎭 Page Object Pattern

### Basic Page Object

```python
# pages/base_page.py
class BasePage:
    """Base class for all page objects"""

    def __init__(self, browser):
        self.browser = browser

    def navigate(self, url):
        self.browser.get(url)

    def find_element(self, *locator):
        return self.browser.find_element(*locator)

    def find_elements(self, *locator):
        return self.browser.find_elements(*locator)

    def click(self, *locator):
        self.find_element(*locator).click()

    def enter_text(self, text, *locator):
        element = self.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, *locator):
        return self.find_element(*locator).text

# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    URL = '/login'
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    SUBMIT_BUTTON = (By.ID, 'submit')
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message')

    def navigate(self):
        super().navigate(self.URL)

    def enter_email(self, email):
        self.enter_text(email, *self.EMAIL_INPUT)

    def enter_password(self, password):
        self.enter_text(password, *self.PASSWORD_INPUT)

    def submit(self):
        self.click(*self.SUBMIT_BUTTON)

    def login(self, email, password):
        """Complete login action"""
        self.enter_email(email)
        self.enter_password(password)
        self.submit()

    def get_error_message(self):
        return self.get_text(*self.ERROR_MESSAGE)

    def is_displayed(self):
        return self.browser.current_url.endswith(self.URL)
```

### Advanced: Page Component Pattern

**For reusable UI components**:

```python
# components/navigation.py
class NavigationComponent:
    """Reusable navigation component"""

    def __init__(self, browser):
        self.browser = browser

    def navigate_to_cart(self):
        self.browser.find_element(By.ID, 'cart-link').click()

    def navigate_to_profile(self):
        self.browser.find_element(By.ID, 'profile-link').click()

    def logout(self):
        self.browser.find_element(By.ID, 'logout-link').click()

# pages/dashboard_page.py
from components.navigation import NavigationComponent

class DashboardPage(BasePage):
    URL = '/dashboard'

    def __init__(self, browser):
        super().__init__(browser)
        self.navigation = NavigationComponent(browser)

    # Dashboard-specific methods
    def get_welcome_message(self):
        return self.get_text(By.CLASS_NAME, 'welcome-message')

    # Delegated navigation
    def go_to_cart(self):
        self.navigation.navigate_to_cart()
        from pages.cart_page import CartPage
        return CartPage(self.browser)
```

## 🔄 Test Data Patterns

### Pattern 1: Fixture-Based Test Data

```python
# conftest.py
import pytest
from models import User, Product

@pytest.fixture
def test_users(db_session):
    """Predefined test users"""
    users = [
        User(email='customer@test.com', role='customer', name='Test Customer'),
        User(email='admin@test.com', role='admin', name='Test Admin'),
        User(email='guest@test.com', role='guest', name='Guest User'),
    ]
    for user in users:
        user.set_password('TestPass123')
        db_session.add(user)
    db_session.commit()
    return {user.email: user for user in users}

@pytest.fixture
def test_products(db_session):
    """Predefined test products"""
    products = [
        Product(name='Product A', price=10.00, stock=100),
        Product(name='Product B', price=25.50, stock=50),
        Product(name='Product C', price=5.99, stock=200),
    ]
    for product in products:
        db_session.add(product)
    db_session.commit()
    return {product.name: product for product in products}
```

### Pattern 2: Factory Pattern for Test Data

```python
# factories/user_factory.py
from models import User

class UserFactory:
    """Factory for creating test users"""

    _counter = 0

    @classmethod
    def create(cls, **kwargs):
        cls._counter += 1
        defaults = {
            'email': f'user{cls._counter}@test.com',
            'name': f'Test User {cls._counter}',
            'role': 'customer'
        }
        defaults.update(kwargs)

        user = User(**defaults)
        user.set_password(kwargs.get('password', 'TestPass123'))
        return user

    @classmethod
    def create_admin(cls, **kwargs):
        kwargs['role'] = 'admin'
        return cls.create(**kwargs)

# Usage in tests
def test_admin_can_delete_users(db_session, admin_user):
    """
    Given an admin user and a regular user exist
    When the admin deletes the regular user
    Then the user should be removed from the system
    """
    # Given
    admin = UserFactory.create_admin()
    regular_user = UserFactory.create()
    db_session.add_all([admin, regular_user])
    db_session.commit()

    # When
    admin_service.delete_user(admin.id, regular_user.id)

    # Then
    assert db_session.query(User).filter_by(id=regular_user.id).first() is None
```

### Pattern 3: Builder Pattern for Complex Data

```python
# builders/order_builder.py
class OrderBuilder:
    """Builder for complex order test data"""

    def __init__(self):
        self.order_data = {
            'items': [],
            'shipping_address': None,
            'billing_address': None,
            'payment_method': None,
        }

    def with_items(self, *items):
        self.order_data['items'].extend(items)
        return self

    def with_shipping_address(self, address):
        self.order_data['shipping_address'] = address
        return self

    def with_billing_address(self, address):
        self.order_data['billing_address'] = address
        return self

    def with_payment_method(self, payment_method):
        self.order_data['payment_method'] = payment_method
        return self

    def build(self):
        from models import Order
        return Order(**self.order_data)

# Usage
def test_order_with_multiple_items(db_session):
    """Test order creation with multiple items"""
    order = (OrderBuilder()
             .with_items(ProductA, ProductB, ProductC)
             .with_shipping_address(standard_address)
             .with_payment_method('credit_card')
             .build())

    db_session.add(order)
    db_session.commit()

    assert len(order.items) == 3
    assert order.total_price == 41.49
```

## 🚦 Negative Testing Patterns

### Pattern: Explicit Negative Scenarios

```gherkin
Feature: User Authentication

  # Positive scenarios
  Scenario: Successful login with valid credentials
    Given a registered user exists
    When the user logs in with correct credentials
    Then the user should be logged in

  # Negative scenarios
  Scenario: Login fails with incorrect password
    Given a registered user exists
    When the user logs in with incorrect password
    Then an error message "Invalid credentials" should be displayed
    And the user should remain on the login page

  Scenario: Login fails with non-existent email
    Given no user exists with email "nonexistent@test.com"
    When the user attempts to login with that email
    Then an error message "User not found" should be displayed

  Scenario: Login is blocked after 5 failed attempts
    Given a registered user exists
    When the user fails to login 5 times consecutively
    Then the account should be temporarily locked
    And an error message "Account locked" should be displayed
```

### Pattern: Boundary Testing

```python
@pytest.mark.parametrize('quantity,expected_result', [
    (0, 'Quantity must be at least 1'),           # Below minimum
    (1, 'Item added to cart'),                     # Minimum valid
    (100, 'Item added to cart'),                   # Maximum valid
    (101, 'Maximum quantity is 100'),              # Above maximum
])
def test_add_to_cart_quantity_validation(cart_page, product, quantity, expected_result):
    """
    Test boundary conditions for cart quantity
    """
    cart_page.select_product(product)
    cart_page.enter_quantity(quantity)
    cart_page.click_add_to_cart()

    assert cart_page.get_message() == expected_result
```

## 🎯 Scenario Tagging and Filtering

### Behave Tags

```gherkin
@smoke @authentication
Feature: User Login

  @happy_path
  Scenario: Successful login
    Given a registered user
    When user logs in
    Then user sees dashboard

  @negative @security
  Scenario: Login with SQL injection attempt
    Given the login page
    When user enters "admin'--" as username
    Then login should fail securely
```

**Run specific tags**:

```bash
behave --tags=smoke
behave --tags=authentication --tags=happy_path
behave --tags=-slow  # Exclude slow tests
```

### Pytest Markers

```python
import pytest

@pytest.mark.smoke
@pytest.mark.authentication
class TestUserLogin:

    @pytest.mark.happy_path
    def test_successful_login(self, ...):
        """Test successful login"""
        pass

    @pytest.mark.negative
    @pytest.mark.security
    def test_sql_injection_protection(self, ...):
        """Test SQL injection is prevented"""
        pass
```

**Run specific markers**:

```bash
pytest -m smoke
pytest -m "authentication and happy_path"
pytest -m "not slow"
```

## 📝 Documentation as Code Pattern

### Living Documentation

Acceptance tests servem como **especificação executável**:

```gherkin
Feature: Shopping Cart Discount Rules
  As a customer
  I want to receive discounts based on my cart total
  So that I can save money on large purchases

  Business Rule: Free shipping for orders over $50
  Business Rule: 10% discount for orders over $100
  Business Rule: 20% discount for orders over $200

  Scenario: Free shipping applied for $60 order
    Given I have items worth $60 in my cart
    When I proceed to checkout
    Then shipping cost should be $0.00
    And I should see "Free Shipping Applied"

  Scenario: 10% discount applied for $150 order
    Given I have items worth $150 in my cart
    When I proceed to checkout
    Then discount should be $15.00
    And total should be $135.00
```

**Benefits**:

- Requirements documented in tests
- Always up-to-date (if test passes, docs are correct)
- Stakeholders can read and verify

______________________________________________________________________

**Next**: See EXAMPLES.md for complete project implementations.
