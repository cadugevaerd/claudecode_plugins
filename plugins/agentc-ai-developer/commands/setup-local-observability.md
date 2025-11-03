---
description: Interactive guide through Microprocesso 1.2 - Setup Local + Observability. Continues directly from /brief (which created the repo). Guides through 8 activities (skips Git, already done), Python venv setup, dependencies installation, environment configuration, and LangSmith integration. Provides templates inline and validates each step interactively.
---

# 🚀 Microprocesso 1.2: Setup Local + Observabilidade

**Continuação direta do `/brief`**. Este comando guia você interativamente através das **8 atividades** (Git já feito!) para criar um **ambiente reproduzível com observabilidade completa**.

## 📋 O que é Microprocesso 1.2?

**Microprocesso 1.2** é a segunda fase do desenvolvimento agentic, onde você:

✅ Configura **Python venv** isolado
✅ Instala **dependências mínimas** (langchain, anthropic, python-dotenv, langsmith)
✅ Configura **variáveis de ambiente** com segurança (.env + .gitignore)
✅ Integra **LangSmith** para observabilidade completa
✅ Valida tudo com **testes automatizados**

**Pré-requisito**: Ter executado `/brief` (que criou seu repositório Git + README.md)

**Duração**: ~1.5 horas
**Saída**: Ambiente pronto para Microprocesso 1.3 (Spike Agentic)

---

## 🎯 Como Este Comando Funciona

```
┌─────────────────────────────────────────────────┐
│  RESUMO: Você Depois do /brief                 │
├─────────────────────────────────────────────────┤
│  ✅ Repositório Git criado (feito pelo /brief) │
│  ✅ README.md com seu Brief Mínimo             │
│  ❌ Python venv                                │
│  ❌ Dependências instaladas                    │
│  ❌ .env configurado                           │
│  ❌ LangSmith integrado                        │
│  ❌ Observabilidade ativa                      │
└─────────────────────────────────────────────────┘
         👇 Você executa /setup-local-observability
         👇 Escolhe seu modo: Guiado | Automático | Misto
┌─────────────────────────────────────────────────┐
│  RESUMO: Você Depois deste Comando             │
├─────────────────────────────────────────────────┤
│  ✅ Repositório Git criado                     │
│  ✅ README.md com seu Brief Mínimo             │
│  ✅ Python venv                                │
│  ✅ Dependências instaladas                    │
│  ✅ .env configurado                           │
│  ✅ LangSmith integrado                        │
│  ✅ Observabilidade ativa                      │
│  ✅ Tudo validado                              │
└─────────────────────────────────────────────────┘
         👇 Pronto para Microprocesso 1.3
```

---

## 🔄 O Fluxo Completo

### Passo 1: Validação (1 minuto)

O comando verifica:
- ✅ Você está no diretório correto?
- ✅ Existe `README.md` com Brief Mínimo (criado pelo /brief)?
- ✅ Existe `.git/`? (criado pelo /brief)
- ✅ Existe `.gitignore`? (criado pelo /brief)

### Passo 2: Leitura de Contexto (1 minuto)

O comando lê seu `README.md` e extrai:
- Nome do projeto
- Descrição (what does it do?)
- Input/Output esperados
- Ferramentas/APIs

Isso contextualize cada atividade.

### Passo 3: Guia Interativo (8 Atividades - ~1.5 horas)

Para cada atividade:
1. **Explica** o que precisa ser feito
2. **Fornece** templates prontos para copiar/colar
3. **Guia** passo-a-passo
4. **Pede confirmação** quando terminar
5. **Valida** que funcionou
6. **Marca como ✅ Completo**
7. **Passa** para próxima

### Passo 4: Relatório Final (2 minutos)

Mostra:
- ✅ Todas as 8 atividades completadas
- 📊 Status de cada componente
- 🔍 Como validar que tudo funciona
- 🚀 Próximos passos (Microprocesso 1.3)

---

## 📊 As 8 Atividades (Git já feito!)

| # | Atividade | Bloco | Objetivo | Tempo |
|---|-----------|-------|----------|-------|
| 1️⃣ | ~~Criar Repositório Git~~ | ~~A~~ | ✅ Já feito pelo `/brief` | - |
| **2️⃣** | **Setup Python venv** | **A** | **Criar ambiente isolado** | **10 min** |
| **3️⃣** | **Instalar Dependências** | **A** | **pip install packages** | **5 min** |
| **4️⃣** | **Configurar .env** | **A** | **.env + .env.example** | **10 min** |
| **5️⃣** | **Validar Environment** | **A** | **Testar imports** | **5 min** |
| **6️⃣** | **Registrar LangSmith** | **B** | **Criar conta + API key** | **10 min** |
| **7️⃣** | **Configurar LangSmith** | **B** | **Setup local + integração** | **20 min** |
| **8️⃣** | **Integrar Traces** | **B** | **@trace no código** | **20 min** |

