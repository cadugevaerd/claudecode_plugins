---
description: Iniciar desenvolvimento incremental definindo MVP mínimo e escopo da primeira iteração
---

# Start Incremental Development

Este comando inicia o processo de desenvolvimento incremental identificando o **Minimum Viable Product (MVP)** e definindo claramente o que FAZER e o que NÃO FAZER na primeira iteração.

## 🎯 Objetivo

Definir o menor escopo possível que entrega valor, evitando funcionalidades prematuras e over-engineering.

## 📋 Como usar

```
/start-incremental "descrição do objetivo geral"
```

## 🔍 Processo de Execução

Quando este comando for executado, você DEVE:

### 1. Detectar Tipo de Projeto (Novo vs Legacy)

**IMPORTANTE**: Este comando é para NOVOS projetos. Se o projeto já existe, recomende comandos apropriados.

**Detectar projeto LEGACY se**:
- Existem arquivos de código (.py, .js, .ts, etc.) além de configuração
- Estrutura de diretórios já existe (src/, lib/, app/)
- Arquivo de dependências existe (package.json, pyproject.toml, requirements.txt)
- Git history com múltiplos commits

**Se projeto LEGACY detectado**:
```
⚠️  PROJETO EXISTENTE DETECTADO
═══════════════════════════════════════════

Detectei que este projeto já possui código existente.

O comando /start-incremental é para NOVOS projetos.

Para projetos legacy, use:

🔄 Opção 1: Análise Completa + PRD Retroativo
   /adopt-incremental
   └─ Analisa código existente
   └─ Identifica over-engineering
   └─ Cria PRD retroativo
   └─ Gera roadmap de simplificação
   └─ Configura CLAUDE.md

📋 Opção 2: Apenas Criar PRD Retroativo
   /prd-retrofit
   └─ Analisa código existente
   └─ Gera PRD a partir do código
   └─ Útil para documentar projeto sem mudanças

⚙️  Opção 3: Continuar com /start-incremental
   (Se quiser criar PRD do zero ignorando código existente)

Escolha (1, 2 ou 3):
```

**Se usuário escolher 1**: Executar `/adopt-incremental`
**Se usuário escolher 2**: Executar `/prd-retrofit`
**Se usuário escolher 3**: Continuar normalmente (projeto será tratado como novo)

---

### 2. Verificar Existência do PRD

```
🔍 VERIFICANDO PRD...

Procurando docs/PRD.md...
```

**Se PRD NÃO existe**:
```
⚠️  PRD não encontrado

💡 Recomendação: Executar /setup-project-incremental primeiro
   Isso cria CLAUDE.md + PRD v0.1 com informações iniciais

Continuar sem PRD? (s/n)
```

**Se PRD existe**:
```
✅ PRD encontrado (versão [versão])

Consultando objetivos e MVP definidos no PRD...
```

Extrair do PRD:
- Objetivos do projeto
- MVP definido (se fase >= Planejamento)
- Funcionalidades fora do MVP (YAGNI)

---

### 2. Questionar o Objetivo - MODO INTERATIVO

**IMPORTANTE**: Se nenhuma descrição foi fornecida como argumento, ou se PRD não existe, SEMPRE fazer perguntas interativas para criar um PRD completo.

```
═══════════════════════════════════════════
🎯 CRIAÇÃO DE PRD INTERATIVA
═══════════════════════════════════════════

Vou fazer algumas perguntas para criar um PRD completo
e bem estruturado para o seu projeto.

Responda de forma clara e objetiva. Você pode pular
perguntas digitando "pular" ou "skip".

═══════════════════════════════════════════
```

#### Pergunta 1: Contexto do Projeto

```
1️⃣ CONTEXTO DO PROJETO

O que você quer construir?
(Descreva em 1-2 frases o que é o projeto)

Exemplo: "Uma API REST para gerenciar tarefas de um time"
Exemplo: "Um dashboard web para visualizar métricas de vendas"
Exemplo: "Um CLI tool para automatizar deploys"

Sua resposta:
```

**Armazenar**: `projeto_descricao`

---

