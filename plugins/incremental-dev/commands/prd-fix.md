---
description: Corrige ou ajusta seções específicas do PRD.md existente de forma cirúrgica
---

# PRD Fix

Faz correções e ajustes específicos em seções individuais do PRD sem reescrever o documento inteiro.

## Como usar

````bash

# Ajustar uma seção
/prd-fix "Adicionar autenticação OAuth2 nos requisitos"

# Corrigir prioridades
/prd-fix "Mover validação de email para P2"

# Atualizar métricas
/prd-fix "Tempo de resposta deve ser < 200ms"

```text

Ou modo interativo:

```bash
/prd-fix

```text

## Diferença para `/prd-update`

| Comando | Quando usar |
|---------|------------|
| `/prd-fix` | Ajuste CIRÚRGICO em um campo/linha |
| `/prd-update` | Atualizar FASE completa (múltiplas seções) |

Exemplos:
- ✅ `/prd-fix "Mover feature X para fora de escopo"` (pontual)
- ❌ `/prd-fix "Replanejar todo o MVP"` (use `/prd-update planejamento`)

## Processo

1. **Validar PRD existe**:
   - Se não existir: Sugerir `/start-incremental`

2. **Modo operação**:
   - Com argumento: Aplicar mudança direto
   - Sem argumento: Modo interativo (listar seções, escolher)

3. **Aplicar mudança**:
   - Ler PRD atual
   - Localizar seção afetada
   - Fazer ajuste específico
   - Atualizar timestamp

4. **Registrar mudança**:
   - Adicionar na seção "Histórico de Mudanças"
   - Explicar motivo da mudança

5. **Salvar PRD.md**:
   - Preservar resto do documento
   - Validar integridade

## Seções editáveis

- 📋 Visão Geral
- 🎯 Objetivos
- ⚙️ Requisitos Funcionais
- 🔒 Requisitos Não-Funcionais
- 📊 Métricas de Sucesso
- 🗺️ Roadmap
- ❌ Fora de Escopo (YAGNI)
- 🏗️ Arquitetura
- 📈 Incrementos
- 📝 ADRs

## Output esperado

```text

✅ PRD AJUSTADO

📄 docs/PRD.md

Mudança aplicada:
- Seção: Requisitos Funcionais
- Ajuste: Autenticação OAuth2 adicionada
- Motivo: Novo requisito de cliente
- Data: 2025-01-28

Histórico atualizado. PRD pronto para uso.

```text

## Próximos comandos

- `/prd-view` - Ver PRD atualizado
- `/prd-update` - Atualizar fase completa
- `/add-increment` - Adicionar funcionalidade
````
