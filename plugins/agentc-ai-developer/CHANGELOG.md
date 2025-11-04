# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)

## [0.8.0] - 2025-11-03

### Adicionado

- **Novo modo `issues`** para comando `/backlog`

  - Gerencia issues de S2.9 (validação com PO) e S2.8 (rollback)
  - Rastreia problemas de forma estruturada em BACKLOG.md
  - Classifica por severidade (ALTA/MÉDIA/BAIXA)
  - Propõe próximas ações: refine, fast-track, defer, ou rollback

- **Template estruturado de BACKLOG.md**

  - Seção 1: Features e Slices Priorizadas em formato tabular
  - Cálculo automático de Score (Impacto / Horas)
  - Coluna de Status com indicadores visuais (➡️ / 🔄 / ✅ / ⚪ / 🚀 / 🚨)
  - Seção 2: Issues e Feedback com rastreamento de problemas
  - Seção 3: Notas de Integração com referências a SLICE_N_TRACKER.md

- **Suporte a decisões de backlog**

  - Fast-Track identification (\<1h, low risk)
  - Critical rollback triggers
  - Issue-to-slice conversion
  - Deferred item tracking

### Modificado

- Descrição do comando `/backlog` atualizada para mencionar issue tracking
- Argument-hint expandido: `[create|update|view|refine|issues]`
- Template de BACKLOG.md agora obrigatório em create mode

## [0.7.0] - 2025-11-03

### Adicionado

- **Novo comando** `/analyze-slices` para validação de slices contra os gates S1.1

  - Gate 1: Duração 3-6 horas para ciclo padrão
  - Gate 2: Score de impacto >= 2.0 (razão impacto-esforço)
  - Gate 3: Implementação reversível com plano de rollback
  - Gate 4: Isolamento arquitetural com baixo acoplamento
  - Gate 5: Alinhamento com métricas de sucesso do MVP
  - Três modos de análise: `validate`, `refine`, `auto`

- **Modo refinement aprimorado** para comando `/backlog`

  - Novo modo `refine` para análise e refinamento de slices
  - Analisa falhas de gates para cada slice
  - Propõe refinamentos (divisão, aumento de impacto, isolamento)
  - Atualiza BACKLOG.md com slices refinadas
  - Re-valida melhorias automaticamente

- **Keywords expandidas** com `slice-validation`, `s1-gates`, `backlog-refinement`, `macrofluxo`

### Modificado

- Descrição do plugin atualizada para refletir seis comandos (era cinco)
- plugin.json e marketplace.json com descrições melhoradas
- Comando `/backlog` com novos argumentos `[create|update|view|refine]`

## [0.5.0] - 2025-11-03

### Adicionado

- **Novo Comando** `/spike-agentic` (Microprocesso 1.3)
  - AUTONOMOUS command para validação de arquitetura agêntica
  - Validates prerequisites from Microprocesso 1.2 completion
  - Generates `docs/microprocesso-1.3-spike-agentic.md` com guia completo
  - 4 fases: Setup (done), Graph (60-90min), Tests (30min), LangSmith validation (30min)
  - Validates agentic loop (Think → Act → Observe → Think again)
  - Time-boxed spike exploration (3-4 horas)
- **Novo Skill** `spike-agentic` para conhecimento detalhado
  - Complete knowledge base para implementação de agent spike com agentic loop
  - Detailed explanation de State, 4 Nodes, Edges, Route Logic
  - Mock tool patterns para validação de arquitetura
  - Happy-path test patterns (with/without tool)
  - LangSmith trace validation e tree structure inspection
  - Red flags e troubleshooting para falhas de spike
  - Auto-discovery por Claude durante implementação de agent
  - Tools permitidas: Read, Grep, Glob, Write, Bash
- **Arquivo de Suporte** `skills/spike-agentic/GENERATE_GUIDE.md`
  - Template e instruções para gerar `docs/microprocesso-1.3-spike-agentic.md`
  - Document structure e content guidelines
  - Validation checklist para geração completa

### Modificado

- **README.md** - Adicionado `/spike-agentic` command documentation
  - Quick start section com Microprocesso 1.1/1.2/1.3 flow
  - Updated Roadmap para v0.5.0 com Microprocesso 1.3
  - Updated "Support & Contributing" com v0.5.0 e spike-agentic skill
  - Updated Commands section com `/spike-agentic` entry
  - Updated Overview com Microprocesso 1.1/1.2/1.3
  - Skills section agora inclui spike-agentic skill documentation

### Melhorias

- **Command Best Practices**: `/spike-agentic` segue padrões rigorosamente
  - AUTONOMOUS badge com clara responsabilidade
  - TL;DR section com processo resumido
  - Progressive disclosure: detalhes em skill, documentação gerada
  - Conciso (70 linhas) seguindo recommended 50-80 linhas pattern
- **Architecture Validation**: Loop agêntico agora é primeira incerteza validada
  - Foco em viabilidade da arquitetura (questão central)
  - Mock tools removem variáveis de conectividade
  - 2 testes suficientes para validar loop agêntico
  - Happy-path focus (80% do spike) vs error handling (Microprocesso 1.4)

