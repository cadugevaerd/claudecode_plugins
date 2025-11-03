---
description: Atualiza PRD (Product Requirements Document) conforme fase do projeto - descoberta, planejamento, design, incremento ou final
---

# PRD Update

Atualiza o PRD (Product Requirements Document) do projeto conforme a fase atual de desenvolvimento.

## Como usar

````bash
/prd-update descoberta    # Atualizar fase de descoberta
/prd-update planejamento  # Atualizar fase de planejamento
/prd-update design        # Atualizar fase de design
/prd-update incremento    # Registrar um incremento completado
/prd-update final         # Finalizar PRD (as-built)

```text

## Fases do PRD

### 1. Descoberta (v0.1)
Entender o problema e objetivos iniciais.

Atualiza:
- Problema a resolver
- Objetivos principais
- KPIs (Key Performance Indicators)

### 2. Planejamento (v1.0)
Definir escopo e roadmap.

Atualiza:
- Product Vision
- Épicos identificados
- MVP (Minimum Viable Product)
- O que fica fora (YAGNI)
- User Stories

### 3. Design (v1.1)
Definir arquitetura técnica.

Atualiza:
- Arquitetura de alto nível
- Stack tecnológica
- Modelagem de dados
- ADRs (Architectural Decision Records)

### 4. Incremento (v1.x)
Registrar cada incremento completado.

Atualiza:
- Adiciona novo incremento à lista
- Documenta features entregues
- Aprendizados e lições
- Decisões técnicas (se houver)

### 5. Final (v2.0)
Documentação as-built do projeto.

Atualiza:
- Status final do projeto
- Lições aprendidas globais
- Recomendações para próximas iterações
- Timeline completa

## Processo

1. **Validar PRD existe**: Se não, sugerir `/start-incremental`
2. **Coletar informações**: Perguntar sobre a fase específica
3. **Atualizar seções**: Adicionar/modificar dados da fase
4. **Incrementar versão**: v0.1 → v1.0 → v1.1 → v1.2 → v2.0
5. **Salvar PRD.md**: Refletir mudanças

## Diferença para `/prd-fix`

| Comando | Quando usar |
|---------|------------|
| `/prd-update` | Atualizar FASE completa (múltiplas seções) |
| `/prd-fix` | Ajuste CIRÚRGICO (um campo, uma linha) |

Exemplo:
- `prd-update planejamento` → Redefine todo o planejamento
- `prd-fix "Prioridade da API para P1"` → Ajusta só esse item

## Output esperado

```text

✅ PRD ATUALIZADO

📄 docs/PRD.md (v1.2 → v1.3)

Mudanças:
- Incremento 3 registrado
- 4 features novas documentadas
- 2 aprendizados registrados
- 1 ADR adicional criada
- Timestamp de atualização

🔧 Próximos passos:
- /prd-view - Ver PRD atualizado
- /add-increment - Próximo incremento
- /refactor-now - Se padrão emergiu

```text

## Próximos comandos

- `/prd-view` - Visualizar PRD completo
- `/prd-fix` - Ajustes pontuais
- `/add-increment` - Adicionar próxima feature
- `/refactor-now` - Refatorar quando padrão emerge
````
