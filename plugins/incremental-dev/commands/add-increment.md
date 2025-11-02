---
description: Adicionar próxima funcionalidade incremental ao código existente seguindo YAGNI
---

# Add Increment

Este comando orienta a adição de uma ÚNICA funcionalidade incremental ao código existente, garantindo que apenas o necessário seja implementado.

## 🎯 Objetivo

Adicionar a próxima funcionalidade de forma MÍNIMA e INCREMENTAL, evitando antecipar requisitos futuros.

## ❓ When to Use This Command

Use `/add-increment` when you already have:
- ✅ Working MVP (minimum viable product)
- ✅ PRD defined with clear objectives
- ✅ Clean git status (no uncommitted changes)
- ✅ Previous increment tested and working

**DO NOT use** `/add-increment` when:
- ❌ Starting a new project → Use `/start-incremental` instead
- ❌ MVP not yet defined → Use `/prd-update planejamento` first
- ❌ Multiple features to add → Add one at a time
- ❌ Major refactoring needed → Use `/refactor-now` first

### 📊 Command Comparison

| Scenario | Use This Command |
|----------|------------------|
| **Starting new project** | `/start-incremental` - Define MVP and initial scope |
| **Adding next feature to working MVP** | `/add-increment` - Add one feature incrementally |
| **Refactoring when patterns emerge** | `/refactor-now` - Identify refactoring opportunities |
| **Reviewing over-engineering** | `/review-yagni` - Remove unnecessary complexity |

## 📋 How to Use

```bash
/add-increment "feature description"
```

**Examples**:
```bash
/add-increment "Add email validation"
/add-increment "Add retry logic when API fails"
/add-increment "Add logging to critical operations"
```

## 🔍 Processo de Execução

Quando este comando for executado, você DEVE:

### 0. Validate Prerequisites (ALWAYS RUN FIRST)

**CRITICAL**: Before starting increment, ALWAYS validate prerequisites:

```bash
# 1. Check if PRD exists
test -f docs/PRD.md || test -f PRD.md

# 2. Check git status (should be clean)
git status --porcelain

# 3. Check if MVP is defined in PRD
grep -q "MVP" docs/PRD.md || grep -q "MVP" PRD.md
```

**If PRD does NOT exist**:
```
❌ PRD NOT FOUND

Before adding increments, you need:
1. Create PRD: /setup-project-incremental
2. Define MVP: /prd-update planejamento
3. Then: /add-increment

STOP - Do not proceed without PRD
```

**If git status is NOT clean**:
```
⚠️  UNCOMMITTED CHANGES DETECTED

Files with changes:
[list modified files]

Recommendation:
1. Commit current work first
2. Clean working directory
3. Then: /add-increment

Continue anyway? (y/n)
```

**If MVP is NOT defined**:
```
⚠️  MVP NOT DEFINED IN PRD

PRD exists but MVP is not clearly defined.

Recommendation:
1. Define MVP: /prd-update planejamento
2. Document what IS and ISN'T in MVP
3. Then: /add-increment

Continue anyway? (y/n)
```

---

### 📏 Increment Sizing Guide

**Ideal increment size**:
- ⏱️ **Time**: 30 minutes to 2 hours of work
- 📁 **Files**: Modify 1-3 files maximum
- 📝 **Lines**: Add/change 20-100 lines of code
- 🧪 **Tests**: 1-3 new test cases

**If increment seems too large**:
```
⚠️  INCREMENT TOO LARGE DETECTED

Your increment seems to involve:
- 5+ files to modify
- 200+ lines of code
- Multiple features

Recommendation: Break down into smaller increments

Example:
❌ "Add authentication with OAuth, JWT, and role-based access"
✅ "Add basic authentication with hardcoded user"
✅ (Next) "Add JWT token generation"
✅ (Next) "Add role-based access control"

Continue with large increment anyway? (y/n)
```

---

### 1. Analisar Estado Atual

After validating prerequisites:

```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- Funcionalidades existentes: [listar]
- Arquivos principais: [listar]
- Complexidade atual: [simples/moderada/complexa]

📝 Novo Requisito: [descrição fornecida]

Analisando...
```

### 2. Definir Incremento Mínimo

