---
description: Validate acceptance criteria execution and suggest acceptance test creation
allowed-tools: Read, Write, Bash, Grep, AskUserQuestion
model: claude-sonnet-4-5
argument-hint: '[SLICE_ID]'
---

# Validate Acceptance Criteria

Validates that all acceptance criteria for a slice are passing by executing each criterion and suggesting acceptance test creation if all pass.

## 🎯 Objetivo

Executar validação manual/automatizada de critérios de aceitação de um slice para:

- ✅ Identificar qual slice validar (atual em progresso ou SLICE_ID fornecido)
- ✅ Ler critérios de aceitação do SLICE_TRACKER.md
- ✅ Executar cada critério de aceitação (manual ou automatizado)
- ✅ Registrar resultados (PASS/FAIL) para cada critério
- ✅ Se TODOS passarem: Sugerir criação de testes de aceitação automatizados
- ✅ Atualizar SLICE_TRACKER.md com status de validação

**Resultado esperado**: Relatório de validação com status de cada critério e recomendação sobre criar testes de aceitação.

## ⚙️ Preconditions

1. Verify `docs/BACKLOG.md` exists
1. Verify at least one slice exists with status `➡️ Em Progresso`
1. Verify corresponding `docs/slices/SLICE_{N}_TRACKER.md` exists
1. Verify SLICE_TRACKER.md has "Critérios de Aceitação" section populated

If missing: Stop and guide user to run `/iniciar-slice` first.

## 🔧 Instruções

### 1. **Identify Target Slice**

1.1 **If SLICE_ID provided**:
   - Use provided SLICE_ID (e.g., `1`, `2`, `3`)
   - Validate `docs/slices/SLICE_{SLICE_ID}_TRACKER.md` exists
   - If not exists: Display error and list available slices

1.2 **If NO SLICE_ID provided** (auto-detect):
   - Search `docs/BACKLOG.md` for slice with status `➡️ Em Progresso`
   - Extract slice number from matching increment
   - If multiple slices in progress: Ask user to select one
   - If no slice in progress: Display error and suggest `/iniciar-slice`

### 2. **Load Acceptance Criteria**

2.1 **Read SLICE_TRACKER.md**:
   - Open `docs/slices/SLICE_{N}_TRACKER.md`
   - Locate "Critérios de Aceitação" section
   - Extract all checklist items (format: `- [ ] {criterion}`)

2.2 **Parse Criteria**:
   - Count total criteria (should be 3 according to agentc-ai-developer workflow)
   - For each criterion, extract:
     - Criterion ID (1, 2, 3)
     - Criterion description (text after `- [ ]`)
     - Current status (checked `[x]` or unchecked `[ ]`)

2.3 **Validate Criteria Exist**:
   - If no criteria found: Display error
   - If criteria already all checked: Warn user (already validated?)
   - Continue regardless (re-validation allowed)

### 3. **Execute Each Criterion**

For each acceptance criterion, validate execution:

3.1 **Display Criterion**:
```text
📋 Critério {N}/3: {criterion_description}
```

3.2 **Determine Validation Method**:

- **Automated Validation** (if criterion is code-verifiable):
  - Examples: "Tests pass", "Build succeeds", "Lint passes", "Coverage > 80%"
  - Execute corresponding command (e.g., `pytest`, `npm run build`, `ruff check`)
  - Parse command output to determine PASS/FAIL
  - Show command output summary

- **Manual Validation** (if criterion requires human verification):
  - Examples: "UI renders correctly", "User can login", "Documentation updated"
  - Display criterion to user
  - Use `AskUserQuestion` tool to ask: "Does this criterion pass? (yes/no)"
  - Record user response as PASS/FAIL

3.3 **Record Result**:
   - ✅ PASS: Criterion validated successfully
   - ❌ FAIL: Criterion not met, requires fixes
   - ⏭️ SKIP: User chooses to skip this criterion (counts as incomplete)

### 4. **Generate Validation Report**

After validating all criteria, generate report:

4.1 **Calculate Summary**:
   - Total criteria: 3
   - Passed: X criteria ✅
   - Failed: Y criteria ❌
   - Skipped: Z criteria ⏭️
   - Validation rate: (X / 3) * 100%

4.2 **Display Report**:

