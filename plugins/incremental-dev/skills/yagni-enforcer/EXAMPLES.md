# YAGNI Examples & Anti-Patterns

**Common over-engineering patterns with code examples - What NOT to do, and the correct approach.**

## 🚨 Common Over-Engineering Patterns

### Category 1: Premature Abstractions

#### ❌ Abstract Class with Single Implementation

````python
class AbstractProcessor(ABC):  # ← Unnecessary!
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):  # Only implementation
    def process(self): ...

```text

**✅ Simplify to**:

```python
def process_email(data):  # Direct function
    ...

```text


#### ❌ Interface for 1-2 Implementations

```python
class IValidator(Protocol):  # ← Over-engineering
    def validate(self, data) -> bool: ...

# Only 2 implementations

```text

**✅ Simplify to**:

```python
def validate_email(email): ...
def validate_phone(phone): ...

```text


#### ❌ Factory Without Variation

```python
class ProcessorFactory:  # ← Unnecessary
    def create(self):
        return EmailProcessor()  # Always returns same!

```text

**✅ Simplify to**:

```python
processor = EmailProcessor()  # Direct!

```text


### Category 2: Excessive Configuration

#### ❌ Complex ConfigurationManager

```python
class ConfigurationManager:
    def __init__(self):
        self.config = {}

    def load_from_yaml(self, path):
        # 50 lines loading YAML

    def validate_schema(self):
        # 30 lines validating

    def get(self, key, default=None):
        # 20 lines with cache/observers

    # Total: 150+ lines for 3 configs!

```text

**✅ Simplify to**:

```python
CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "debug": False
}

```text


#### ❌ Environment Variables with Manager Class

```python
class EnvManager:
    def get_api_key(self):
        return os.getenv("API_KEY")

    def get_timeout(self):
        return int(os.getenv("TIMEOUT", "30"))

    # 10+ methods for envs

```text

**✅ Simplify to**:

```python
API_KEY = os.getenv("API_KEY")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))

```text


### Category 3: Unnecessary Patterns

#### ❌ Singleton for Stateless Object

```python
class EmailSender:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def send(self, email):
        # Stateless function - doesn't need singleton!

```text

**✅ Simplify to**:

```python
def send_email(email):
    # Simple function!

```text


#### ❌ Observer Pattern Without Need

```python
class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer): ...
    def notify(self): ...

class ConcreteObserver:
    def update(self): ...

# Used only in 1 place, no dynamic switching

```text

**✅ Simplify to**:

```python
def on_event_happened():
    handle_event()  # Direct call!

```text


#### ❌ Strategy Pattern Without Runtime Variation

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

class QuickSort(SortStrategy): ...
class MergeSort(SortStrategy): ...

# Always uses QuickSort, never switches
sorter = QuickSort()

```text

**✅ Simplify to**:

```python
data.sort()  # Use Python's default!

```text


### Category 4: Unused Code

#### ❌ Functions/Classes Never Called

```python

# Search in codebase:

# - Definition exists

# - No calls found

class LegacyProcessor:  # ← Nobody uses
    def process(self): ...

```text

**✅ Action**:

```text

DELETE completely

```text


#### ❌ Unused Parameters

```python
def process_email(email, retry=3, timeout=30, debug=False):
    # retry, timeout, debug never used in code
    send(email)

```text

**✅ Simplify to**:

```python
def process_email(email):
    send(email)

```text


#### ❌ Unused Imports

```python
import requests  # ← Not used
from typing import Dict, List, Optional  # ← Only Dict used

```text

**✅ Simplify to**:

```python
from typing import Dict

```text


## 🎯 Simplification Strategies

### 1. Replace Class with Function

**When**: Class without state (stateless)

```python

# Before
class EmailValidator:
    def validate(self, email):
        return "@" in email

validator = EmailValidator()
result = validator.validate(email)

# After
def validate_email(email):
    return "@" in email

result = validate_email(email)

```text