**Bloco A** (Atividades 2-5): ~30 minutos - Git + Python Setup
**Bloco B** (Atividades 6-8): ~50 minutos - Observabilidade

---

## 🎨 Estrutura Visual

```
┌──────────────────────────────────────────────────┐
│       MICROPROCESSO 1.2: 8 ATIVIDADES            │
│                                                  │
│  ENTRADA: Repositório do /brief ✅              │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │ BLOCO A: PYTHON SETUP (2-5)               │  │
│  ├────────────────────────────────────────────┤  │
│  │ 2️⃣ Setup Python venv                       │  │
│  │ 3️⃣ Instalar Dependências Mínimas         │  │
│  │ 4️⃣ Configurar .env                        │  │
│  │ 5️⃣ Validar Environment                    │  │
│  └────────────────────────────────────────────┘  │
│                  ↓ (~30 min)                     │
│  ┌────────────────────────────────────────────┐  │
│  │ BLOCO B: LANGSMITH (6-8)                  │  │
│  ├────────────────────────────────────────────┤  │
│  │ 6️⃣ Registrar LangSmith                     │  │
│  │ 7️⃣ Configurar LangSmith Localmente       │  │
│  │ 8️⃣ Integrar Traces no Código             │  │
│  └────────────────────────────────────────────┘  │
│                  ↓ (~50 min)                     │
│  ✅ SAÍDA: Ambiente Reproduzível + Observável  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

```bash
# 1. Você já executou /brief (criou repositório)
# 2. Execute este comando no diretório do projeto
/setup-local-observability

# 3. ESCOLHA SEU MODO:
#    [1] Guiado: Você faz tudo manualmente, comando orienta e valida
#    [2] Automático: Comando cria tudo sozinho (você apenas aprova por atividade)
#    [3] Misto: Você escolhe por atividade (alguns manual, alguns automático)

# 4. ~30 min até ~1.5 horas (depende do modo escolhido)
# 5. Ambiente pronto! ✨
```

---

## 🎯 Modos de Operação

### Modo 1: Guiado (Padrão)

**Você quer controle total e aprende fazendo**

```
Para cada atividade:
├─ Comando explica o que fazer
├─ Fornece templates prontos para copiar/colar
├─ Você executa os passos
├─ Comando valida que funcionou
└─ Próxima atividade

Tempo: ~1.5 horas
Aprende: ✅ Sim, muito
Controle: ✅ Total
```

**Bom para**:
- Primeira vez configurando
- Quer entender cada passo
- Quer customizar coisas
- Tem tempo disponível

---

### Modo 2: Automático

**Comando faz tudo, você só aprova**

```
Para cada atividade:
├─ Comando descreve o que será criado
├─ "Deseja que eu crie isso? (S/N)"
├─ Se S: Comando cria arquivos, estrutura, configuração
│          Mostra exatamente o que foi criado
│          Você revisa a saída
├─ Se N: Ignora e passa para próxima
└─ Próxima atividade

Tempo: ~30-45 minutos
Aprende: ❌ Não muito
Controle: ✅ Parcial (aprova por atividade)
```

**Bom para**:
- Já fez setup antes
- Quer ser rápido
- Confia no template padrão
- Pouco tempo disponível

**⚠️ IMPORTANTE**: Comando NÃO executa bash de verdade. Apenas descreve e documenta o que FARIA criar.

---

### Modo 3: Misto (Escolhe por Atividade)

**Você decide para cada atividade se quer fazer manual ou automático**

```
Atividade 2 (Setup Python venv):
├─ Modo? [1] Manual [2] Automático
├─ Você escolhe → Segue esse fluxo

Atividade 3 (Instalar Dependências):
├─ Modo? [1] Manual [2] Automático
├─ Você escolhe → Segue esse fluxo

[... cada atividade você escolhe ...]

