# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)

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
