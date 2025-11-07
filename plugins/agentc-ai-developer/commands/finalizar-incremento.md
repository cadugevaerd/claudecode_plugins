---
description: Finalize current increment with metrics validation, regression detection, and automatic decision on next steps
allowed-tools: Read, Bash, Write, Grep, AskUserQuestion
argument-hint: ''
model: claude-sonnet-4-5
---

# Finalizar Incremento - Complete Increment Validation Loop

Finalize the current increment by validating metrics, checking for regressions, and automatically determining whether to continue or conclude the slice.

## Preconditions

Verify before starting:

1. **SLICE_N_TRACKER.md exists** - Slice must be initialized
1. **Section 3 (INCREMENTOS) exists** - Must have created incremento with `/novo-incremento`
1. **Incremento N exists with status "Em Progresso"** - Current increment active
1. **At least one commit since incremento start** - Code changes made (validates implementation)
1. **Git working directory is clean** - No uncommitted changes
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

### Step 3: Validate Regressions

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

### Step 4: Automatic Code Quality Check

Perform automated validation of implementation quality:

1. **Verify Implementation Exists**:

   - Execute: `git diff {base_commit} HEAD --stat`
   - Verify: ≥1 file modified with real changes
   - Confirm: Incremento size within ≤30 lines
   - Result: 🟢 Implementation found OR ❌ No changes detected

1. **Run Lint Check (if available)**:

   - Execute: `uv run CI.py --lint` (or `python CI.py --lint`)
   - Capture: Lint output with errors and warnings
   - Classify:
     - 🟢 No errors (warnings allowed)
     - 🟡 Minor issues (line length, unused imports)
     - ❌ Critical errors (syntax, undefined names)

1. **Generate Auto-Review Report**:

   Display results:

   ```
   #### Self-Review Automático

   ✅ Implementation Detected: {N} files modified, {lines} lines changed
   ✅ Code Quality: Lint {PASSED/WARNINGS/ERRORS}

   {If warnings}:
      ⚠️  Warning list (auto-generated from lint output)

   **Result**: {✅ APPROVED / 🟡 APPROVED_WITH_WARNINGS / ❌ NEEDS_REVIEW}
   ```

**Note**: Comprehensive code review (testing quality, component isolation, breaking changes) deferred to `/concluir-slice` at slice completion level.

### Step 5: Apply Stopping Criteria

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

**Critério 3**: Code Quality OK (Automatic)?

```
Implementation detected: ✅ YES
Lint check: {PASSED / WARNINGS / ERRORS}
Result: {✅ PASS / 🟡 PASS_WITH_WARNINGS / ❌ FAIL}
```

**Note**: This is automatically validated in Step 4. User intervention only if critical errors detected.

### Step 6: Make Automatic Decision

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
- **Avg Latency**: {W}ms (delta: {W-baseline}ms)
- **Capturado em**: {ISO_TIMESTAMP}
```

### Add Validations Section:

```markdown
#### Validações
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
   Latency: {W}ms
   Timestamp: {ISO_TIMESTAMP}

✓ VALIDAÇÕES:
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

**If regressions detected**:

- Display broken tests
- Ask: "Accept regressions? (y/n)"
- If no: git revert and start over
- If yes: Continue (with warning)

**If lint check fails (critical errors)**:

- Display lint errors
- Ask: "Fix code quality issues and try again? (y/n)"
- If no: Do NOT update incremento status
- If yes: User fixes issues and re-runs `/finalizar-incremento`

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

## Exemplos

### Exemplo 1: Incremento bem-sucedido - todos critérios atingidos

```bash
/finalizar-incremento
```

**Cenário:**

- Incremento 1 implementado com sucesso
- Testes passando (12/12)
- Success rate acima do target (95% vs 85%)
- Sem regressões detectadas

**Resultado:**

