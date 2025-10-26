---
description: Atualiza PRD (Product Requirements Document) conforme fase do projeto - descoberta, planejamento, design, incremento ou final
---

# PRD Update

Este comando atualiza o PRD (Product Requirements Document) do projeto conforme a fase atual de desenvolvimento.

## 🎯 Objetivo

Evoluir o PRD ao longo do ciclo de vida do projeto, mantendo documentação atualizada e sincronizada com o estado real do desenvolvimento.

## 📋 Como usar

```bash
/prd-update descoberta
/prd-update planejamento
/prd-update design
/prd-update incremento
/prd-update final
```

## 🔍 Fases do PRD

### 1. Descoberta (PRD v0.1)
```bash
/prd-update descoberta
```

**Quando usar**: Início do projeto, entendendo o problema

**Atualiza**:
- Problema a resolver
- Objetivos iniciais
- KPIs (Key Performance Indicators)
- Visão geral

**Perguntas ao usuário**:
- Qual problema este projeto resolve?
- Quais os objetivos principais?
- Como mediremos sucesso (KPIs)?

---

### 2. Planejamento (PRD v1.0)
```bash
/prd-update planejamento
```

**Quando usar**: Após descoberta, antes de implementar

**Atualiza**:
- Product Vision completa
- Épicos identificados
- Definição de MVP
- Roadmap de incrementos
- User Stories com Acceptance Criteria

**Perguntas ao usuário**:
- Quais épicos compõem o projeto?
- Qual o MVP (features essenciais)?
- O que fica FORA do MVP (YAGNI)?
- Quais as user stories principais?

---

### 3. Design (PRD v1.1)
```bash
/prd-update design
```

**Quando usar**: Após planejar, definindo arquitetura

**Atualiza**:
- Arquitetura de alto nível
- Stack tecnológica escolhida
- Modelagem de dados
- Definição de APIs/Contratos
- ADRs (Architectural Decision Records)

**Perguntas ao usuário**:
- Qual arquitetura escolhida?
- Quais tecnologias usar?
- Como modelar dados?
- Quais decisões arquiteturais importantes?

---

### 4. Incremento (PRD v1.x)
```bash
/prd-update incremento
```

**Quando usar**: Após completar cada incremento

**Atualiza**:
- Adiciona novo incremento à seção "Incrementos Implementados"
- Registra funcionalidades entregues
- Documenta lições aprendidas
- Incrementa versão do PRD (1.1 → 1.2 → 1.3...)

**Perguntas ao usuário**:
- Qual incremento foi completado?
- Quais funcionalidades foram implementadas?
- Quais aprendizados teve neste incremento?
- Alguma decisão técnica importante?

---

### 5. Final (PRD v2.0 - As-Built)
```bash
/prd-update final
```

**Quando usar**: Projeto finalizado

**Atualiza**:
- Marca PRD como "Documento Final (As-Built)"
- Consolida todos os incrementos
- Resume lições aprendidas completas
- Documenta estado final de produção
- Adiciona métricas reais coletadas

**Gera**:
- Documento final completo
- Timeline de evolução do projeto
- Retrospectiva geral

---

## 🔄 Processo de Execução

### 1. Verificar Existência do PRD

```
🔍 VERIFICANDO PRD...

Procurando em: docs/PRD.md
```

**Se PRD NÃO existe**:
```
❌ PRD não encontrado em docs/PRD.md

💡 Execute primeiro: /setup-project-incremental
   Isso criará o PRD v0.1 inicial.

Deseja criar PRD agora? (s/n)
```

**Se PRD existe**:
```
✅ PRD encontrado

Versão atual: [versão]
Última atualização: [data]
Status: [status]
```

---

### 2. Fazer Backup Antes de Atualizar

```
💾 BACKUP DO PRD

Criando: docs/PRD.md.backup.[timestamp]
```

**SEMPRE fazer backup antes de modificar!**

---

### 3. Coletar Informações do Usuário

Conforme fase selecionada, perguntar informações relevantes:

**Exemplo - Fase Planejamento**:
```
📋 ATUALIZAR PRD - PLANEJAMENTO

Responda as perguntas para atualizar o PRD:

1. Qual a visão do produto?
   > [usuário responde]

2. Quais os épicos principais? (separados por vírgula)
   > [usuário responde]

3. Quais features fazem parte do MVP? (separadas por vírgula)
   > [usuário responde]

4. O que NÃO deve estar no MVP? (YAGNI)
   > [usuário responde]

5. Alguma user story importante? (opcional)
   > [usuário responde]
```

---

### 4. Atualizar PRD

```
📝 ATUALIZANDO PRD...

Versão: [versão atual] → [nova versão]
Seções atualizadas:
├─ ✅ [Seção 1]
├─ ✅ [Seção 2]
└─ ✅ [Seção 3]

Data de atualização: [YYYY-MM-DD]
```

**Regras de versionamento**:
- Descoberta: v0.1
- Planejamento: v1.0
- Design: v1.1
- Incremento 1: v1.2
- Incremento 2: v1.3
- Final: v2.0

---

### 5. Mostrar Preview das Mudanças

```
═══════════════════════════════════════════
📄 PREVIEW - MUDANÇAS NO PRD
═══════════════════════════════════════════

[Preview das seções atualizadas]

---

Salvar mudanças? (s/n)
```

---

### 6. Salvar e Confirmar

```
✅ PRD ATUALIZADO COM SUCESSO!

Arquivo: docs/PRD.md
Versão: [nova versão]
Backup: docs/PRD.md.backup.[timestamp]

Próximos passos:
1. Revisar PRD atualizado
2. [Ação específica da fase]

PRD agora reflete fase: [fase]
```

---

## 📚 Exemplos de Uso

### Exemplo 1: Atualizar para Fase de Planejamento

```bash
/prd-update planejamento
```

**Fluxo**:
```
🔍 VERIFICANDO PRD...
✅ PRD encontrado (v0.1)

💾 Criando backup...
✅ Backup criado: docs/PRD.md.backup.20250125_143022

📋 ATUALIZAR PRD - PLANEJAMENTO

1. Qual a visão do produto?
   > Sistema de processamento de documentos com IA para automatizar extração de dados

2. Quais os épicos principais?
   > Upload de documentos, Processamento com IA, Dashboard de resultados

3. Quais features fazem parte do MVP?
   > Upload PDF, Extração de texto, Exibição de resultado

4. O que NÃO deve estar no MVP?
   > OCR avançado, Múltiplos formatos, Autenticação, API REST completa

📝 ATUALIZANDO PRD...

Versão: 0.1 → 1.0
Seções atualizadas:
├─ ✅ Product Vision
├─ ✅ Épicos
├─ ✅ MVP (Minimum Viable Product)
└─ ✅ Histórico de Versões

═══════════════════════════════════════════
📄 PREVIEW - MUDANÇAS NO PRD
═══════════════════════════════════════════

## 📋 FASE 2: PLANEJAMENTO (v1.0+)

### Product Vision
Sistema de processamento de documentos com IA para automatizar
extração de dados, reduzindo tempo de processamento manual em 80%.

### Épicos
1. **Upload de documentos**: Permitir upload seguro de PDFs
2. **Processamento com IA**: Extrair dados usando LLM
3. **Dashboard de resultados**: Visualizar dados extraídos

### MVP (Minimum Viable Product)
**Definição do MVP**:
- [x] Upload de PDF
- [x] Extração de texto
- [x] Exibição de resultado

**Fora do MVP** (YAGNI):
- ❌ OCR avançado
- ❌ Múltiplos formatos
- ❌ Autenticação
- ❌ API REST completa

---

Salvar mudanças? (s)

✅ PRD ATUALIZADO COM SUCESSO!

Versão: 1.0
Próximos passos:
1. Revisar PRD completo
2. Executar: /start-incremental (para começar MVP)
```

---

### Exemplo 2: Registrar Incremento Completado

```bash
/prd-update incremento
```