### 2. Inline Complex Abstraction

**When**: Abstraction used only once

```python

# Before
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):
    def process(self):
        return send_email()

processor = EmailProcessor()
result = processor.process()

# After
result = send_email()  # Direct!

```text


### 3. Replace Configuration Class with Constants

**When**: Simple configuration (< 10 values)

```python

# Before (50 lines)
class Config:
    def __init__(self):
        self._config = self._load()

    def _load(self):
        # complexity...

    def get(self, key):
        # more complexity...

config = Config()
max_retries = config.get("max_retries")

# After (3 lines)
MAX_RETRIES = 3
TIMEOUT = 30

```text


### 4. Remove Unused Code

**When**: Code not called

```python

# Before
class LegacyProcessor:  # Nobody uses
    def process(self): ...

def old_function():  # Nobody calls
    ...

# After

# [DELETED]

```text


## 🚧 Detecting Over-Engineering During Increments

### Warning Signs When Adding Features:

#### ❌ Pattern 1: Creating Class for Simple Function

```python

# OVER-ENGINEERING when adding validation
class EmailValidator:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def validate(self, email):
        for rule in self.rules:
            if not rule.check(email):
                return False
        return True

validator = EmailValidator()
validator.add_rule(HasAtSymbolRule())

```text

**✅ Correct increment**:

```python
def validate_email(email):
    return "@" in email  # Simple function!

```text


#### ❌ Pattern 2: Adding Complex Configuration

```python

# OVER-ENGINEERING when adding retry
config = {
    "retry": {
        "max_attempts": 3,
        "backoff": "exponential",
        "initial_delay": 1,
        "max_delay": 60,
        "exceptions": [NetworkError, TimeoutError]
    }
}

```text

**✅ Correct increment**:

```python
MAX_RETRIES = 1  # Simple constant!

```text


#### ❌ Pattern 3: Creating Premature Abstraction

```python

# OVER-ENGINEERING when adding second processor
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self, data): pass

class EmailProcessor(AbstractProcessor):
    def process(self, data): ...

class SMSProcessor(AbstractProcessor):
    def process(self, data): ...

```text

**✅ Correct increment**:

```python
def process_email(email): ...
def process_sms(sms): ...  # Two functions for now!

```text

**When to create abstraction?**: When you have 3+ processors AND clear pattern emerged.


## 🔍 Questions to Ask Before Implementing

**ALWAYS question**:
- "Do you need this NOW?"
- "What happens if we don't implement this?"
- "Does this solve the minimum problem?"

**Avoid phrases like**:
- ❌ "Let's prepare for the future..."
- ❌ "In case we need to add..."
- ❌ "To facilitate expansion..."
- ❌ "Following clean architecture..."

**Prefer phrases like**:
- ✅ "Let's make it work first"
- ✅ "We can add this when necessary"
- ✅ "Focus on current use case"
- ✅ "We'll refactor when pattern emerges"


## 📊 Signs of Over-Engineering in MVP

### MVP Anti-Patterns

#### ❌ Abstract classes in MVP

```python

# OVER-ENGINEERING
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass

```text

**✅ MVP correct**:

```python

# SIMPLE FUNCTION
def process_email(email):
    return "processed"

```text


#### ❌ Factory Pattern in MVP

```python

# OVER-ENGINEERING
class ProcessorFactory:
    def create_processor(self, type): ...

```text

**✅ MVP correct**:

```python

# DIRECT CALL
result = process_email(email)

```text


#### ❌ Complex configuration in MVP

```python

# OVER-ENGINEERING
config = ConfigManager()
config.load_from_yaml()
config.validate_schema()

```text

**✅ MVP correct**:

```python

# HARDCODED IS OK FOR MVP!
MAX_RETRIES = 3

```text


**This is a LIVING examples document. Add new patterns as they emerge!**
````
