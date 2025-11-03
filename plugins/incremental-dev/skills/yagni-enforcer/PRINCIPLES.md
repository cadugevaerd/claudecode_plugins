# YAGNI Principles

**YAGNI (You Aren't Gonna Need It)** - Core principles for incremental development and avoiding over-engineering.

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

## 📏 The Rule of 3

**Wait for 3 similar cases before creating abstraction:**

- **1 case**: Direct function
- **2 cases**: Two functions (duplication OK!)
- **3 cases**: NOW abstract (pattern emerged)

### Example: Validators

#### 1 Validator (no abstraction)

````python
def validate_email(email):
    return "@" in email

```text

#### 2 Validators (still no abstraction)

```python
def validate_email(email):
    return "@" in email

def validate_phone(phone):  # Duplication is OK!
    return len(phone) == 10

```text

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

```text


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


## 🔄 When to Refactor

**DO NOT refactor during increment** unless:
- ✅ Clear pattern emerged (3+ similar cases)
- ✅ Obvious duplication (exact copy-paste)
- ✅ Impossible to add increment without refactoring

**Refactor AFTER** several increments, not during.


## 📈 Incremental Development Strategy

### 1. Add, Don't Modify (when possible)
Prefer adding new code to modifying existing:
- Less risk of breaking
- Easy to revert
- Pattern becomes clearer

### 2. Test After Each Increment
After each increment:

```text

✅ POST-INCREMENT CHECKLIST:
- [ ] Code compiled/executed without error
- [ ] Functionality works (manual test)
- [ ] Old code still works
- [ ] Commit the increment

```text

### 3. One Increment at a Time
- Don't add multiple features together
- Simple first, then abstractions
- Working > Perfection
- Reversible (small increment is easy to revert)
- Testable (small increment is easy to test)


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


## 🎓 Remember

- YAGNI = Delete unnecessary code
- Simple > Complex
- Less code = Fewer bugs
- Abstractions should emerge, not be planned
- If it's not used, probably not necessary
- "Ugly but functional" > "Beautiful but complex"
- Refactor = Simplify, not complicate
- **Document over-engineering learnings in PRD**


**This is a LIVING principles document. Update as new patterns emerge!**
````
