# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)

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

---

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

---

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

---

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