## [0.4.0] - 2025-11-02

### Adicionado

- **Novo Skill** `microprocesso-1-2` para conhecimento detalhado de setup (675 linhas)
  - Complete knowledge base para as 8 atividades de Microprocesso 1.2
  - Provides step-by-step guidance, templates, troubleshooting, validation
  - Support para todos os 3 operating modes (Guiado, Automático, Misto)
  - Auto-discovery por Claude para ajuda durante setup
  - Tools permitidas: Read, Bash, Write para operações de ambiente
- **Documentação de Best Practices** em plugin-creator.md
  - Comprehensive "Command Best Practices" section (~400 linhas)
  - Anatomia de excelentes commands, emojis para visual hierarchy
  - Behavioral badges (INTERACTIVE, AUTONOMOUS, DELEGATED)
  - Progressive disclosure pattern para commands >80 linhas
  - 3 command templates por tipo, quality checklist
  - Scoring de existing commands, anti-patterns
  - Decision matrix para Skills vs Commands vs Agents

### Modificado

- **Refatoração do comando `/brief`** para seguir best practices
  - Added INTERACTIVE badge e TL;DR section
  - Visual prerequisites section com checkmarks
  - Improved structure com emoji scanning
  - Maintained all existing content com melhor organização
- **Refatoração do comando `/setup-local-observability`** (556 → 146 linhas)
  - Complete rewrite com progressive disclosure pattern
  - Command agora é overview conciso, skill contém 675 linhas de detalhe
  - Added INTERACTIVE badge e TL;DR
  - 3 operating modes table para comparação rápida
  - Links to skill microprocesso-1-2 para detailed guidance
- **Refatoração do comando `/update-claude-md`** (94 linhas)
  - Added AUTONOMOUS badge e TL;DR section
  - Renamed "Using the Command" to "🚀 Usage"
  - Visual improvements com emojis (📝, ✨, ⚠️)
  - Better structure com visual hierarchy
  - Prerequisite checklist com time estimate (\<1 minute)
- **README.md** completamente atualizado
  - New "## Skills" section documentando microprocesso-1-2
  - Detailed description de quando skill é auto-invocada
  - Updated Roadmap para v0.4.0 com skill documentation
  - Updated "Support & Contributing" com v0.4.0 e skill mention
  - Better organization com Skills section entre Agents e Legacy Agents

### Melhorias

- **Progressive Disclosure Pattern**: 3 commands agora seguem padrão rigorosamente
  - Commands ≤150 linhas com TL;DR, overview, quick start
  - Skill contém 675 linhas de detailed knowledge
  - Commands referenciam skill para detailed guidance
- **Visual Hierarchy**: Consistent emoji usage e behavioral badges
  - 🎯 What It Does, 🚀 Usage, 📝 What Gets Added, ✨ Key Features, ⚠️ Troubleshooting
  - Badges indicam tipo de comando: INTERACTIVE, AUTONOMOUS
  - TL;DR format padronizado: `action → process → result`
- **Command Quality**: All commands agora seguem best practices documentadas
  - Size limits respeitados (50-100 linhas ideal, max 150)
  - Structure patterns consistentes
  - Behavioral indicators claros
  - Progressive disclosure com referências a skills/agents
- **Documentation Completeness**:
  - microprocesso-1-2 skill com 675 linhas covers 8 atividades detalhadamente
  - Templates copy/paste prontos para todos os arquivos
  - Real examples em Python, bash, markdown
  - Troubleshooting coverage para 7+ common issues

### Informação de Versão

Este é o v0.4.0 (MINOR update) do Agentc AI Developer com:

- Novo skill `microprocesso-1-2` para progressive disclosure de setup knowledge
- Refatoração de todos 3 commands para seguir best practices
- Comprehensive command best practices documentation em plugin-creator.md
- Melhoria na arquitetura: commands como overview + skills como detailed knowledge
- Progressive disclosure pattern aplicado rigorosamente
- Visual hierarchy melhorada com badges e emojis
- README.md completamente atualizado com skill documentation

## [0.3.0] - 2025-11-02

### Adicionado

- **Novo comando** `/update-claude-md` para integração de projeto (máx 40 linhas)
  - Lê Brief Minimo do README.md gerado pelo `/brief`
  - Cria seção concisa no CLAUDE.md com guia de uso
  - Segue padrão progressive disclosure (conciso + referências)
- **Novo agente** `help-assistant` para suporte e orientação
  - Explica conceitos do Brief Minimo e metodologia
  - Fornece troubleshooting para `/brief` e `/setup-local-observability`
  - Esclarece conceitos técnicos (venv, .env, LangSmith, traces, Docker, etc.)
  - Oferece práticas recomendadas e alternativas

### Modificado

- Comando `/brief` agora 100% interativo (sem delegação a agente)
  - Todo o workflow de entrevista acontece no comando
  - Sem referências a "brief-assistant agent"
- Comando `/setup-local-observability` refletido com 3 modos funcionais
  - Modo Guiado: você executa, comando orienta
  - Modo Automático: descreve sem executar bash real
  - Modo Misto: você escolhe por atividade
