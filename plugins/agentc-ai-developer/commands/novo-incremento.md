---
description: Create AI-suggested increment from pending acceptance criteria
allowed-tools: Read, Grep, Bash, Write, AskUserQuestion
argument-hint: '[auto|interactive]'
---

# Novo Incremento - Start Incremental Development Loop

Automatically analyze current slice progress, suggest next increment based on pending acceptance criteria and code state, and create Section 3 tracking in SLICE_TRACKER.md.

## Preconditions

Verify before starting:

1. **SLICE_N_TRACKER.md exists** - Run `/iniciar-slice` first if missing
1. **Section 2 (DESENVOLVIMENTO) exists** - Slice must be initialized
1. **Section 3 (INCREMENTOS) exists or will be created** - For first increment
1. **At least one acceptance criterion is unchecked** - Something to work on
1. **Git branch is active** - Currently on slice branch (slice-N-\*)
1. **Last increment (if any) was finalized** - Previous increment completed successfully

If any precondition fails: Stop and guide user to complete prerequisites.

## Analysis Algorithm - AI-Suggested Increment

### Step 1: Load Current State

1. **Read SLICE_TRACKER.md**:

   - Extract Section 1 (Planejamento):
     - Acceptance criteria checklist
     - Success rate target
     - Reversibility requirements
   - Extract Section 2 (Desenvolvimento):
     - Baseline metrics
     - Git branch name
   - Check if Section 3 exists
     - If yes: Count existing increments (N-1)
     - If no: This will be Incremento 1

1. **Analyze git state**:

   - Get last N commits (last 5-10)
   - Extract files modified recently
   - Determine current code direction

1. **Extract pending criteria**:

   - Parse acceptance criteria checklist
   - Identify unchecked items
   - Order by dependency (prerequisites first)

### Step 2: Analyze Code Context

1. **Get recent changes**:

   - Execute: `git log -10 --oneline --name-status`
   - Extract: Modified files, commit patterns

1. **Quick code scan**:

   - For each modified file in last 3 commits:
     - Count lines changed (should be \<= 30 per increment)
     - Identify patterns (new functions, tests, refactoring)
     - Note any files that are getting large

1. **Estimate progress**:

   - How many criteria already met?
   - What's blocking next steps?
   - What's the natural next step?

### Step 3: Generate Increment Suggestion

Based on analysis, suggest next increment with:

**Increment Metadata**:

- Suggested title (descriptive, max 8 words)
- Estimated duration: 15-20 min
- Estimated lines: \<= 30
- Related acceptance criteria (which ones it addresses)

**Activity Suggestions** (AI-generated):

- 3-5 specific, actionable tasks
- Each task should be atomic and testable
- Include "add tests" as explicit activity
- Include "verify no regressions" as final activity

**Success Metrics**:

- Expected success_rate delta: +X%
- Expected test count delta: +M tests
- Expected coverage contribution

### Step 4: Display Suggestion

Display to user in this format:

```
🤖 Analyzing Slice {N} Progress...

📊 Current State:
   ✓ Acceptance Criteria: X of Y met
   ✓ Success Rate Baseline: {X}%
   ✓ Incrementos Completed: {N-1}
   ✓ Files Modified: {list}

💡 Next Increment Suggested:

   📌 Incremento {N}: {Suggested Title}
   ⏱️  Duration: 15-20 min
   📏 Estimated Lines: ≤30 lines
   🎯 Criteria Addressed: Criterion X, Criterion Y

   #### Activities Suggested:
   1. {Activity 1}
   2. {Activity 2}
   3. {Activity 3}
   4. Add/update tests for above
   5. Verify no regressions (run CI.py)

   🔍 Rationale:
      {Explain why this increment is suggested based on current state}

{In interactive mode}:
   Aceitar esta sugestão? (y/n)
   ou digitar alterações: [open for user input]

{In auto mode}:
   [Automatically accept and proceed]
```

## Update SLICE_TRACKER.md - Section 3

After suggestion accepted (or confirmed in interactive mode):

### Step 1: Create or append to Section 3

If Section 3 doesn't exist, create it after Section 2:

```markdown
## Incrementos (Section 3)

```

### Step 2: Add Incremento N entry

Add new increment with this template:

```markdown
### Incremento {N}: {Title}

- **Status**: ➡️ Em Progresso
- **Iniciado em**: {ISO_TIMESTAMP}
- **Duração Estimada**: 15-20 min
- **Linhas Estimadas**: ≤30 linhas

#### Atividades Sugeridas
- [ ] Atividade 1 (AI-generated)
- [ ] Atividade 2 (AI-generated)
- [ ] Atividade 3 (AI-generated)
- [ ] Adicionar/atualizar testes
- [ ] Validar regressões (rodar CI.py)

#### Critérios de Aceitação Relacionados
- [ ] Criterion X (from Section 1)
- [ ] Criterion Y (from Section 1)

#### Métricas Esperadas
- **Success Rate Delta**: +X%
- **Test Count Delta**: +M testes
- **Coverage Contribution**: +Z%

#### Desenvolvimento
- **Commit Base**: {current_commit_hash}
- **Arquivos para Modificar**: [list suggested]
- **Início**: {ISO_TIMESTAMP}
- **Fim**: [to be filled by /finalizar-incremento]
```