```
✅ Incremento 1 Finalizado!

📊 MÉTRICAS CAPTURADAS:
   Success Rate: 95% (baseline: 80%, delta: +15%)
   Test Count: 12 tests (baseline: 10, delta: +2)
   Avg Latency: 145ms (baseline: 150ms, delta: -5ms)
   Timestamp: 2025-01-15T14:32:18Z

✓ VALIDAÇÕES:
   ✅ Regressão = 0: 0 detected
   ✅ Self-review checklist: ALL PASSED

🎯 CRITÉRIOS DE PARADA:
   Critério 1 (Success Rate): ✅ PASS (95% >= 85%)
   Critério 2 (Regressão): ✅ PASS (0 regressions)
   Critério 3 (Self-Review): ✅ PASS

➡️ DECISÃO AUTOMÁTICA:
   🎉 SLICE PODE SER CONCLUÍDA!

   Todos 3 critérios atingidos. Você pode:
   1. Executar: /concluir-slice
      └─ Para finalizar e fazer merge
   2. Executar: /novo-incremento
      └─ Para adicionar mais melhorias (opcional)

📝 FILES UPDATED:
   ✓ docs/slices/SLICE_1_TRACKER.md
     • Section 3.1 metrics updated
     • Status: ✅ Finalizado
     • Decision recorded

🚀 PRÓXIMOS PASSOS:
   1. Review changes: git log --oneline -5
   2. Run /concluir-slice para finalizar
   3. Ou continue com /novo-incremento
```

______________________________________________________________________

### Exemplo 2: Incremento que requer continuação - success rate abaixo do target

```bash
/finalizar-incremento
```

**Cenário:**

- Incremento 1 implementado
- Testes passando (11/11)
- Success rate abaixo do target (72% vs 85%)
- Sem regressões detectadas

**Resultado:**

```
✅ Incremento 1 Finalizado!

📊 MÉTRICAS CAPTURADAS:
   Success Rate: 72% (baseline: 70%, delta: +2%)
   Test Count: 11 tests (baseline: 10, delta: +1)
   Avg Latency: 148ms
   Timestamp: 2025-01-15T10:15:42Z

✓ VALIDAÇÕES:
   ✅ Regressão = 0: 0 detected
   ✅ Self-review checklist: ALL PASSED

🎯 CRITÉRIOS DE PARADA:
   Critério 1 (Success Rate): ❌ FAIL (72% < 85%)
   Critério 2 (Regressão): ✅ PASS
   Critério 3 (Self-Review): ✅ PASS

➡️ DECISÃO AUTOMÁTICA:
   ⏳ CONTINUAR COM PRÓXIMO INCREMENTO

   Critério(s) não atingido(s):
   ❌ Success rate: 72% < 85% (faltam 13%)

   Próximo passo: /novo-incremento

📝 FILES UPDATED:
   ✓ docs/slices/SLICE_1_TRACKER.md
     • Section 3.1 metrics updated
     • Status: ✅ Finalizado
     • Decision: CONTINUAR

🚀 PRÓXIMOS PASSOS:
   1. Review metrics delta
   2. Run /novo-incremento para próximo incremento
   3. Focus: Improve success rate by 13%
```

______________________________________________________________________

### Exemplo 3: Incremento com regressões detectadas

```bash
/finalizar-incremento
```

**Cenário:**

- Incremento 2 implementado
- 2 testes quebrados (8/10 passando)
- Success rate OK (88% >= 85%)

**Resultado:**

```
⚠️ Incremento 2 - Regressões Detectadas!

📊 MÉTRICAS CAPTURADAS:
   Success Rate: 88% (baseline: 80%, delta: +8%)
   Test Count: 10 tests (baseline: 12, delta: -2)
   Avg Latency: 142ms
   Timestamp: 2025-01-15T16:45:30Z

✓ VALIDAÇÕES:
   ❌ Regressão = 2: 2 tests removed/broken
      • test_user_authentication_flow
      • test_data_validation_edge_case
   ⚠️ Self-review: NEEDS ATTENTION

🎯 CRITÉRIOS DE PARADA:
   Critério 1 (Success Rate): ✅ PASS (88% >= 85%)
   Critério 2 (Regressão): ❌ FAIL (2 regressions)
   Critério 3 (Self-Review): ❌ FAIL

➡️ DECISÃO AUTOMÁTICA:
   ⏳ CONTINUAR COM PRÓXIMO INCREMENTO

   Critério(s) não atingido(s):
   ❌ Regressão: 2 testes quebrados
   ❌ Self-review: Testes removidos sem justificativa

❓ AÇÃO REQUERIDA:
   Some tests were removed. Continue anyway? (y/n)

   Recomendação: Restaurar testes ou justificar remoção
```

______________________________________________________________________

## Tips for Best Results

1. **Validate early and often**: Check metrics and regressions frequently
1. **TDD approach**: Write tests before code
1. **Check regressions**: Ensure no existing tests break
1. **Review code**: Self-review checklist is important
1. **Keep commits atomic**: 1 increment = 1-3 commits
1. **Update tracker**: Keep Section 3.N up to date
