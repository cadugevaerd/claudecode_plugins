---
description: Initialize incremental development for new or existing projects with auto-detection of project type
argument-hint: '[project-description]'
---

# Initialize Incremental Development

Unified command to bootstrap incremental development workflow. Auto-detects project type and applies appropriate setup.

## Usage

````bash
# Auto-detect and initialize (interactive)
/init-incremental

# With project description (new projects)
/init-incremental "API REST with FastAPI to manage users"
/init-incremental "LangGraph agent for document processing"

# Adopt in existing project (interactive)
/init-incremental
  └─ Auto-detects existing code and offers adoption

```text

## How It Works

### Step 1: Auto-Detection

The command automatically detects your project type:

- **🆕 NEW Project**: No source code found
  - Sets up CLAUDE.md with YAGNI principles
  - Creates PRD v0.1 with MVP definition
  - Asks about project objectives

- **🔄 EXISTING Project**: Source code detected
  - Offers to adopt incremental development
  - Analyzes current codebase
  - Identifies over-engineering opportunities
  - Creates retroactive PRD v1.0

- **📦 LEGACY Project**: Significant codebase detected
  - Full analysis with metrics
  - Generates simplification roadmap
  - Creates comprehensive retroactive PRD

### Step 2: Information Collection (Interactive)

For **new projects**:
1. What do you want to build? (1-2 sentences)
2. What problem does it solve? (pain point/need)
3. Who will use it? (persona/role)
4. What's the main functionality? (most important)
5. Other nice-to-have features? (list)
6. What NOT to do? (YAGNI - explicitly out of scope)
7. MVP priority #1? (absolute minimum)
8. Success metric? (how to measure if it works)
9. Timeline/urgency? (deadline, context)
10. Spike format? (notebooks or scripts for exploration)

For **existing projects**:
1. Current project description? (what it does now)
2. Intended purpose? (if different from current)
3. Known over-engineering areas? (optional)
4. Team goals for refactoring? (optional)
5. Phase to focus on? (discovery/planning/design)

### Step 3: Setup & Configuration

- Creates/updates `CLAUDE.md` with YAGNI principles
- Generates `PRD.md` (v0.1 for new, v1.0 for existing)
- Optional: Creates `ROADMAP.md` for legacy projects
- Sets up template structure for incremental development

### Step 4: Confirmation & Next Steps

Displays summary and recommends next actions based on project type.

## Project Type Scenarios

### NEW Projects

**Output**:
```text
✅ INCREMENTAL DEVELOPMENT INITIALIZED

📄 CLAUDE.md (created with YAGNI)
📄 PRD.md (v0.1 - Discovery phase)

🎯 Next Steps:
1. Review PRD.md - Understand MVP definition
2. /add-increment "first feature" - Start implementing
3. /quality yagni - Check for over-engineering
4. /prd update planejamento - Move to planning phase

**Your MVP is defined. Start building!** 🚀
```

### EXISTING Projects (Adoption)

**Output**:
```text
✅ INCREMENTAL ADOPTION COMPLETE

📄 CLAUDE.md (updated with YAGNI)
📄 PRD.md (v1.0 retroactive)
📋 ROADMAP.md (simplification phases)

📊 Analysis:
- Over-engineering detected: 12 opportunities
- Quick wins: 5 simple refactorings
- Technical debt: 3 critical areas

🚀 Next Steps:
1. /prd view - Review retroactive PRD
2. /quality yagni - Identify specific issues
3. /prd fix - Adjust PRD as needed
4. /add-increment "next feature" - Continue with YAGNI

**Project analyzed. Ready to evolve incrementally!** 🚀
```

### LEGACY Projects (Full Analysis)

**Output**:
```text
✅ LEGACY MODERNIZATION STARTED

📄 CLAUDE.md (configured for YAGNI)
📄 PRD.md (v1.0 comprehensive retroactive)
📋 ROADMAP.md (phased simplification plan)

📊 Code Analysis:
- Lines of code: 15,000
- Over-engineering: 18 opportunities
- Phase 1 (quick wins): 1 week
- Phase 2 (refactorings): 2-4 weeks
- Phase 3 (new features with YAGNI): ongoing

🎯 Simplification Phases:
- Phase 1: Remove unused code, simplify config
- Phase 2: Extract patterns, refactor abstractions
- Phase 3: New features with incremental YAGNI

**Legacy project ready for incremental evolution!** 🚀
```

## What Gets Created/Updated

### CLAUDE.md Updates

```markdown
## 🏗️ Development Approach

This project follows **incremental development** with **YAGNI** principles:
- ✅ Implement only what's NEEDED NOW
- ✅ Add features incrementally
- ✅ Refactor when pattern emerges (Rule of 3)
- ❌ Don't build for "future use"
- ❌ Don't prepare for scenarios not requested

See PRD.md for product vision and roadmap.
```

### PRD.md (v0.1 or v1.0)

- Project description and problem statement
- MVP definition (minimum viable product)
- Phase-by-phase roadmap
- YAGNI scope (what's NOT included)
- Success metrics
- Architectural decisions (as they emerge)

### ROADMAP.md (for legacy only)

- Phase 1: Quick wins (1 week)
- Phase 2: Refactorings (2-4 weeks)
- Phase 3: New features with YAGNI

## Related Commands

- `/prd` - Manage PRD (view, update, fix, help)
- `/add-increment` - Add next feature to implementation
- `/quality` - Check for over-engineering or refactoring opportunities
- `/update-claude-md` - Update project's CLAUDE.md with plugin config

## Key Principles

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
- Takes months to build

### YAGNI (You Aren't Gonna Need It)

Always ask yourself:
- "Do I need this NOW?"
- "What happens if I don't implement it?"
- "Does this solve the MINIMUM problem?"

Avoid:
- "Let's prepare for the future..."
- "In case we need to add..."
- "To make it easier to expand..."

### Rule of 3 (Refactoring)

- **1 case**: Keep inline (simple)
- **2 cases**: Duplication OK
- **3 cases**: REFACTOR NOW! Pattern emerged

## Next Steps After Initialization

1. **Review PRD** → `/prd view`
2. **Start implementing** → `/add-increment "feature"`
3. **Check quality** → `/quality yagni`
4. **Register progress** → `/prd update incremento`
5. **Iterate** → Back to step 2

## Help

- New project? → `/init-incremental "Your idea"`
- Existing project? → `/init-incremental` (auto-detects)
- Questions? → `/prd help "Your question"`
- View PRD? → `/prd view`

**Start your incremental journey now!** 🚀
````
