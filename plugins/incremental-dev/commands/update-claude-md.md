---
name: update-claude-md
description: Update project's CLAUDE.md with incremental-dev plugin configuration following best practices
---

# Update CLAUDE.md with Incremental-Dev Configuration

This command updates the project's CLAUDE.md file with the incremental-dev plugin configuration, following best practices:
- ≤40 lines of content
- Progressive disclosure (link to README.md for complete docs)
- Mentions ONLY agents and MCPs (skills and commands are auto-discovered)
- 3-5 critical rules

## When to Use This Command

Use `/update-claude-md` when:
- Project's CLAUDE.md doesn't have incremental-dev plugin configuration
- CLAUDE.md was corrupted or deleted
- Need to update/reconfigure plugin instructions after plugin update
- Want to ensure CLAUDE.md follows current best practices

## What This Command Does

1. ✅ Checks if CLAUDE.md exists in project root
2. ✅ Creates basic CLAUDE.md if it doesn't exist
3. ✅ Detects if incremental-dev section already exists
4. ✅ Asks to overwrite if section exists
5. ✅ Adds/updates section following best practices:
   - ≤40 lines
   - Agents available (incremental-dev-coach)
   - 3-5 critical rules
   - Link to plugin README.md
   - Note: "Skills and commands are auto-discovered"
6. ✅ Validates CLAUDE.md after update

## ⚠️ What This Command DOES NOT Do

❌ Does NOT mention skills (auto-discovered when plugin is installed via `/plugin install`)
❌ Does NOT mention commands (auto-discovered on Claude startup)
❌ Does NOT add >40 lines to CLAUDE.md
❌ Does NOT create `.claude/knowledge/` directory (DOES NOT EXIST - hallucination!)
❌ Does NOT create `.claude/knowledgements/` directory (DOES NOT EXIST - hallucination!)

## Workflow

```
┌─────────────────────────────────────────────┐
│ Step 1: Check CLAUDE.md Existence          │
└─────────────────────────────────────────────┘
                    ↓
        ┌───────────┴───────────┐
        │                       │
   [Exists]              [Does NOT Exist]
        │                       │
        ↓                       ↓
┌───────────────┐    ┌─────────────────────┐
│ Step 2a:      │    │ Step 2b:            │
│ Read Current  │    │ Create Basic        │
│ CLAUDE.md     │    │ CLAUDE.md           │
└───────────────┘    └─────────────────────┘
        │                       │
        └───────────┬───────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Step 3: Detect Incremental-Dev Section     │
└─────────────────────────────────────────────┘
                    ↓
        ┌───────────┴───────────┐
        │                       │
   [Exists]              [Does NOT Exist]
        │                       │
        ↓                       ↓
┌───────────────┐    ┌─────────────────────┐
│ Step 4a:      │    │ Step 4b:            │
│ Ask to        │    │ Prepare to Add      │
│ Overwrite     │    │ Section             │
└───────────────┘    └─────────────────────┘
        │                       │
        └───────────┬───────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Step 5: Add/Update Section (≤40 lines)     │
│ - Agent: incremental-dev-coach              │
│ - 3-5 Critical Rules                        │
│ - Link to README.md                         │
│ - Note about auto-discovery                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Step 6: Write Updated CLAUDE.md            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Step 7: Validate & Report Success          │
└─────────────────────────────────────────────┘
```

## Step 1: Check CLAUDE.md Existence

Check if CLAUDE.md file exists in project root.

```bash
test -f "CLAUDE.md" && echo "EXISTS" || echo "NOT_FOUND"
```

**If NOT_FOUND**: Proceed to Step 2b (create basic file)
**If EXISTS**: Proceed to Step 2a (read current file)

---

## Step 2a: Read Current CLAUDE.md

If file exists, read its current content to preserve existing sections.

**Use Read tool**:
- file_path: `CLAUDE.md` (project root)
- Read entire file to preserve all content

---

## Step 2b: Create Basic CLAUDE.md

If file doesn't exist, create basic CLAUDE.md with minimal structure:

```markdown
# CLAUDE.md

Project-specific instructions for Claude Code.

---
```

**Inform user**:
```
📝 CLAUDE.md not found - creating basic file
```

