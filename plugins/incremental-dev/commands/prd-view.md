---
description: Exibe resumo do PRD (Product Requirements Document) atual com status, fase e próximos passos
---

# PRD View

Este comando exibe um resumo visual do PRD (Product Requirements Document) atual do projeto, mostrando versão, status, fase, e próximos passos recomendados.

## 🎯 Objetivo

Fornecer visão rápida e clara do estado atual do PRD sem precisar ler o documento completo.

## 📋 Como usar

```bash
/prd-view
```

Ou visualizar seção específica:

```bash
/prd-view mvp
/prd-view incrementos
/prd-view adrs
/prd-view timeline
```

## 🔍 Processo de Execução

### 1. Verificar Existência do PRD

```
🔍 PROCURANDO PRD...

Locais verificados:
- docs/PRD.md
- PRD.md
- docs/prd.md
```

**Se PRD NÃO existe**:
```
❌ PRD NÃO ENCONTRADO

O projeto ainda não possui PRD.

💡 Para criar PRD inicial:
   /setup-project-incremental

Isso criará:
- CLAUDE.md com instruções incrementais
- docs/PRD.md v0.1 (Descoberta inicial)

Criar PRD agora? (s/n)
```

**Se PRD existe**:
```
✅ PRD ENCONTRADO: docs/PRD.md
```

---

### 2. Extrair Informações do PRD

Ler PRD e extrair:
- Versão atual
- Data de última atualização
- Status do documento
- Fase atual
- Seções completadas
- Incrementos implementados
- ADRs registrados
- Próximas ações

---

### 3. Exibir Resumo Visual

```
═══════════════════════════════════════════
📄 PRD - [NOME DO PROJETO]
═══════════════════════════════════════════

📊 INFORMAÇÕES GERAIS

Versão: [versão]
Última Atualização: [data]
Status: [status]

═══════════════════════════════════════════
📍 FASE ATUAL
═══════════════════════════════════════════

[Fase atual] - [Descrição da fase]

Progresso:
[Barra de progresso visual]

═══════════════════════════════════════════
✅ SEÇÕES COMPLETADAS
═══════════════════════════════════════════

✅ Descoberta
   ├─ Problema definido
   ├─ Objetivos claros
   └─ KPIs estabelecidos

✅ Planejamento
   ├─ Product Vision
   ├─ Épicos identificados
   ├─ MVP definido
   └─ Roadmap criado

[Outras seções...]

═══════════════════════════════════════════
💻 INCREMENTOS IMPLEMENTADOS
═══════════════════════════════════════════

Total: [N] incrementos

1. [Nome Incremento 1] (Data)
   ✅ [Features implementadas]

2. [Nome Incremento 2] (Data)
   ✅ [Features implementadas]

═══════════════════════════════════════════
🎯 PRÓXIMOS PASSOS
═══════════════════════════════════════════

Recomendações baseadas na fase atual:

1. [Próxima ação 1]
2. [Próxima ação 2]
3. [Próxima ação 3]

═══════════════════════════════════════════
📈 TIMELINE DE EVOLUÇÃO
═══════════════════════════════════════════

[Data 1] v0.1 - Descoberta inicial
[Data 2] v1.0 - Planejamento completo
[Data 3] v1.1 - Design técnico
[Data 4] v1.2 - Incremento 1
[Data 5] v1.3 - Incremento 2
...

═══════════════════════════════════════════

Comandos úteis:
- /prd-update [fase]    - Atualizar PRD
- /prd-view incrementos - Ver apenas incrementos
- /prd-view adrs        - Ver decisões arquiteturais
- /start-incremental    - Começar próximo incremento

═══════════════════════════════════════════
```

---

## 📚 Exemplos de Uso

### Exemplo 1: Visualizar PRD Completo

```bash
/prd-view
```

