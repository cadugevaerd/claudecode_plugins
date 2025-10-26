---
description: Central de ajuda do plugin incremental-dev - responde perguntas sobre YAGNI, PRD, desenvolvimento incremental e uso do plugin
---

# PRD Help - Central de Ajuda Incremental Dev

Central de ajuda interativa para desenvolvimento incremental, YAGNI, PRD e uso do plugin.

## 🎯 Objetivo

Ajudar usuários a:
- Entender conceitos de desenvolvimento incremental
- Aprender a usar os comandos do plugin
- Tirar dúvidas sobre YAGNI e Evolutionary Architecture
- Obter orientação sobre gestão de PRD
- Resolver problemas comuns

## 📋 Como Usar

### Modo Pergunta Direta

```bash
# Fazer pergunta específica
/prd-help "Como criar um PRD inicial?"
/prd-help "O que é YAGNI?"
/prd-help "Qual diferença entre /prd-update e /prd-fix?"
/prd-help "Como decidir quando refatorar?"
```

### Modo Interativo

```bash
# Sem argumentos - menu interativo
/prd-help
```

## 🔍 Processo de Execução

### 1. Detectar Modo de Operação

**Se pergunta fornecida** (modo direto):
- Analisar pergunta
- Identificar categoria (PRD, YAGNI, Comandos, Conceitos)
- Responder diretamente
- Sugerir recursos relacionados

**Se SEM argumentos** (modo interativo):
- Mostrar menu de categorias
- Permitir navegação
- Responder perguntas
- Mostrar exemplos práticos

### 2. Modo Interativo - Menu Principal

```
═══════════════════════════════════════════
❓ AJUDA - INCREMENTAL DEV
═══════════════════════════════════════════

Escolha uma categoria ou faça uma pergunta:

📚 CATEGORIAS:
1. 🚀 Começar a Usar (Primeiros Passos)
2. 📋 Gestão de PRD (Product Requirements Document)
3. ⚙️ Comandos Disponíveis (Referência Rápida)
4. 💡 Conceitos (YAGNI, Incremental, MVP)
5. 🔧 Troubleshooting (Problemas Comuns)
6. 📖 Exemplos Práticos (Casos de Uso Reais)

💬 PERGUNTAR:
7. Fazer uma pergunta específica

0. Sair

Escolha (0-7):
```

### 3. Categoria 1: Começar a Usar

```
═══════════════════════════════════════════
🚀 COMEÇAR A USAR
═══════════════════════════════════════════

## Fluxo para PROJETOS NOVOS

1️⃣ **Configurar Projeto**
   /setup-project-incremental
   └─ Configura CLAUDE.md com regras YAGNI

2️⃣ **Criar PRD Inicial**
   /start-incremental
   └─ Cria PRD.md com requisitos do projeto

3️⃣ **Desenvolver Incrementalmente**
   /add-increment "próxima funcionalidade"
   └─ Adiciona features uma a uma

4️⃣ **Revisar Over-engineering**
   /review-yagni
   └─ Detecta código desnecessário

5️⃣ **Refatorar Quando Necessário**
   /refactor-now
   └─ Identifica momento de refatorar

---

## Fluxo para PROJETOS EXISTENTES (Legacy)

🔄 **Adotar Desenvolvimento Incremental**
   /adopt-incremental
   └─ Analisa projeto existente
   └─ Cria PRD retroativo
   └─ Identifica over-engineering
   └─ Gera roadmap de simplificação

   OU (se só quer criar PRD):

📋 **Criar Apenas PRD Retroativo**
   /prd-retrofit
   └─ Analisa código existente
   └─ Gera PRD a partir do código
   └─ Útil para documentar projeto sem código

═══════════════════════════════════════════

Mais informações:
- Ver comandos: Escolha opção 3
- Ver exemplos: Escolha opção 6
- Voltar: Digite 'voltar'
```

### 4. Categoria 2: Gestão de PRD