---

## Step 3: Detect Incremental-Dev Section

Search for existing incremental-dev section in CLAUDE.md content.

**Section markers to detect**:
- `# Incremental Development` (exact match)
- OR `# incremental-dev` (lowercase variant)
- OR any heading containing "incremental" and "development"

**Use pattern matching**:
```
Check if content contains:
- "# Incremental Development" OR
- "# incremental-dev" OR
- Heading with both "incremental" and "development"
```

**Result**:
- **Section FOUND**: Proceed to Step 4a (ask to overwrite)
- **Section NOT FOUND**: Proceed to Step 4b (prepare to add)

---

## Step 4a: Ask to Overwrite Existing Section

If incremental-dev section already exists, ask user if they want to overwrite it.

**Inform user**:
```
⚠️  CLAUDE.md already has Incremental Development section

Do you want to overwrite it with updated configuration? (y/n)
```

**User response**:
- **y (yes)**: Proceed to Step 5 (replace section)
- **n (no)**: ABORT command with message:
  ```
  ❌ Aborted - CLAUDE.md not modified

  If you want to manually edit, the section is located at:
  CLAUDE.md (search for "Incremental Development")
  ```

---

## Step 4b: Prepare to Add Section

If section doesn't exist, prepare to add it at the end of CLAUDE.md.

**Inform user**:
```
✅ Adding Incremental Development section to CLAUDE.md
```

---

## Step 5: Add/Update Section (≤40 lines)

Create the incremental-dev section following best practices.

**CRITICAL REQUIREMENTS**:
1. ✅ Total section ≤40 lines (STRICT LIMIT)
2. ✅ Mention ONLY agent (incremental-dev-coach) - NO skills, NO commands
3. ✅ Include 3-5 critical rules (most important)
4. ✅ Link to plugin README.md for complete documentation
5. ✅ Add note: "Skills and commands are auto-discovered"

**Template (EXACTLY this structure)**:

```markdown
---

# Incremental Development

**Plugin**: incremental-dev
**Purpose**: Guide iterative/incremental development following YAGNI and Evolutionary Architecture.

**Agent Available**:
- **incremental-dev-coach**: Coaches incremental development (does NOT implement code)
  - Use via Task tool when: defining MVP, questioning premature features, detecting over-engineering
  - Trigger terms: "MVP", "YAGNI", "simplify", "over-engineering", "refactor when"

## Critical Rules

✅ **ALWAYS:**
- Start with MVP (3-5 essential features)
- Add ONE feature per iteration (test between increments)
- Refactor when pattern appears 3+ times (Rule of 3)

❌ **NEVER:**
- Add features "for the future" (YAGNI violation)
- Create abstractions before 3+ concrete cases
- Anticipate hypothetical requirements

## Commands Available

All commands are auto-discovered on Claude startup. Key commands:
- `/start-incremental` - Define MVP
- `/add-increment` - Add next feature incrementally
- `/refactor-now` - Detect when to refactor
- `/review-yagni` - Identify over-engineering
- `/prd-update` - Update Product Requirements Document
- `/adopt-incremental` - Adopt YAGNI in legacy projects

**Skills**: Auto-discovered when plugin is installed via `/plugin install` - no manual setup needed.

📖 **Complete documentation:** `plugins/incremental-dev/README.md`

---
```

**Validation checklist**:
- [ ] Total lines ≤40
- [ ] Agent mentioned: incremental-dev-coach
- [ ] 3-5 critical rules present
- [ ] Link to README.md included
- [ ] Note about auto-discovery present
- [ ] NO manual skill copying instructions
- [ ] NO creation of `.claude/knowledge/` directory

---

## Step 6: Write Updated CLAUDE.md

Write the updated CLAUDE.md file.

**If section exists** (overwrite scenario):
1. Find section boundaries (start and end)
2. Replace ONLY the incremental-dev section
3. Preserve all other content before and after

**If section doesn't exist** (new section):
1. Append section to end of file
2. Preserve all existing content

**Use Edit tool** (if overwriting) or **append** (if new section).

---

## Step 7: Validate & Report Success

After writing CLAUDE.md, validate and report to user.