**Output**:
```
═══════════════════════════════════════════
📄 PRD - SISTEMA DE PROCESSAMENTO DE DOCUMENTOS
═══════════════════════════════════════════

📊 INFORMAÇÕES GERAIS

Versão: 1.3
Última Atualização: 2025-01-25
Status: Em Desenvolvimento - Documento Vivo

═══════════════════════════════════════════
📍 FASE ATUAL
═══════════════════════════════════════════

Desenvolvimento (Incremento 3)

Progresso do MVP:
████████████░░░░░░░░ 60% (3/5 incrementos)

═══════════════════════════════════════════
✅ SEÇÕES COMPLETADAS
═══════════════════════════════════════════

✅ Descoberta
   ├─ Problema: Processamento manual de documentos demora horas
   ├─ Objetivo: Reduzir tempo em 80% com IA
   └─ KPI: Tempo de processamento < 2min por documento

✅ Planejamento
   ├─ Product Vision: Sistema automatizado de extração de dados
   ├─ Épicos: Upload, Processamento IA, Dashboard
   ├─ MVP: Upload PDF + Extração texto + Exibição resultado
   └─ YAGNI: OCR avançado, Múltiplos formatos, API completa

✅ Design
   ├─ Arquitetura: FastAPI + LangChain + PostgreSQL
   ├─ Stack: Python 3.11, FastAPI, LangChain, React
   └─ ADRs: 3 decisões arquiteturais registradas

═══════════════════════════════════════════
💻 INCREMENTOS IMPLEMENTADOS
═══════════════════════════════════════════

Total: 3 incrementos completados

1. Upload de PDF (2025-01-15)
   ✅ Upload via drag-and-drop
   ✅ Validação de formato
   ✅ Preview do arquivo
   📝 Aprendizado: Limite 10MB necessário

2. Extração de Texto (2025-01-20)
   ✅ Integração com LangChain
   ✅ Extração de texto simples
   ✅ Exibição de resultado
   📝 Aprendizado: Prompt engineering crítico

3. Armazenamento de Resultados (2025-01-25)
   ✅ PostgreSQL configurado
   ✅ Schema de dados criado
   ✅ CRUD básico implementado
   📝 Aprendizado: Indexação melhora performance em 300%

═══════════════════════════════════════════
🏗️  DECISÕES ARQUITETURAIS (ADRs)
═══════════════════════════════════════════

ADR-001: Usar FastAPI FileUpload (2025-01-15)
├─ Contexto: Método eficiente para upload de PDFs
├─ Decisão: FastAPI FileUpload ao invés de base64
└─ Consequências: Melhor performance, requer multipart/form-data

ADR-002: LangChain para processamento (2025-01-20)
├─ Contexto: Necessário orquestrar LLM + extração
├─ Decisão: Usar LangChain LCEL com chains
└─ Consequências: Flexível mas curva de aprendizado

ADR-003: PostgreSQL com índices (2025-01-25)
├─ Contexto: Queries lentas sem índices
├─ Decisão: Adicionar índices em user_id e created_at
└─ Consequências: Performance 300% melhor, espaço +15%

═══════════════════════════════════════════
🎯 PRÓXIMOS PASSOS
═══════════════════════════════════════════

Baseado na fase atual (Desenvolvimento):

1. Implementar Incremento 4: Interface de Usuário
   Comando: /add-increment "dashboard para visualização"

2. Após implementar, registrar no PRD
   Comando: /prd-update incremento

3. Verificar se é momento de refatorar
   Comando: /refactor-now

4. Quando 5 incrementos completos, finalizar MVP
   Comando: /prd-update final

═══════════════════════════════════════════
📈 TIMELINE DE EVOLUÇÃO
═══════════════════════════════════════════

2025-01-10  v0.1  Descoberta inicial
2025-01-12  v1.0  Planejamento completo
2025-01-14  v1.1  Design técnico definido
2025-01-15  v1.2  Incremento 1: Upload de PDF
2025-01-20  v1.3  Incremento 2: Extração de Texto
2025-01-25  v1.4  Incremento 3: Armazenamento ← VOCÊ ESTÁ AQUI

═══════════════════════════════════════════

📖 Ver PRD completo: cat docs/PRD.md
🔄 Atualizar PRD: /prd-update [fase]
➕ Próximo incremento: /add-increment "descrição"

═══════════════════════════════════════════
```

---

### Exemplo 2: Visualizar Apenas Incrementos

```bash
/prd-view incrementos
```