```
═══════════════════════════════════════════
📋 GESTÃO DE PRD
═══════════════════════════════════════════

## O que é PRD?

Product Requirements Document - documento vivo que define:
- 🎯 O que construir
- 🎯 Por que construir
- 🎯 Como medir sucesso
- 🎯 O que NÃO construir (escopo)

## Comandos de PRD

┌──────────────────────────────────────────────┐
│ Comando              │ Quando Usar           │
├──────────────────────────────────────────────┤
│ /start-incremental   │ Criar PRD novo        │
│ /prd-retrofit        │ PRD retroativo (legacy)│
│ /prd-view           │ Visualizar PRD        │
│ /prd-update         │ Atualizar completo    │
│ /prd-fix            │ Ajuste cirúrgico      │
│ /prd-help           │ Ajuda (você está aqui)│
└──────────────────────────────────────────────┘

## Perguntas Comuns

Q: Quando criar um PRD?
A: No início do projeto, antes de escrever código.
   Use: /start-incremental

Q: E se meu projeto já existe?
A: Use /prd-retrofit para criar PRD retroativo
   a partir do código existente. Analisa estrutura,
   funcionalidades e gera documentação.

Q: Como atualizar uma seção do PRD?
A: Para mudanças pequenas: /prd-fix "mudança"
   Para reescrever completo: /prd-update

Q: PRD é obrigatório?
A: Não, mas ajuda MUITO a manter foco e evitar
   over-engineering. Recomendado para projetos
   com > 1 semana de duração.

═══════════════════════════════════════════

Exemplos práticos: Escolha opção 6
Voltar: Digite 'voltar'
```

### 5. Categoria 3: Comandos Disponíveis

```
═══════════════════════════════════════════
⚙️ COMANDOS DISPONÍVEIS
═══════════════════════════════════════════

## Comandos de Setup

/setup-project-incremental
└─ Configura CLAUDE.md do projeto
   Uso: /setup-project-incremental [descrição]

## Comandos de Workflow

/start-incremental
└─ Inicia desenvolvimento incremental + cria PRD
   Uso: /start-incremental [objetivo]

/adopt-incremental
└─ Adota YAGNI em projeto existente (legacy)
   Analisa código, cria PRD retroativo, identifica
   over-engineering e gera roadmap de simplificação
   Uso: /adopt-incremental

/add-increment
└─ Adiciona próximo incremento
   Uso: /add-increment "funcionalidade"

/review-yagni
└─ Revisa código identificando over-engineering
   Uso: /review-yagni

/refactor-now
└─ Identifica quando refatorar
   Uso: /refactor-now

## Comandos de PRD

/prd-view
└─ Visualiza PRD completo
   Uso: /prd-view [seção]

/prd-retrofit
└─ Cria PRD retroativo a partir de código existente
   Analisa projeto legacy e gera documentação PRD
   Uso: /prd-retrofit

/prd-update
└─ Atualiza PRD completo
   Uso: /prd-update

/prd-fix
└─ Ajusta seção específica do PRD
   Uso: /prd-fix "mudança"

/prd-help
└─ Esta ajuda
   Uso: /prd-help [pergunta]

═══════════════════════════════════════════

Ver exemplos: Escolha opção 6
Voltar: Digite 'voltar'
```

### 6. Categoria 4: Conceitos

```
═══════════════════════════════════════════
💡 CONCEITOS FUNDAMENTAIS
═══════════════════════════════════════════

## YAGNI - You Aren't Gonna Need It

**Definição**: Não adicione funcionalidade até
que seja REALMENTE necessária.

**Exemplo Ruim** ❌:
class User {
  // Hoje só precisa de name
  name: string
  email: string
  // "No futuro pode precisar"
  avatar?: string
  preferences?: JSON
  settings?: object
  metadata?: any
}

**Exemplo Bom** ✅:
class User {
  name: string
  email: string
  // Só isso! Adiciona o resto QUANDO precisar
}

## Desenvolvimento Incremental

**Definição**: Construir software em pequenos
incrementos funcionais.

**Fluxo**:
MVP → Incremento 1 → Incremento 2 → ...

Cada incremento:
- ✅ Funciona sozinho
- ✅ Agrega valor
- ✅ Pode ser entregue

## Evolutionary Architecture

**Definição**: Arquitetura que evolui com o
código, não é definida 100% no início.

**Como aplicar**:
1. Começar simples
2. Identificar padrões ao codificar
3. Refatorar quando padrão emerge 3x
4. Evoluir arquitetura baseado em necessidade real

## MVP - Minimum Viable Product

**Definição**: Menor versão funcional que
entrega valor e permite aprendizado.

**Não é**:
- Produto incompleto
- Protótipo descartável
- Versão bugada

**É**:
- Mínimo funcional
- Testável com usuários reais
- Base para evoluir

═══════════════════════════════════════════

Exemplos práticos: Escolha opção 6
Voltar: Digite 'voltar'
```

