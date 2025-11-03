---
description: Create PRD template file in docs/ directory for project reference and validation structure
argument-hint: '[--force]'
---

# PRD Template Creation

Create a PRD template file in `docs/PRD.TEMPLATE.md` for project reference with complete structure guidance and validation reference.

## Usage

```bash
/prd-template              # Create template if doesn't exist
/prd-template --force      # Recreate template (overwrite existing)
```

## What It Does

1. Create `docs/` directory if needed
1. Generate `docs/PRD.TEMPLATE.md` with complete PRD structure
1. Add `docs/PRD.TEMPLATE.md` to `.gitignore`
1. Display confirmation with location and next steps

## Template Structure

The generated template follows **increment-focused design** aligned with YAGNI principles:

- **Section 1**: Vision & Strategy (Problem, Outcomes, KPIs, Product Vision, Now/Next/Later Roadmap)
- **Section 2**: MVP Definition (Essential Features, Hypothesis, YAGNI Scope - what NOT to build)
- **Section 3**: Increments (Completed, In Development, Planned - design documented *inside* each)
- **Section 4**: As-Built Definitions (Current state of architecture, tech stack, APIs, ADRs)

## Design Principles

This template enforces **true incremental development** and **YAGNI (You Ain't Gonna Need It)**:

### ✅ Design is Just-In-Time, Not Up-Front

- Architecture, data models, and APIs are designed *within* each increment, not pre-planned
- Prevents over-engineering by focusing on *actual* needs of current increment
- Design emerges naturally as features are built, reducing waste

### ✅ Roadmap is Flexible (Now/Next/Later)

- Replaces rigid Gantt charts with prioritized flexibility
- Allows reprioritization based on learnings from previous increments
- Focuses on outcomes, not output timelines

### ✅ No "Design Phase"

- Eliminates false separation between planning and development
- Design decisions are made *when building*, not beforehand
- ADRs capture reasoning *as features are implemented*

### ✅ As-Built Reflects Reality

- Section 4 documents what *actually exists*, not what was planned
- Updated after each completed increment
- Single source of truth for current system state

## When to Use

- **New projects**: Create template during initialization for reference
- **Legacy projects**: Adopt incremental methodology by generating template
- **Team training**: Share template to teach PRD methodology
- **Validation reference**: Template structure supports `/prd validate` completeness checks

## Workflow Context

### For New Projects

1. Run `/prd-template` → Creates reference
1. Run `/init-incremental "Your project"` → Creates actual PRD.md
1. Reference template while filling sections
1. Validate with `/prd validate`

### For Existing Projects

1. Run `/prd-template` → Creates reference
1. Run `/init-incremental` → Offers adoption for existing project
1. Migrate current documentation to template structure
1. Use template as reference for completeness

## Template Preview

The generated `docs/PRD.TEMPLATE.md` includes this structure:

```markdown
# PRD - [Project Name]

**Status:** Living Document

## 1. 🎯 Vision & Strategy

- **Problem:** [What problem does this solve?]
- **Outcomes:** [What do we want to achieve?]
- **KPIs:** [How will we measure success?]
- **Product Vision:** [Long-term direction]
- **Roadmap (Now/Next/Later):**
  - **Now:** [Current increment]
  - **Next:** [Prioritized next increments]
  - **Later:** [Backlog for exploration]

## 2. 📦 MVP Definition

- **Essential Features:** [Core capabilities to validate hypothesis]
- **Hypothesis:** "We believe that [features] will [validate/solve]..."
- **YAGNI Scope:** [What we explicitly will NOT build now]

## 3. 🚀 Increments

### Increment 1: [Epic/Goal Name]
- **Status:** Completed | In Development | Planned
- **User Stories:** [Features delivered]
- **Design & Decisions:**
  - *Architecture:* [What changed in this increment]
  - *Data Models:* [Schemas created/modified]
  - *ADRs:* [Decisions made during implementation]
- **Validations:** [Test results, metrics]
- **Retrospective:** [What worked, what didn't, learnings]

### Increment 2: [Epic/Goal Name]
- **Status:** [...]
- *[Minimal details until increment starts]*

## 4. 🛠️ As-Built Definitions

*Current state of the system (updated each increment):*

- **Architecture:** [How system actually exists today]
- **Tech Stack:** [Current technologies in use]
- **APIs:** [Current contracts and endpoints]
- **ADRs:** [Link to all decisions made]
```

## Validation Integration

Template automatically validates when running `/prd validate`:

- Checks template exists in `docs/` before validating PRD.md
- Suggests creation if missing before validation begins
- Uses template structure as reference for completeness checks
- Reports missing sections and required fields

## Related Commands

- `/prd` - View, update, validate, and fix PRD sections
- `/prd validate` - Validate PRD against template structure
- `/init-incremental` - Initialize incremental development with PRD.md
- `/add-increment` - Add next feature to implementation
- `/quality` - Check code for over-engineering (YAGNI) or refactoring opportunities
