---
description: Validate backlog slices against S1.1 decision gates and trigger refinement if needed
allowed-tools: Read, Write, Edit, Grep
argument-hint: '[validate|refine|auto]'
model: sonnet
---

# Analyze Slices Against S1.1 Gates

## 🎯 Objetivo

Validar cada slice (incremento) do backlog contra os 5 Decision Gates da metodologia Brief Minimo (S1.1) para garantir que:

- ✅ Duração está entre 3-6 horas (Gate 1)
- ✅ Score impacto/esforço ≥ 2.0 (Gate 2)
- ✅ Slice é reversível (Gate 3)
- ✅ Arquitetura está isolada/baixo acoplamento (Gate 4)
- ✅ Contribui para métrica de sucesso (Gate 5)
- 🚀 Identifica slices elegíveis para Fast-Track (\<1h, baixo risco)
- 📋 Cria trackers automáticos para slices aprovados (GO)
- 🔄 Identifica slices que precisam de refinamento (NO-GO)

**Resultado esperado**: Relatório de análise com decisão GO/NO-GO para cada slice e próxima ação recomendada.

## ⚙️ Preconditions

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

1. Generate analysis report:

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

## POST-VALIDATION: Slice Tracking

After validation analysis, automatically update project files based on GO/NO-GO decisions:

### For GO Slices (All Gates Passed)