### 7. Categoria 5: Troubleshooting

```
═══════════════════════════════════════════
🔧 PROBLEMAS COMUNS
═══════════════════════════════════════════

## Problema 1: PRD não encontrado

❌ Erro: "PRD.md não encontrado"

✅ Solução:
   /start-incremental
   └─ Cria PRD.md na raiz do projeto

---

## Problema 2: Como saber se estou fazendo over-engineering?

💡 Sinais de alerta:
- Abstrações antes de duplicação
- Classes com < 10 linhas
- Interfaces com 1 implementação
- "Pode ser útil no futuro"
- Mais tempo pensando que codificando

✅ Solução:
   /review-yagni
   └─ Detecta over-engineering automaticamente

---

## Problema 3: Quando refatorar?

💡 Regra dos 3:
- 1x: Código inline (simples)
- 2x: Ainda pode deixar duplicado
- 3x: AGORA refatore!

✅ Solução:
   /refactor-now
   └─ Identifica padrões que repetem 3x+

---

## Problema 4: PRD está muito grande

💡 PRD grande = escopo grande

✅ Solução:
1. /prd-view
2. Identifique o CORE (MVP)
3. /prd-fix "Mover X para 'Fora de Escopo'"
4. Foque no essencial primeiro

---

## Problema 5: Como começar projeto novo?

✅ Fluxo recomendado:
1. /setup-project-incremental "descrição"
2. /start-incremental
3. Responda perguntas sobre o projeto
4. PRD será criado
5. Comece pelo MVP do PRD

---

## Problema 6: Projeto já existe, como adotar YAGNI?

💡 Projeto legacy sem documentação?

✅ Solução completa:
   /adopt-incremental
   └─ Analisa código automaticamente
   └─ Cria PRD retroativo
   └─ Identifica over-engineering
   └─ Gera roadmap de simplificação

✅ Solução rápida (só PRD):
   /prd-retrofit
   └─ Cria apenas o PRD retroativo
   └─ Útil para documentar projeto existente

═══════════════════════════════════════════

Mais problemas: Digite sua dúvida
Voltar: Digite 'voltar'
```

### 8. Categoria 6: Exemplos Práticos