**Validation**:
```bash
# Verify CLAUDE.md exists
test -f "CLAUDE.md" && echo "✅ File exists"

# Check section is present
grep -q "# Incremental Development" CLAUDE.md && echo "✅ Section added"
```

**Report to user**:

```
═══════════════════════════════════════════
✅ CLAUDE.md UPDATED SUCCESSFULLY
═══════════════════════════════════════════

📄 File: CLAUDE.md (project root)

✅ Incremental Development section added/updated
✅ Configuration follows best practices:
   - Agent documented: incremental-dev-coach
   - 3-5 critical rules included
   - Link to plugin README.md
   - Auto-discovery note present
   - Section ≤40 lines

═══════════════════════════════════════════

🚀 NEXT STEPS:

Claude Code will now automatically:
- Auto-discover all plugin commands on startup
- Auto-discover all plugin skills when plugin installed
- Use incremental-dev-coach agent when you delegate via Task tool

💡 To verify configuration:
cat CLAUDE.md | grep -A 50 "# Incremental Development"

📖 Full documentation:
plugins/incremental-dev/README.md

═══════════════════════════════════════════
```

---

## Error Handling

### Error 1: CLAUDE.md Read Permission Denied

**Detection**:
```bash
test -r "CLAUDE.md"
```

**Action**:
```
❌ ERROR: Cannot read CLAUDE.md

Reason: Permission denied
Solution: Check file permissions and try again

chmod 644 CLAUDE.md
/update-claude-md
```

---

### Error 2: CLAUDE.md Write Permission Denied

**Detection**: Edit/Write tool returns permission error

**Action**:
```
❌ ERROR: Cannot write to CLAUDE.md

Reason: Permission denied
Solution: Check file permissions and try again

chmod 644 CLAUDE.md
/update-claude-md
```

---

### Error 3: CLAUDE.md Corrupted or Invalid Format

**Detection**: Read tool returns malformed content or encoding errors

**Action**:
```
❌ ERROR: CLAUDE.md appears corrupted

Reason: File encoding or format issue
Solution: Backup current file and create fresh CLAUDE.md

mv CLAUDE.md CLAUDE.md.backup
/update-claude-md
```

---

### Error 4: Project Root Detection Failed

**Detection**: Unable to determine project root directory

**Action**:
```
❌ ERROR: Cannot determine project root

Reason: Not in a valid project directory
Solution: Navigate to project root and try again

cd /path/to/project
/update-claude-md
```

---

## Examples

### Example 1: Fresh Project (No CLAUDE.md)

**Scenario**: New project without CLAUDE.md

**User command**:
```
/update-claude-md
```

**Agent output**:
```
📝 CLAUDE.md not found - creating basic file
✅ Adding Incremental Development section to CLAUDE.md

═══════════════════════════════════════════
✅ CLAUDE.md UPDATED SUCCESSFULLY
═══════════════════════════════════════════

📄 File: CLAUDE.md (project root)

✅ Incremental Development section added
✅ Configuration follows best practices
   - Section: 38 lines (within 40-line limit ✅)

═══════════════════════════════════════════
```

---

### Example 2: Existing CLAUDE.md Without Plugin Config

**Scenario**: CLAUDE.md exists with other content, but no incremental-dev section

**User command**:
```
/update-claude-md
```

**Agent output**:
```
✅ CLAUDE.md found - preserving existing content
✅ Adding Incremental Development section to CLAUDE.md

═══════════════════════════════════════════
✅ CLAUDE.md UPDATED SUCCESSFULLY
═══════════════════════════════════════════

📄 File: CLAUDE.md (project root)

✅ Incremental Development section appended
✅ All existing content preserved

═══════════════════════════════════════════
```

---

### Example 3: Existing CLAUDE.md With Old Plugin Config

**Scenario**: CLAUDE.md has old incremental-dev section that needs updating

**User command**:
```
/update-claude-md
```

**Agent output**:
```
⚠️  CLAUDE.md already has Incremental Development section

Do you want to overwrite it with updated configuration? (y/n)
```

**User responds**: `y`

