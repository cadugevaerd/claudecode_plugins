---
description: Check code quality - identify over-engineering (YAGNI) or refactoring opportunities when patterns emerge
argument-hint: "[check-type] [optional-path]"
---

# Code Quality Checks

Unified command to analyze code quality from two perspectives: YAGNI violations (over-engineering) and refactoring readiness.

## Usage

````bash
# Check for over-engineering (YAGNI violations)
/quality yagni                           # Full codebase scan
/quality yagni "path/to/file.py"        # Specific file
/quality yagni "module-name"            # Specific module

# Check refactoring readiness (Rule of 3)
/quality refactor                        # Identify refactoring opportunities
/quality refactor "path/to/module"      # Analyze specific module
/quality refactor "pattern-name"        # Look for specific pattern

```text

## Subcommands

### `/quality yagni [optional-path]`

Analyzes code for over-engineering and complexity that violates YAGNI (You Aren't Gonna Need It) principles.

**Detects**:
- 🔴 **Premature abstractions**: Interfaces/abstract classes with only 1 implementation
- 🔴 **Dead code**: Functions never called, unused imports, orphaned files
- 🟡 **Excessive configuration**: Config files with unused variables, redundant settings
- 🟡 **Over-validation**: Complex regex/validation when simpler check works
- 🟡 **Premature optimization**: Caching, async, or complex logic for simple operations

**Output Example**:
```text
⚠️ OVER-ENGINEERING DETECTED

📊 Findings: 12 opportunities
- Premature abstractions: 4
- Dead code: 5
- Excessive configuration: 3

🔴 CRITICAL (remove):
- UserValidator interface (never used)
- calculate_hash() function (called 1x, could be inline)
- CacheManager pattern (caches cold data)

🟡 WARNING (consider):
- DatabaseInterface with 1 implementation (PostgreSQL)
- Config with 20 unused variables
- Regex validation too complex for pattern

💡 Recommendation:
Try `/quality refactor` to find patterns ready to refactor
Or `/prd fix` to document YAGNI decisions
```

### `/quality refactor [optional-path]`

Identifies code patterns that are ready to refactor using the **Rule of 3**: refactor only when pattern repeats 3+ times.

**Rule of 3**:
- **1 case**: Keep inline (simple, don't abstract)
- **2 cases**: Duplication is OK, don't refactor yet
- **3 cases**: REFACTOR NOW! Pattern has emerged

**Detects**:
- 📋 Duplicate logic patterns (if appears 3+ times)
- 📋 Similar function structures (ready to extract)
- 📋 Repeated validation logic (candidate for helper)
- 📋 Similar error handling (can be standardized)

**Output Example**:
```text
✅ REFACTORING IDENTIFIED

📊 Patterns detected: 3

🔄 Refactoring Opportunity #1:
- **Extract email validation** from users.py, accounts.py, subscriptions.py
- Occurrences: 3
- Lines saved: ~20
- Risk: LOW
- Effort: 20 minutes
- New function: validate_email_format()

🔄 Refactoring Opportunity #2:
- **Extract user existence check** from 4 endpoints
- Occurrences: 4
- Lines saved: ~15
- Risk: LOW
- Effort: 15 minutes
- New middleware: check_user_exists()

💡 Ready to implement?
1. Choose refactoring from above
2. Implement extraction/abstraction
3. Run tests to verify
4. `/add-increment "refactor: extracted email validation"`

⚠️ DO NOT refactor when:
- Pattern appeared only 1-2 times (wait for 3rd)
- Code is broken (fix first)
- Tests missing (add tests first)
- Deadline is tight (ship first, refactor later)
```

## Workflows

### Check for Over-Engineering (YAGNI)

```text
1. /quality yagni
   └─ Scan entire codebase

2. Review findings
   └─ Read the report

3. Address critical issues
   └─ Remove dead code, simplify

4. Update PRD (if policy changed)
   └─ /prd fix "Added YAGNI constraint about..."

5. Commit changes
   └─ /commit
```

### Find Refactoring Opportunities

```text
1. /quality refactor
   └─ Identify patterns that repeat 3+ times

2. Choose opportunity
   └─ Pick one refactoring to implement

3. Implement refactoring
   └─ Extract/abstract the pattern

4. Test thoroughly
   └─ Ensure no behavior changes

5. Register progress
   └─ /add-increment "refactor: extracted..."

6. Repeat
   └─ /quality refactor again to find more
```

## Key Principles

### YAGNI (You Aren't Gonna Need It)

Don't implement features, abstractions, or configurations until actually needed.

**Anti-patterns to avoid**:
```python
# ❌ BAD - Preparing for future
class User:
    name: str
    email: str
    avatar: str = None          # "might need later"
    preferences: Dict = None    # "for future versions"
    settings: JSON = None       # "when we expand"

# ✅ GOOD - Only what's needed
class User:
    name: str
    email: str
    # Add fields when truly needed
```

### Rule of 3 (Refactoring Timing)

Only refactor when pattern emerges (3+ occurrences):

```text
Email validation in:
1. UserModel.validate() - Keep inline
2. RegistrationForm.submit() - Duplication OK, still inline
3. PasswordReset.execute() - REFACTOR NOW! Extract validate_email()
```

## Over-Engineering Red Flags

| Pattern | Why it's bad | Solution |
|---------|-------------|----------|
| Abstraction with 1 implementation | Premature complexity | Remove abstraction, use directly |
| Unused imports/functions | Dead code/cognitive load | Delete unused code |
| Config with 50+ variables | Most never used | Remove unused, hardcode for now |
| Complex validation regex | Hard to maintain | Use simpler check or library |
| Async for single operation | Premature optimization | Use sync, optimize when needed |
| Factory pattern for 1 object type | Over-engineered creation | Direct instantiation OK |

## Related Commands

- `/init-incremental` - Bootstrap incremental development
- `/prd` - Manage PRD and document decisions
- `/add-increment` - Add next feature
- `/update-claude-md` - Update project config

## Decision Matrix

| Scenario | Use `/quality yagni` | Use `/quality refactor` |
|----------|-------------------|----------------------|
| New feature has too much abstraction | ✅ | ❌ |
| Pattern repeats 3+ times | ❌ | ✅ |
| Unused code found | ✅ | ❌ |
| Need to check before commit | ✅ | ❌ |
| Code seems duplicated | ✅ | ✅ |

## Next Steps

- Found over-engineering? → `/quality yagni` to see report
- Ready to refactor? → `/quality refactor` for opportunities
- Want to document YAGNI decisions? → `/prd fix "..."`
- Implement feature safely? → `/add-increment "feature"`

**Keep your code simple and focused!** ✨
````