**Output**:
```
═══════════════════════════════════════════
💻 INCREMENTOS IMPLEMENTADOS
═══════════════════════════════════════════

Total: 3 incrementos | Progresso MVP: 60% (3/5)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Incremento 1: Upload de PDF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: 2025-01-15
Versão PRD: 1.2

Funcionalidades:
✅ Upload via drag-and-drop
✅ Validação de formato (apenas PDF)
✅ Preview do arquivo antes de processar
✅ Limite de 10MB implementado

Aprendizados:
📝 Usuários tentam enviar arquivos muito grandes
📝 Necessário feedback visual de progresso
📝 Validação client-side melhora UX

Decisões Técnicas:
🔧 ADR-001: FastAPI FileUpload escolhido

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Incremento 2: Extração de Texto
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: 2025-01-20
Versão PRD: 1.3

Funcionalidades:
✅ Integração com LangChain
✅ Extração de texto básica
✅ Exibição de resultado formatado
✅ Tratamento de erros de processamento

Aprendizados:
📝 Prompt engineering é CRÍTICO para qualidade
📝 Alguns PDFs têm encoding problemático
📝 Timeout de 30s necessário para PDFs grandes

Decisões Técnicas:
🔧 ADR-002: LangChain LCEL escolhido

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Incremento 3: Armazenamento de Resultados
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: 2025-01-25
Versão PRD: 1.4

Funcionalidades:
✅ PostgreSQL configurado
✅ Schema de dados (documents, extractions)
✅ CRUD básico implementado
✅ Relacionamento user → documents

Aprendizados:
📝 Índices melhoram performance em 300%
📝 Migrations com Alembic facilitam evolução
📝 Connection pooling essencial para produção

Decisões Técnicas:
🔧 ADR-003: PostgreSQL com índices

═══════════════════════════════════════════

📊 Resumo:
- Total de features implementadas: 12
- ADRs registrados: 3
- Aprendizados documentados: 9

🎯 Próximo incremento sugerido:
   /add-increment "Interface de usuário para visualização"

═══════════════════════════════════════════
```

---

### Exemplo 3: Visualizar Apenas ADRs

```bash
/prd-view adrs
```

**Output**:
```
═══════════════════════════════════════════
🏗️  DECISÕES ARQUITETURAIS (ADRs)
═══════════════════════════════════════════

Total: 3 ADRs registrados

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADR-001: Usar FastAPI FileUpload
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: 2025-01-15
Status: ✅ Aceito
Relacionado: Incremento 1

Contexto:
Precisávamos de método eficiente para upload de PDFs.
Alternativas consideradas: base64 encoding, presigned URLs S3.

Decisão:
Usar FastAPI FileUpload com multipart/form-data.

Consequências:
✅ Positivas:
   - Melhor performance para arquivos grandes
   - Streaming nativo do FastAPI
   - Fácil implementar progress bar

❌ Negativas:
   - Requer multipart/form-data (não JSON puro)
   - Frontend precisa usar FormData

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADR-002: LangChain para Processamento
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: 2025-01-20
Status: ✅ Aceito
Relacionado: Incremento 2

Contexto:
Necessário orquestrar LLM + extração de dados estruturados.
Alternativas: LangChain, LlamaIndex, implementação manual.

Decisão:
Usar LangChain LCEL (Expression Language) com chains.

Consequências:
✅ Positivas:
   - Composição elegante de chains com |
   - Abstrações úteis (PromptTemplate, OutputParser)
   - Comunidade ativa e documentação

❌ Negativas:
   - Curva de aprendizado LCEL
   - Dependência externa pesada
   - Debugging pode ser complexo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADR-003: PostgreSQL com Índices
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data: 2025-01-25
Status: ✅ Aceito
Relacionado: Incremento 3

Contexto:
Queries de listagem de documentos estavam lentas (500ms).
Queries frequentes: filtrar por user_id e ordenar por created_at.

Decisão:
Adicionar índices compostos em (user_id, created_at).

Consequências:
✅ Positivas:
   - Performance melhorou 300% (500ms → 150ms)
   - Escalabilidade para muitos usuários
   - PostgreSQL otimiza queries automaticamente

❌ Negativas:
   - Espaço em disco +15%
   - Inserts ligeiramente mais lentos (não perceptível)
   - Precisa manter índices atualizados

═══════════════════════════════════════════

💡 Lembrete:
ADRs são registrados automaticamente quando você:
- Usa /refactor-now e faz decisão arquitetural
- Usa /prd-update incremento e documenta decisões

═══════════════════════════════════════════
```