Identificar a MENOR mudança possível:

```
✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] Mudança 1 (mínima e necessária)
- [ ] Mudança 2 (mínima e necessária)
- [ ] Mudança 3 (mínima e necessária)

Onde adicionar:
- Arquivo: [nome do arquivo]
- Função/Classe: [onde modificar]
- Linhas aproximadas: [contexto]

❌ NÃO ADICIONAR AGORA (YAGNI):
- Feature relacionada mas não pedida
- Validação excessiva
- Abstração prematura
- Tratamento de erros elaborado
- Configuração complexa
- Cache/otimização

💡 Princípio: Adicione APENAS o que foi pedido

Implementar este incremento? (s/n)
```

### 3. Questionar Necessidade

**SEMPRE perguntar**:
- "Esta funcionalidade é realmente necessária AGORA?"
- "Existe um caso de uso REAL para isso?"
- "O que acontece se não implementarmos isso agora?"

### 4. Validar Impacto

Avaliar impacto da mudança:

```
📊 IMPACTO DO INCREMENTO:

Complexidade: [Baixa/Média/Alta]

Arquivos afetados:
- [arquivo1]: [tipo de mudança]
- [arquivo2]: [tipo de mudança]

Testes necessários:
- [ ] Teste 1 (caso básico)
- [ ] Teste 2 (edge case mínimo)

⚠️  Refatoração necessária? [SIM/NÃO]

Se SIM: Este é o momento de refatorar porque [padrão emergiu / duplicação clara / etc]
Se NÃO: Adicione de forma direta no código atual
```

## 📚 Exemplos Práticos

### Exemplo 1: Adicionar Validação de Email

**Estado atual**: Sistema processa emails básicos (MVP funcionando)

**Requisito**: "Adicionar validação de email"

**Resposta correta**:
```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- MVP funciona: processa emails
- Arquivo principal: email_processor.py
- Função: process_email(email: str)

📝 Novo Requisito: Validação de email

✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] Função validate_email(email: str) -> bool
- [ ] Validação básica (contém "@")
- [ ] Chamar antes de processar

Código:
def validate_email(email: str) -> bool:
    return "@" in email  # Validação mínima!

def process_email(email: str):
    if not validate_email(email):
        return "erro: email inválido"
    # resto do processamento...

❌ NÃO ADICIONAR AGORA:
- Regex complexo de validação
- Verificar domínio DNS
- Múltiplos tipos de validação
- Classe EmailValidator
- Sistema de erros customizados
- Logging de validações

💡 Validação mínima funciona. Adicionar complexidade APENAS quando necessário.

Implementar? (s/n)
```

### Exemplo 2: Adicionar Retry em LangGraph

**Estado atual**: API LangGraph com 1 node funcionando (MVP)

**Requisito**: "Adicionar retry quando der erro"

**Resposta correta**:
```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- LangGraph com 1 node: process_node
- API endpoint: POST /process
- Sem tratamento de erro

📝 Novo Requisito: Retry quando der erro

✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] Try/except no node
- [ ] Retry simples (1 tentativa)
- [ ] Retornar erro se falhar

Código:
def process_node(state):
    try:
        result = do_processing(state)
        return {"result": result}
    except Exception as e:
        # Retry UMA vez
        try:
            result = do_processing(state)
            return {"result": result}
        except:
            return {"result": "erro", "error": str(e)}

❌ NÃO ADICIONAR AGORA:
- Biblioteca de retry (tenacity, backoff)
- Retry exponencial
- Configuração de max_retries
- Logging estruturado
- Métricas de falhas
- Dead letter queue
- Circuit breaker

💡 Retry simples resolve. Adicionar complexidade APENAS quando padrão emergir.

Implementar? (s/n)
```

### Exemplo 3: Adicionar Logging

**Estado atual**: Sistema funciona sem logs

**Requisito**: "Adicionar logging"

