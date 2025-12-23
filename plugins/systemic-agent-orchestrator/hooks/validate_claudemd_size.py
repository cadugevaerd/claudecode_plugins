#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Hook to validate CLAUDE.md file size on Stop event.

Blocks if CLAUDE.md exceeds 200 lines.
"""

import json
import sys
from pathlib import Path

MAX_LINES = 200
WARNING_THRESHOLD = 180


def find_claudemd() -> Path | None:
    """Find CLAUDE.md in current directory or parent directories."""
    cwd = Path.cwd()

    # Check current directory and parents
    for directory in [cwd, *cwd.parents]:
        claudemd = directory / "CLAUDE.md"
        if claudemd.exists():
            return claudemd
        # Stop at home or root
        if directory == Path.home() or directory == Path("/"):
            break

    return None


def main() -> None:
    """Validate CLAUDE.md line count on Stop event."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    # Only run on Stop event
    hook_event = input_data.get("hook_event_name", "")
    if hook_event != "Stop":
        print(json.dumps({}))
        return

    claudemd_path = find_claudemd()
    if not claudemd_path:
        # No CLAUDE.md found, pass
        print(json.dumps({}))
        return

    try:
        content = claudemd_path.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
    except Exception:
        print(json.dumps({}))
        return

    if line_count > MAX_LINES:
        reason = f"""=== CLAUDE.md Size Validation ===

[FAIL] CLAUDE.md exceeds {MAX_LINES}-line limit

File: {claudemd_path}
Current lines: {line_count}
Maximum allowed: {MAX_LINES}
Excess lines: {line_count - MAX_LINES}

RECOMMENDATIONS - Reduce CLAUDE.md size:

1. **Remove redundant sections:**
   - Consolidate similar rules
   - Remove duplicated information
   - Merge related instructions

2. **Use references instead of inline content:**
   - Link to external docs
   - Reference memory files for detailed info
   - Keep only essential instructions

3. **Prioritize critical rules:**
   - Keep workflow rules
   - Keep testing requirements
   - Remove verbose examples

4. **Move details to other locations:**
   - Detailed examples → memory files
   - Tool-specific guides → separate docs
   - Long checklists → external files

Run /systemic-agent-orchestrator:micro-task to refactor CLAUDE.md"""

        result = {
            "decision": "block",
            "reason": reason
        }
        print(json.dumps(result))
        return

    if line_count > WARNING_THRESHOLD:
        # Warning but don't block
        print(json.dumps({}))
        return

    print(json.dumps({}))


if __name__ == "__main__":
    main()
