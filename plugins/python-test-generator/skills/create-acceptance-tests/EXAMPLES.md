# Acceptance Testing Examples - Complete Project Implementations

Exemplos completos e práticos de acceptance tests usando behave, pytest-bdd e pytest puro.

## 📦 Example 1: E-commerce Application (Behave)

### Project Structure

```
ecommerce_project/
├── features/
│   ├── environment.py
│   ├── authentication.feature
│   ├── shopping_cart.feature
│   ├── checkout.feature
│   └── steps/
│       ├── authentication_steps.py
│       ├── shopping_cart_steps.py
│       └── checkout_steps.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── product_page.py
│   └── checkout_page.py
├── helpers/
│   └── test_data.py
├── requirements-test.txt
└── behave.ini
```

### Configuration Files

**behave.ini**:

```ini
[behave]
show_skipped = false
show_timings = true
color = true
format = pretty
stdout_capture = false
stderr_capture = false
log_capture = true

[behave.userdata]
base_url = http://localhost:8000
browser = chrome
headless = false
```

**requirements-test.txt**:

```
behave==1.2.6
selenium==4.15.0
webdriver-manager==4.0.1
```

### Feature Files

**features/shopping_cart.feature**:

```gherkin
Feature: Shopping Cart Management
  As a customer
  I want to manage items in my shopping cart
  So that I can purchase the products I need

  Background:
    Given the following products are available:
      | name          | price | stock |
      | Laptop        | 999   | 10    |
      | Mouse         | 25    | 50    |
      | Keyboard      | 75    | 30    |
    And I am logged in as a customer

  Scenario: Add single item to cart
    When I add "Laptop" to my cart with quantity 1
    Then my cart should contain 1 item
    And the cart total should be "$999.00"

  Scenario: Add multiple items to cart
    When I add "Laptop" to my cart with quantity 1
    And I add "Mouse" to my cart with quantity 2
    Then my cart should contain 3 items
    And the cart total should be "$1,049.00"

  Scenario: Remove item from cart
    Given I have "Laptop" in my cart
    When I remove "Laptop" from my cart
    Then my cart should be empty
    And the cart total should be "$0.00"

  Scenario: Update item quantity in cart
    Given I have "Mouse" in my cart with quantity 2
    When I update "Mouse" quantity to 5
    Then my cart should contain 5 items
    And the cart total should be "$125.00"

  @negative
  Scenario: Cannot add out of stock item
    Given "Laptop" is out of stock
    When I attempt to add "Laptop" to my cart
    Then I should see an error "Product out of stock"
    And my cart should be empty
```

**features/checkout.feature**:

```gherkin
Feature: Order Checkout
  As a customer
  I want to complete the checkout process
  So that I can purchase my items

  Background:
    Given I am logged in as a customer
    And I have the following items in my cart:
      | product  | quantity |
      | Laptop   | 1        |
      | Mouse    | 2        |

  @happy_path
  Scenario: Successful checkout with credit card
    Given I am on the checkout page
    When I enter shipping address:
      | field      | value           |
      | street     | 123 Main St     |
      | city       | San Francisco   |
      | state      | CA              |
      | zip        | 94102           |
    And I select "Credit Card" as payment method
    And I enter credit card details:
      | field  | value           |
      | number | 4111111111111111|
      | expiry | 12/25           |
      | cvv    | 123             |
    And I confirm the order
    Then I should see order confirmation
    And I should receive a confirmation email
    And my cart should be empty

  @negative
  Scenario: Checkout fails with invalid credit card
    Given I am on the checkout page
    When I enter shipping address with valid details
    And I select "Credit Card" as payment method
    And I enter invalid credit card number "1234"
    And I confirm the order
    Then I should see an error "Invalid credit card number"
    And the order should not be created

  Scenario: Apply discount code
    Given I am on the checkout page
    And a discount code "SAVE10" exists for 10% off
    When I enter shipping address with valid details
    And I apply discount code "SAVE10"
    Then the discount should be "$104.90"
    And the total should be "$944.10"
```