#### Pergunta 2: Problema a Resolver

```
2️⃣ PROBLEMA A RESOLVER

Que problema REAL você está tentando resolver?
(Seja específico sobre a dor/necessidade atual)

Exemplo: "Times perdem tarefas porque usam planilhas Excel desorganizadas"
Exemplo: "Gerentes perdem 2h/dia consolidando relatórios manualmente"
Exemplo: "Deploy manual está causando erros e downtime"

Sua resposta:
```

**Armazenar**: `problema`

---

#### Pergunta 3: Usuário Final

```
3️⃣ USUÁRIO FINAL

Quem vai usar este sistema?
(Seja específico sobre persona/papel)

Exemplo: "Desenvolvedores do time de produto"
Exemplo: "Gerentes de vendas regionais"
Exemplo: "DevOps engineers da empresa"

Sua resposta:
```

**Armazenar**: `usuario_final`

---

#### Pergunta 4: Funcionalidade Principal

```
4️⃣ FUNCIONALIDADE PRINCIPAL

Qual a ÚNICA funcionalidade mais importante?
(Se você pudesse ter apenas UMA coisa funcionando, qual seria?)

Exemplo: "Criar e listar tarefas"
Exemplo: "Gráfico de vendas totais do mês"
Exemplo: "Deploy com um comando"

Sua resposta:
```

**Armazenar**: `funcionalidade_principal`

---

#### Pergunta 5: Outras Funcionalidades (Opcional)

```
5️⃣ OUTRAS FUNCIONALIDADES

Que outras funcionalidades você imagina?
(Liste outras features que PODEM ser úteis - vamos priorizar depois)

Digite uma por linha, ou "pronto" quando terminar:

Exemplo:
- Atribuir tarefas a pessoas
- Filtrar tarefas por status
- Notificações de tarefas atrasadas
- Exportar para CSV

Suas respostas (digite "pronto" para finalizar):
```

**Armazenar**: `funcionalidades_extras` (lista)

---

#### Pergunta 6: O que NÃO Fazer (YAGNI)

```
6️⃣ O QUE NÃO FAZER AGORA

Tem algo que você SABE que NÃO deve fazer na v1?
(Features complexas, integrações, otimizações prematuras...)

Exemplo: "Autenticação OAuth (usar apenas API key v1)"
Exemplo: "Exportar para PDF (só CSV por enquanto)"
Exemplo: "Cache Redis (começar sem cache)"

Digite uma por linha, ou "pular" se não tiver:
```

**Armazenar**: `fora_de_escopo` (lista)

---

#### Pergunta 7: Prioridade #1 para MVP

```
7️⃣ PRIORIDADE #1 PARA MVP

Revisando suas respostas, qual funcionalidade deve
estar pronta PRIMEIRO para considerar um MVP?

Funcionalidades mencionadas:
1. [funcionalidade_principal]
2. [funcionalidades_extras[0]] (se houver)
3. [funcionalidades_extras[1]] (se houver)
...

Qual o mínimo absoluto para ter valor? (número ou descrever)

Sua resposta:
```

**Armazenar**: `mvp_prioridade`

---

#### Pergunta 8: Como Medir Sucesso (Opcional)

```
8️⃣ MÉTRICA DE SUCESSO

Como você vai saber se o projeto está funcionando bem?
(Métrica mensurável, não apenas "funcionar")

Exemplo: "Time usa o sistema para 80%+ das tarefas"
Exemplo: "Gerentes reduzem tempo de relatório de 2h para 15min"
Exemplo: "Zero deploys falhados em 1 mês"

Sua resposta (ou "pular"):
```

**Armazenar**: `metrica_sucesso`

---

#### Pergunta 9: Prazo/Urgência (Opcional)

```
9️⃣ PRAZO / URGÊNCIA

Tem algum prazo ou deadline?
(Ajuda a definir escopo realista)

Exemplo: "Preciso de MVP em 2 semanas"
Exemplo: "Sem prazo fixo, mas quanto antes melhor"
Exemplo: "Apresentação para stakeholders em 1 mês"

Sua resposta (ou "pular"):
```