```
═══════════════════════════════════════════
📖 EXEMPLOS PRÁTICOS
═══════════════════════════════════════════

## Exemplo 1: API REST do Zero

Objetivo: Criar API de tarefas (TODO)

# Passo 1: Setup
/setup-project-incremental "API REST de tarefas"

# Passo 2: Criar PRD
/start-incremental
> O que quer construir? API de tarefas
> Quem vai usar? Desenvolvedores (integração)
> Principal funcionalidade? CRUD de tarefas
> Prioridade #1? Listar e criar tarefas
> Fora de escopo? Autenticação (v2)

# Passo 3: MVP (do PRD gerado)
Implementar: GET /tasks e POST /tasks

# Passo 4: Incremento 1
/add-increment "Adicionar PUT /tasks/:id e DELETE /tasks/:id"

# Passo 5: Incremento 2
/add-increment "Adicionar filtros em GET /tasks?status=done"

# Passo 6: Revisar
/review-yagni
> Detecta se adicionou validações desnecessárias

# Passo 7: Refatorar (se padrão emergir)
/refactor-now
> Detecta se repository pattern apareceu 3x

---

## Exemplo 2: Dashboard Web

Objetivo: Dashboard de métricas

# Passo 1: PRD Interativo
/start-incremental
> O que quer? Dashboard de vendas
> Usuários? Gerentes de vendas
> Métrica principal? Total de vendas do mês
> Outras métricas? Vendas por produto, por região
> Prioridade? Total mensal primeiro

# Passo 2: MVP
Implementar: Gráfico de total mensal

# Passo 3: Incremento 1
/add-increment "Gráfico de vendas por produto"

# Passo 4: Incremento 2
/add-increment "Filtro por período (último mês, trimestre)"

# Passo 5: Ajustar PRD
/prd-fix "Adicionar requisito: exportar para PDF"

# Passo 6: Ver PRD atualizado
/prd-view

---

## Exemplo 3: Microserviço

Objetivo: Serviço de notificações

# Passo 1: Definir escopo
/start-incremental
> O que construir? Serviço de notificações
> Canais? Email e SMS
> Prioridade? Email primeiro
> Fora de escopo? Push notifications (v2)

# Passo 2: MVP
Implementar: Envio de email via SMTP

# Passo 3: Review YAGNI
/review-yagni
> Não implementar fila de mensagens ainda!
> Só quando tiver volume que justifique

# Passo 4: Incremento 1
/add-increment "Adicionar templates de email"

# Passo 5: Quando refatorar?
/refactor-now
> Se template pattern repetir 3x, refatore

---

## Exemplo 4: Projeto Legacy (Adotar YAGNI)

Objetivo: Adotar YAGNI em projeto existente

# Passo 1: Analisar projeto e criar PRD retroativo
/adopt-incremental
> Detecta código automaticamente
> Analisa estrutura e funcionalidades
> Identifica over-engineering
> Cria PRD.md retroativo
> Gera roadmap de simplificação

# Passo 2: Revisar over-engineering detectado
> Claude apresenta relatório:
  - Abstrações com 1 implementação
  - Código não usado
  - Complexidade desnecessária

# Passo 3: Aplicar roadmap incremental
> Seguir roadmap gerado:
  1. Remover código não usado
  2. Simplificar abstrações
  3. Refatorar incrementalmente

# Passo 4 (Alternativa): Só criar PRD
/prd-retrofit
> Se só precisa do PRD retroativo
> Sem análise completa de over-engineering

═══════════════════════════════════════════

Voltar ao menu: Digite 'voltar'
Fazer pergunta: Digite sua dúvida
```

### 9. Modo Pergunta Direta

**Analisar pergunta e responder**:

**Exemplo 1**: `/prd-help "O que é YAGNI?"`
```
═══════════════════════════════════════════
❓ O QUE É YAGNI?
═══════════════════════════════════════════

YAGNI = "You Aren't Gonna Need It"

**Princípio**: Não adicione código/funcionalidade
pensando "pode ser útil no futuro".

**Desenvolva apenas o que é necessário AGORA.**

## Por que YAGNI?

✅ Benefícios:
- Código mais simples
- Menos bugs
- Entrega mais rápida
- Fácil de mudar

❌ Sem YAGNI:
- Complexidade desnecessária
- Código nunca usado
- Difícil manutenção
- Over-engineering

## Como aplicar?

Pergunte: "Preciso AGORA ou 'pode precisar'?"
- AGORA: Implemente ✅
- Pode precisar: NÃO implemente ❌

═══════════════════════════════════════════

📚 Recursos relacionados:
- Ver conceitos completos: /prd-help → opção 4
- Detectar over-engineering: /review-yagni
- Exemplos práticos: /prd-help → opção 6
```