```text
═══════════════════════════════════════════
📊 VALIDATION REPORT - Slice {N}
═══════════════════════════════════════════

Slice Name: {slice_title}
Total Criteria: 3

Results:
✅ Critério 1: {description} → PASS
❌ Critério 2: {description} → FAIL
✅ Critério 3: {description} → PASS

Summary:
- Passed: 2/3 (66%)
- Failed: 1/3 (33%)
- Skipped: 0/3 (0%)

Status: ⚠️ INCOMPLETE (not all criteria passing)

═══════════════════════════════════════════
```

### 5. **Decision Logic Based on Results**

5.1 **ALL Criteria PASS** (100% validation rate):

```text
🎉 Todos os critérios de aceitação passaram!

✅ Slice está pronto para conclusão

💡 Próximos Passos Recomendados:
1. 🧪 Criar testes de aceitação automatizados
   - Execute: /create-acceptance-tests docs/slices/SLICE_{N}_TRACKER.md
   - Isso gerará testes BDD/pytest baseados nos critérios validados

2. ✅ Concluir slice
   - Execute: /finalizar-slice {N}
   - Registra métricas finais e atualiza status para ✅ Concluído

Deseja criar testes de aceitação agora? (y/n)
```

If user accepts: Execute `/create-acceptance-tests` command with SLICE_TRACKER path

5.2 **SOME Criteria FAIL** (< 100%):

```text
⚠️ Alguns critérios ainda não passaram

❌ Critérios falhando:
- Critério 2: {description}

💡 Próximos Passos:
1. Corrigir implementação para atender critérios falhando
2. Re-executar validação: /validate-criterios-aceitacao {N}
3. Quando todos passarem, criar testes de aceitação

❌ NÃO é recomendado concluir slice com critérios falhando
```

5.3 **ALL Criteria SKIP** (0% validation attempted):

```text
⏭️ Nenhum critério foi validado

💡 Execute novamente sem pular critérios para validar slice corretamente
```

### 6. **Update SLICE_TRACKER.md**

6.1 **Update Acceptance Criteria Checkboxes**:
   - For each PASS criterion: Change `- [ ]` to `- [x]`
   - For FAIL/SKIP: Keep as `- [ ]` (unchecked)

6.2 **Add Validation Log Entry**:

In "Development Log" section, add:

```markdown
- `{ISO_TIMESTAMP}` - Validation executed: {X}/3 criteria passed
```

Example:
```markdown
- `2025-11-07T18:45:30` - Validation executed: 3/3 criteria passed ✅
```