### Step Definitions

**features/steps/shopping_cart_steps.py**:

```python
from behave import given, when, then
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from helpers.test_data import create_product

@given('the following products are available')
def step_impl(context):
    """Create products from table"""
    context.products = {}
    for row in context.table:
        product = create_product(
            name=row['name'],
            price=float(row['price']),
            stock=int(row['stock'])
        )
        context.products[row['name']] = product

@given('I am logged in as a customer')
def step_impl(context):
    """Login as test customer"""
    from pages.login_page import LoginPage
    login_page = LoginPage(context.browser)
    login_page.navigate()
    login_page.login(
        email=context.test_user['email'],
        password=context.test_user['password']
    )

@when('I add "{product_name}" to my cart with quantity {quantity:d}')
def step_impl(context, product_name, quantity):
    """Add product to cart"""
    product_page = ProductPage(context.browser)
    product_page.search_product(product_name)
    product_page.select_product(product_name)
    product_page.set_quantity(quantity)
    product_page.click_add_to_cart()

@then('my cart should contain {count:d} item(s)')
def step_impl(context, count):
    """Verify cart item count"""
    cart_page = CartPage(context.browser)
    cart_page.navigate()
    assert cart_page.get_item_count() == count, \
        f"Expected {count} items, but found {cart_page.get_item_count()}"

@then('the cart total should be "{expected_total}"')
def step_impl(context, expected_total):
    """Verify cart total"""
    cart_page = CartPage(context.browser)
    actual_total = cart_page.get_total()
    assert actual_total == expected_total, \
        f"Expected total {expected_total}, but got {actual_total}"

@given('I have "{product_name}" in my cart')
def step_impl(context, product_name):
    """Add product to cart via API or UI"""
    # Fast approach: Use API to add to cart
    from api.cart_api import add_to_cart
    product = context.products[product_name]
    add_to_cart(context.test_user['id'], product.id, quantity=1)

@given('I have "{product_name}" in my cart with quantity {quantity:d}')
def step_impl(context, product_name, quantity):
    """Add product with specific quantity"""
    from api.cart_api import add_to_cart
    product = context.products[product_name]
    add_to_cart(context.test_user['id'], product.id, quantity=quantity)

@when('I remove "{product_name}" from my cart')
def step_impl(context, product_name):
    """Remove product from cart"""
    cart_page = CartPage(context.browser)
    cart_page.navigate()
    cart_page.remove_item(product_name)

@when('I update "{product_name}" quantity to {new_quantity:d}')
def step_impl(context, product_name, new_quantity):
    """Update item quantity in cart"""
    cart_page = CartPage(context.browser)
    cart_page.navigate()
    cart_page.update_quantity(product_name, new_quantity)

@then('my cart should be empty')
def step_impl(context):
    """Verify cart is empty"""
    cart_page = CartPage(context.browser)
    assert cart_page.is_empty(), "Cart should be empty but contains items"

@given('"{product_name}" is out of stock')
def step_impl(context, product_name):
    """Set product stock to 0"""
    product = context.products[product_name]
    product.stock = 0
    context.db.commit()

@when('I attempt to add "{product_name}" to my cart')
def step_impl(context, product_name):
    """Try to add out-of-stock product"""
    product_page = ProductPage(context.browser)
    product_page.search_product(product_name)
    product_page.select_product(product_name)
    product_page.click_add_to_cart()

@then('I should see an error "{error_message}"')
def step_impl(context, error_message):
    """Verify error message displayed"""
    from pages.base_page import BasePage
    base_page = BasePage(context.browser)
    actual_error = base_page.get_error_message()
    assert error_message in actual_error, \
        f"Expected error '{error_message}', but got '{actual_error}'"
```

**features/steps/checkout_steps.py**:

```python
from behave import given, when, then
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage

@given('I have the following items in my cart')
def step_impl(context):
    """Add items to cart from table"""
    from api.cart_api import add_to_cart
    for row in context.table:
        product = context.products[row['product']]
        quantity = int(row['quantity'])
        add_to_cart(context.test_user['id'], product.id, quantity)

@given('I am on the checkout page')
def step_impl(context):
    """Navigate to checkout"""
    checkout_page = CheckoutPage(context.browser)
    checkout_page.navigate()
    context.checkout_page = checkout_page

@when('I enter shipping address')
def step_impl(context):
    """Enter shipping address from table"""
    address_data = {row['field']: row['value'] for row in context.table}
    context.checkout_page.enter_shipping_address(address_data)

@when('I select "{payment_method}" as payment method')
def step_impl(context, payment_method):
    """Select payment method"""
    context.checkout_page.select_payment_method(payment_method)

@when('I enter credit card details')
def step_impl(context):
    """Enter credit card from table"""
    card_data = {row['field']: row['value'] for row in context.table}
    context.checkout_page.enter_card_details(card_data)

@when('I confirm the order')
def step_impl(context):
    """Click confirm order button"""
    context.checkout_page.confirm_order()

@then('I should see order confirmation')
def step_impl(context):
    """Verify order confirmation page"""
    confirmation_page = OrderConfirmationPage(context.browser)
    assert confirmation_page.is_displayed(), \
        "Order confirmation page should be displayed"
    context.order_number = confirmation_page.get_order_number()

@then('I should receive a confirmation email')
def step_impl(context):
    """Verify confirmation email sent"""
    from helpers.email_helper import check_email_sent
    assert check_email_sent(
        to=context.test_user['email'],
        subject=f"Order Confirmation #{context.order_number}"
    ), "Confirmation email not sent"

@given('a discount code "{code}" exists for {percent:d}% off')
def step_impl(context, code, percent):
    """Create discount code"""
    from models import DiscountCode
    discount = DiscountCode(code=code, percent=percent)
    context.db.add(discount)
    context.db.commit()
    context.discount_code = discount

@when('I apply discount code "{code}"')
def step_impl(context, code):
    """Apply discount code"""
    context.checkout_page.enter_discount_code(code)
    context.checkout_page.apply_discount()

@then('the discount should be "{expected_discount}"')
def step_impl(context, expected_discount):
    """Verify discount amount"""
    actual_discount = context.checkout_page.get_discount_amount()
    assert actual_discount == expected_discount, \
        f"Expected discount {expected_discount}, but got {actual_discount}"
```

### Environment Setup

**features/environment.py**:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from helpers.test_data import create_test_user
from models import db

def before_all(context):
    """Setup once before all features"""
    # Database setup
    context.db = db
    context.base_url = context.config.userdata.get('base_url', 'http://localhost:8000')

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Browser setup
    options = webdriver.ChromeOptions()
    if context.config.userdata.get('headless', 'false').lower() == 'true':
        options.add_argument('--headless')

    service = Service(ChromeDriverManager().install())
    context.browser = webdriver.Chrome(service=service, options=options)
    context.browser.implicitly_wait(10)
    context.browser.maximize_window()

    # Create test user
    context.test_user = create_test_user(
        email='testuser@example.com',
        password='TestPass123'
    )

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    # Screenshot on failure
    if scenario.status == 'failed':
        screenshot_name = f"screenshots/{scenario.name.replace(' ', '_')}.png"
        context.browser.save_screenshot(screenshot_name)
        print(f"Screenshot saved: {screenshot_name}")

    # Close browser
    context.browser.quit()

    # Database cleanup
    context.db.rollback()

def after_all(context):
    """Cleanup after all features"""
    pass