**Armazenar**: `prazo`

---

#### Pergunta 10: Formato de Spikes de Validação Técnica

```
🔟 FORMATO DE SPIKES DE VALIDAÇÃO

Quando precisar fazer Spikes de Validação Técnica (exploração de tecnologias,
protótipos, provas de conceito), qual formato você prefere?

📓 Opção 1: Notebooks (.ipynb)
   ✅ Exploração interativa e incremental
   ✅ Documentação inline com markdown
   ✅ Visualizações e gráficos integrados
   ✅ Histórico de experimentação preservado
   ✅ Fácil compartilhamento de aprendizados
   ⚠️  Requer Jupyter/VS Code com suporte

📄 Opção 2: Scripts Python (.py)
   ✅ Mais leve e simples
   ✅ Funciona em qualquer editor
   ✅ Mais fácil versionamento
   ⚠️  Menos interativo

💡 Recomendação: Notebooks são melhores para exploração técnica

Sua escolha (1=notebooks, 2=scripts, ou "pular" para decidir depois):
```

**Armazenar**: `formato_spikes`

**Valores possíveis**:
- `"notebooks"` - se usuário escolher 1
- `"scripts"` - se usuário escolher 2
- `"nao-definido"` - se usuário pular

---

#### Resumo e Confirmação

```
═══════════════════════════════════════════
📋 RESUMO DO SEU PRD
═══════════════════════════════════════════

Projeto: [projeto_descricao]
Problema: [problema]
Usuário: [usuario_final]

🎯 MVP (Prioridade #1):
- [mvp_prioridade]

⚙️ Outras Funcionalidades (priorizadas depois):
- [funcionalidades_extras]

❌ Fora de Escopo (YAGNI - não fazer v1):
- [fora_de_escopo]

📊 Métrica de Sucesso:
- [metrica_sucesso]

🗓️ Prazo:
- [prazo]

🔬 Formato de Spikes de Validação:
- [formato_spikes] (notebooks/scripts/não-definido)

═══════════════════════════════════════════

Este resumo está correto? (s/n/editar)

- s: Criar PRD.md com estas informações
- n: Cancelar e recomeçar
- editar: Ajustar uma resposta específica
```

**Se usuário escolher "editar"**:
```
Qual pergunta deseja ajustar? (1-10)
```
Permitir reresponder a pergunta escolhida.

**Se usuário confirmar (s)**:
Prosseguir para criar PRD.md completo usando o template em `templates/PRD.md` e preenchendo com as respostas coletadas.

**Se PRD existe**: Alinhar novas respostas com objetivos documentados no PRD existente

---

### 3. Definir MVP (Iteração 1)

Identificar apenas o ESSENCIAL:

```
📦 DESENVOLVIMENTO INCREMENTAL - MVP

Objetivo: [descrição do objetivo]

🎯 MVP (Iteração 1):
- [ ] Funcionalidade 1 (mínima)
- [ ] Funcionalidade 2 (mínima)
- [ ] Funcionalidade 3 (mínima)

❌ NÃO FAZER AGORA (YAGNI):
- Feature prematura 1
- Feature prematura 2
- Abstração desnecessária
- Configuração complexa
- Validações avançadas
- Sistema de erros elaborado
- Logging sofisticado
- Cache/otimização prematura

💡 Princípio: Fazer o caso mais simples funcionar primeiro

Características do MVP:
• Sem abstrações (código direto)
• Sem patterns (adicionar quando padrões emergirem)
• Validações mínimas
• Configuração hardcoded OK para MVP
• Foco em FUNCIONAR, não em "código bonito"

Começar implementação? (s/n)
```

### 3. Aplicar Princípios YAGNI

**SEMPRE questionar**:
- "Você precisa disso AGORA?"
- "O que acontece se não implementar isso?"
- "Isso resolve o problema mínimo?"

**Evitar frases como**:
- ❌ "Vamos preparar para o futuro..."
- ❌ "Caso precise adicionar..."
- ❌ "Para facilitar expansão..."
- ❌ "Seguindo clean architecture..."

