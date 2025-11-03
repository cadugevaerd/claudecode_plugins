---
description: Add next incremental feature to codebase following YAGNI principles - minimal, simple, and focused
allowed-tools: Read, Write, Edit, Bash(git:*)
---

# Add Increment

Implements the next incremental feature to existing codebase, ensuring only what's necessary is implemented (YAGNI).

## Usage

````bash
/add-increment "description of feature"
/add-increment "Add user authentication"
/add-increment "Create API endpoint for user profile"

```text

## Prerequisites

Always validate BEFORE starting:

1. **PRD exists?** `test -f docs/PRD.md || test -f PRD.md`
2. **Git clean?** `git status --porcelain` (no uncommitted changes)
3. **MVP defined?** Must be documented in PRD
4. **Previous code works?** Test existing features

If any prerequisite fails, suggest:
- No PRD: `/init-incremental "Your project description"`
- Git dirty: Commit changes first
- MVP undefined: `/prd update planejamento`

## Process

1. **Validate prerequisites** → STOP if any fail
2. **Analyze current state** → List existing features
3. **Define MINIMAL increment**:
   - ⏱️ 30 minutes to 2 hours of work
   - 📁 Modify 1-3 files maximum
   - 📝 20-100 lines of new code
   - 🧪 1-3 new tests

4. **Question necessity** → "Is this REALLY needed NOW?"
5. **Validate impact** → Which files, tests needed
6. **Implement** → Simple code, no premature abstractions
7. **Test thoroughly** → New feature works + previous code intact
8. **Register in PRD** (optional) → `/prd update incremento`
9. **Commit** → Changes for this increment

## 🚩 Detecting Oversized Increment

If it seems too large:
- 5+ files to modify
- 200+ lines of new code
- Multiple features

→ **BREAK INTO SMALLER INCREMENTS**

Example:

```text

❌ TOO LARGE: "Add OAuth authentication with JWT and RBAC"
✅ MINIMAL: "Add simple auth with hardcoded user"
✅ LATER: "Implement JWT token generation"
✅ LATER: "Add RBAC role-based access"

```text

## YAGNI Anti-Patterns

**What NOT to do**:
- ❌ Add optional fields "for the future"
- ❌ Create abstractions for single use case
- ❌ Build for scenarios not yet requested
- ❌ Implement validation beyond MVP
- ❌ Add configuration for future flexibility

**What to do**:
- ✅ Implement exact minimum needed
- ✅ Hardcode values if OK for MVP
- ✅ Keep code simple and direct
- ✅ Add structure when pattern repeats (Rule of 3)

## Rule of 3 (Refactoring)

- **1 case**: Keep code inline (simple)
- **2 cases**: Duplication is OK, keep separate
- **3 cases**: NOW REFACTOR! Pattern emerged

Don't refactor during increment! Use `/quality refactor` later.

## ✅ Post-Increment Checklist

- [ ] Code compiles/executes
- [ ] New feature works correctly
- [ ] Previous code still works
- [ ] Tests pass
- [ ] Ready for commit

## Increment Workflow Loop

```text
1. /add-increment "feature"
   └─ Implement feature

2. /quality yagni
   └─ Check for over-engineering (optional)

3. /prd update incremento
   └─ Register progress in PRD (optional)

4. /commit
   └─ Commit changes

5. Repeat → /add-increment "next feature"
   OR
   /quality refactor
   └─ Refactor if pattern emerged (3+ cases)
```

## Related Commands

- `/init-incremental` - Bootstrap project setup
- `/prd` - Manage PRD (view, update, fix)
- `/quality` - Check code quality (YAGNI, refactoring)
- `/update-claude-md` - Update project config

## Key Principles

- **Minimal**: Only what's needed NOW
- **Simple**: No premature complexity
- **Functional**: Works first, elegance later
- **Present**: Build for today, not tomorrow

## Next Steps

After successful implementation:

```bash
/prd update incremento     # Register in PRD (optional)
/commit                    # Commit changes
/add-increment "next"      # Next increment OR
/quality refactor          # Refactor if pattern emerged

```text

**Small, focused increments lead to better code!** ✨
````
