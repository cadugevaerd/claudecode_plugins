---
description: Identificar momento certo para refatorar código quando padrões emergem naturalmente
---

# Refactor Now

Identifica o **momento certo** para refatorar - nem muito cedo (over-engineering) nem muito tarde (technical debt).

## Como usar

````bash
/refactor-now
/refactor-now "módulo específico"

```text

## Regra dos 3

- **1 caso**: Deixe código inline (simples)
- **2 casos**: Duplication OK, não refatore
- **3 casos**: AGORA refatore! Padrão emergiu

## Processo

1. **Analisar código**:
   - Scan codebase procurando duplicação
   - Detectar padrões que repetem 3+ vezes
   - Identificar abstrações prematuras (com < 3 usos)

2. **Validar com "Rule of 3"**:
   - Contar cada padrão encontrado
   - Se < 3 ocorrências: Não refatore
   - Se ≥ 3 ocorrências: Sugerir refatoração

3. **Calcular impacto**:
   - Linhas a serem reduzidas
   - Complexidade diminuída
   - Risco da mudança

4. **Sugerir refatorações**:
   - Listadas por impacto (maior primeiro)
   - Com exemplo de antes/depois
   - Indicação de risco e esforço

5. **Implementar** (se autorizado):
   - Aplicar mudança
   - Executar testes
   - Validar que funciona

## Output esperado

```text

✅ REFATORAÇÃO IDENTIFICADA

📊 Padrões detectados: 3
Impacto estimado: -45 linhas

🔄 Refatoração proposta:
- Extrair função validacao_email()
- Linhas economizadas: 15
- Risco: LOW
- Esforço: 15 min

Refatorar? (s/n)

```text

## ⚠️ Não refatore quando

- ❌ Padrão apareceu 1-2 vezes (use /add-increment)
- ❌ Código está quebrado (conserte primeiro)
- ❌ Testes ausentes (adicione testes primeiro)
- ❌ Deadline apertado (deixa para depois)

## Próximos comandos

- `/commit` - Commitar refatoração
- `/add-increment` - Próximo incremento
- `/review-yagni` - Revisar over-engineering
````
