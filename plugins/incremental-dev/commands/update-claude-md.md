---
description: Update project's CLAUDE.md with incremental-dev plugin configuration and YAGNI principles
---

# Update CLAUDE.md

Updates or creates project's `CLAUDE.md` file with incremental development instructions and references to incremental-dev plugin commands.

## Usage

````bash
/update-claude-md

```text

## What It Updates

Adds or updates in `CLAUDE.md`:

### 1. Incremental Development Section
- YAGNI principles explained
- Rule of 3 for refactoring
- MVP-first approach
- Evolutionary architecture

### 2. Plugin Commands Reference
- Quick reference of 5 consolidated commands
- When to use each command
- Recommended workflow
- Workflow diagrams

### 3. Documentation Links
- `/prd help` for questions
- Command descriptions
- Next steps

### 4. Best Practices
- Don't over-engineer
- Simple > Elegant
- Works > Perfect
- Now > Hypothetical future

## Process

1. **Read current CLAUDE.md** (if exists):
   - Preserve existing content
   - Update incremental section if present

2. **Update sections**:
   - Add/update command references
   - Maintain project coherence
   - Validate links

3. **Save CLAUDE.md**:
   - Keep < 40KB if possible
   - Validate markdown
   - Ensure clean organization

## Updated Commands

The incremental-dev plugin has been refactored to 5 core commands:

- `/init-incremental` - Initialize or adopt incremental development
- `/prd` - Manage PRD (view, update, fix, help)
- `/add-increment` - Add next feature incrementally
- `/quality` - Check code quality (YAGNI, refactoring)
- `/update-claude-md` - Update project configuration

## Output Expected

```text

✅ CLAUDE.md UPDATED

📝 Sections added:
- Incremental Development (YAGNI principles)
- Available commands (consolidated)
- Recommended workflows
- Useful links

🔗 References:
- /prd help - Help center
- Full documentation in README

✨ Ready to use!

```text

## Next Commands

- `/init-incremental` - Set up new or adopt incremental dev
- `/prd help` - Get answers about the plugin
- `/add-increment "feature"` - Start implementing features

## Related Commands

- `/init-incremental` - Bootstrap incremental development
- `/prd` - Manage Product Requirements Document
- `/add-increment` - Implement next feature
- `/quality` - Code quality analysis

**Keep your project configuration up-to-date!** 📚
````