**Agent output**:
```
✅ Updating Incremental Development section in CLAUDE.md

═══════════════════════════════════════════
✅ CLAUDE.md UPDATED SUCCESSFULLY
═══════════════════════════════════════════

📄 File: CLAUDE.md (project root)

✅ Incremental Development section updated
✅ Old content replaced with current best practices
✅ All other sections preserved

═══════════════════════════════════════════
```

---

### Example 4: User Declines Overwrite

**Scenario**: User doesn't want to overwrite existing section

**User command**:
```
/update-claude-md
```

**Agent output**:
```
⚠️  CLAUDE.md already has Incremental Development section

Do you want to overwrite it with updated configuration? (y/n)
```

**User responds**: `n`

**Agent output**:
```
❌ Aborted - CLAUDE.md not modified

If you want to manually edit, the section is located at:
CLAUDE.md (search for "Incremental Development")

To update in the future, run: /update-claude-md
```

---

## Related Commands

- `/setup-project-incremental` - Full project setup (creates PRD + CLAUDE.md)
- `/prd-update` - Update Product Requirements Document
- `/start-incremental` - Define MVP for new development

**When to use which command:**

| Command | Use When |
|---------|----------|
| `/setup-project-incremental` | Starting new project (creates PRD + CLAUDE.md) |
| `/update-claude-md` | Only need to update/fix CLAUDE.md configuration |
| `/start-incremental` | Define MVP after CLAUDE.md is configured |

---

## Best Practices

### ✅ DO

- Run `/update-claude-md` when plugin is updated to get latest best practices
- Verify configuration after update: `cat CLAUDE.md | grep -A 50 "# Incremental Development"`
- Read plugin README.md for complete documentation
- Use agent via Task tool: `/task "use incremental-dev-coach to define MVP"`

### ❌ DON'T

- Don't manually copy skills to project (auto-discovered when plugin installed)
- Don't create `.claude/knowledge/` directory (DOES NOT EXIST)
- Don't add >40 lines to CLAUDE.md (use progressive disclosure)
- Don't mention all commands in CLAUDE.md (auto-discovered on startup)

---

## Technical Notes

### Progressive Disclosure Pattern

This command follows progressive disclosure:
- **CLAUDE.md**: ≤40 lines, essential info only
- **README.md**: Complete documentation, examples, advanced topics
- **User reads README.md** when needs detail (via Read tool or manually)

### Auto-Discovery Mechanism

**Commands**: Auto-discovered on Claude Code startup
- Claude scans `plugins/*/commands/*.md`
- No CLAUDE.md mention needed

**Skills**: Auto-discovered when plugin installed via `/plugin install`
- Claude scans `plugins/*/skills/*/SKILL.md`
- No manual copying needed
- No CLAUDE.md mention needed (agent is sufficient)

**Agents**: Must be mentioned in CLAUDE.md
- Agents are NOT auto-discovered
- Need explicit documentation for user to know when to use via Task tool

---

## Troubleshooting

### Issue: CLAUDE.md section too long

**Symptom**: Section exceeds 40 lines

**Solution**: This command enforces ≤40 line limit. If custom content causes excess, use progressive disclosure:
1. Keep 3-5 critical rules in CLAUDE.md
2. Move detailed content to `docs/development/INCREMENTAL_DEV.md`
3. Link from CLAUDE.md

---

### Issue: Skills not working after update

**Symptom**: Skills don't activate automatically

**Cause**: Plugin not installed or Claude needs restart

**Solution**:
```bash
# Ensure plugin is installed
/plugin list | grep incremental-dev

# If not listed, install it
/plugin install incremental-dev

# Refresh plugin cache
/plugin refresh

# Skills are now auto-discovered
```

---

### Issue: Agent not available

**Symptom**: incremental-dev-coach not available in Task tool

**Cause**: Agent not documented in CLAUDE.md

**Solution**: Run `/update-claude-md` to add agent documentation to CLAUDE.md

---

## Performance Notes

- Command execution: ~2-5 seconds (file I/O operations)
- CLAUDE.md size impact: +~1,500 characters (≤40 lines)
- No impact on Claude startup time (agent already documented)
- Skills auto-discovered on plugin install (one-time operation)

---

**Developed by Carlos Araujo for incremental-dev plugin** 🚀