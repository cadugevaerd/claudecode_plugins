---
description: Adotar desenvolvimento incremental em projeto existente - analisa código, cria PRD retroativo e sugere simplificações
allowed-tools: Read, Write, Grep, Bash(git:*)
---

# Adopt Incremental

Permite adotar desenvolvimento incremental em **projetos já iniciados**, analisando código existente e criando um PRD retroativo baseado no estado atual.

## Como usar

````bash
/adopt-incremental
/adopt-incremental "API REST com FastAPI para gerenciar usuários"

```text

## Diferença para `/prd-retrofit`

| Comando | O que faz |
|---------|-----------|
| `/prd-retrofit` | **Apenas** cria PRD retroativo |
| `/adopt-incremental` | PRD + identifica over-engineering + roadmap de simplificação + configura CLAUDE.md |

## Processo completo (5 passos)

1. **Detectar projeto existente**:
   - Encontrar arquivos de código (.py, .js, .ts, etc)
   - Analisar estrutura de diretórios
   - Verificar git history

2. **Analisar código automaticamente**:
   - Coletar métricas (LOC, complexidade)
   - Detectar funcionalidades implementadas
   - Identificar over-engineering (abstrações com 1 implementação, código não usado)

3. **Gerar PRD retroativo**:
   - Documentar funcionalidades encontradas
   - Listar oportunidades de simplificação
   - Criar roadmap de melhorias

4. **Configurar CLAUDE.md**:
   - Adicionar instruções YAGNI
   - Definir regras de desenvolvimento incremental
   - Linkar PRD e roadmap

5. **Gerar Action Roadmap**:
   - Phase 1: Quick wins (1 semana)
   - Phase 2: Refactorings (2-4 semanas)
   - Phase 3: Novas features com YAGNI

## Output esperado

```text

✅ ADOÇÃO DE INCREMENTAL COMPLETA

📄 docs/PRD.md (v1.0 retroativo)
📝 CLAUDE.md (atualizado com YAGNI)
📋 ROADMAP.md (fases de melhoria)

📊 Análise:
- Over-engineering detectado: 12 oportunidades
- Quick wins: 5 refactorings simples
- Débito técnico: 3 áreas críticas

🚀 Próximas ações:
- Revisar PRD retroativo
- Executar Phase 1 do roadmap
- Usar /add-increment para novas features

```text

## Próximos comandos

- `/prd-view` - Visualizar PRD gerado
- `/prd-fix` - Ajustar seções do PRD
- `/review-yagni` - Detectar mais over-engineering
- `/add-increment` - Adicionar features com YAGNI
````
