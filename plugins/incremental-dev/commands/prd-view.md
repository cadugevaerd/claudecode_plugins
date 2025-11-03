---
description: Exibe resumo do PRD (Product Requirements Document) atual com status, fase e próximos passos
---

# PRD View

Exibe um resumo visual do PRD (Product Requirements Document) atual do projeto, mostrando versão, status, fase e próximos passos.

## Como usar

````bash
/prd-view                # PRD completo
/prd-view mvp           # Apenas MVP
/prd-view incrementos   # Incrementos implementados
/prd-view adrs          # Decisões arquiteturais
/prd-view timeline      # Timeline de evolução
/prd-view status        # Status atual e próximos passos

```text

## Processo

1. Procure PRD em `docs/PRD.md` ou `PRD.md`
2. Se não existir, sugira `/setup-project-incremental`
3. Se existir, extraia:
   - Versão e data de última atualização
   - Fase atual (Descoberta, Planejamento, Design, Desenvolvimento, Final)
   - Seções completadas com checkmarks
   - Incrementos implementados com datas
   - ADRs registrados
   - Próximos passos recomendados

## Saída formatada

Exiba resumo visual com estrutura clara:

- **📊 Informações Gerais**: Versão, data, status
- **📍 Fase Atual**: Fase e progresso visual (barra %)
- **✅ Seções Completadas**: Checklist de áreas prontas
- **💻 Incrementos**: Lista com datas e features
- **🏗️ ADRs**: Decisões arquiteturais registradas
- **🎯 Próximos Passos**: Ações recomendadas
- **📈 Timeline**: Evolução do PRD em cronograma

## Argumentos opcionais

- `mvp` - Mostrar apenas definição do MVP
- `incrementos` - Mostrar apenas incrementos implementados
- `adrs` - Mostrar apenas decisões arquiteturais
- `timeline` - Mostrar apenas timeline de evolução
- `status` - Mostrar apenas status e próximos passos

## Se PRD não existe

Exiba mensagem clara:

```text

❌ PRD NÃO ENCONTRADO

Para criar PRD inicial:
   /setup-project-incremental

Ou para projeto existente (legacy):
   /prd-retrofit

```text

## Próximos comandos úteis

- `/prd-update [fase]` - Atualizar PRD completo
- `/prd-fix "mudança"` - Ajuste cirúrgico em uma seção
- `/add-increment` - Adicionar próximo incremento
- `/prd-retrofit` - Criar PRD retroativo

**PRD View: Visibilidade rápida do estado do projeto!**
````