**Resposta correta**:
```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- Sistema funciona sem logs
- Difícil debugar problemas

📝 Novo Requisito: Logging

✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] print() nos pontos críticos
- [ ] Logar entrada e saída

Código:
def process_email(email: str):
    print(f"Processing: {email}")  # Log simples!
    result = do_something(email)
    print(f"Result: {result}")
    return result

❌ NÃO ADICIONAR AGORA:
- Biblioteca logging configurada
- Múltiplos níveis (DEBUG, INFO, ERROR)
- Formatação estruturada (JSON)
- Rotação de logs
- Envio para serviço externo (Datadog, Sentry)
- Context managers
- Logging assíncrono

💡 print() funciona perfeitamente para começar. Trocar por logging quando necessário.

Implementar? (s/n)
```

## ⚠️ Detectar Over-Engineering no Incremento

> **📘 Complete Guide**: See `docs/YAGNI_REFERENCE.md` section "Detecting Over-Engineering During Increments" for comprehensive anti-patterns and examples.

### Quick Warning Signs:

**❌ Pattern 1**: Creating class for simple function → Use function instead
**❌ Pattern 2**: Adding complex configuration → Use simple constant
**❌ Pattern 3**: Creating premature abstraction → Use direct functions (wait for 3+ cases)

**For detailed code examples**, refer to `docs/YAGNI_REFERENCE.md`.

## 🎯 Estratégia de Incremento

### 1. Regra dos 3

> **📘 The Rule of 3**: Complete guide in `docs/YAGNI_REFERENCE.md`

Quick reference:
- **1 case**: Direct function
- **2 cases**: Two functions (duplication OK!)
- **3 cases**: NOW abstract (pattern emerged)

### 2. Add, Don't Modify (quando possível)
Prefira adicionar código novo a modificar existente:
- Menos risco de quebrar
- Fácil de reverter
- Padrão fica mais claro

### 3. Test After Each Increment
Após cada incremento:
```
✅ CHECKLIST PÓS-INCREMENTO:
- [ ] Código compilou/executou sem erro
- [ ] Funcionalidade funciona (teste manual)
- [ ] Código antigo ainda funciona
- [ ] Commit do incremento
```

## 🚀 Fluxo de Incremento

```
1. /add-increment "nova feature"
   ↓
2. Validate Prerequisites (PRD exists, git clean, MVP defined)
   ↓
3. Analisar estado atual
   ↓
4. Definir incremento MÍNIMO (30min-2h, 1-3 files)
   ↓
5. Questionar necessidade ("É necessário AGORA?")
   ↓
6. Implementar (código simples, sem abstrações)
   ↓
7. Testar incremento (functionality works)
   ↓
8. Register in PRD (/prd-update incremento) ← INTEGRATED STEP
   ↓
9. Commit (with learnings documented)
   ↓
10. Próximo incremento OU refatorar (se padrão emergiu)
```

**Key Change**: PRD update is now PART of the increment workflow, not an afterthought!

## 💡 Princípios do Incremento

> **📘 Full Guide**: See `docs/YAGNI_REFERENCE.md` section "Incremental Development Strategy"

Quick principles:
1. **One at a time** - Don't add multiple features together
2. **Simple first** - Direct code before abstractions
3. **Working > Perfect** - Working increment > "Beautiful" code
4. **Reversible** - Small increment is easy to revert
5. **Testable** - Small increment is easy to test

## 🔄 Quando Refatorar?

> **📘 When to Refactor**: Complete guide in `docs/YAGNI_REFERENCE.md`

**DO NOT refactor during increment** unless:
- ✅ Clear pattern emerged (3+ similar cases)
- ✅ Obvious duplication (exact copy-paste)
- ✅ Impossible to add increment without refactoring

**Use** `/refactor-now` after several increments, not during.

## 📄 Após Implementar Incremento

Ao completar implementação do incremento:

```
✅ INCREMENTO IMPLEMENTADO!

Deseja registrar este incremento no PRD? (s/n)
```

**Se SIM**:
```
Executando: /prd-update incremento

[Fluxo do comando /prd-update incremento]
```

**Se NÃO**:
```
💡 Lembrete: Você pode registrar depois com:
   /prd-update incremento
```

---

## ⚡ Lembre-se

- Incremento = MÍNIMO necessário
- Simplicidade > Elegância
- Funcionar > Padrões
- Agora > Futuro
- Adicione apenas o que foi PEDIDO
- Refatore depois, não durante
- **Registre aprendizados no PRD** após cada incremento