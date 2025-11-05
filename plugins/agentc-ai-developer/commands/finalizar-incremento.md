---
description: Finalize current increment with metrics validation, coverage check (≥70%), regression tests, and automatic decision on next steps
allowed-tools: Read, Bash, Write, Grep, AskUserQuestion
argument-hint: ''
---

# Finalizar Incremento - Complete Increment Validation Loop

Finalize the current increment by validating metrics, ensuring test coverage ≥70%, checking for regressions, and automatically determining whether to continue or conclude the slice.

## Preconditions

Verify before starting:

1. **SLICE_N_TRACKER.md exists** - Slice must be initialized
1. **Section 3 (INCREMENTOS) exists** - Must have created incremento with `/novo-incremento`
1. **Incremento N exists with status "Em Progresso"** - Current increment active
1. **At least one commit since incremento start** - Code changes made
1. **Git working directory is clean** - No uncommitted changes
1. **pytest-cov installed** - For coverage validation: `pip install pytest-cov`
1. **CI.py exists in project root** - For metrics collection

If any precondition fails: Stop and guide user to complete prerequisites.

## Validation Pipeline

### Step 1: Verify Incremento State

1. **Locate current incremento**:

   - Find latest `### Incremento {N}:` in Section 3
   - Verify status: `- **Status**: ➡️ Em Progresso`
   - Extract start time: `- **Iniciado em**: {ISO_TIMESTAMP}`

1. **Verify git commits**:

   - Get current branch: `git branch --show-current`
   - Count commits since incremento start
   - If 0 commits: Ask user "No changes made. Continue anyway? (y/n)"

1. **Verify uncommitted changes**:

   - Run: `git status --porcelain`
   - If any uncommitted: Block with "Commit your changes first: git add . && git commit"

### Step 2: Capture Final Metrics

Execute CI.py to capture final metrics:

1. **Run CI.py**:

   - Execute: `uv run CI.py` (or `python CI.py`)
   - Capture: success_rate, test_count, latency_ms, timestamp
   - If fails: Display error and ask to fix tests first

1. **Extract metrics**:

   ```
   Final Metrics:
   - Success Rate: {X}%
   - Test Count: {N} tests
   - Avg Latency: {Y}ms
   - Timestamp: {ISO_TIMESTAMP}
   ```

1. **Compare to baseline**:

   - Read Section 2: Baseline metrics
   - Calculate delta:
     - Success Rate Delta: (Final - Baseline)%
     - Test Count Delta: (Final - Baseline)
     - Latency Delta: (Final - Baseline)ms

### Step 3: Validate Test Coverage (BLOCKING)

Validate that test coverage >= 70%:

1. **Run pytest with coverage**:

   ```bash
   uv run pytest --cov --cov-report=json --cov-report=term
   ```

1. **Extract coverage %**:

   - Parse output: `TOTAL` coverage line
   - Extract percentage: {Z}%

1. **Validate >= 70%**:

   - If coverage >= 70%:
     - Continue to Step 4
   - If coverage < 70%:
     - **BLOCK**: "❌ Coverage too low: {Z}% < 70% minimum"
     - Display: "Add more tests to reach 70% coverage"
     - Display: Missing coverage areas
     - Exit with error (do NOT continue)

### Step 4: Validate Regressions

Check for breaking changes:

1. **Get baseline test count**:

   - Read Section 2: `- **Test Count**: {N} tests`
   - Store as: baseline_tests

1. **Compare current tests**:

   - Current test count from Step 2
   - If current_tests < baseline_tests:
     - **REGRESSION DETECTED**: Test count decreased
     - Identify which tests were removed
     - Ask: "Some tests were removed. Continue anyway? (y/n)"
     - If no: Exit with error

1. **Check test results**:

   - If any test FAILED (from CI.py output):
     - **REGRESSION DETECTED**: Tests broken
     - List failing tests
     - Ask: "Some tests are failing. Continue anyway? (y/n)"
     - If no: Exit with error

1. **Regression status**:

   - If no regressions: `✅ Regressão = 0`
   - If regressions: `⚠️ Regressão = {count}`