**Preferir frases como**:
- ✅ "Vamos fazer funcionar primeiro"
- ✅ "Podemos adicionar isso quando necessário"
- ✅ "Foco no caso de uso atual"
- ✅ "Refatoramos quando o padrão emergir"

## 📚 Exemplos Práticos

### Exemplo 1: Sistema de Processamento de Emails

**Objetivo do usuário**: "Criar sistema de processamento de emails com validação, fila e logging"

**Resposta correta do MVP**:
```
📦 MVP - PROCESSAMENTO DE EMAIL

🎯 MVP (Iteração 1):
- [ ] Receber um email (string)
- [ ] Processar (função process_email simples)
- [ ] Retornar "processado" ou "erro"

❌ NÃO FAZER AGORA:
- Sistema de filas (RabbitMQ, Celery)
- Validação complexa de email
- Múltiplos processadores
- Logging estruturado
- Rate limiting
- Retry automático
- Métricas e monitoramento

💡 Código MVP:
def process_email(email: str) -> str:
    # Apenas processar caso mais simples
    if not email:
        return "erro"
    # Lógica mínima aqui
    return "processado"

Implementar este MVP? (s/n)
```

### Exemplo 2: API REST com LangGraph

**Objetivo do usuário**: "Criar API REST com LangGraph para processar documentos, com cache, validação, retry e monitoramento"

**Resposta correta do MVP**:
```
📦 MVP - API LANGGRAPH DOCUMENTOS

🎯 MVP (Iteração 1):
- [ ] Endpoint POST /process
- [ ] Receber documento (texto simples)
- [ ] LangGraph com 1 node (process)
- [ ] Retornar resultado

❌ NÃO FAZER AGORA:
- Cache Redis
- Validação Pydantic complexa
- Retry logic
- Middleware de autenticação
- Logging estruturado
- Métricas Prometheus
- Múltiplos nodes no graph
- State complexo

💡 Código MVP:
from fastapi import FastAPI
from langgraph.graph import StateGraph

app = FastAPI()

def process_node(state):
    return {"result": "processed"}

graph = StateGraph(dict)
graph.add_node("process", process_node)
graph.set_entry_point("process")
graph.set_finish_point("process")
app_graph = graph.compile()

@app.post("/process")
def process_doc(text: str):
    result = app_graph.invoke({"text": text})
    return result

Implementar este MVP? (s/n)
```

## ⚠️ Sinais de Over-Engineering

> **📘 Complete Guide**: See `docs/YAGNI_REFERENCE.md` section "Signs of Over-Engineering in MVP"

Quick MVP anti-patterns:
- ❌ **Abstract classes in MVP** → Use simple function
- ❌ **Factory Pattern in MVP** → Use direct call
- ❌ **Complex configuration in MVP** → Use hardcoded constants (OK for MVP!)

**For detailed examples**, refer to `docs/YAGNI_REFERENCE.md`.

## 🎓 Princípios a Seguir

> **📘 Core Principles**: Full list in `docs/YAGNI_REFERENCE.md`

Quick principles:
1. **YAGNI** - Don't implement until REALLY necessary
2. **Simplicity First** - Simple code > Premature abstractions
3. **Evolutionary Architecture** - Architecture evolves with requirements
4. **Fast Feedback** - MVP tests hypotheses quickly
5. **Right-Time Refactoring** - Refactor when patterns EMERGE

## 🚀 Próximos Passos Após MVP

Após implementar o MVP:

1. **Testar**: Garantir que funciona para o caso mais simples
2. **Executar**: Colocar em uso real (mesmo que limitado)
3. **Observar**: Identificar próxima funcionalidade REALMENTE necessária
4. **Iterar**: Usar `/add-increment` para adicionar próxima feature

**IMPORTANTE**: Não planejar múltiplas iterações antecipadamente! Cada iteração revela o que a próxima deve ser.

## 💡 Lembre-se

- MVP não precisa ser "código bonito"
- Hardcode é OK para MVP
- Abstrações vêm depois, quando padrões emergirem
- Funcionar > Perfeição
- Simples > Complexo
- Agora > Futuro hipotético