- Descrição do plugin atualizada para refletir novo comando e agente
- README.md reorganizado com seções de Commands, Agents e Legacy Agents
- Keywords expandidas para incluir "help-assistant"

### Removido

- Agente `brief-assistant` (funcionalidade integrada no comando `/brief`)

### Informação de Versão

Este é o v0.3.0 (MINOR update) do Agentc AI Developer com:

- Comando `/brief` 100% interativo no comando (sem agente)
- Novo agente `help-assistant` para suporte especializado
- Novo comando `/update-claude-md` para integração de projetos com progressive disclosure
- Melhoria na arquitetura: separação clara de responsabilidades (commands/agents/skills)

## [0.2.0] - 2025-11-02

### Adicionado

- **Microprocesso 1.2**: Novo comando `/setup-local-observability` para setup de ambiente local
  - Guia interativo através de 8 atividades (Git já criado pelo `/brief`)
  - Setup Python venv com validações
  - Instalação de dependências mínimas (langchain, anthropic, langsmith, python-dotenv)
  - Configuração de variáveis de ambiente (.env + .env.example)
  - Integração completa com LangSmith para observabilidade
  - Validação de ambiente e testes automatizados
  - Suporte para projetos novos e existentes
  - Leitura de README.md do brief para contextualização

### Modificado

- Descrição do plugin agora reflete Microprocessos 1.1 (planning) e 1.2 (setup)
- README.md reorganizado com seções de "Microprocesso 1.1" e "Microprocesso 1.2"
- Roadmap expandido com menção a Microprocesso 1.3 (futuro)
- Keywords expandidas para incluir "setup", "environment", "langsmith", "observability", "microprocessos", "interactive"

### Melhorias

- Integração perfeita entre `/brief` (cria repositório) e `/setup-local-observability` (configura ambiente)
- Ambiente reproduzível garantido via requirements.txt
- Observabilidade completa com LangSmith desde o início
- Suporte a detecção automática de estado do projeto (novo vs existente)
- Documentação com templates prontos para copiar/colar

### Informação de Versão

Este é o v0.2.0 (MINOR update) do Agentc AI Developer com o Microprocesso 1.2 totalmente implementado. Agora os usuários têm um fluxo completo: `/brief` (planning) → `/setup-local-observability` (environment) para começar o desenvolvimento de agentes agentic com confiança.

## [0.1.0] - 2025-11-02

### Adicionado

- Suporte para 4 modos de operação do Brief Minimo:
  - Modo 1: Criar novo agente (padrão, 30 minutos)
  - Modo 2: Atualizar agente existente (15-20 minutos)
  - Modo 3: Validar agente contra critérios Brief Minimo (20 minutos)
  - Modo 4: Documentar agente existente retroativamente (20 minutos)
- Detecção automática de contexto (novo projeto vs projeto existente)
- Seleção de modo adaptativo baseada no contexto detectado
- Entrevistas adaptadas para cada modo com duração otimizada
- Fluxos de entrevista específicos por modo
- Suporte a atualização de briefs existentes
- Geração de relatórios de validação
- Documentação retroativa de agentes em produção
- Integração seamless com projetos existentes
- Exemplos de uso com agentes de produção
- Exemplos de uso com agentes legacy

### Modificado

- Agent `brief-assistant` agora detecta contexto do projeto
- Entrevista adapta-se ao modo selecionado
- Documentação expandida com casos de uso em projetos existentes
- README.md com novas seções "Usage Modes" e "Using in Existing Projects"
- Description do plugin atualizada para refletir 4 modos
- Keywords expandidas para incluir "documentation", "validation", "existing-projects"

### Melhorias

- Maior flexibilidade para integração em projetos em andamento
- Suporte a agentes já em produção
- Funcionalidade de validação e qualidade
- Preservação de conhecimento institucional via documentação retroativa
- Alinhamento de equipe através de briefs atualizados

### Informação de Versão

Este é o v0.1.0 (MINOR update) do Agentc AI Developer com a metodologia Brief Minimo expandida para 4 modos de operação. Agora suporta tanto projetos greenfield quanto projetos existentes com agentes em desenvolvimento ou produção.

## [0.0.0] - 2025-11-02

### Adicionado

- Lançamento inicial do plugin Agentc AI Developer
- Comando `/brief` para iniciar o processo de Brief Minimo
- Agent `brief-assistant` para conduzir entrevista interativa de planejamento
- Metodologia Brief Minimo com as 5 perguntas fundamentais:
  - O que o agente FAZ?
  - Qual é o INPUT?
  - Qual é o OUTPUT?
  - Qual é a Ferramenta/API?
  - O que é Sucesso?
- Documentação completa no README.md
- Guia detalhado no agent brief-assistant.md
- Geração automática de documento de especificação (README.md)
- Validação de respostas específicas (não vagas)
- Suporte para exemplos concretos de input/output
- Verificação de acesso a ferramentas e custo

### Informação de Versão

Este é o v0.0.0 (versão inicial) do Agentc AI Developer com o primeiro macroprocesso implementado (Brief Minimo). Versões futuras adicionarão novos macroprocessos e funcionalidades para o ciclo completo de desenvolvimento de agentes de IA.
