# YAGNI Reference Guide

**YAGNI (You Aren't Gonna Need It)** - Complete reference for incremental development principles.

This document centralizes all YAGNI principles, patterns, and anti-patterns used across the incremental-dev plugin. Reference this document instead of duplicating content in commands.

---

## 📚 Core YAGNI Principles

### 1. You Aren't Gonna Need It
Don't implement functionality until it is REALLY necessary.

### 2. Simplicity First
Simple, direct code is better than premature abstractions.

### 3. Evolutionary Architecture
Architecture evolves as new requirements emerge, not beforehand.

### 4. Fast Feedback
MVP allows testing hypotheses quickly with less code.

### 5. Refactoring at the Right Time
Refactor when PATTERNS EMERGE, not anticipatorily.

### Core Mantras

- **Delete > Refactor**: If it's not used, delete it (don't "improve" it)
- **Simple > Elegant**: Simple code > "Well-architected" code
- **Direct > Abstract**: Direct call > Complex abstraction
- **Now > Future**: Solve current problem, not hypothetical future
- **Measure Use**: If unused for 3+ months, probably unnecessary
- **Working > Perfect**: Code that works > "Beautiful" code
- **Less Code = Fewer Bugs**: Minimal code reduces bug surface area

---

## 🚨 Common Over-Engineering Patterns

### Category 1: Premature Abstractions

#### ❌ Abstract Class with Single Implementation
```python
class AbstractProcessor(ABC):  # ← Unnecessary!
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):  # Only implementation
    def process(self): ...
```

**✅ Simplify to**:
```python
def process_email(data):  # Direct function
    ...
```

---

#### ❌ Interface for 1-2 Implementations
```python
class IValidator(Protocol):  # ← Over-engineering
    def validate(self, data) -> bool: ...

# Only 2 implementations
```

**✅ Simplify to**:
```python
def validate_email(email): ...
def validate_phone(phone): ...
```

---

#### ❌ Factory Without Variation
```python
class ProcessorFactory:  # ← Unnecessary
    def create(self):
        return EmailProcessor()  # Always returns same!
```

**✅ Simplify to**:
```python
processor = EmailProcessor()  # Direct!
```

---

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
```

**✅ Simplify to**:
```python
CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "debug": False
}
```

---

#### ❌ Environment Variables with Manager Class
```python
class EnvManager:
    def get_api_key(self):
        return os.getenv("API_KEY")

    def get_timeout(self):
        return int(os.getenv("TIMEOUT", "30"))

    # 10+ methods for envs
```

**✅ Simplify to**:
```python
API_KEY = os.getenv("API_KEY")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
```

---

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
```

**✅ Simplify to**:
```python
def send_email(email):
    # Simple function!
```

---

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
```

**✅ Simplify to**:
```python
def on_event_happened():
    handle_event()  # Direct call!
```

---

#### ❌ Strategy Pattern Without Runtime Variation
```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

class QuickSort(SortStrategy): ...
class MergeSort(SortStrategy): ...

# Always uses QuickSort, never switches
sorter = QuickSort()
```

**✅ Simplify to**:
```python
data.sort()  # Use Python's default!
```

---

### Category 4: Unused Code

#### ❌ Functions/Classes Never Called
```python
# Search in codebase:
# - Definition exists
# - No calls found

class LegacyProcessor:  # ← Nobody uses
    def process(self): ...
```

**✅ Action**:
```
DELETE completely
```

---

#### ❌ Unused Parameters
```python
def process_email(email, retry=3, timeout=30, debug=False):
    # retry, timeout, debug never used in code
    send(email)
```

**✅ Simplify to**:
```python
def process_email(email):
    send(email)
```

---

#### ❌ Unused Imports
```python
import requests  # ← Not used
from typing import Dict, List, Optional  # ← Only Dict used
```

**✅ Simplify to**:
```python
from typing import Dict
```

---

## 📏 The Rule of 3

**Wait for 3 similar cases before creating abstraction:**

- **1 case**: Direct function
- **2 cases**: Two functions (duplication OK!)
- **3 cases**: NOW abstract (pattern emerged)

### Example: Validators

#### 1 Validator (no abstraction)
```python
def validate_email(email):
    return "@" in email
```

#### 2 Validators (still no abstraction)
```python
def validate_email(email):
    return "@" in email

def validate_phone(phone):  # Duplication is OK!
    return len(phone) == 10
```

#### 3 Validators (NOW abstract)
```python
# Pattern emerged! Now create abstraction
VALIDATORS = {
    "email": lambda x: "@" in x,
    "phone": lambda x: len(x) == 10,
    "zip": lambda x: len(x) == 5
}

