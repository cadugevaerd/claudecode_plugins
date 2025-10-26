# Changelog

Todas as mudanças notáveis neste plugin serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.4.0] - 2025-10-26

### Adicionado
- Comando `/adopt-incremental` para adoção completa de YAGNI em projetos legacy
  - Análise automática de código existente
  - Detecção de over-engineering com métricas (LOC, complexidade, duplicação)
  - Criação de PRD retroativo a partir do código
  - Geração de roadmap de simplificação priorizado
  - Configuração automática de CLAUDE.md
- Comando `/prd-retrofit` para criar PRD retroativo apenas
  - Análise de código e estrutura do projeto
  - Detecção automática de versão (pyproject.toml, setup.py, __init__.py, git tags)
  - Geração de PRD completo a partir de código existente
  - Inferência de decisões arquiteturais (ADRs retroativos)
  - Análise de histórico git (commits, tags, contributors)
- Detecção automática de projetos legacy em todos os comandos
  - Verificação de código existente (arquivos .py, .js, .ts, etc.)
  - Detecção de estrutura de diretórios (src/, lib/, app/)
  - Verificação de git history
  - Redirecionamento para comandos apropriados
- Análise com `git blame` no `/review-yagni`
  - Identifica quando código foi adicionado
  - Detecta abstrações adicionadas "para o futuro" que nunca foram usadas
  - Mostra autor e mensagem de commit do código suspeito
- Priorização por impacto no `/refactor-now`
  - Fórmula: Impacto = (Ocorrências × 2) + (LOC_Reduzidas / 10) - Risco
  - Ordenação de refatorações por maior impacto primeiro
  - Cálculo de risco (baixo, médio, alto)
- Documentação completa de novos comandos no `/prd-help`
  - Seção específica para projetos legacy
  - Exemplo prático de adoção de YAGNI
  - Q&A sobre projetos existentes
- Keywords "legacy", "retrofit", "adoption", "code-analysis"

### Modificado
- `/setup-project-incremental` agora detecta projetos legacy e oferece opções
  - Opção 1: /adopt-incremental (análise completa)
  - Opção 2: /prd-retrofit (apenas PRD)
  - Opção 3: Continuar com setup normal
- `/start-incremental` detecta código existente e redireciona para comandos legacy
  - Previne criação de PRD do zero em projetos com código
  - Sugere /adopt-incremental ou /prd-retrofit
- `/review-yagni` com análise de git history para projetos legacy
  - Mostra quando código foi adicionado
  - Identifica código antigo nunca modificado (possivelmente obsoleto)
- `/refactor-now` prioriza refatorações por impacto em projetos legacy
  - Calcula impacto baseado em ocorrências, LOC reduzidas e risco
  - Apresenta refatorações ordenadas por maior benefício
- `incremental-dev-coach.md` (agente) detecta tipo de projeto (novo vs legacy)
  - Recomenda fluxo apropriado baseado no tipo de projeto
  - Sugere /adopt-incremental para projetos legacy
- Template CLAUDE.md em todos os comandos lista novos comandos para legacy
- Descrição do plugin menciona suporte a projetos legacy
- Descrição do marketplace atualizada com "análise retroativa" e "roadmap de simplificação"

### Benefícios para Projetos Legacy
- Adotar YAGNI em projetos existentes sem reescrever tudo
- Documentar código legado automaticamente com PRD retroativo
- Identificar e remover over-engineering acumulado
- Priorizar refatorações por impacto real
- Entender histórico de decisões técnicas via git blame
- Gerar roadmap incremental de simplificação

## [1.3.0] - 2025-10-25

### Adicionado
- Preferência por notebooks (.ipynb) para Spikes de Validação Técnica
- Pergunta 10 em `/start-incremental` sobre formato preferido de spikes (notebooks vs scripts)
- Pergunta 5 em `/setup-project-incremental` sobre formato de spikes
- Seção "Formato de Spikes de Validação Técnica" no template PRD.md
- Cenário 5 no agente `incremental-dev-coach` demonstrando uso de notebooks para spikes
- Orientação sobre quando usar notebooks vs scripts
- Keywords "notebooks" e "spikes" no plugin.json

### Modificado
- Agente `incremental-dev-coach` agora recomenda notebooks primeiro para exploração técnica
- Coach verifica preferência do usuário no PRD antes de sugerir formato de spike
- Template PRD.md inclui seção "Configurações de Desenvolvimento" com formato de spikes
- Descrição do plugin no marketplace.json menciona preferência por notebooks

### Benefícios dos Notebooks para Spikes
- Exploração interativa e incremental
- Documentação inline com markdown
- Visualizações e gráficos integrados
- Histórico de experimentação preservado
- Fácil compartilhamento de aprendizados

## [1.2.0] - 2025-10-25

### Adicionado
- Comando `/prd-fix` para ajustes cirúrgicos em seções específicas do PRD
- Comando `/prd-help` - central de ajuda interativa sobre YAGNI, PRD e uso do plugin
- Modo interativo ao criar PRD com `/start-incremental` - 9 perguntas guiadas
- Perguntas detalhadas sobre contexto, problema, usuário, funcionalidades e métricas
- Confirmação e edição de respostas antes de criar PRD
- Preenchimento automático do template PRD.md com respostas coletadas

### Modificado
- `/start-incremental` agora faz perguntas interativas quando executado sem argumentos
- `/start-incremental` coleta informações completas para criar PRD estruturado
- Fluxo de criação de PRD muito mais guiado e amigável

## [1.1.0] - 2025-10-24

### Adicionado
- Comandos `/prd-view` e `/prd-update` para gestão de Product Requirements Document
- Skill `prd-manager` para gestão automática de PRD
- Template `PRD.md` em `templates/` com estrutura completa
- README.md com documentação detalhada do plugin

### Modificado
- Agente `incremental-dev-coach` com suporte a PRD
- Comandos existentes integrados com gestão de PRD

## [1.0.0] - 2025-10-20

### Adicionado
- Lançamento inicial do plugin
- Comando `/setup-project-incremental` para configurar CLAUDE.md
- Comando `/start-incremental` para iniciar desenvolvimento incremental
- Comando `/add-increment` para adicionar incrementos
- Comando `/review-yagni` para revisar over-engineering
- Comando `/refactor-now` para identificar quando refatorar
- Agente `incremental-dev-coach` para orientação em YAGNI
- Skills `yagni-enforcer` e `refactor-advisor`