**Exemplo 2**: `/prd-help "Diferença entre /prd-update e /prd-fix"`
```
═══════════════════════════════════════════
❓ PRD-UPDATE vs PRD-FIX
═══════════════════════════════════════════

## /prd-update

**Uso**: Atualizar PRD COMPLETO
**Quando**: Mudanças grandes, reescrever PRD

Exemplo:
/prd-update
> Faz perguntas sobre TODO o projeto
> Reescreve PRD inteiro

## /prd-fix

**Uso**: Ajustar UMA seção específica
**Quando**: Mudança pontual, correção pequena

Exemplo:
/prd-fix "Adicionar OAuth2 nos requisitos"
> Adiciona apenas esse item
> Preserva resto do PRD

## Decisão Rápida

┌────────────────────────────────────────┐
│ Mudança                │ Comando       │
├────────────────────────────────────────┤
│ Adicionar 1 requisito  │ /prd-fix     │
│ Mudar 1 prioridade     │ /prd-fix     │
│ Adicionar 1 métrica    │ /prd-fix     │
│                        │              │
│ Mudar objetivo geral   │ /prd-update  │
│ Adicionar 5+ requisitos│ /prd-update  │
│ Repensar MVP           │ /prd-update  │
└────────────────────────────────────────┘

═══════════════════════════════════════════

📚 Recursos relacionados:
- Ver todos comandos: /prd-help → opção 3
- Exemplos de uso: /prd-help → opção 6
```

## 🎯 Base de Conhecimento (Respostas Rápidas)

O comando deve ter respostas prontas para perguntas comuns:

### Perguntas sobre PRD
- "Como criar PRD?" → `/start-incremental`
- "Como criar PRD retroativo?" → `/prd-retrofit` (projeto legacy)
- "Como atualizar PRD?" → `/prd-update` ou `/prd-fix`
- "Como ver PRD?" → `/prd-view`
- "PRD é obrigatório?" → Não, mas recomendado
- "Onde fica o PRD?" → `PRD.md` na raiz ou `docs/PRD.md`
- "Projeto já existe, como criar PRD?" → `/prd-retrofit`

### Perguntas sobre YAGNI
- "O que é YAGNI?" → Explicação completa
- "Como aplicar YAGNI?" → Não adicione "pode precisar"
- "Como detectar over-engineering?" → `/review-yagni`
- "Quando refatorar?" → Quando padrão repete 3x (`/refactor-now`)

### Perguntas sobre Comandos
- "Quais comandos existem?" → Lista completa
- "Como usar X?" → Ajuda específica do comando
- "Diferença entre X e Y?" → Comparação
- "Projeto legacy, qual comando usar?" → `/adopt-incremental` (completo) ou `/prd-retrofit` (só PRD)
- "Diferença entre /adopt-incremental e /prd-retrofit?" → `/adopt-incremental` = análise completa + PRD + roadmap; `/prd-retrofit` = só PRD

### Perguntas sobre Conceitos
- "O que é MVP?" → Explicação
- "O que é incremental?" → Explicação
- "O que é Evolutionary Architecture?" → Explicação

## ✅ SEMPRE Fazer

1. **Responder de forma clara**: Sem jargão desnecessário
2. **Dar exemplos práticos**: Código ou comandos reais
3. **Sugerir próximos passos**: Links para outros recursos
4. **Navegação fácil**: Permitir voltar ao menu
5. **Busca inteligente**: Entender sinônimos e variações

## 💡 Dicas para Usuários

```
💡 DICAS RÁPIDAS

✅ Começando agora?
   /prd-help → opção 1 (Começar a Usar)

✅ Quer ver todos comandos?
   /prd-help → opção 3 (Comandos)

✅ Não entende YAGNI?
   /prd-help "O que é YAGNI?"

✅ Problema específico?
   /prd-help "sua dúvida aqui"

✅ Ver exemplos reais?
   /prd-help → opção 6 (Exemplos)
```

## 🔗 Recursos Externos

```
📚 LEITURA RECOMENDADA

- YAGNI: https://martinfowler.com/bliki/Yagni.html
- Evolutionary Architecture: https://www.thoughtworks.com/evolutionary-architecture
- MVP: https://www.lean.org/lexicon-terms/minimum-viable-product/
- Incremental Development: https://agilemanifesto.org/principles.html

📺 VÍDEOS (se disponíveis)
- "YAGNI in Practice"
- "Building MVPs the Right Way"
```

---

**Desenvolvido para incremental-dev** - Sua central de ajuda completa! ❓✨