```

### Page Objects

**pages/base_page.py**:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    """Base class for all page objects"""

    def __init__(self, browser, base_url='http://localhost:8000'):
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(browser, 10)

    def navigate(self, path=''):
        """Navigate to page"""
        self.browser.get(f"{self.base_url}{path}")

    def find_element(self, *locator):
        """Find element with wait"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, *locator):
        """Find multiple elements"""
        return self.browser.find_elements(*locator)

    def click(self, *locator):
        """Click element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, text, *locator):
        """Enter text in input field"""
        element = self.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, *locator):
        """Get element text"""
        return self.find_element(*locator).text

    def is_element_present(self, *locator, timeout=5):
        """Check if element is present"""
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_error_message(self):
        """Get error message from page"""
        from selenium.webdriver.common.by import By
        return self.get_text(By.CLASS_NAME, 'error-message')
```

**pages/cart_page.py**:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Shopping cart page object"""

    # Locators
    CART_ITEMS = (By.CLASS_NAME, 'cart-item')
    ITEM_NAME = (By.CLASS_NAME, 'item-name')
    ITEM_QUANTITY = (By.CLASS_NAME, 'item-quantity')
    REMOVE_BUTTON = (By.CLASS_NAME, 'remove-item')
    CART_TOTAL = (By.ID, 'cart-total')
    EMPTY_CART_MESSAGE = (By.CLASS_NAME, 'empty-cart')

    def navigate(self):
        """Navigate to cart page"""
        super().navigate('/cart')

    def get_item_count(self):
        """Get total number of items in cart"""
        items = self.find_elements(*self.CART_ITEMS)
        total_quantity = 0
        for item in items:
            quantity_text = item.find_element(*self.ITEM_QUANTITY).text
            total_quantity += int(quantity_text)
        return total_quantity

    def get_total(self):
        """Get cart total"""
        return self.get_text(*self.CART_TOTAL)

    def is_empty(self):
        """Check if cart is empty"""
        return self.is_element_present(*self.EMPTY_CART_MESSAGE)

    def remove_item(self, product_name):
        """Remove item from cart by name"""
        items = self.find_elements(*self.CART_ITEMS)
        for item in items:
            name = item.find_element(*self.ITEM_NAME).text
            if name == product_name:
                item.find_element(*self.REMOVE_BUTTON).click()
                return
        raise ValueError(f"Product '{product_name}' not found in cart")

    def update_quantity(self, product_name, new_quantity):
        """Update item quantity"""
        items = self.find_elements(*self.CART_ITEMS)
        for item in items:
            name = item.find_element(*self.ITEM_NAME).text
            if name == product_name:
                quantity_input = item.find_element(*self.ITEM_QUANTITY)
                quantity_input.clear()
                quantity_input.send_keys(str(new_quantity))
                # Trigger update (e.g., blur event)
                self.browser.execute_script("arguments[0].blur();", quantity_input)
                return
        raise ValueError(f"Product '{product_name}' not found in cart")
```

## 📦 Example 2: REST API Testing (Pytest-BDD)

### Project Structure

```
api_project/
├── tests/
│   ├── acceptance/
│   │   ├── features/
│   │   │   ├── user_api.feature
│   │   │   └── order_api.feature
│   │   ├── test_user_api.py
│   │   ├── test_order_api.py
│   │   └── conftest.py
│   └── conftest.py
├── pytest.ini
└── requirements-test.txt
```

### Feature File

**tests/acceptance/features/user_api.feature**:

```gherkin
Feature: User API
  Test user management via REST API

  Scenario: Create new user
    When I send POST request to "/api/users" with data:
      """
      {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "SecurePass123"
      }
      """
    Then the response status code should be 201
    And the response should contain field "id"
    And the response should contain field "email" with value "newuser@example.com"
    And the response should not contain field "password"

  Scenario: Get user by ID
    Given a user exists with email "john@example.com"
    When I send GET request to "/api/users/{user_id}"
    Then the response status code should be 200
    And the response should match:
      """
      {
        "id": "{user_id}",
        "email": "john@example.com",
        "name": "John Doe"
      }
      """

  Scenario: Update user email
    Given a user exists with email "old@example.com"
    When I send PATCH request to "/api/users/{user_id}" with data:
      """
      {"email": "new@example.com"}
      """
    Then the response status code should be 200
    And the user email should be updated to "new@example.com"

  Scenario: Delete user
    Given a user exists with email "delete@example.com"
    When I send DELETE request to "/api/users/{user_id}"
    Then the response status code should be 204
    And the user should not exist in database
```

### Test Implementation

**tests/acceptance/test_user_api.py**:

```python
import pytest
import json
from pytest_bdd import scenarios, given, when, then, parsers

# Load all scenarios from feature file
scenarios('features/user_api.feature')

@when(parsers.parse('I send {method} request to "{endpoint}" with data:\n{data}'))
def send_request_with_data(api_client, method, endpoint, data, context):
    """Send API request with JSON data"""
    payload = json.loads(data)
    response = api_client.request(method, endpoint, json=payload)
    context['response'] = response
    context['endpoint'] = endpoint

@when(parsers.parse('I send {method} request to "{endpoint}"'))
def send_request(api_client, method, endpoint, context, user_id):
    """Send API request without data"""
    # Replace {user_id} placeholder with actual ID
    endpoint = endpoint.replace('{user_id}', str(user_id))
    response = api_client.request(method, endpoint)
    context['response'] = response

@then(parsers.parse('the response status code should be {expected_status:d}'))
def verify_status_code(context, expected_status):
    """Verify response status code"""
    actual_status = context['response'].status_code
    assert actual_status == expected_status, \
        f"Expected status {expected_status}, got {actual_status}"

@then(parsers.parse('the response should contain field "{field}"'))
def verify_field_exists(context, field):
    """Verify field exists in response"""
    response_data = context['response'].json()
    assert field in response_data, \
        f"Field '{field}' not found in response: {response_data}"

@then(parsers.parse('the response should contain field "{field}" with value "{expected_value}"'))
def verify_field_value(context, field, expected_value):
    """Verify field value in response"""
    response_data = context['response'].json()
    actual_value = response_data.get(field)
    assert str(actual_value) == expected_value, \
        f"Expected {field}='{expected_value}', got '{actual_value}'"

@then(parsers.parse('the response should not contain field "{field}"'))
def verify_field_not_present(context, field):
    """Verify field does not exist in response"""
    response_data = context['response'].json()
    assert field not in response_data, \
        f"Field '{field}' should not be in response but was found"

@then(parsers.parse('the response should match:\n{expected_json}'))
def verify_response_matches(context, expected_json, user_id):
    """Verify response matches expected JSON"""
    expected = json.loads(expected_json.replace('{user_id}', str(user_id)))
    actual = context['response'].json()
    assert actual == expected, \
        f"Response mismatch.\nExpected: {expected}\nActual: {actual}"

@given(parsers.parse('a user exists with email "{email}"'))
def create_user(db_session, email, context):
    """Create test user in database"""
    from models import User
    user = User(email=email, name="John Doe")
    user.set_password("TestPass123")
    db_session.add(user)
    db_session.commit()
    context['user_id'] = user.id
    return user.id

@then(parsers.parse('the user email should be updated to "{new_email}"'))
def verify_email_updated(db_session, context, new_email):
    """Verify user email was updated in database"""
    from models import User
    user = db_session.query(User).get(context['user_id'])
    assert user.email == new_email, \
        f"Expected email '{new_email}', got '{user.email}'"

@then('the user should not exist in database')
def verify_user_deleted(db_session, context):
    """Verify user was deleted from database"""
    from models import User
    user = db_session.query(User).get(context['user_id'])
    assert user is None, "User should be deleted but still exists"
```

**tests/acceptance/conftest.py**:

```python
import pytest

@pytest.fixture
def context():
    """Shared context for storing data between steps"""
    return {}

@pytest.fixture
def user_id(context):
    """Get user ID from context"""
    return context.get('user_id')

@pytest.fixture
def api_client():
    """API client for making requests"""
    import requests

    class APIClient:
        BASE_URL = 'http://localhost:8000'

        def request(self, method, endpoint, **kwargs):
            url = f"{self.BASE_URL}{endpoint}"
            return requests.request(method, url, **kwargs)

    return APIClient()
```

## 📦 Example 3: CLI Application (Pytest Pure)

**tests/acceptance/test_cli_commands.py**:

```python
import pytest
import subprocess
import json

class TestUserCLI:
    """Acceptance tests for user management CLI"""

    def test_create_user_command_creates_new_user(self, cli_runner, temp_db):
        """
        Given a clean database
        When I run 'app user create' with valid user data
        Then a new user should be created
        And the command should output success message
        """
        # When
        result = cli_runner.invoke([
            'user', 'create',
            '--email', 'newuser@example.com',
            '--name', 'New User',
            '--password', 'SecurePass123'
        ])

        # Then
        assert result.exit_code == 0
        assert 'User created successfully' in result.output
        assert 'newuser@example.com' in result.output

        # Verify in database
        from models import User
        user = temp_db.query(User).filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.name == 'New User'

    def test_list_users_command_shows_all_users(self, cli_runner, users_fixture):
        """
        Given multiple users exist in the database
        When I run 'app user list'
        Then all users should be displayed
        And output should be formatted as table
        """
        # When
        result = cli_runner.invoke(['user', 'list'])

        # Then
        assert result.exit_code == 0
        for user in users_fixture:
            assert user.email in result.output
            assert user.name in result.output

    def test_delete_user_command_removes_user(self, cli_runner, existing_user):
        """
        Given a user exists
        When I run 'app user delete' with user ID
        Then the user should be deleted
        And a confirmation message should be shown
        """
        # When
        result = cli_runner.invoke([
            'user', 'delete',
            '--id', str(existing_user.id),
            '--confirm'
        ])

        # Then
        assert result.exit_code == 0
        assert 'User deleted successfully' in result.output

        # Verify deletion
        from models import User
        user = cli_runner.db.query(User).get(existing_user.id)
        assert user is None

    @pytest.mark.parametrize('invalid_email', [
        'notanemail',
        '@example.com',
        'user@',
        'user @example.com',
    ])
    def test_create_user_rejects_invalid_email(self, cli_runner, invalid_email):
        """
        Given various invalid email formats
        When I attempt to create user with invalid email
        Then the command should fail
        And an error message should be displayed
        """
        # When
        result = cli_runner.invoke([
            'user', 'create',
            '--email', invalid_email,
            '--name', 'Test User',
            '--password', 'TestPass123'
        ])

        # Then
        assert result.exit_code != 0
        assert 'Invalid email format' in result.output

@pytest.fixture
def cli_runner(temp_db):
    """CLI test runner"""
    from click.testing import CliRunner
    from app.cli import cli

    runner = CliRunner()
    runner.db = temp_db
    return runner

@pytest.fixture
def existing_user(temp_db):
    """Create existing user for tests"""
    from models import User
    user = User(email='existing@example.com', name='Existing User')
    user.set_password('TestPass123')
    temp_db.add(user)
    temp_db.commit()
    return user

@pytest.fixture
def users_fixture(temp_db):
    """Create multiple users"""
    from models import User
    users = [
        User(email=f'user{i}@example.com', name=f'User {i}')
        for i in range(1, 6)
    ]
    for user in users:
        user.set_password('TestPass123')
        temp_db.add(user)
    temp_db.commit()
    return users
```

______________________________________________________________________

**Conclusão**: Estes exemplos demonstram implementações completas para diferentes tipos de aplicações (web, API, CLI) usando os três frameworks principais (behave, pytest-bdd, pytest puro). Use-os como templates para seus próprios projetos.
