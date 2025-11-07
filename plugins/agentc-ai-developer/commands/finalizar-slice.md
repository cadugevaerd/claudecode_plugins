---
description: Complete slice validation with success rate verification, regression detection, and automatic BACKLOG.md update
allowed-tools: Read, Bash, Write, Edit, Grep, AskUserQuestion
argument-hint: ''
model: claude-sonnet-4-5
---

# Finalizar Slice - Complete Slice Validation and Closure

Finalize the current slice by validating success criteria, checking regressions, and updating project documentation. Ensures slice meets all quality gates before marking as complete.

## 🎯 Objetivo

Validar e finalizar slice atual garantindo que:

- ✅ Success Rate atingiu critério definido (Gate de sucesso)
- ✅ Regressão = 0 (nenhum teste antigo quebrou)
- ✅ CI.py validações passaram (se script existe)
- ✅ SLICE_N_TRACKER.md finalizado com métricas
- ✅ BACKLOG.md atualizado com status `✅ Concluído`

**Resultado esperado**: Slice validada, documentada e marcada como concluída no backlog.

## ⚙️ Preconditions

Verify before starting:

1. **SLICE_N_TRACKER.md exists** - Slice deve ter sido inicializada via `/iniciar-slice`
1. **At least one increment completed** - `/novo-incremento` e `/finalizar-incremento` executados
1. **Last increment status is "✅ Finalizado"** - Último incremento deve estar completo
1. **Git working directory is clean** - Nenhuma mudança uncommitted
1. **On slice branch** - Branch deve ser `slice-{N}-*`

If any precondition fails: Stop and guide user to complete prerequisites.

## 🔍 Validation Pipeline

### Step 1: Verify Slice State

1. **Identify active slice**:

   - Get current branch: `git branch --show-current`
   - Extract slice number from branch name (e.g., `slice-3-*` → N=3)
   - Verify SLICE_N_TRACKER.md exists

1. **Verify last increment**:

   - Read SLICE_N_TRACKER.md Section 3 (INCREMENTOS)
   - Find latest `### Incremento {M}:`
   - Verify status: `- **Status**: ✅ Finalizado`
   - If not finalized: Block with "Complete current increment with /finalizar-incremento first"

1. **Verify git state**:

   - Run: `git status --porcelain`
   - If any uncommitted: Block with "Commit your changes first"

### Step 2: Execute CI.py Validation (If Exists)

**If CI.py exists in project root**:

1. **Run full validation**:

   - Execute: `uv run CI.py` (or `python CI.py`)
   - Capture: success_rate, test_count, exit_code
   - Display results

1. **Extract final metrics**:

   ```
   Final Validation Results:
   - Success Rate: {X}%
   - Test Count: {N} tests
   - Exit Code: {code}
   - Timestamp: {ISO_TIMESTAMP}
   ```

**If CI.py does NOT exist**:

1. Display: "⚠️ CI.py not found. Manual validation required."
1. Ask user: "Run pytest manually for validation? (y/n)"
1. If yes: Execute `pytest --tb=short -v`
1. Extract success rate from pytest output

### Step 3: Validate Success Criteria

Apply the 3 stopping criteria from `/finalizar-incremento`:

**Critério 1**: Success rate >= target?

```
Target (from Section 1): {X}%
Current (from CI.py): {Y}%
Result: {Y >= X ? ✅ PASS : ❌ FAIL}
```

**Critério 2**: Regressão = 0?

1. Read baseline test_count from Section 2 (DESENVOLVIMENTO)
1. Compare with current test_count
1. If current < baseline: ❌ FAIL (tests removed)
1. If any test FAILED: ❌ FAIL (tests broken)
1. Else: ✅ PASS

```
Baseline Tests: {baseline_count}
Current Tests: {current_count}
Result: {✅ PASS / ❌ FAIL}
```

**Critério 3**: All acceptance criteria met?

1. Read Section 1 (PLANEJAMENTO) → Critérios de Aceitação
1. Count checkboxes: `- [ ]` (pending) vs `- [x]` (completed)
1. If any unchecked: ❌ FAIL
1. Else: ✅ PASS

```
Acceptance Criteria: {completed} / {total}
Result: {✅ PASS / ❌ FAIL}
```

### Step 4: Apply Decision Logic

Based on 3 criteria:

**IF all 3 are PASS**:

```
🎉 TODOS 3 CRITÉRIOS ATINGIDOS!

Slice pode ser CONCLUÍDA:
  ✅ Success rate: {Y}% >= {X}%
  ✅ Regressão = 0
  ✅ Acceptance criteria: All met

Status: Pronto para merge
```