def validate(data, type):
    return VALIDATORS[type](data)
```

---

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
```

---

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
```

---

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
```

---

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
```

---

## ✅ YAGNI Checklist for Code Review

### For Each File:

```
[ ] Abstract classes have 3+ implementations?
    ❌ Less than 3 → REMOVE abstraction

[ ] Factory creates 3+ different types?
    ❌ Only 1-2 → USE direct creation

[ ] Pattern used in 3+ contexts?
    ❌ Only 1-2 → SIMPLIFY to function

[ ] Configuration manages 10+ values?
    ❌ Less than 10 → USE dict/constants

[ ] Function has 3+ parameters used?
    ❌ Unused parameters → REMOVE

[ ] Class has state that varies?
    ❌ Stateless → USE function

[ ] Code used in last 3 months?
    ❌ Not used → DELETE

[ ] Complexity justified by real requirement?
    ❌ Anticipated complexity → SIMPLIFY
```

---

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
```

**✅ Correct increment**:
```python
def validate_email(email):
    return "@" in email  # Simple function!
```

---

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
```

**✅ Correct increment**:
```python
MAX_RETRIES = 1  # Simple constant!
```

---

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
```

**✅ Correct increment**:
```python
def process_email(email): ...
def process_sms(sms): ...  # Two functions for now!
```

**When to create abstraction?**: When you have 3+ processors AND clear pattern emerged.

---

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

---

## 📊 Signs of Over-Engineering in MVP

### MVP Anti-Patterns

#### ❌ Abstract classes in MVP
```python
# OVER-ENGINEERING
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass
```

**✅ MVP correct**:
```python
# SIMPLE FUNCTION
def process_email(email):
    return "processed"
```

---

#### ❌ Factory Pattern in MVP
```python
# OVER-ENGINEERING
class ProcessorFactory:
    def create_processor(self, type): ...
```

**✅ MVP correct**:
```python
# DIRECT CALL
result = process_email(email)
```

---

#### ❌ Complex configuration in MVP
```python
# OVER-ENGINEERING
config = ConfigManager()
config.load_from_yaml()
config.validate_schema()
```

**✅ MVP correct**:
```python
# HARDCODED IS OK FOR MVP!
MAX_RETRIES = 3
```

---

## 💡 MVP Principles

### What MVP Should Be:

- ✅ Simplest implementation that works
- ✅ Direct code without abstractions
- ✅ Minimal validations
- ✅ Hardcoded configuration OK
- ✅ Focus on WORKING, not "beautiful code"

### What MVP Should NOT Be:

- ❌ Perfect architecture
- ❌ Multiple design patterns
- ❌ Complex validations
- ❌ Sophisticated error handling
- ❌ Premature optimizations
- ❌ "Future-proof" design

---

## 🔄 When to Refactor

**DO NOT refactor during increment** unless:
- ✅ Clear pattern emerged (3+ similar cases)
- ✅ Obvious duplication (exact copy-paste)
- ✅ Impossible to add increment without refactoring

**Refactor AFTER** several increments, not during.

---

## 📈 Incremental Development Strategy

### 1. Add, Don't Modify (when possible)
Prefer adding new code to modifying existing:
- Less risk of breaking
- Easy to revert
- Pattern becomes clearer

### 2. Test After Each Increment
After each increment:
```
✅ POST-INCREMENT CHECKLIST:
- [ ] Code compiled/executed without error
- [ ] Functionality works (manual test)
- [ ] Old code still works
- [ ] Commit the increment
```

### 3. One Increment at a Time
- Don't add multiple features together
- Simple first, then abstractions
- Working > Perfection
- Reversible (small increment is easy to revert)
- Testable (small increment is easy to test)

---

## 📏 Ideal Increment Size

**Recommended size**:
- ⏱️ **Time**: 30 minutes to 2 hours of work
- 📁 **Files**: Modify 1-3 files maximum
- 📝 **Lines**: Add/change 20-100 lines of code
- 🧪 **Tests**: 1-3 new test cases

**If increment too large**:
- Break down into smaller increments
- Example:
  - ❌ "Add authentication with OAuth, JWT, and role-based access"
  - ✅ "Add basic authentication with hardcoded user"
  - ✅ (Next) "Add JWT token generation"
  - ✅ (Next) "Add role-based access control"

---

## 🎓 Remember

- YAGNI = Delete unnecessary code
- Simple > Complex
- Less code = Fewer bugs
- Abstractions should emerge, not be planned
- If it's not used, probably not necessary
- "Ugly but functional" > "Beautiful but complex"
- Refactor = Simplify, not complicate
- **Document over-engineering learnings in PRD**

---

**This is a LIVING reference document. Update as new patterns emerge!**
