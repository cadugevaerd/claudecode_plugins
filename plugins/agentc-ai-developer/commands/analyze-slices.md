---
description: Validate backlog slices against S1.1 decision gates and trigger refinement if needed
allowed-tools: Read, Write, Grep
argument-hint: '[validate|refine|auto]'
---

# Analyze Slices Against S1.1 Gates

## Preconditions

1. Verify docs/BACKLOG.md exists
1. Verify Brief Minimo specification is complete in README.md
1. Ensure at least one increment is defined in backlog

If missing: Stop and guide user to run `/backlog create` first.

## Validation Mode (Default)

1. Read docs/BACKLOG.md
1. Analyze each slice (increment) against S1.1 decision gates:

### Decision Gates

For each slice, validate:

- **Gate 1 - Duration 3-6h?**: Check "Horas Estimadas" is between 3-6 hours

  - FAIL: Slice is too large (>6h) or too small (\<3h for standard cycle)
  - PASS: Duration fits standard cycle window

- **Gate 2 - Score >= 2.0?**: Calculate impact score:

  - HIGH impact = 3, MEDIUM = 2, LOW = 1
  - Score = (Impact level) / (Estimated hours / 3)
  - Must be >= 2.0 (ensures good impact-to-effort ratio)
  - FAIL: Low impact relative to effort invested
  - PASS: Efficient slice with good ROI

- **Gate 3 - Reversible?**: Assess if slice can be rolled back

  - FAIL: Slice modifies shared state or core architecture without rollback plan
  - PASS: Clear rollback strategy documented or changes are isolated

- **Gate 4 - Architecturally Isolated?**: Check coupling level

  - FAIL: Slice depends on multiple external components
  - PASS: Slice focuses on single isolated component (low coupling)

- **Gate 5 - Increases success_rate?**: Calculate contribution to success metrics

  - Extract success metric from README.md (Pergunta 5 do Brief Minimo)
  - For each slice, assess: "How does this slice move the metric toward the target?"
  - FAIL: Slice has no measurable contribution to success metric (0% delta)
  - PASS: Slice measurably improves success metric (>0% estimated delta)
  - Example:
    - Brief Target: "85% accuracy on email classification"
    - Slice 1: "Implement core classifier logic" → estimated delta +40%
    - Slice 2: "Add edge case handling" → estimated delta +15%
    - Slice 3: "Code review polish" → estimated delta +5%

3. Generate analysis report:

   - Slices that PASS all gates (GO): Ready for execution
   - Slices that FAIL any gate (NO-GO): Blockers identified
   - Summary: X GO slices / Y NO-GO slices total

1. For each NO-GO slice, list which gates failed and why

## Fast-Track Validation (S1.1 Fast-Track)

After validating against standard gates, check if slices qualify for Fast-Track (quick validation path for trivial work):

### Fast-Track Criteria

For each GO slice (passed all 5 gates), validate Fast-Track eligibility:

- **Duration < 1h?**: Estimated hours must be under 1 hour

  - FAIL: Slice takes 1h or longer (use standard development path)
  - PASS: Slice is truly trivial (\<1h)

- **Risk Level LOW?**: Assess risk classification

  - FAIL: Slice has medium/high risk (modifies core logic, API changes, etc.)
  - PASS: Low risk work (documentation, simple fixes, tests, minor refactors)

- **No Architecture Changes?**: Verify slice doesn't modify system design

  - FAIL: Slice changes interfaces, schemas, or architectural decisions
  - PASS: Slice operates within existing architecture boundaries

- **Clear Success Criteria?**: Validate acceptance criteria are simple and testable

  - FAIL: Vague success definition or complex validation needed
  - PASS: Simple, obvious success criteria (e.g., "button renders", "test passes")

### Fast-Track Decision

- **All criteria PASS**: Slice is FAST-TRACK eligible

  - Development continues in Fast-Track workflow (minimal validation, quick iteration)
  - Skip full testing cycle, use smoke tests only
  - Enable quick feedback loops for trivial work

- **Any criterion FAIL**: Slice is NOT Fast-Track eligible

  - Development returns to standard cycle (all 5 gates + full validation)
  - Requires standard testing and review process
  - Follow regular development workflow

### Fast-Track Examples

**FAST-TRACK PASS** (✅ Quick Path):

- "Add docstring to utility function" (\<1h, low risk, no architecture change, obvious success)
- "Fix typo in error message" (\<1h, low risk, no architecture change, obvious success)
- "Add test for existing function" (\<1h, low risk, no architecture change, clear success)

**FAST-TRACK FAIL** (❌ Standard Path):

- "Implement core classifier algorithm" (>6h, high risk, architecture-dependent, complex validation)
- "Refactor API response schema" (1-2h, medium risk, architecture change, requires testing)
- "Add optional parameter to function" (1h, medium risk, interface change, requires validation)

## Success Rate Calculation

For each slice, calculate how much it increases the success metric:

### Step 1: Extract baseline from Brief Minimo

- Read README.md "What is SUCCESS?" section
- Identify: Current baseline (if exists) and target metric
- Example: "Current: 45% accuracy | Target: 85% accuracy | Gap: 40%"

### Step 2: Estimate delta per slice

- For each slice, ask: "What % of the target gap does this slice close?"
- Assign estimated delta (conservative estimate):
  - Core functionality slices: 20-40% of gap
  - Enhancement slices: 10-20% of gap
  - Polish/optimization slices: 5-15% of gap
- Example breakdown for 40% gap:
  - Slice 1 (Core classifier): +25% (closes 62.5% of gap)
  - Slice 2 (Edge cases): +10% (closes 25% of gap)
  - Slice 3 (Polish): +5% (closes 12.5% of gap)

### Step 3: Validate cumulative coverage

- Sum all estimated deltas
- Check: "Do all slices together meet or exceed target?"
- Example: 25% + 10% + 5% = 40% ≥ Target 40% ✅

### Step 4: Assign success_rate contribution

- Gate 5 PASS: Slice delta > 0% (measurable contribution)
- Gate 5 FAIL: Slice delta = 0% (no measurable value)

## Refine Mode

1. Run validation analysis first
1. If all slices FAIL (entire backlog is invalid):
   - Display: "Entire backlog requires refinement"
   - Execute `/backlog refine` to initiate backlog refinement process
1. If mixed results (some GO, some NO-GO):
   - Display which slices are GO (ready to execute)
   - Display which slices need refinement
   - Ask user: "Refine failing slices now? (y/n)"
   - If yes: Execute `/backlog refine` with failing slice names

## Auto Mode

1. Run validation analysis automatically
1. If any slices FAIL gates:
   - Automatically execute `/backlog refine`
   - Pass list of failing slices to refine process
1. If all slices PASS gates:
   - Display "All slices ready for execution"
   - Show next recommended GO slice to start

## Output Summary

Display analysis results:

- Total slices analyzed
- GO slices (passed all gates)
- NO-GO slices with gate failures
- Score calculations for each slice
- **Success Rate Impact Analysis**:
  - Global success metric and target (from Brief Minimo)
  - Estimated success_rate delta for each slice (% contribution)
  - Cumulative success_rate if all slices execute sequentially
  - Validation: Total estimated delta meets or exceeds target gap
- **Fast-Track Classification**:
  - FAST-TRACK eligible slices (\<1h, low risk, no architecture changes, clear success)
  - Standard path slices (all others)
  - Workflow recommendation for each slice
- Recommendation: Next action (execute, fast-track, or refine)
- Gate failure distribution (helps identify pattern issues)