### Step 3: Update BACKLOG.md

If BACKLOG.md exists, update increment entry if needed:

1. Find slice in BACKLOG.md
1. Update if needed: note that incrementos have started
1. Keep slice status as: `➡️ Em Progresso`

### Step 4: Display confirmation

```
✅ Incremento {N} criado!

📝 Updates:
   • Section 3 added to SLICE_TRACKER.md
   • Incremento {N}: {Title} initialized
   • Activities checklist created
   • Timestamp recorded: {ISO_TIMESTAMP}

🚀 Next Steps:
   1. Follow the suggested activities checklist
   2. Keep changes <= 30 lines total
   3. Add tests as you code (TDD)
   4. When ready, run: /finalizar-incremento
   5. See SLICE_TRACKER.md Section 3.{N} for details

💡 Tip:
   Review the "Atividades Sugeridas" checklist
   Check them off as you complete each one
```

## Execution Modes

### Interactive Mode (default)

When no argument or `interactive` specified:

1. Perform analysis
1. Display increment suggestion
1. Ask: "Aceitar esta sugestão? (y/n)"
1. If yes: Create Section 3.N and confirm
1. If no: Offer to modify suggestion or request different approach
1. User can edit suggestion before accepting

### Auto Mode

When argument is `auto`:

1. Perform analysis
1. Skip user confirmation
1. Automatically accept suggestion
1. Create Section 3.N
1. Display summary with next steps

## Error Handling

**If preconditions not met**:

- Stop and list missing prerequisites
- Guide user to complete them (e.g., "Run `/iniciar-slice` first")

**If no acceptance criteria pending**:

- Check: "All acceptance criteria already met?"
- Suggest: "Run `/concluir-slice` to finalize this slice"

**If git branch not found**:

- Verify: "On slice branch? Run: `git branch --show-current`"
- Suggest: "Switch to slice branch first"

**If analysis fails**:

- Fall back to interactive mode
- Ask user to manually describe next increment
- Validate against increment criteria (30 lines, 15-20 min, etc)

## Increment Validation

Before creating incremento, validate:

- [ ] ≤30 lines estimated
- [ ] 15-20 minutes estimated
- [ ] Addresses at least 1 acceptance criterion
- [ ] Independent and testable
- [ ] Reversible with git revert
- [ ] Includes test task

If validation fails: Ask user to adjust or accept anyway with warning.

## Integration with Other Commands

**Workflow continuation**:

1. `/iniciar-slice` → Section 2 created
1. `/novo-incremento` ← **YOU ARE HERE**
   - Creates Incremento 1 in Section 3
   - Guides development loop
1. [Developer codes the increment]
1. `/finalizar-incremento` → Validates + updates status
1. Loop back to `/novo-incremento` for next increment
1. After slice complete: `/concluir-slice`

## ✅ Critérios de Sucesso

Após executar `/novo-incremento`, verifique:

**Análise e Sugestão**:

- [ ] SLICE_TRACKER.md foi lido e analisado corretamente
- [ ] Estado atual (acceptance criteria, incrementos passados) identificado
- [ ] Git log analisado (últimos commits e arquivos modificados)
- [ ] Critérios pendentes identificados e priorizados
- [ ] Sugestão de incremento gerada com título, duração e atividades

**Incremento Criado**:

- [ ] Section 3 existe ou foi criada em SLICE_TRACKER.md
- [ ] Incremento N adicionado com status "➡️ Em Progresso"
- [ ] Timestamp de início registrado (ISO format)
- [ ] Duração estimada: 15-20 min
- [ ] Linhas estimadas: ≤30 linhas
- [ ] Checklist de atividades sugeridas criado (3-5 + testes + CI)
- [ ] Critérios de aceitação relacionados listados
- [ ] Métricas esperadas definidas (success_rate, test_count, coverage)
- [ ] Commit base registrado (hash atual)

**Validação**:

- [ ] Incremento validado contra critérios (≤30 linhas, 15-20 min)
- [ ] Incremento endereça pelo menos 1 acceptance criterion
- [ ] Incremento é independente e testável
- [ ] Incremento é reversível (git revert)
- [ ] Incremento inclui task de testes

**Confirmação ao Usuário**:

- [ ] Mensagem de sucesso exibida com resumo das mudanças
- [ ] Next steps apresentados claramente
- [ ] Path para SLICE_TRACKER.md Section 3.N indicado

## Tips for Best Results

1. **Keep it small**: Enforce \<= 30 lines rule
1. **Focus on tests**: Always include testing in activities
1. **Git frequently**: Each increment = 1 commit
1. **Check criteria**: Focus on unchecked acceptance criteria
1. **Reversibility**: Ensure each increment can be reverted