1. **Create Slice Tracker**:

   - Create directory: `docs/slices/` (if doesn't exist)
   - Create file: `docs/slices/SLICE_{N}_TRACKER.md` for each GO slice
   - Use slice number from BACKLOG.md increment (e.g., "### 1." → SLICE_1_TRACKER.md)

1. **Populate Tracker - Section 1 (Planning)**:

   - **Slice ID**: Extract from increment number (e.g., 1)
   - **Slice Name**: Copy from "### N. [Title]" in BACKLOG.md
   - **Status**: Set to "➡️ Em Progresso"
   - **Objetivo**: Copy from "- **Objetivo**:" field in BACKLOG.md (exact 1-sentence copy)
   - **Critérios de Aceitação**: Extract 3 checkpoints from "- **Tarefas**:" checklist (convert 3 tasks to acceptance criteria)
   - **Reversibilidade**: Extract from Gate 3 validation result (rollback plan)
   - **Timestamp Início**: Current ISO 8601 timestamp (e.g., `2025-11-05T17:30:45`)

1. **Populate Tracker - Gate Validation Section**:

   - Copy all 5 Gate validation results from analysis
   - Include PASS/FAIL status, criteria met, and score

1. **Update BACKLOG.md**:

   - Find increment in BACKLOG.md (by number)
   - Replace status from "⏳ Planejado" to "📋 TODO"
   - Add new field: `- **Tracker**: [SLICE_{N}_TRACKER.md](./slices/SLICE_{N}_TRACKER.md)`

### For NO-GO Slices (Any Gate Failed)

1. **Update BACKLOG.md**:

   - Find increment in BACKLOG.md (by number)
   - Replace status from "⏳ Planejado" to "🔄 Revalidar"
   - Add field: `- **Gates Falhadas**: [Gate 1, Gate 3]` (list which gates failed)
   - Do NOT create tracker file (tracker only created for GO slices)

1. **Display Summary**:

   - Show which gates failed
   - Suggest user run `/backlog refine` to fix issues

### Fast-Track Slices (GO + All Fast-Track Criteria Pass)

1. **Update BACKLOG.md**:
   - Add field: `- **Fast-Track**: 🚀 Elegível para Fast-Track`
   - Note: This is in addition to "📋 TODO" and tracker creation

### Tracker File Template

Create tracker with this structure:

```markdown
# Slice {N} Tracker - {Slice Title}

## Metadata
- **Slice ID**: {N}
- **Status**: ➡️ Em Progresso
- **Iniciado em**: {ISO_TIMESTAMP}

## Planejamento (Section 1)

### Nome
{Slice Title}

### Objetivo
{1-sentence objective from BACKLOG.md}

### Critérios de Aceitação
- [ ] {Acceptance Criterion 1 from task 1}
- [ ] {Acceptance Criterion 2 from task 2}
- [ ] {Acceptance Criterion 3 from task 3}

### Reversibilidade
{Rollback plan from Gate 3 validation}

### Timestamp Início
{ISO_TIMESTAMP}

## Validação S1.1 (Gates)

### Gate 1 - Duration (3-6h)
- **Status**: ✅ PASS / ❌ FAIL
- **Horas Estimadas**: {X}h
- **Validação**: {Why passed or failed}

### Gate 2 - Score >= 2.0
- **Status**: ✅ PASS / ❌ FAIL
- **Nível de Impacto**: HIGH / MEDIUM / LOW ({numeric value})
- **Score**: {calculated score}
- **Validação**: {Why passed or failed}

### Gate 3 - Reversível
- **Status**: ✅ PASS / ❌ FAIL
- **Plano de Rollback**: {Description}
- **Validação**: {Why passed or failed}

### Gate 4 - Isolado
- **Status**: ✅ PASS / ❌ FAIL
- **Nível de Acoplamento**: LOW / MEDIUM / HIGH
- **Validação**: {Why passed or failed}

### Gate 5 - Contribui para Success Rate
- **Status**: ✅ PASS / ❌ FAIL
- **Delta Estimado**: {+X}% (closes Y% of gap)
- **Validação**: {Why passed or failed}

## Classificação Fast-Track
- **Elegível**: ✅ YES / ❌ NO
- **Motivo**: {Why fast-track eligible or not}

## Development Log
- `{ISO_TIMESTAMP}` - Slice approved (GO decision)

## Notas
[Developer notes will be added during development]
```

## 📝 Exemplos de Uso

### Exemplo 1: Modo Validate (Padrão)

```bash
/analyze-slices validate
# ou simplesmente
/analyze-slices
```

**Output esperado:**

```text
🔍 Analisando slices contra S1.1 Decision Gates...

✅ Slice 1: Implementar core classifier
   Gate 1 (Duration): ✅ PASS (4h, dentro de 3-6h)
   Gate 2 (Score): ✅ PASS (Score: 2.25, Impact: HIGH)
   Gate 3 (Reversible): ✅ PASS (Rollback: restore from backup)
   Gate 4 (Isolated): ✅ PASS (Low coupling)
   Gate 5 (Success Rate): ✅ PASS (+25% accuracy delta)
   Fast-Track: ❌ NO (>1h, high complexity)
   → Status: GO (Tracker criado: docs/slices/SLICE_1_TRACKER.md)

⚠️ Slice 2: Add edge case handling
   Gate 1 (Duration): ✅ PASS (3h)
   Gate 2 (Score): ❌ FAIL (Score: 1.5, Impact: MEDIUM, Effort: 3h)
   Gate 3 (Reversible): ✅ PASS
   Gate 4 (Isolated): ✅ PASS
   Gate 5 (Success Rate): ✅ PASS (+10% delta)
   → Status: NO-GO (Gate 2 failed: low impact/effort ratio)

📊 Resumo:
- Total: 2 slices
- GO: 1 slice (50%)
- NO-GO: 1 slice (50%)
- Fast-Track: 0 slices

🔄 Próxima ação: Refinar Slice 2 ou iniciar Slice 1 com /iniciar-slice
```

### Exemplo 2: Modo Refine

```bash
/analyze-slices refine
```

**Output esperado:**

```text
🔍 Analisando slices... (mesmo output acima)

❌ Slice 2 falhou Gate 2 (Score < 2.0)

🔧 Deseja refinar slices que falharam? (y/n)
> y

🚀 Executando /backlog refine para Slice 2...
[Processo de refinement iniciado]
```

### Exemplo 3: Modo Auto

```bash
/analyze-slices auto
```

**Output esperado:**

```text
🔍 Analisando slices automaticamente...

✅ Slice 1: GO
⚠️ Slice 2: NO-GO (Gate 2 failed)

🤖 AUTO MODE: Refinando automaticamente slices NO-GO...
🚀 Executando /backlog refine [Slice 2]

[Após refinamento]
✅ Todos os slices prontos para execução!
📋 Próximo slice recomendado: Slice 1 (Impact: HIGH)
💡 Execute /iniciar-slice para começar desenvolvimento
```

### Exemplo 4: Todos Slices GO + Fast-Track

```bash
/analyze-slices
```

**Output esperado:**

```text
🔍 Analisando slices...

✅ Slice 1: Implementar classifier (GO, Standard Path)
✅ Slice 2: Add docstring (GO, 🚀 FAST-TRACK)
✅ Slice 3: Fix typo in error message (GO, 🚀 FAST-TRACK)

📊 Resumo:
- Total: 3 slices
- GO: 3 slices (100%)
- NO-GO: 0 slices
- Fast-Track: 2 slices (66%)

🎉 Todos os slices aprovados!
🚀 2 slices elegíveis para Fast-Track (desenvolvimento rápido)
📋 Trackers criados: SLICE_1_TRACKER.md, SLICE_2_TRACKER.md, SLICE_3_TRACKER.md

💡 Próxima ação: Execute /iniciar-slice para começar com Slice 2 (Fast-Track)
```

## ✅ Critérios de Sucesso

Validação de que o comando `/analyze-slices` foi executado corretamente:

- [ ] BACKLOG.md localizado e lido com sucesso
- [ ] Brief Minimo extraído do README.md (métrica de sucesso identificada)
- [ ] Todos os slices validados contra os 5 Decision Gates
- [ ] Score de impacto calculado para cada slice (Gate 2: Impact/Effort ≥ 2.0)
- [ ] Contribuição para success_rate calculada para cada slice (Gate 5: Delta > 0%)
- [ ] Classificação Fast-Track determinada para slices GO (\<1h, baixo risco, sem mudanças arquiteturais)
- [ ] Trackers criados para slices GO (`docs/slices/SLICE_{N}_TRACKER.md`)
- [ ] BACKLOG.md atualizado com status correto:
  - `📋 TODO` para slices GO
  - `🔄 Revalidar` para slices NO-GO
  - `🚀 Elegível para Fast-Track` para slices Fast-Track
- [ ] Relatório de análise apresentado (GO/NO-GO summary, gate failure distribution)
- [ ] Próxima ação recomendada identificada (`/iniciar-slice` ou `/backlog refine`)

## 🔗 Next Steps - Start Development

After all GO slices are validated and trackers created:

**Execute `/iniciar-slice` to start development**:

1. **Automatic slice selection**:

   - Selects next eligible slice with status `📋 TODO`
   - Prioritizes Fast-Track slices for quick wins
   - Orders by Impact level (HIGH → MEDIUM → LOW)

1. **Initialize development environment**:

   - Creates git branch: `slice-{N}-{kebab-case-title}`
   - Captures baseline metrics via CI.py
   - Updates BACKLOG.md: `📋 TODO` → `➡️ Em Progresso`
   - Populates Section 2 (DESENVOLVIMENTO) in SLICE_TRACKER.md

1. **Ready for TDD development**:

   - Write tests first (recommended)
   - Implement functionality
   - Track progress in SLICE_TRACKER.md Development Log

### Command Usage

```bash
# Interactive mode (ask for confirmation)
/iniciar-slice

# Auto mode (skip confirmation)
/iniciar-slice auto
```

### Workflow Integration

```text
1. /brief                   → Define agent scope
2. /backlog create          → Create BACKLOG.md with slices
3. /analyze-slices validate → Validate slices against S1.1 gates
4. /iniciar-slice           ← CREATE SLICE TRACKERS AND START HERE
5. [Development]            → Write code and tests
6. (Future) /concluir-slice → Record completion metrics
```
