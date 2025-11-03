---
description: Manage PRD (Product Requirements Document) - view, update, fix, and get help on development phases
argument-hint: '[subcommand] [options]'
---

# PRD Management

Unified command for managing Product Requirements Document with multiple subcommands for different operations.

## Usage

````bash
# View PRD
/prd view                    # Full PRD with all sections
/prd view mvp               # Only MVP definition
/prd view incrementos       # Only implemented increments
/prd view adrs              # Only architectural decisions
/prd view timeline          # Evolution timeline
/prd view status            # Current status and next steps

# Update PRD (phase-based)
/prd update descoberta      # Update discovery phase (v0.1)
/prd update planejamento    # Update planning phase (v1.0)
/prd update design          # Update design phase (v1.1)
/prd update incremento      # Register completed increment (v1.x)
/prd update final           # Finalize PRD as-built (v2.0)

# Validate existing PRD
/prd validate                    # Validate PRD.md in current directory
/prd validate path/to/PRD.md     # Validate specific PRD file

# Surgical fixes
/prd fix "description of change"  # Targeted adjustment to specific section
/prd fix "Move feature X out of scope"
/prd fix "Update success metric to 500ms"

# Get help
/prd help                    # Interactive help menu
/prd help "Your specific question"  # Direct answer to question

```text

## Subcommands

### `/prd view [section]`

Displays PRD summary with optional filtering by section.

**Sections**: `mvp`, `incrementos`, `adrs`, `timeline`, `status`, or leave blank for full view

**Output**:
- 📊 General information (version, date, status)
- 📍 Current phase and progress
- ✅ Completed sections checklist
- 💻 Implemented increments with dates
- 🏗️ Architectural Decision Records
- 🎯 Next recommended actions
- 📈 Evolution timeline (optional)

### `/prd update [phase]`

Updates PRD for specific development phase. Auto-increments version.

**Phases**: `descoberta`, `planejamento`, `design`, `incremento`, `final`

**Each phase updates**:
- **Discovery** (v0.1): Problem, objectives, KPIs
- **Planning** (v1.0): Vision, epics, MVP definition, YAGNI scope
- **Design** (v1.1): Architecture, tech stack, data models, ADRs
- **Increment** (v1.x): New features, learnings, technical decisions
- **Final** (v2.0): Lessons learned, recommendations, complete timeline

### `/prd fix "change description"`

Makes surgical targeted adjustments to specific PRD sections without rewriting entire phases.

**When to use**:
- ✅ Adjust one field or line
- ✅ Add a specific requirement
- ✅ Update a metric
- ❌ NOT for full phase rewrites (use `/prd update` instead)

### `/prd validate [path]`

Validates existing PRD.md against template structure and completeness.

**Usage modes**:
- `/prd validate` - Auto-detects and validates PRD.md in project root
- `/prd validate ./docs/PRD.md` - Validate specific file

**Validation checks**:
- ✅ Required sections by phase (v0.1, v1.0, v1.1, v1.x)
- ✅ Mandatory fields present and non-empty
- ✅ Proper markdown structure
- ✅ Version progression (0.1 → 1.0 → 1.1 → 1.x)
- ✅ Field consistency across sections

**Output includes**:
- 📊 Completion percentage by phase
- ⚠️ Missing fields with recommendations
- 🎯 Next suggested phase updates
- 💡 Quick fixes for common issues

**Example output**:
```
✅ PRD VALIDATION REPORT

📋 Project: my-project
🔄 Version: 1.1
📅 Last updated: 2025-11-03

PHASES DETECTED:
✅ Phase 1 (Discovery v0.1) - 100%
✅ Phase 2 (Planning v1.0) - 90%
⚠️  Phase 3 (Design v1.1) - 60%

MISSING FIELDS:
⚠️  MVP: Feature X still not documented
⚠️  Design: ADR-002 file missing

OVERALL PROGRESS: 83%
NEXT STEP: Run `/prd update design`
```

### `/prd help [question]`

Interactive help center for incremental development, YAGNI, PRD management, and plugin usage.

**Usage modes**:
- `/prd help` - Interactive menu with categories
- `/prd help "Your question"` - Direct answer

**Help categories**:
1. 🚀 Getting Started (new and legacy projects)
2. 📋 PRD Management (creation, updates, structure)
3. ⚙️ Available Commands (quick reference)
4. 💡 Concepts (YAGNI, Incremental, MVP, Evolutionary Architecture)
5. 🔧 Troubleshooting (common problems and solutions)
6. 📖 Practical Examples (real-world use cases)

## Workflows

### For NEW Projects

```text
1. /init-incremental "project description"
   └─ Creates PRD with MVP definition

2. /prd view
   └─ Review created PRD

3. /add-increment "first feature"
   └─ Implement first increment

4. /prd update incremento
   └─ Register completed increment

5. /quality yagni
   └─ Detect over-engineering
```

### For EXISTING/LEGACY Projects

```text
1. /init-incremental
   └─ Auto-detects and offers adoption

2. /prd view status
   └─ Check current state

3. /prd update descoberta
   └─ Update discovery phase with current findings

4. /quality yagni
   └─ Identify over-engineering opportunities
```

### PRD vs /prd-fix Decision

| Situation | Use |
|-----------|-----|
| Adding entire new phase information | `/prd update [phase]` |
| Adjusting one requirement | `/prd fix "..."` |
| Rewriting multiple sections | `/prd update [phase]` |
| Updating single field/line | `/prd fix "..."` |
| Moving feature between scope sections | `/prd fix "..."` |

## Key Concepts

### Phases

1. **Discovery (v0.1)**: Understand problem and objectives
2. **Planning (v1.0)**: Define scope and MVP
3. **Design (v1.1)**: Technical architecture
4. **Development (v1.x)**: Incremental feature delivery
5. **Final (v2.0)**: As-built documentation

### YAGNI (You Aren't Gonna Need It)

Don't add functionality until ACTUALLY needed.

✅ **Good**: Simple code, add when needed
❌ **Bad**: Prepare for future, add optional fields

### Incremental Development

1. Start with MVP
2. Implement one feature at a time
3. Refactor when pattern emerges (Rule of 3)
4. Update PRD with learnings
5. Evolve architecture naturally

## Related Commands

- `/init-incremental` - Initialize new project or adopt incremental in existing one
- `/add-increment` - Add next feature to implementation
- `/quality` - Check for over-engineering (YAGNI) or refactoring opportunities
- `/update-claude-md` - Update project's CLAUDE.md with plugin configuration

## Help & Next Steps

- First time? → `/prd help "How to start?"`
- Create PRD? → `/init-incremental "Your project idea"`
- View current PRD? → `/prd view`
- Add feature? → `/add-increment "Feature description"`
- Check quality? → `/quality yagni`

**Master PRD management for better incremental development!** 📚
````