**IF any 1+ is FAIL**:

```
⚠️ CRITÉRIOS NÃO ATINGIDOS

Critério(s) faltando:
  {list failed criteria with details}

❌ BLOQUEADO: Slice não pode ser finalizada

Ação requerida: Criar novo incremento com /novo-incremento
```

If FAIL: Stop execution and display blockers. Do NOT finalize slice.

## 📝 Update SLICE_TRACKER.md - Section 4 (FINALIZAÇÃO)

**Only if all 3 criteria PASS**, create Section 4:

1. **Locate insertion point**:

   - Find last `### Incremento {M}:` section
   - Insert Section 4 after all incrementos

1. **Create Section 4 with this template**:

```markdown
## Finalização (Section 4)

### Status Final
- **Status**: ✅ Concluído
- **Finalizado em**: {ISO_TIMESTAMP}
- **Duração Total**: {duration from Section 2 to now}

### Métricas Finais
- **Success Rate Final**: {Y}% (baseline: {baseline}%, delta: +{delta}%)
- **Test Count Final**: {N} tests (baseline: {baseline_tests}, delta: +{delta_tests})
- **Avg Latency Final**: {Z}ms
- **Capturado em**: {ISO_TIMESTAMP}

### Validação de Critérios
- ✅ **Critério 1** (Success Rate): {Y}% >= {X}% (PASS)
- ✅ **Critério 2** (Regressão): 0 regressions detected (PASS)
- ✅ **Critério 3** (Acceptance Criteria): {total}/{total} met (PASS)

### Commits Summary
- **Base Commit**: {from Section 2}
- **Final Commit**: {current HEAD hash}
- **Total Commits**: {count}
- **Incrementos Completed**: {M}

### Rollback Plan (Documented)
{Copy from Section 1 → Reversibilidade}

### Notes
[Developer notes about implementation, challenges, learnings]
```

1. **Update Metadata section**:

   - Find: `- **Status**: ➡️ Em Progresso`
   - Replace: `- **Status**: ✅ Concluído`
   - Update: `- **Finalizado em**: {ISO_TIMESTAMP}`

## 📋 Update BACKLOG.md

After SLICE_TRACKER.md updated:

1. **Locate slice in BACKLOG.md**:

   - Find line: `### {N}.` (slice number from branch)

1. **Update status**:

   - Find: `- **Status**: ➡️ Em Progresso`
   - Replace: `- **Status**: ✅ Concluído`

1. **Add completion timestamp**:

   - Add field: `- **Finalizado em**: {ISO_TIMESTAMP}`
   - Place after Status field

1. **Add final metrics field**:

   - Add field: `- **Success Rate Final**: {Y}%`
   - Place after Finalizado em

1. **Verify update**:

   - Display confirmation with updated section

## 🔄 Git Workflow Integration

After all documentation updated:

1. **Display next steps**:

```
✅ Slice {N} Finalizada com Sucesso!

📝 FILES UPDATED:
   ✓ docs/slices/SLICE_{N}_TRACKER.md (Section 4 added)
   ✓ docs/BACKLOG.md (Status: ✅ Concluído)

🌿 GIT WORKFLOW:
   Current Branch: slice-{N}-{title}
   Ready for: Merge to main

🚀 PRÓXIMOS PASSOS:
   1. Review changes: git log --oneline
   2. Merge to main:
      git checkout main
      git merge slice-{N}-{title}
      git push origin main
   3. Delete branch (optional):
      git branch -d slice-{N}-{title}
   4. Start next slice: /iniciar-slice
```

1. **Ask user for automatic merge** (optional):

   - Ask: "Merge slice branch to main automatically? (y/n)"
   - If yes: Execute merge workflow
   - If no: Display manual merge instructions

## 📊 Error Handling

**If CI.py fails**:

- Display error output
- Ask: "CI.py failed. Accept anyway? (y/n)"
- If no: Exit without finalizing
- If yes: Continue with warning

**If criteria not met**:

- Display which criteria failed
- Display specific blockers
- Suggest: "Run /novo-incremento to address gaps"
- Exit without finalizing

**If git issues**:

- Verify working directory clean
- Check branch is slice branch
- Offer to stash changes

**If acceptance criteria unchecked**:

- Display unchecked criteria
- Ask: "Mark criteria as met manually? (y/n)"
- If yes: Update SLICE_TRACKER.md checkboxes
- If no: Exit without finalizing

## 🔗 Integration with Other Commands

**Workflow continuation**:

1. `/iniciar-slice` → Section 2 created, baseline captured
1. `/novo-incremento` → Section 3.1 created
1. [Developer codes Incremento 1]
1. `/finalizar-incremento` → Incremento 1 validated
1. Loop: Steps 2-4 for Incremento 2, 3, etc.
1. `/finalizar-slice` ← **YOU ARE HERE**
   - Validates all criteria
   - Creates Section 4
   - Updates BACKLOG.md
   - Prepares for merge
1. Git merge → Slice integrated to main
1. `/iniciar-slice` → Start next slice

## 📝 Exemplos

### Exemplo 1: Slice bem-sucedida - todos critérios atingidos

```bash
/finalizar-slice
```

**Cenário:**

- Slice 1 com 3 incrementos completos
- Success rate: 92% (target: 85%)
- Regressão: 0 (15 tests, todos passando)
- Acceptance criteria: 3/3 met

**Resultado:**

```
🎉 TODOS 3 CRITÉRIOS ATINGIDOS!

Slice pode ser CONCLUÍDA:
  ✅ Success rate: 92% >= 85%
  ✅ Regressão = 0 (15/15 tests passing)
  ✅ Acceptance criteria: 3/3 met

📊 MÉTRICAS FINAIS:
   Success Rate: 92% (baseline: 70%, delta: +22%)
   Test Count: 15 tests (baseline: 10, delta: +5)
   Avg Latency: 138ms

✅ Slice 1 Finalizada com Sucesso!

📝 FILES UPDATED:
   ✓ docs/slices/SLICE_1_TRACKER.md (Section 4 added)
   ✓ docs/BACKLOG.md (Status: ✅ Concluído)

🚀 PRÓXIMOS PASSOS:
   1. Review changes: git log --oneline
   2. Merge to main: git checkout main && git merge slice-1-implement-core
   3. Start next slice: /iniciar-slice
```

______________________________________________________________________

### Exemplo 2: Slice com critérios não atingidos

```bash
/finalizar-slice
```

**Cenário:**

- Slice 2 com 2 incrementos completos
- Success rate: 78% (target: 85%)
- Regressão: 0
- Acceptance criteria: 2/3 met (1 pending)

**Resultado:**

```
⚠️ CRITÉRIOS NÃO ATINGIDOS

Critério(s) faltando:
  ❌ Success rate: 78% < 85% (faltam 7%)
  ❌ Acceptance criteria: 2/3 met
     • Pending: [ ] Edge case handling for null inputs

❌ BLOQUEADO: Slice não pode ser finalizada

Ação requerida:
  1. Criar novo incremento: /novo-incremento
  2. Focus: Increase success rate by 7%
  3. Complete pending acceptance criterion
```

______________________________________________________________________

### Exemplo 3: Slice com regressões detectadas

```bash
/finalizar-slice
```

**Cenário:**

- Slice 3 com 1 incremento completo
- Success rate: 88% (target: 85%)
- Regressão: 2 tests broken
- Acceptance criteria: 3/3 met

**Resultado:**

```
⚠️ CRITÉRIOS NÃO ATINGIDOS

Critério(s) faltando:
  ❌ Regressão = 2 (tests broken)
     • test_user_authentication_flow
     • test_data_validation_edge_case

❌ BLOQUEADO: Slice não pode ser finalizada

Ação requerida:
  1. Fix broken tests
  2. Run: /novo-incremento (create fix increment)
  3. Ensure all tests pass before finalizing
```

## ✅ Critérios de Sucesso

Validação de que o comando `/finalizar-slice` foi executado corretamente:

- [ ] Preconditions verificadas (SLICE_TRACKER.md, último incremento finalizado, git clean)
- [ ] CI.py executado (se existe) ou pytest manual executado
- [ ] Success rate validado contra target (Gate 1)
- [ ] Regressão = 0 verificado (Gate 2)
- [ ] Acceptance criteria checados (Gate 3)
- [ ] Decisão automática aplicada (PASS all 3 → finalize / FAIL any → block)
- [ ] SLICE_TRACKER.md Section 4 criada (apenas se PASS)
- [ ] BACKLOG.md atualizado com status `✅ Concluído` (apenas se PASS)
- [ ] Próximos passos apresentados (merge to main ou /novo-incremento)
- [ ] Se FAIL: Blockers identificados e sugestões fornecidas

## 💡 Tips for Best Results

1. **Complete all increments first**: Ensure `/finalizar-incremento` executed for all
1. **Check acceptance criteria early**: Review Section 1 criteria before finalizing
1. **Run CI.py frequently**: Validate metrics throughout development
1. **Keep git clean**: Commit all changes before finalizing
1. **Review metrics**: Ensure success rate meets target before running command
1. **Document learnings**: Add notes in Section 4 for future reference