---

### Exemplo 4: Timeline de Evolução

```bash
/prd-view timeline
```

**Output**:
```
═══════════════════════════════════════════
📈 TIMELINE DE EVOLUÇÃO DO PRD
═══════════════════════════════════════════

┌─────────────────────────────────────────┐
│ DESCOBERTA                               │
└─────────────────────────────────────────┘
  2025-01-10  v0.1  Descoberta inicial
  ├─ Problema identificado
  ├─ Objetivos definidos
  └─ KPIs estabelecidos

┌─────────────────────────────────────────┐
│ PLANEJAMENTO                             │
└─────────────────────────────────────────┘
  2025-01-12  v1.0  Planejamento completo
  ├─ Product Vision criada
  ├─ Épicos mapeados: 3
  ├─ MVP definido: 5 incrementos
  └─ Roadmap estabelecido

┌─────────────────────────────────────────┐
│ DESIGN                                   │
└─────────────────────────────────────────┘
  2025-01-14  v1.1  Design técnico
  ├─ Arquitetura: FastAPI + LangChain
  ├─ Stack definida
  └─ Modelagem de dados

┌─────────────────────────────────────────┐
│ DESENVOLVIMENTO                          │
└─────────────────────────────────────────┘
  2025-01-15  v1.2  Incremento 1: Upload
  ├─ Features: 4
  ├─ Aprendizados: 3
  └─ ADR-001 registrado

  2025-01-20  v1.3  Incremento 2: Extração
  ├─ Features: 4
  ├─ Aprendizados: 3
  └─ ADR-002 registrado

  2025-01-25  v1.4  Incremento 3: Storage ← ATUAL
  ├─ Features: 4
  ├─ Aprendizados: 3
  └─ ADR-003 registrado

┌─────────────────────────────────────────┐
│ PRÓXIMOS PASSOS                          │
└─────────────────────────────────────────┘
  [Previsto]  v1.5  Incremento 4: UI Dashboard
  [Previsto]  v1.6  Incremento 5: API REST
  [Previsto]  v2.0  PRD Final (As-Built)

═══════════════════════════════════════════

📊 Estatísticas:
- Duração total: 15 dias
- Incrementos completados: 3/5 (60%)
- Velocidade média: 5 dias/incremento
- Previsão conclusão MVP: ~2025-02-10

═══════════════════════════════════════════
```

---

## 🎯 Seções Disponíveis

Visualizar partes específicas do PRD:

| Comando | Exibe |
|---------|-------|
| `/prd-view` | Resumo completo |
| `/prd-view mvp` | Apenas definição do MVP |
| `/prd-view incrementos` | Lista de incrementos implementados |
| `/prd-view adrs` | Decisões arquiteturais registradas |
| `/prd-view timeline` | Timeline de evolução do PRD |
| `/prd-view status` | Status atual e próximos passos |

---

## ⚠️ Se PRD Não Existe

```
❌ PRD NÃO ENCONTRADO

💡 O PRD é criado automaticamente quando você executa:
   /setup-project-incremental

Isso cria:
1. CLAUDE.md - Instruções de desenvolvimento incremental
2. docs/PRD.md v0.1 - Documento inicial de requisitos

Benefícios do PRD:
✅ Documentação viva que evolui com o projeto
✅ Registro de decisões e aprendizados
✅ Timeline clara de evolução
✅ Alinhamento entre equipe

Criar PRD agora? (s/n)
```

---

## 💡 Dicas

1. **Use regularmente**: `/prd-view` mostra progresso real
2. **Antes de incremento**: Confira status atual
3. **Após incremento**: Veja o que falta para MVP
4. **Decisões importantes**: Consulte ADRs
5. **Timeline**: Útil para retrospectivas

---

## 🔗 Comandos Relacionados

- `/prd-update [fase]` - Atualizar PRD
- `/setup-project-incremental` - Criar PRD inicial
- `/start-incremental` - Começar desenvolvimento (consulta PRD)
- `/add-increment` - Adicionar funcionalidade (sugere atualizar PRD)

---

**PRD View: Visibilidade rápida do estado do projeto!**