Tempo: ~45 min até ~1.5 horas (depende das escolhas)
Aprende: ✅ Variável
Controle: ✅ Total - você escolhe cada um
```

**Bom para**:
- Quer mix (alguns automático, alguns manual)
- Já sabe algumas coisas, não sabe outras
- Confiante com alguns passos, quer aprender outros

---

## 📊 Comparação de Modos

| Aspecto | Guiado | Automático | Misto |
|---------|--------|-----------|-------|
| **Tempo** | ~1.5h | ~30-45min | ~45min-1.5h |
| **Aprende** | ✅ Muito | ❌ Pouco | ✅ Variável |
| **Controle** | ✅ Total | ✅ Parcial | ✅ Total |
| **Melhor para** | Iniciante | Experiente | Híbrido |
| **Customização** | ✅ Fácil | ❌ Difícil | ✅ Flexível |

---

## 🎪 Estrutura de Cada Atividade (Guiado)

```
╔════════════════════════════════════════════════╗
║ ATIVIDADE N: [Nome]                           ║
║ Tempo: ~X min | Modo: Guiado                  ║
╚════════════════════════════════════════════════╝

📖 O QUE FAZER:
[Explicação clara do objetivo dessa atividade]

🎯 VALIDAÇÃO ESPERADA:
[O que precisa estar funcionando ao final]

📋 PASSOS:
1. [Passo 1]
   → Detalhes e motivos
2. [Passo 2]
   → Detalhes e motivos
3. [etc...]

💾 TEMPLATE PRONTO:
[Código ou comandos prontos para copiar/colar]

🔧 COMO CRIAR:
[Instruções específicas por SO]
- macOS: [comandos]
- Linux: [comandos]
- Windows: [comandos]

✅ VALIDAR QUANDO TERMINAR:
[Comandos para testar que funcionou]

❌ TROUBLESHOOTING:
[Se algo deu errado, aqui está o que fazer]

→ Continuar para próxima atividade? (S/N)
```

---

## 🎪 Estrutura de Cada Atividade (Automático)

```
╔════════════════════════════════════════════════╗
║ ATIVIDADE N: [Nome]                           ║
║ Tempo: ~X min | Modo: Automático              ║
╚════════════════════════════════════════════════╝

📖 O QUE SERÁ CRIADO:
[Descrição clara do que será feito]

📋 ARQUIVOS A CRIAR:
- arquivo1.txt (X linhas)
- arquivo2.py (Y linhas)
- pasta/arquivo3.json
[etc...]

💾 CONTEÚDO ESPERADO:
[Exemplo do que será gerado]

🤔 DESEJA QUE EU CRIE ISSO? (S/N/V)
- S: Criar agora (simular criação)
- N: Pular para próxima
- V: Ver mais detalhes antes de decidir

[Se S] ✅ CRIADO:
Arquivos gerados:
- ✅ arquivo1.txt
- ✅ arquivo2.py
[etc...]

→ Próxima atividade? (S/N)
```

---

## 📋 Checklist Geral (O que será feito)

Ao completar este comando:

```
✅ BLOCO A: Python Setup
  ✅ venv criado e ativado
  ✅ Python 3.10+ confirmado
  ✅ Dependências instaladas:
     • langchain
     • anthropic
     • langsmith
     • python-dotenv
     • pydantic
     • pytest
  ✅ .env.example criado (template)
  ✅ .env local criado (com secrets)
  ✅ .gitignore protege .env ✓
  ✅ Imports funcionam ✓

✅ BLOCO B: Observabilidade
  ✅ Conta LangSmith criada
  ✅ API key obtida
  ✅ src/langsmith_config.py criado
  ✅ src/agent.py com @trace criado
  ✅ Traces aparecem no dashboard ✓

✅ Estrutura Final
  ✅ src/ com código
  ✅ tests/ com validações
  ✅ .env e .env.example
  ✅ requirements.txt
  ✅ README.md com Quick Start

✅ Reprodutibilidade
  ✅ Alguém consegue fazer:
     git clone → setup → run
```

---

## 📚 Estrutura de Arquivos Esperada

Após completar, terá isso:

```
seu_agente_ai/
├── .git/                          # ✅ Criado pelo /brief
├── .gitignore                     # ✅ Criado pelo /brief
├── README.md                      # ✅ Criado pelo /brief (seu Brief)
├── .env                           # ← Criaremos (Atividade 4)
├── .env.example                   # ← Criaremos (Atividade 4)
├── requirements.txt               # ← Criaremos (Atividade 3)
├── venv/                          # ← Criaremos (Atividade 2)
│
├── src/                           # ← Criaremos
│   ├── __init__.py
│   ├── config.py                  # ← Criaremos (Atividade 4)
│   ├── langsmith_config.py        # ← Criaremos (Atividade 7)
│   └── agent.py                   # ← Criaremos (Atividade 8)
│
└── tests/                         # ← Criaremos
    ├── __init__.py
    ├── test_environment.py        # ← Criaremos (Atividade 5)
    └── test_langsmith_int.py      # ← Criaremos (Atividade 8)
