---
description: Select next slice from BACKLOG.md, create git branch, capture baseline metrics, and initialize development tracking
allowed-tools: Read, Write, Bash, Grep
argument-hint: '[auto|interactive]'
---

# Iniciar Slice - Start Development Workflow

Automatically select the next slice from BACKLOG.md, create git branch, capture baseline metrics, and initialize development tracking in SLICE_TRACKER.md.

## Preconditions

Verify before starting:

1. **docs/BACKLOG.md exists** - Run `/backlog create` first if missing
1. **At least one slice has status "📋 TODO"** - Run `/analyze-slices` first to validate
1. **Git repository is clean** - No uncommitted changes (`git status` shows clean)
1. **On main/default branch** - Currently on main branch, no unmerged changes
1. **docs/slices/ directory exists** - Created by `/analyze-slices` for GO slices
1. **CI.py exists or will be created** - Baseline metrics collection script

If any precondition fails: Stop and guide user to complete prerequisites.

## Selection Algorithm - Automatic Slice Selection

Before starting any development, analyze BACKLOG.md and select the highest-priority slice using:

### Priority Rules (in order)

1. **Status Filter**: Only select slices with status `📋 TODO`

   - Skip: `⏳ Planejado` (not validated yet)
   - Skip: `🔄 Revalidar` (failed validation)
   - Skip: `➡️ Em Progresso` (already started)
   - Skip: `✅ Concluído` (completed)

1. **Fast-Track Priority**: Quick wins first

   - **IF** any slice has `🚀 Elegível para Fast-Track`:
     - **SELECT**: Lowest numbered Fast-Track slice
     - **Reason**: Unblock faster, build momentum, validate workflow
   - **ELSE**: Proceed to standard slices

1. **Impact-Based Priority** (for standard slices):

   - Sort by Impact level: HIGH > MEDIUM > LOW
   - Within same Impact: lowest number first

### Selection Process