6.3 **Add Validation Section** (if doesn't exist):

Create new section in SLICE_TRACKER.md:

```markdown
## Validação de Critérios

### Última Validação
- **Data**: {ISO_TIMESTAMP}
- **Resultado**: {X}/3 critérios passaram
- **Status**: ✅ COMPLETO / ⚠️ INCOMPLETO

### Detalhes
- ✅ Critério 1: {description} → PASS
- ❌ Critério 2: {description} → FAIL
- ✅ Critério 3: {description} → PASS
```

## 📊 Formato de Saída

### Caso 1: Todos Critérios Passam (100%)

```text
═══════════════════════════════════════════
📊 VALIDATION REPORT - Slice 1
═══════════════════════════════════════════

Slice Name: Implementar core classifier
Total Criteria: 3

Results:
✅ Critério 1: Classifier retorna predição válida → PASS
✅ Critério 2: Accuracy > 80% no dataset teste → PASS
✅ Critério 3: Testes unitários passam → PASS

Summary:
- Passed: 3/3 (100%)
- Failed: 0/3 (0%)
- Skipped: 0/3 (0%)

Status: ✅ COMPLETO

═══════════════════════════════════════════

🎉 Todos os critérios de aceitação passaram!

💡 Próximos Passos Recomendados:
1. 🧪 Criar testes de aceitação automatizados
2. ✅ Concluir slice com /finalizar-slice 1

Deseja criar testes de aceitação agora? (y/n)
> y

🚀 Executando /create-acceptance-tests docs/slices/SLICE_1_TRACKER.md...
```

### Caso 2: Alguns Critérios Falham

```text
═══════════════════════════════════════════
📊 VALIDATION REPORT - Slice 2
═══════════════════════════════════════════

Slice Name: Add edge case handling
Total Criteria: 3

Results:
✅ Critério 1: Edge cases identificados → PASS
❌ Critério 2: Testes de edge cases passam → FAIL
✅ Critério 3: Documentação atualizada → PASS

Summary:
- Passed: 2/3 (66%)
- Failed: 1/3 (33%)
- Skipped: 0/3 (0%)

Status: ⚠️ INCOMPLETO

═══════════════════════════════════════════

⚠️ Alguns critérios ainda não passaram

❌ Critérios falhando:
- Critério 2: Testes de edge cases passam

💡 Próximos Passos:
1. Corrigir testes falhando
2. Re-executar: /validate-criterios-aceitacao 2
3. Quando todos passarem, criar testes de aceitação

❌ NÃO concluir slice até todos critérios passarem
```

### Caso 3: Auto-detect Slice (sem SLICE_ID)

```text
🔍 Detectando slice atual...

✅ Slice encontrado: Slice 3 - Polish algorithm
📁 Tracker: docs/slices/SLICE_3_TRACKER.md

[... continua com validação normal ...]
```

## ✅ Critérios de Sucesso

Validação de que o comando `/validate-criterios-aceitacao` foi executado corretamente:

- [ ] Slice identificado corretamente (fornecido ou auto-detectado)
- [ ] SLICE_TRACKER.md localizado e lido com sucesso
- [ ] Critérios de aceitação extraídos (3 critérios esperados)
- [ ] Cada critério executado (automaticamente ou com input do usuário)
- [ ] Resultados registrados para cada critério (PASS/FAIL/SKIP)
- [ ] Relatório de validação gerado com summary
- [ ] Se 100% PASS: Sugestão de criar testes de aceitação apresentada
- [ ] Se < 100%: Orientação de corrigir e re-executar apresentada
- [ ] SLICE_TRACKER.md atualizado:
  - Checkboxes marcados para critérios PASS
  - Development Log com entrada de validação
  - Seção "Validação de Critérios" criada/atualizada
- [ ] Timestamp ISO 8601 registrado corretamente

## ❌ Anti-Patterns

### ❌ Erro 1: Validar slice sem estar em progresso

Não valide slices que não estão com status `➡️ Em Progresso`:

```bash
# ❌ Errado - Slice ainda em planejamento
/validate-criterios-aceitacao 5
# Slice 5 status: ⏳ Planejado (não iniciado ainda)

# ✅ Correto - Validar apenas slices em progresso
# Primeiro: /iniciar-slice 5
# Depois: /validate-criterios-aceitacao 5
```

**Por quê?** Slices não iniciados não têm código implementado para validar.

### ❌ Erro 2: Marcar critério como PASS sem executar validação

Não marque critérios como passando sem verificar:

```bash
# ❌ Errado - Usuário marca todos como PASS sem testar
Critério 1: Testes passam → PASS (sem executar pytest)
Critério 2: Coverage > 80% → PASS (sem verificar coverage)

# ✅ Correto - Executar validação real
Critério 1: Testes passam → PASS (executou: pytest --exitfirst)
Critério 2: Coverage > 80% → FAIL (executou: coverage report → 65%)
```

**Por quê?** Validação falsa leva a slice incompleto sendo marcado como concluído.

### ❌ Erro 3: Criar testes de aceitação com critérios falhando

Não crie testes de aceitação quando critérios ainda não passam:

```bash
# ❌ Errado - Criar testes com 66% validação
Passed: 2/3 (66%)
Deseja criar testes de aceitação? y
# Testes criados refletirão comportamento incorreto!

# ✅ Correto - Só criar testes quando 100% PASS
Passed: 3/3 (100%)
Deseja criar testes de aceitação? y
# Testes refletirão comportamento correto validado
```

**Por quê?** Testes de aceitação devem validar comportamento correto, não bugs.

### ❌ Erro 4: Ignorar falhas e concluir slice

Não conclua slice com critérios falhando:

```bash
# ❌ Errado - Concluir com 66% validação
Passed: 2/3 (66%)
/finalizar-slice 1
# Slice marcado como ✅ Concluído incorretamente

# ✅ Correto - Corrigir antes de concluir
Passed: 2/3 (66%)
# 1. Corrigir implementação
# 2. /validate-criterios-aceitacao 1 (re-validar)
# 3. Verificar 100% PASS
# 4. /finalizar-slice 1
```

**Por quê?** Slice "concluído" deve atender TODOS os critérios de aceitação.

### ❌ Erro 5: Validação manual sem documentar evidência

Ao validar manualmente, não confie apenas em memória:

```bash
# ❌ Errado - Validação manual sem evidência
Critério 1: UI renders correctly → PASS (usuário diz "sim" sem screenshot)

# ✅ Correto - Validação com evidência documentada
Critério 1: UI renders correctly → PASS
  - Evidência: Screenshot salvo em docs/validation/ui-render.png
  - Timestamp: 2025-11-07T18:30:00
  - Validador: Manual (user confirmation)
```

**Por quê?** Evidência permite revisão futura e auditoria de qualidade.

## 📝 Exemplo Completo

```bash
# Cenário: Validar slice atual em progresso
/validate-criterios-aceitacao

# Output:
🔍 Detectando slice atual...
✅ Slice encontrado: Slice 1 - Implementar core classifier
📁 Tracker: docs/slices/SLICE_1_TRACKER.md

📋 Critério 1/3: Classifier retorna predição válida
🤖 Automated validation detected: Running tests...
$ pytest tests/test_classifier.py::test_predict_valid
✅ PASS (tests/test_classifier.py::test_predict_valid passed)

📋 Critério 2/3: Accuracy > 80% no dataset teste
🤖 Automated validation detected: Checking accuracy...
$ python scripts/evaluate_accuracy.py
Accuracy: 85.3%
✅ PASS (Accuracy 85.3% > 80% threshold)

📋 Critério 3/3: Testes unitários passam
🤖 Automated validation detected: Running all tests...
$ pytest tests/
✅ PASS (18 tests passed, 0 failed)

═══════════════════════════════════════════
📊 VALIDATION REPORT - Slice 1
═══════════════════════════════════════════

Slice Name: Implementar core classifier
Total Criteria: 3

Results:
✅ Critério 1: Classifier retorna predição válida → PASS
✅ Critério 2: Accuracy > 80% no dataset teste → PASS
✅ Critério 3: Testes unitários passam → PASS

Summary:
- Passed: 3/3 (100%)
- Failed: 0/3 (0%)
- Skipped: 0/3 (0%)

Status: ✅ COMPLETO

═══════════════════════════════════════════

🎉 Todos os critérios de aceitação passaram!

✅ Slice está pronto para conclusão

💡 Próximos Passos Recomendados:
1. 🧪 Criar testes de aceitação automatizados
   - Execute: /create-acceptance-tests docs/slices/SLICE_1_TRACKER.md

2. ✅ Concluir slice
   - Execute: /finalizar-slice 1

Deseja criar testes de aceitação agora? (y/n)
> y

🚀 Executando /create-acceptance-tests docs/slices/SLICE_1_TRACKER.md...

[Testes de aceitação criados com sucesso]

✅ SLICE_TRACKER.md atualizado:
   - Critérios marcados como concluídos [x]
   - Validation log adicionado: 2025-11-07T18:45:30
   - Seção "Validação de Critérios" criada

💡 Execute /finalizar-slice 1 para concluir o slice
```

## 🔗 Integration with Agentc AI Developer Workflow

Este comando integra-se ao workflow incremental:

```text
1. /brief                          → Define agent scope
2. /setup-local-observability      → Configure environment
3. /backlog create                 → Create BACKLOG.md with slices
4. /analyze-slices validate        → Validate slices against S1.1 gates
5. /iniciar-slice                  → Start development (create tracker)
6. [Development]                   → Write code and tests
7. /validate-criterios-aceitacao   ← VALIDATE ACCEPTANCE CRITERIA HERE
8. /create-acceptance-tests        → Generate automated acceptance tests
9. /finalizar-slice                → Record completion metrics and close slice
```

**When to use:**
- After implementing functionality for a slice
- Before creating acceptance tests
- Before finalizing slice with `/finalizar-slice`
- To verify all acceptance criteria are met

**Output used by:**
- `/create-acceptance-tests` (uses validated criteria to generate tests)
- `/finalizar-slice` (verifies 100% validation before allowing completion)
