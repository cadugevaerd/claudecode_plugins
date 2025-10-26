# Changelog

Todas as mudanças notáveis neste plugin serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

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