```

---

## ⚠️ Pré-Requisitos

Antes de executar este comando, você deve ter:

✅ **Executado `/brief`**
  - Projeto criado em diretório com Git
  - README.md com seu Brief Mínimo
  - .git/ e .gitignore já existem

✅ **Python 3.10+ instalado**
  - Verificar: `python --version` ou `python3 --version`

✅ **API Key de um LLM**
  - Guardar em segurança (será usada em .env)

✅ **Email para LangSmith** (será solicitado na Atividade 6)
  - De: https://smith.langchain.com

✅ **~1.5 horas disponível**
  - Não é automático - você guia através dos passos
  - Requer criar arquivos, instalar packages, testar

---

## 🔍 Como o Comando Guia

Cada atividade segue este padrão:

```
╔════════════════════════════════════════════════╗
║ ATIVIDADE N: [Nome da Atividade]              ║
║ Tempo: ~[X min]                                ║
╚════════════════════════════════════════════════╝

📖 O QUE FAZER:
[Explicação clara do objetivo]

🎯 VALIDAÇÃO:
[O que precisa estar funcionando ao final]

📋 PASSOS:
1. [Passo 1]
2. [Passo 2]
3. [etc...]

💾 TEMPLATE PRONTO (copiar/colar):
[Código completo, pronto para usar]

🔧 COMO CRIAR:
[Instruções específicas]
   - Se macOS: [instruções]
   - Se Linux: [instruções]
   - Se Windows: [instruções]

✅ CONFIRME QUANDO TERMINAR:
[Validação manual que você pode fazer]
[Se não funcionar, aqui está o troubleshooting]

Deseja continuar para próxima atividade? (S/N)
```

---

## 💬 Durante o Comando

O comando é **completamente interativo**:

- 🎤 Faz perguntas
- 📖 Explica cada passo
- 💾 Fornece templates completos
- ✅ Pede confirmação
- 🔍 Valida que funcionou
- 📊 Mostra progresso
- ❌ Se algo falhar, oferece troubleshooting

---

## 🚀 Próximos Passos

Após completar Microprocesso 1.2:

```
✅ Seu ambiente está pronto!

→ Próximo: Microprocesso 1.3 (Spike Agentic)
   Duração: 2 horas
   O que: Construir agente mínimo
   Entrada: Ambiente pronto (✅ você tem)
   Saída: Agente executando + traces no LangSmith

Execute quando estiver pronto:
  /setup-spike-agentic
  (comando para Microprocesso 1.3)
```

---

## ❓ Perguntas Frequentes

**P: E se eu já comecei o setup?**
A: O comando detecta o que já existe (venv, .env, etc) e continua de onde parou.

**P: Posso fazer apenas algumas atividades?**
A: Sim! O comando deixa você pular atividades já completas.

**P: E se eu cometi um erro no Brief?**
A: Edite seu `README.md` e continue. O setup não depende do Brief estar 100% perfeito.

**P: LangSmith é realmente necessário?**
A: Sim. Observabilidade é crítica para entender o comportamento do agente. LangSmith tem free tier generoso.

**P: Quanto de espaço em disco preciso?**
A: ~200-500MB para venv + packages. Depende das dependências.

**P: Posso fazer em etapas?**
A: Sim! Cada atividade é independente. Pode fazer tudo de uma vez ou em partes.

---

## 🎓 Por que Este Setup Importa?

| Benefício | Por quê |
|-----------|--------|
| **Reprodutibilidade** | Qualquer pessoa consegue clonar e rodar |
| **Segurança** | Secrets em .env, protegidos pelo .gitignore |
| **Observabilidade** | LangSmith rastreia CADA execução |
| **Debugging** | Traces facilitam encontrar problemas |
| **Colaboração** | Novo dev consegue contribuir rapidinho |
| **CI/CD Ready** | Está setup pronto para automação |

---

## 🔗 Veja Também

- `/brief` - Microprocesso 1.1 (cria o repositório)
- `/setup-spike-agentic` - Microprocesso 1.3 (próximo passo)
- Documentação: `docs/microprocesso_1_2_completo.md`

---

**Pronto? Execute:**

```bash
/setup-local-observability
```

**E siga as instruções interativas! 🚀**

O comando vai guiar você através de cada atividade, com templates, validações e tudo que você precisa.

Quando terminar, seu ambiente estará 100% pronto para Microprocesso 1.3! ✨