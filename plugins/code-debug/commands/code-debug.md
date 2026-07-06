---
description: Debug a code/runtime failure by reproducing the command, collecting evidence, and reporting verified root cause plus fix suggestion
argument-hint: "<debug/reproduction command, stack trace, or bug context>"
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
  - MultiEdit
  - Write
  - TodoWrite
---

# Code Debug

Use the `code-debug` skill to investigate this failure with strict root-cause discipline.

## Debug target

`$ARGUMENTS`

## Mandatory behavior

1. Reproduce the failure or explain the exact blocker.
2. Analyze logs, stack traces, code, configs, state and environment before concluding.
3. Add minimal temporary logs/instrumentation when evidence is insufficient.
4. Never assume the cause. Treat ideas as hypotheses until tested.
5. Return a report with verified root cause and suggested fix. If not verified, say `causa raiz nao comprovada ainda` and list the missing evidence.

Follow the output format defined in the `code-debug` skill.