1. **Parse BACKLOG.md**:

   - Extract all increments with their:
     - Slice number (### N.)
     - Title
     - Status
     - Impacto (HIGH/MEDIUM/LOW)
     - Tracker path
     - Fast-Track indicator (if present)

1. **Apply filters**:

   - Keep only slices with status `📋 TODO`
   - If no eligible slices: Display options and exit

1. **Apply priority**:

   - Extract Fast-Track eligible slices
   - If found: Select lowest numbered Fast-Track
   - Else: Sort by (Impact level DESC, Slice number ASC)
   - Select first slice from sorted list

1. **Validate selected slice**:

   - Verify SLICE_N_TRACKER.md exists
   - Verify tracker doesn't already have Section 2 (not already started)
   - If validation fails: Skip to next eligible slice

### Selection Output

**Display selected slice** (with mode argument):

```
🔍 Analisando BACKLOG.md...

✅ Slice {N} selecionada!
   📌 Título: {Title from BACKLOG.md}
   🎯 Impacto: {Impact level}
   ⏱️  Estimativa: {Hours}h
   🚀 Fast-Track: {YES/NO}
   📄 Tracker: docs/slices/SLICE_{N}_TRACKER.md

{In interactive mode}:
   Continuar com esta slice? (y/n)

{In auto mode}:
   [Automatically proceed without user confirmation]
```

## Git Branch Creation

After slice selection confirmed:

1. **Generate branch name**:

   - Format: `slice-{N}-{kebab-case-title}`
   - Extract title from BACKLOG.md increment title
   - Convert to kebab-case (lowercase, replace spaces with hyphens)
   - Examples:
     - "Implement core classifier algorithm" → `slice-1-implement-core-classifier`
     - "Add Edge Case Handling" → `slice-2-add-edge-case-handling`

1. **Create branch**:

   - Execute: `git checkout -b slice-{N}-{title}`
   - Capture created branch name and base commit hash: `git rev-parse HEAD`

1. **Verify branch creation**:

   - Confirm: `git branch --list | grep slice-{N}`
   - Display branch name and base commit to user

## Baseline Metrics Collection

Before starting development, capture baseline metrics using CI.py:

### Step 1: Ensure CI.py exists

**If CI.py NOT found in project root**:

1. Create template CI.py with this content:

```python
#!/usr/bin/env python
"""
CI.py - Metrics Collection Script

Runs tests and collects baseline metrics for tracking.
Execute this script before starting a slice and after completion.

Usage:
    python CI.py              # Run tests and collect metrics
    python CI.py --baseline   # Capture baseline only
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

def run_tests():
    """Run pytest and return results."""
    try:
        result = subprocess.run(
            ["pytest", "--tb=short", "-q"],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result
    except FileNotFoundError:
        print("⚠️  pytest not found. Install with: pip install pytest")
        return None

def collect_metrics(test_result):
    """Extract metrics from pytest output."""
    if test_result is None:
        return {
            "success_rate": 0.0,
            "test_count": 0,
            "latency_ms": 0,
            "timestamp": datetime.now().isoformat(),
            "status": "NO_TESTS"
        }

    # Parse pytest output format: "X passed, Y failed in Zs"
    output = test_result.stdout + test_result.stderr

    # Extract test counts
    import re
    match = re.search(r"(\d+) passed", output)
    passed = int(match.group(1)) if match else 0

    match = re.search(r"(\d+) failed", output)
    failed = int(match.group(1)) if match else 0

    total = passed + failed
    success_rate = (passed / total * 100) if total > 0 else 0.0

    match = re.search(r"(\d+\.\d+)s", output)
    latency_ms = int(float(match.group(1)) * 1000) if match else 0

    return {
        "success_rate": round(success_rate, 1),
        "test_count": total,
        "latency_ms": latency_ms,
        "timestamp": datetime.now().isoformat(),
        "status": "COMPLETED" if total > 0 else "NO_TESTS",
        "passed": passed,
        "failed": failed
    }

if __name__ == "__main__":
    print("🔄 Running tests and collecting metrics...")
    result = run_tests()
    metrics = collect_metrics(result)

    print(f"\n📊 Metrics collected:")
    print(f"   Success Rate: {metrics['success_rate']}%")
    print(f"   Test Count: {metrics['test_count']}")
    print(f"   Latency: {metrics['latency_ms']}ms")

    # Save metrics to metrics.json for reference
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n✅ Metrics saved to metrics.json")
```

2. Save as `CI.py` in project root
1. Display: "CI.py created with template. Edit to customize metrics collection."

**If CI.py exists**:

1. Execute: `python CI.py` (or `uv run CI.py`)
1. Verify exit code is 0

### Step 2: Execute CI.py and capture metrics

1. **Run CI.py**:

   - Execute: `python CI.py` or `uv run CI.py`
   - Capture stdout, stderr, exit code

1. **Extract metrics**:

   - Parse output for:
     - `success_rate`: Percentage (float)
     - `test_count`: Number of tests
     - `latency_ms`: Average execution time
   - If metrics.json created: read and parse
   - If output format different: extract via regex patterns

1. **Display baseline**:

```
📊 Baseline Metrics Captured:
   ✓ Success Rate: {X}%
   ✓ Test Count: {N} tests
   ✓ Avg Latency: {Y}ms
   ✓ Captured At: {ISO_TIMESTAMP}
```

## Update BACKLOG.md

After metrics captured, update BACKLOG.md:

1. **Locate slice in BACKLOG.md**:

   - Find line: `### {N}.` (slice number)

1. **Update status**:

   - Find: `- **Status**: 📋 TODO`
   - Replace with: `- **Status**: ➡️ Em Progresso`

1. **Add branch field** (if not exists):

   - Add line: `- **Branch**: slice-{N}-{kebab-case-title}`
   - Place after Status field

1. **Verify update**:

   - Display confirmation with updated section

## Update SLICE_TRACKER.md - Section 2

Add Section 2 (DESENVOLVIMENTO) to SLICE_TRACKER.md:

1. **Locate insertion point**:

   - Find line: `## Classificação Fast-Track`
   - Insert Section 2 **after** this section, **before** `## Development Log`

1. **Create Section 2 with this template**:

```markdown
## Desenvolvimento (Section 2)

### Git Branch
- **Branch Name**: `slice-{N}-{kebab-case-title}`
- **Created At**: {ISO_TIMESTAMP}
- **Base Commit**: {commit_hash}

### Metrics Baseline (Initial)
Captured at: {ISO_TIMESTAMP}
- **Success Rate**: {X}%
- **Test Count**: {N} tests
- **Avg Latency**: {Y}ms
- **Status**: READY_FOR_DEV

### Environment Setup
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] LangSmith connection validated (if applicable)
- [ ] CI.py baseline captured
- [ ] Branch created and verified

### Development Checkpoints

#### Testing Tasks (Slice-Level Quality Gates)
- [ ] **Smoke tests** created for critical paths
- [ ] **Unit tests** written for all new functions/classes
- [ ] **Integration tests** (if applicable - see criteria below)
- [ ] **Regression tests** added to prevent breaking changes
- [ ] **Test coverage** validated: ≥70% coverage achieved
- [ ] All tests passing locally (pytest)

#### Implementation Tasks
- [ ] Core implementation complete
- [ ] Edge cases handled
- [ ] Code follows project patterns

#### Quality Review
- [ ] Code reviewed (self or peer)
- [ ] CI.py validation passed with no regressions
- [ ] Documentation updated (if applicable)

---

**Integration Tests Criteria** (when to include):

Add integration tests if your slice involves:
- ✅ External APIs or services (HTTP, gRPC, webhooks)
- ✅ Database operations (multiple tables, transactions)
- ✅ Multiple components interaction (e.g., LangChain chains + tools)
- ✅ Message queues or async processing
- ✅ Authentication/authorization flows
- ✅ File system operations with side effects

Skip integration tests if:
- ❌ Pure business logic (use unit tests)
- ❌ Single component/class (use unit tests)
- ❌ No external dependencies

### Metrics Delta (Target vs Actual)
- **Target Success Rate Delta**: [from Brief Minimo Gate 5]
- **Actual Success Rate Delta**: [to be filled during development]
- **Expected Contribution**: [% of gap closed by this slice]
```

1. **Update Metadata status**:

   - Find: `- **Status**: ➡️ Em Progresso` in Metadata
   - Ensure timestamp is recent: `- **Iniciado em**: {current_ISO_TIMESTAMP}`

1. **Display confirmation**:

```markdown
📝 SLICE_TRACKER.md Updated:
   ✓ Section 2 (DESENVOLVIMENTO) added
   ✓ Baseline metrics recorded
   ✓ Environment checklist initialized
```

## Execution Modes

### Interactive Mode (default)

When no argument or `interactive` specified:

1. Display selected slice with details
1. Ask user: "Continuar com esta slice? (y/n)"
1. If yes: Proceed with branch creation and setup
1. If no: Select next eligible slice and repeat

### Auto Mode

When argument is `auto`:

1. Select next eligible slice
1. Skip user confirmation
1. Automatically create branch and setup
1. Display summary of completed actions

## Final Validation

After all updates completed:

1. **Verify BACKLOG.md update**:

   - Confirm status changed to `➡️ Em Progresso`
   - Confirm branch field added

1. **Verify SLICE_TRACKER.md update**:

   - Confirm Section 2 present
   - Confirm baseline metrics recorded

1. **Verify git branch**:

   - Confirm on new branch: `git branch --show-current`
   - Confirm branch name matches expected format

1. **Display success summary**:

```markdown
✅ Slice {N} initialized successfully!

📂 Files Updated:
   • docs/BACKLOG.md (status: ➡️ Em Progresso)
   • docs/slices/SLICE_{N}_TRACKER.md (Section 2 added)

🌿 Git Branch:
   • Active: slice-{N}-{kebab-case-title}
   • Base Commit: {hash}

📊 Baseline Metrics:
   • Success Rate: {X}%
   • Test Count: {N}
   • Avg Latency: {Y}ms
   • Captured: {timestamp}

🚀 Next Steps:
   1. Implement slice according to objectives in SLICE_TRACKER.md
   2. Follow TDD approach: write tests first
   3. Update Development Log in SLICE_TRACKER.md as you progress
   4. Execute tests frequently: pytest tests/
   5. When complete, will create /concluir-slice command for finalization
```

## Error Handling

**If preconditions not met**:

- Stop and guide user to prerequisites
- List missing items clearly

**If no eligible slices found**:

- Display available options:
  1. Run `/analyze-slices` to validate pending slices
  1. Run `/backlog view` to check current status
  1. Review completed slices: `✅ Concluído`

**If git branch creation fails**:

- Check git status
- Verify branch doesn't exist
- Offer to delete old branch if exists

**If CI.py execution fails**:

- Display error output
- Offer to create template or use manual baseline entry

## Integration with Other Commands

**Workflow continuation**:

1. `/brief` → Generate Brief Minimo
1. `/backlog create` → Create BACKLOG.md
1. `/analyze-slices` → Validate and create SLICE_TRACKER.md
1. `/iniciar-slice` ← **YOU ARE HERE**
1. [Development happens]
1. (Future) `/concluir-slice` → Record completion metrics
