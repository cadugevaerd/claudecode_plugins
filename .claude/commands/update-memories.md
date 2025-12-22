---
description: Analyze recent project changes and update Claude Code memory files (CLAUDE.md, rules) following best practices
allowed-tools: Bash(git log:*), Bash(git diff:*), Bash(git show:*), Read, Write, Edit, Glob, Grep
---

# Update Memories Command

You are tasked with analyzing recent changes in the project and updating Claude Code memory files accordingly.

## Context

- Recent commits: !`git log --oneline -20`
- Changed files (last 5 commits): !`git diff --name-only HEAD~5..HEAD 2>/dev/null || git diff --name-only HEAD 2>/dev/null || echo "No commits yet"`

## Your Task

Analyze the recent changes and update Claude Code memory files following these steps:

### Step 1: Identify Significant Changes

Review the commits and changed files above. Focus on:

- New patterns, conventions, or architectural decisions
- New tools, dependencies, or commands added
- Bug fixes that reveal important constraints
- New features that affect how the project works
- Schema changes (database, API, etc.)

### Step 2: Categorize Updates

Determine where each update should go:

| Change Type | Destination |
|-------------|-------------|
| Project overview, common commands | `CLAUDE.md` |
| Architecture patterns | `.claude/rules/architecture.md` |
| Database schemas, SQL conventions | `.claude/rules/database.md` |
| Testing conventions | `.claude/rules/testing.md` |
| LLM/AI guidelines | `.claude/rules/llm-guidelines.md` |
| Evaluation system | `.claude/rules/evals.md` |
| Historical changelog | `.claude/rules/CHANGELOG.md` |
| New topic (create new file) | `.claude/rules/<topic>.md` |

### Step 3: Apply Updates

For each identified update:

1. **Read the target file** to understand current content
1. **Determine the update type**:
   - Add new section/information
   - Update existing section with new details
   - Add to CHANGELOG.md for historical record
1. **Make minimal, focused edits** - don't rewrite entire files
1. **Use consistent formatting** with existing content

### Step 4: Update CHANGELOG.md

Always add a dated entry to `.claude/rules/CHANGELOG.md` documenting:

- What was changed/added
- Why it matters
- Reference to relevant commits if applicable

Use format:

```markdown
## YYYY-MM-DD

### Category Name
- Change description
- Another change
```

## Guidelines

### DO:

- Keep entries concise and actionable
- Use bullet points and tables for clarity
- Reference specific files, functions, or patterns
- Date all CHANGELOG entries

### DON'T:

- Add verbose explanations
- Duplicate information across files
- Remove existing content unless outdated
- Add speculative or future features

## Output

After updating, summarize:

1. Files updated
1. Key changes made
1. Any manual review recommended