### Step 5: Self-Review Validation

Present interactive checklist:

```
📋 Self-Review Checklist (3 min):

1. Código segue padrões do projeto?
   [ ] Naming conventions OK
   [ ] Indentation/formatting OK
   [ ] No code duplication

2. Testes adicionados adequadamente?
   [ ] Tests cover happy path
   [ ] Tests cover edge cases
   [ ] Tests are isolated

3. Componente é isolável?
   [ ] Low coupling to other modules
   [ ] Can be tested in isolation
   [ ] Changes are reversible

4. Sem breaking changes?
   [ ] Existing APIs unchanged
   [ ] Backward compatible
   [ ] No deprecated features removed

Resultado: ✅ APPROVED | ❌ NEEDS REVISION
```

User must answer all 4 questions before proceeding.

### Step 6: Apply Stopping Criteria

Evaluate the 3 decision criteria:

**Critério 1**: Success rate >= target?

```
Target (from Section 1): {X}%
Current: {Y}%
Result: {Y >= X ? ✅ PASS : ❌ FAIL}
```

**Critério 2**: Regressão = 0?

```
Regressions detected: {count}
Result: {count == 0 ? ✅ PASS : ❌ FAIL}
```

**Critério 3**: Self-review OK?

```
All checklist items: ✅ PASS
Result: ✅ PASS
```

### Step 7: Make Automatic Decision

Based on 3 criteria:

**IF all 3 are PASS**:

```
🎉 TODOS 3 CRITÉRIOS ATINGIDOS!

Este é o último incremento necessário?
Você pode:
  1. Executar /concluir-slice para finalizar
  2. Criar novo incremento se quiser mais melhorias

Status: Slice pode ser CONCLUÍDA
```

**IF any 1+ is FAIL**:

```
⏳ CONTINUAR COM PRÓXIMO INCREMENTO

Critério(s) não atingido(s):
  ❌ Success rate: {Y}% < {X}%
  ❌ Regressão: {count} testes quebrados
  ❌ Self-review: Item X falhou

Próximo passo: /novo-incremento

```

## Update SLICE_TRACKER.md - Incremento N

After all validations complete, update Section 3.N:

### Replace Incremento status:

**OLD**:

```markdown
### Incremento {N}: {Title}

- **Status**: ➡️ Em Progresso
- **Iniciado em**: {ISO_TIMESTAMP}
```

**NEW**:

```markdown
### Incremento {N}: {Title}

- **Status**: ✅ Finalizado
- **Iniciado em**: {ISO_TIMESTAMP}
- **Finalizado em**: {NEW_ISO_TIMESTAMP}
- **Duração Real**: {Xm Ys}
```

### Add Metrics Section:

```markdown
#### Métricas Finalizadas
- **Success Rate**: {Y}% (delta: +{Y-baseline}%)
- **Test Count**: {N} (delta: +{N-baseline})
- **Coverage**: {Z}%
- **Avg Latency**: {W}ms (delta: {W-baseline}ms)
- **Capturado em**: {ISO_TIMESTAMP}
```

### Add Validations Section:

```markdown
#### Validações
- ✅ Coverage ≥ 70%: {Z}%
- ✅ Regressão = 0: {count} detected
- ✅ Self-review: [PASSED/FAILED per item]
```

### Add Decision Section:

```markdown
#### Decisão Final
- **Critério 1 (Success Rate)**: {✅ PASS / ❌ FAIL}
- **Critério 2 (Regressão)**: {✅ PASS / ❌ FAIL}
- **Critério 3 (Self-Review)**: {✅ PASS / ❌ FAIL}
- **Próximo Passo**: {CONTINUAR com /novo-incremento / CONCLUIR com /concluir-slice}
- **Razão**: {Explanation based on criteria}

#### Commits
- **Base Commit**: {from Section 3.N inicial}
- **Final Commit**: {current HEAD hash}
- **Commit Count**: {number of commits}
```

## Update BACKLOG.md (if exists)

If BACKLOG.md exists, optionally note progress:

1. Find slice in BACKLOG.md
1. Status remains: `➡️ Em Progresso` (still working)
1. Optionally add note: "N incrementos completed"

## Display Final Report

Show user comprehensive summary:

```
✅ Incremento {N} Finalizado!

📊 MÉTRICAS CAPTURADAS:
   Success Rate: {Y}% (baseline: {X}%, delta: +{Y-X}%)
   Test Count: {N} tests (baseline: {B}, delta: +{N-B})
   Coverage: {Z}% (✅ >= 70% required)
   Latency: {W}ms
   Timestamp: {ISO_TIMESTAMP}

✓ VALIDAÇÕES:
   ✅ Coverage >= 70%: {Z}%
   ✅ Regressão = 0: {regressão_count} detected
   ✅ Self-review checklist: ALL PASSED

🎯 CRITÉRIOS DE PARADA:
   Critério 1 (Success Rate): {✅ PASS / ❌ FAIL}
   Critério 2 (Regressão): {✅ PASS / ❌ FAIL}
   Critério 3 (Self-Review): {✅ PASS / ❌ FAIL}

➡️ DECISÃO AUTOMÁTICA:

{IF all 3 PASS}:
   🎉 SLICE PODE SER CONCLUÍDA!

   Todos 3 critérios atingidos. Você pode:
   1. Executar: /concluir-slice
      └─ Para finalizar e fazer merge
   2. Executar: /novo-incremento
      └─ Para adicionar mais melhorias (opcional)

{IF any FAIL}:
   ⏳ CONTINUAR COM PRÓXIMO INCREMENTO

   Critério(s) não atingido(s):
   {list failed criteria}

   Próximo passo: /novo-incremento

📝 FILES UPDATED:
   ✓ docs/slices/SLICE_{N}_TRACKER.md
     • Section 3.{N} metrics updated
     • Status: ✅ Finalizado
     • Decision recorded

🚀 PRÓXIMOS PASSOS:
   {IF all pass}:
      1. Review changes: git log --oneline -5
      2. Run /concluir-slice para finalizar
      3. Ou continue com /novo-incremento

   {IF continue}:
      1. Review metrics delta
      2. Run /novo-incremento para próximo incremento
      3. Implement suggested activities
```

## Error Handling

**If CI.py fails**:

- Display error output
- Ask: "Fix tests and try again? (y/n)"
- If no: Offer to manually set metrics

**If coverage < 70%**:

- Block with error message
- Suggest areas needing more tests
- Do NOT update incremento status
- User must add tests and re-run

**If regressions detected**:

- Display broken tests
- Ask: "Accept regressions? (y/n)"
- If no: git revert and start over
- If yes: Continue (with warning)

**If self-review fails**:

- Ask user to fix specific items
- Offer to re-run checklist
- Do NOT update incremento status

**If git issues**:

- Verify working directory clean
- Check branch is correct
- Offer to stash changes and continue

## Integration with Other Commands

**Workflow continuation**:

1. `/iniciar-slice` → Section 2 created
1. `/novo-incremento` → Section 3.1 created
1. [Developer codes Incremento 1]
1. `/finalizar-incremento` ← **YOU ARE HERE**
   - Validates all metrics
   - Decides: continue or conclude
1. Loop: goto 2 for Incremento 2, 3, etc
1. After all criteria met: `/concluir-slice` → Section 4 created, merge to main

## Configuration Requirements

### pytest-cov Setup

If not already present, project should have:

**pytest.ini or pyproject.toml**:

```ini
[tool:pytest]
addopts = --cov=. --cov-report=json --cov-report=html
testpaths = tests
```

Or in pyproject.toml:

```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=json --cov-report=html"
testpaths = ["tests"]
```

### Installation

If pytest-cov not installed:

```bash
uv add pytest-cov --dev
```

## Tips for Best Results

1. **Run frequently**: Don't wait until end to check coverage
1. **TDD approach**: Write tests before code
1. **Check regressions**: Ensure no existing tests break
1. **Review code**: Self-review checklist is important
1. **Keep commits atomic**: 1 increment = 1-3 commits
1. **Update tracker**: Keep Section 3.N up to date
