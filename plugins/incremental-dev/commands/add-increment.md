---
description: Adicionar próxima funcionalidade incremental ao código existente seguindo YAGNI
allowed-tools: Read, Write, Edit, Bash(git:*)
---

# Add Increment

Adiciona a próxima funcionalidade incremental ao código existente, garantindo que apenas o necessário seja implementado (YAGNI).

## Como usar

````bash
/add-increment "descrição da funcionalidade"

```text

## Pré-requisitos

Sempre validar ANTES de começar:

1. **PRD existe?** `test -f docs/PRD.md || test -f PRD.md`
2. **Git limpo?** `git status --porcelain` (sem mudanças)
3. **MVP definido?** Deve estar no PRD
4. **Código anterior funciona?** Testar incremento anterior

Se algum pré-requisito falhar, sugira:
- PRD: `/setup-project-incremental`
- Git sujo: Commitar primeiro
- MVP indefinido: `/prd-update planejamento`

## Processo

1. **Validar pré-requisitos** → STOP se falhar
2. **Analisar estado atual** → Listar funcionalidades existentes
3. **Definir incremento MÍNIMO**:
   - ⏱️ 30 minutos a 2 horas de trabalho
   - 📁 Modificar 1-3 arquivos máximo
   - 📝 20-100 linhas de código novo
   - 🧪 1-3 testes novos

4. **Questionar necessidade** → "É realmente necessário AGORA?"
5. **Validar impacto** → Quais arquivos, testes necessários
6. **Implementar** → Código simples, sem abstrações prematuras
7. **Testar** → Funcionalidade funciona + código anterior intacto
8. **Registrar no PRD** (opcional) → `/prd-update incremento`
9. **Commit** → Mudança do incremento

## ⚠️ Detectar Incremento Grande Demais

Se parecer grande:
- 5+ arquivos a modificar
- 200+ linhas de código
- Múltiplas features

→ **Quebrar em incrementos menores**

Exemplo:

```text

❌ GRANDE: "Adicionar autenticação OAuth com JWT e RBAC"
✅ PEQUENO: "Adicionar autenticação com usuário hardcoded"
✅ DEPOIS: "Gerar JWT tokens"
✅ DEPOIS: "Implementar RBAC"

```text

## Regra dos 3 (Para Refatoração)

- **1 caso**: Deixar código inline
- **2 casos**: Duplication OK, deixar como está
- **3 casos**: AGORA abstrair padrão

Não refatore durante incremento! Use `/refactor-now` depois.

## ✅ Checklist Pós-Incremento

- [ ] Código compilou/executou
- [ ] Funcionalidade funciona
- [ ] Código anterior continua funcionando
- [ ] Testes passam
- [ ] Pronto para commit

## Próximos passos

Após implementar com sucesso:

```bash
/prd-update incremento    # Registrar no PRD (opcional)
/commit                   # Fazer commit
/add-increment "próx"     # Próximo incremento OU
/refactor-now            # Refatorar se padrão emergiu

```text

**Princípios**:
- Mínimo necessário
- Simples > Elegância
- Funcionar > Padrões
- Agora > Futuro
````