**Fluxo**:
```
🔍 VERIFICANDO PRD...
✅ PRD encontrado (v1.1)

📋 REGISTRAR INCREMENTO

1. Qual incremento foi completado?
   > Incremento 1: Upload de PDF

2. Quais funcionalidades foram implementadas?
   > Upload via drag-and-drop, Validação de formato, Preview do arquivo

3. Quais aprendizados teve neste incremento?
   > Necessário limitar tamanho de arquivo. Descobrimos que usuários tentam enviar
     arquivos grandes. Adicionamos limite de 10MB.

4. Alguma decisão técnica importante?
   > Decidimos usar FastAPI FileUpload ao invés de base64. Mais eficiente para
     arquivos grandes.

📝 ATUALIZANDO PRD...

Versão: 1.1 → 1.2
Nova entrada em "Incrementos Implementados"

═══════════════════════════════════════════
📄 PREVIEW - INCREMENTO ADICIONADO
═══════════════════════════════════════════

## 💻 DESENVOLVIMENTO

### Incrementos Implementados

#### Incremento 1: Upload de PDF
- **Data**: 2025-01-25
- **Funcionalidades**:
  - ✅ Upload via drag-and-drop
  - ✅ Validação de formato
  - ✅ Preview do arquivo
- **Aprendizados**:
  - Necessário limitar tamanho de arquivo a 10MB
  - Usuários tentam enviar arquivos muito grandes
  - FastAPI FileUpload é mais eficiente que base64

### ADRs (Architectural Decision Records)

#### ADR-001: Usar FastAPI FileUpload
- **Data**: 2025-01-25
- **Status**: Aceito
- **Contexto**: Precisávamos de método eficiente para upload de PDFs
- **Decisão**: Usar FastAPI FileUpload ao invés de base64
- **Consequências**: Melhor performance, mas requer multipart/form-data

---

Salvar mudanças? (s)

✅ PRD ATUALIZADO COM SUCESSO!

Versão: 1.2
Incremento registrado!

Próximo incremento: /add-increment "próxima funcionalidade"
```

---

## ⚠️ Regras Importantes

### 1. NUNCA Sobrescrever PRD Existente

**SEMPRE**:
- ✅ Fazer backup antes de modificar
- ✅ Preservar seções existentes
- ✅ Adicionar/atualizar apenas seções relevantes
- ✅ Incrementar versão corretamente

**NUNCA**:
- ❌ Deletar seções anteriores
- ❌ Modificar sem backup
- ❌ Sobrescrever histórico de versões

---

### 2. Versionamento Semântico do PRD

| Fase | Versão | Exemplo |
|------|--------|---------|
| Descoberta | 0.1 | PRD inicial |
| Planejamento | 1.0 | PRD completo |
| Design | 1.1 | + Decisões técnicas |
| Incremento 1 | 1.2 | + Primeiro incremento |
| Incremento 2 | 1.3 | + Segundo incremento |
| Incremento N | 1.N | + N-ésimo incremento |
| Final | 2.0 | Documento as-built |

---

### 3. Atualizar Data de Modificação

Sempre atualizar campo "Última Atualização" com data atual (YYYY-MM-DD).

---

### 4. Histórico de Versões

Sempre adicionar entrada na seção "Histórico de Versões":

```markdown
| Versão | Data | Mudanças |
|--------|------|----------|
| 1.2 | 2025-01-25 | Incremento 1: Upload de PDF |
```

---

## 🎯 Workflow Completo

```
1. /setup-project-incremental
   ↓ Cria PRD v0.1 (Descoberta)

2. /prd-update planejamento
   ↓ Atualiza para PRD v1.0 (Planejamento)

3. /prd-update design
   ↓ Atualiza para PRD v1.1 (Design)

4. /start-incremental + /add-increment
   ↓ Implementa incrementos

5. /prd-update incremento
   ↓ Registra cada incremento (v1.2, v1.3...)

6. /prd-update final
   ↓ Finaliza PRD v2.0 (As-Built)
```

---

## 💡 Dicas

1. **Backup automático**: Sempre criado antes de modificar
2. **Preview antes de salvar**: Sempre mostrar mudanças
3. **Versão incremental**: Cada incremento aumenta versão (1.2 → 1.3)
4. **ADRs importantes**: Registrar decisões arquiteturais em incrementos
5. **Lições aprendidas**: Sempre documentar aprendizados

---

## 🔗 Comandos Relacionados

- `/prd-view` - Visualizar resumo do PRD atual
- `/setup-project-incremental` - Criar PRD inicial
- `/add-increment` - Adicionar incremento (sugere atualizar PRD)
- `/refactor-now` - Refatorar (adiciona ADR ao PRD)

---

**PRD é um documento VIVO que evolui com o projeto!**