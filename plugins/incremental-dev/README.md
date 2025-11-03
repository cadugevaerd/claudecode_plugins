# Incremental Development Plugin

Master incremental development with **YAGNI** (You Aren't Gonna Need It) principles and **Evolutionary Architecture**. Avoid over-engineering, promote simplicity, and build features one step at a time.

## 🎯 What This Plugin Does

Acts as your development **coach**:

- ✅ Questions premature features
- ✅ Suggests minimal MVPs
- ✅ Detects over-engineering automatically
- ✅ Identifies perfect refactoring moments
- ✅ Prevents premature abstractions
- ❌ Never makes decisions without your approval

## 📦 Installation

````bash
/plugin marketplace add cadugevaerd/claudecode_plugins
/plugin install incremental-dev

```text

## 🧠 Core Concepts

### YAGNI (You Aren't Gonna Need It)

**Principle**: Don't add features until actually needed.

❌ **Wrong** (building for the future):
```python
def process_email(email, retry=3, timeout=30, async_mode=False):
    send(email)  # Extra params unused!
```

✅ **Right** (only what's needed now):
```python
def process_email(email):
    send(email)
# Add retry/timeout WHEN actually needed
```

### Evolutionary Architecture

Architecture evolves as requirements emerge, not planned upfront.

❌ **Over-engineering**:
```python
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):  # Only 1 implementation!
    def process(self): ...
```

✅ **Evolutionary**:
```python
# Iteration 1-4: Simple function
def process_email(email):
    ...

# Iteration 5: Now 3+ processors exist - TIME TO ABSTRACT
class Processor:
    def process(self): ...

class EmailProcessor(Processor): ...
class SMSProcessor(Processor): ...
```

### Rule of 3 (When to Refactor)

Refactor only when pattern appears 3+ times:

```
1 occurrence   → Keep inline (simple)
2 occurrences → Duplication OK
3+ occurrences → REFACTOR NOW! Pattern confirmed
```

### Incremental Development

Add one feature at a time, test, then next:

```
Iteration 1: MVP (basic email processing)
    ↓ test
Iteration 2: Add validation
    ↓ test
Iteration 3: Add retry logic
    ↓ test
Iteration 4: Refactor (patterns emerged)
```

## 🎯 5 Core Commands

### 1️⃣ `/init-incremental [description]`

**Initialize or adopt incremental development**

Auto-detects project type and applies appropriate setup.

```bash
# New projects (interactive)
/init-incremental "API for managing users"

# Existing projects - auto-detects
/init-incremental
```

**What it does**:
- Creates/updates `CLAUDE.md` with YAGNI principles
- Generates `PRD.md` (v0.1 for new, v1.0 for existing)
- Optional: Creates `ROADMAP.md` for legacy projects

**When to use**:
- Starting a new project
- Adopting incremental dev in existing project
- Modernizing legacy codebase

---

### 2️⃣ `/prd [subcommand]`

**Manage Product Requirements Document with flexible operations**

Unified command for PRD management with multiple subcommands:

```bash
# View PRD
/prd view                    # Full PRD
/prd view mvp               # Only MVP definition
/prd view status            # Current status & next steps
/prd view timeline          # Evolution timeline

# Update PRD by phase
/prd update descoberta      # Discovery phase (v0.1)
/prd update planejamento    # Planning phase (v1.0)
/prd update design          # Design phase (v1.1)
/prd update incremento      # Register increment (v1.x)
/prd update final           # Finalize as-built (v2.0)

# Make surgical fixes
/prd fix "Move feature X out of scope"
/prd fix "Update success metric to 500ms"

# Get help
/prd help                    # Interactive menu
/prd help "Your question"    # Direct answer
```

**When to use**:
- View project roadmap and status
- Update PRD as phases complete
- Make targeted PRD adjustments
- Answer questions about incremental dev

---

### 3️⃣ `/add-increment "feature description"`

**Implement next incremental feature with YAGNI discipline**

Adds one feature at a time, ensuring minimal viable implementation.

```bash
/add-increment "Add user authentication"
/add-increment "Create API endpoint for profiles"
/add-increment "Implement email validation"
```

**What it does**:
1. Validates prerequisites (PRD exists, git clean)
2. Analyzes current code state
3. Defines minimal increment (30min-2hrs, 1-3 files)
4. Questions necessity: "Is this REALLY needed NOW?"
5. Validates impact and required tests
6. Implements simple code (no premature abstractions)
7. Ensures previous features still work
8. Optionally registers progress in PRD

**Minimal increment guidelines**:
- ⏱️ 30 minutes to 2 hours
- 📁 Modify 1-3 files max
- 📝 20-100 lines of code
- 🧪 1-3 new tests

**When to use**:
- Implementing features between iterations
- Following MVP-driven development
- Maintaining code simplicity

---

### 4️⃣ `/quality [check-type] [optional-path]`

**Check code quality: detect over-engineering or refactoring opportunities**

Two perspectives: YAGNI violations and refactoring readiness.

```bash
# Check for over-engineering (YAGNI violations)
/quality yagni                    # Scan entire codebase
/quality yagni "path/to/file.py"  # Specific file
/quality yagni "module-name"      # Specific module

# Check refactoring readiness (Rule of 3)
/quality refactor                 # Find opportunities
/quality refactor "path/to/module" # Analyze specific module
```

**YAGNI check detects**:
- 🔴 Premature abstractions (interfaces with 1 implementation)
- 🔴 Dead code (unused functions, imports, files)
- 🟡 Excessive configuration (unused config variables)
- 🟡 Over-validation (complex validation for simple checks)

**Refactor check detects**:
- 📋 Duplicate logic patterns (3+ occurrences)
- 📋 Similar function structures
- 📋 Repeated validation logic
- 📋 Similar error handling

**When to use**:
- Before committing code (quality check)
- After implementing 3+ features (refactoring opportunities)
- When code feels complex

---

### 5️⃣ `/update-claude-md`

**Update project's CLAUDE.md with plugin configuration**

Updates or creates `CLAUDE.md` with incremental development instructions.

```bash
/update-claude-md
```

**What it updates**:
- Incremental development section
- Plugin commands reference
- YAGNI principles
- Recommended workflows
- Documentation links

**When to use**:
- After initializing incremental development
- When onboarding team members
- To refresh project guidelines

---

## 🔄 Recommended Workflows

### New Project Workflow

```text
1. /init-incremental "Your project idea"
   └─ Creates PRD.md with MVP definition

2. /prd view
   └─ Review created PRD

3. /add-increment "first feature"
   └─ Implement first increment

4. /prd update incremento
   └─ Register completed increment

5. /quality yagni
   └─ Check for over-engineering

6. Repeat from step 3
```

### Existing Project Workflow

```text
1. /init-incremental
   └─ Auto-detects and offers adoption

2. /prd view status
   └─ Check current state

3. /quality yagni
   └─ Identify over-engineering opportunities

4. /prd fix "adjustments based on findings"
   └─ Update PRD with current reality

5. /add-increment "next feature"
   └─ Continue with YAGNI principles

6. Repeat as needed
```

### Refactoring Workflow

```text
1. Implement features using /add-increment

2. After 3+ similar patterns appear:
   /quality refactor
   └─ Identify refactoring opportunities

3. Implement refactoring:
   /add-increment "refactor: extracted..."

4. /quality yagni
   └─ Verify no over-engineering introduced

5. /prd update incremento
   └─ Register refactoring as increment
```

---

## ✨ Key Principles

### Simplicity First

| Instead of | Use |
|-----------|-----|
| `Abstract base class` | Direct function |
| `Config file with 50 vars` | Hardcode for MVP |
| `Async task queue` | Simple function call |
| `Complex validation regex` | Simple string checks |
| `Multiple environments` | Single environment + hardcoding |

### Increment Size

- **Too small**: Less than 30 minutes (combine into larger feature)
- **Just right**: 30 minutes to 2 hours
- **Too large**: More than 2 hours (break into smaller increments)

### YAGNI Anti-Patterns to Avoid

❌ "Let's prepare for the future..."
❌ "In case we need to..."
❌ "To make it easier to expand..."
❌ "Optional fields for later..."
❌ "Flexibility we might need..."

✅ "What's the minimum to solve THIS problem?"
✅ "Add when actually requested"
✅ "Keep it simple for now"

---

## 📚 Related Concepts

### MVP (Minimum Viable Product)

✅ **Good MVP**:
- Smallest working version
- Solves core problem
- Testable and learnable
- Delivered quickly

❌ **Bad MVP**:
- Incomplete or broken
- Missing critical features
- Over-engineered
- Takes months

### Technical Debt vs Simplicity

- **Technical Debt**: Shortcuts that hurt later
- **Simplicity**: Minimum now, evolve when needed

Always choose **simplicity** - it's not debt!

---

## 🚀 Quick Start

1. **Initialize your project**:
   ```bash
   /init-incremental "Your project description"
   ```

2. **Review the PRD**:
   ```bash
   /prd view
   ```

3. **Implement features**:
   ```bash
   /add-increment "First feature"
   /add-increment "Second feature"
   ```

4. **Monitor code quality**:
   ```bash
   /quality yagni
   /quality refactor
   ```

5. **Register progress**:
   ```bash
   /prd update incremento
   ```

6. **Repeat** from step 3!

---

## 📖 Learn More

- `/prd help` - Get answers about the plugin
- `/prd help "Your specific question"` - Direct answers
- `/prd view` - See your project's PRD and roadmap
- Check project's `CLAUDE.md` - Incremental development guidelines

---

## 🎓 Philosophy

> "The best software is the simplest software that solves the problem.
> Build what you need today, not what you might need tomorrow."

This plugin embodies:
- **YAGNI**: You Aren't Gonna Need It
- **Occam's Razor**: Simplest solution wins
- **MVP-Driven**: Start small, iterate often
- **Evolutionary Architecture**: Structures emerge naturally

---

## ✅ Success Indicators

You're doing incremental development right when:

- ✅ Features ship in 1-2 hour increments
- ✅ Code is simple and direct
- ✅ No unused abstractions or configurations
- ✅ Architecture naturally evolves with codebase
- ✅ Team members understand each feature
- ✅ Changes are low-risk and testable

---

**Master incremental development and build better software, faster.** 🚀
