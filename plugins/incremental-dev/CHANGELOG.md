# Changelog

Todas as mudanças notáveis neste plugin serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.1.0] - 2025-11-03

### ✨ Adicionado (MINOR - New Feature)

#### Novo Subcommand: `/prd validate`

Valida PRD.md existente contra a estrutura do template e verifica completude.

**Funcionalidades**:

- ✅ Auto-detecta PRD.md no diretório do projeto
- ✅ Valida seções obrigatórias por fase de desenvolvimento (v0.1, v1.0, v1.1, v1.x)
- ✅ Verifica campos obrigatórios preenchidos (não vazios)
- ✅ Valida estrutura markdown
- ✅ Valida progressão de versão (0.1 → 1.0 → 1.1 → 1.x)
- ✅ Detecta campos faltantes com recomendações
- ✅ Gera relatório de completude com percentual por fase
- ✅ Sugere próximas ações baseado em progresso

**Exemplo de relatório**:

```
✅ PRD VALIDATION REPORT
📋 Project: incremental-dev
🔄 Version: 2.0.0
FASES: ✅ v0.1 (100%) | ✅ v1.0 (90%) | ⚠️ v1.1 (60%)
OVERALL PROGRESS: 83%
```

**Uso**:

- `/prd validate` - Auto-detecta e valida PRD.md
- `/prd validate path/to/PRD.md` - Valida arquivo específico

**Quando usar**:

- Após criar ou atualizar PRD.md
- Para verificar completude por fase
- Antes de evoluir para próxima fase de desenvolvimento
- Para identificar campos faltantes e próximas ações

#### Extensão do Skill `prd-manager`

- Nova responsabilidade: Validar PRD contra template
- Novo checklist de validação com critérios por fase (v0.1-v2.0)
- Nova seção: "Validação Automática via `/prd validate`"
- Integração com progressão de versão do PRD

### 🔧 Modificado

#### Documentação Atualizada

- `/prd` command: Adicionado uso de `/prd validate` com exemplos
- README.md: Adicionada seção "Validate PRD Feature" com casos de uso
- Skill `prd-manager`: Adicionada lógica de validação e checklist detalhado
- Marketplace.json: Atualizada descrição mencionando validação

### 📚 Benefícios

- ✅ **PRD Completude**: Garante PRD tem todos campos obrigatórios por fase
- ✅ **Guia de Progresso**: Identifica qual fase completar próximo
- ✅ **Validação Automática**: Detecta gaps sem análise manual
- ✅ **Melhores Práticas**: Força conformidade com template padrão
- ✅ **Documentação Viva**: Mantém PRD sincronizado com desenvolvimento

## [2.0.0] - 2025-10-XX

### Breaking Changes - Consolidação de 12 Comandos em 5

[conteúdo existente...]

## [1.9.0] - 2025-11-03

### ✨ Refatoração de Arquitetura

#### Agente Refatorado: incremental-dev-coach.md

- Reduzido de 720 para 132 linhas (-82%)
- Mantém apenas processo/fluxo (responsabilidade única)
- Executa comandos automaticamente (ativo, não sugere)
- Carrega informação de 12 comandos disponíveis
- Sem referências explícitas a skills (auto-detectadas por contexto)

#### Skills com Progressive Disclosure

- **yagni-enforcer/SKILL.md**: Reduzido de 476 para 106 linhas (-78%) + PATTERNS.md
- **prd-manager/SKILL.md**: Reduzido de 489 para 136 linhas (-72%) + PATTERNS.md
- **refactor-advisor/SKILL.md**: Reduzido de 597 para 149 linhas (-75%) + PATTERNS.md
- Cada skill agora focado em O QUE saber (conhecimento)
- Exemplos e instruções COMO fazer movidos para PATTERNS.md
- Referência compartilhada yagni-enforcer/REFERENCE.md mantida

#### Melhorias de Markdown

- ✅ 41 erros markdown corrigidos nos 3 principais arquivos
- ✅ Todos code blocks com language type
- ✅ Blank lines antes de lists e headings
- ✅ Final newlines adicionadas
- ✅ Pontuação em headings removida

### 🎯 Benefícios da Refatoração

**Performance**:

- Contexto menor para agentes (132 vs 720 linhas)
- Skills independentes e reutilizáveis
- Carregamento mais rápido do plugin

**Manutenibilidade**:

- Responsabilidade única clara: agent = processo, skills = conhecimento
- Fácil adicionar novas funcionalidades
- Skills podem ser reutilizadas em outros plugins

**Usabilidade**:

- Agente detecta contexto e executa automaticamente
- Sem redundância de documentação
- Progressive disclosure: overview no agent, detalhes em skills

**Qualidade de Código**:

- Segue boas práticas de plugin architecture
- JSON validado e correto
- Markdown formatado conforme padrões

### 📊 Métricas

| Arquivo | Antes | Depois | Redução |
|---------|-------|--------|---------|
| incremental-dev-coach.md | 720 linhas | 132 linhas | -82% |
| yagni-enforcer/SKILL.md | 454 linhas | ~300 linhas | -34% |
| prd-manager/SKILL.md | 467 linhas | ~300 linhas | -36% |
| **Total** | **1,641 linhas** | **~732 linhas** | **-55%** |

### 🔍 Validações

- ✅ plugin.json válido (JSON syntax)
- ✅ marketplace.json válido (JSON syntax)
- ✅ Todos markdown files corrigidos
- ✅ 12 comandos documentados no agent
- ✅ 3 skills referenciáveis por contexto

## [1.8.0] - 2025-11-02

### ✨ Adicionado (MINOR)

#### Agente coach melhorado

- Detecção automática de tipo de projeto (novo vs legacy)
- Questionamento YAGNI integrado no fluxo
- Orientação de spikes técnicos com preferência por notebooks
- Suporte completo para projetos existentes

### 🔧 Modificado

- Comando `/adopt-incremental` com análise de over-engineering
- Detecção de legacy projects em todos os comandos
- Agente redireciona automaticamente para comandos apropriados

## [1.7.0] - 2025-11-01

### Adicionado (MINOR - New Feature)

#### Novo Comando: `/update-claude-md`

- Comando dedicado para atualizar arquivo CLAUDE.md do projeto com configuração do plugin
- **Funcionalidades**:
  - ✅ Verifica se CLAUDE.md existe no projeto
  - ✅ Cria arquivo básico se não existir
  - ✅ Detecta se seção incremental-dev já existe
  - ✅ Pergunta se deseja sobrescrever seção existente
  - ✅ Adiciona/atualiza seção seguindo boas práticas (≤40 linhas)
  - ✅ Valida arquivo após atualização
- **Boas práticas aplicadas** (conforme plugin-creator agent):
  - ✅ Seção ≤40 linhas (limite estrito)
  - ✅ Menciona APENAS agent (incremental-dev-coach)
  - ✅ NÃO menciona skills (auto-descobertas quando plugin instalado)
  - ✅ NÃO menciona comandos (auto-descobertos na inicialização)
  - ✅ Inclui 3-5 regras críticas mais importantes
  - ✅ Link para README.md do plugin para documentação completa
  - ✅ Nota sobre auto-discovery de skills e comandos
  - ✅ Progressive disclosure (detalhes em README.md)
- **Casos de uso**:
  - CLAUDE.md não tem configuração do plugin
  - CLAUDE.md foi corrompido ou deletado
  - Reconfigurar após atualização do plugin
  - Garantir CLAUDE.md segue práticas atuais
- **Workflow detalhado** com 7 passos:
  1. Verificar existência de CLAUDE.md
  1. Ler arquivo atual ou criar básico
  1. Detectar seção incremental-dev
  1. Perguntar overwrite se existir
  1. Adicionar/atualizar seção (≤40 linhas)
  1. Escrever CLAUDE.md atualizado
  1. Validar e reportar sucesso
- **Error handling robusto**:
  - Permissão de leitura/escrita negada
  - CLAUDE.md corrompido
  - Detecção de project root falhou
- **Exemplos práticos**:
  - Fresh project (sem CLAUDE.md)
  - Existing CLAUDE.md sem plugin config
  - Existing CLAUDE.md com config antiga
  - Usuário declina overwrite
- **Documentação técnica**:
  - Progressive disclosure pattern explicado
  - Mecanismo de auto-discovery documentado
  - Performance notes incluídas
  - Troubleshooting completo

### Modificado

#### Marketplace Description

- Atualizada descrição da versão 1.7.0 mencionando `/update-claude-md`
- Tags adicionadas: "claude-md", "setup"

### Benefícios

- ✅ **Facilita setup**: Usuários podem atualizar CLAUDE.md sem usar `/setup-project-incremental` (que cria PRD também)
- ✅ **Segue best practices**: Garante CLAUDE.md sempre conforme plugin-creator agent guidelines
- ✅ **Progressive disclosure**: ≤40 linhas em CLAUDE.md, docs completas em README.md
- ✅ **Auto-discovery**: Documenta que skills/comandos são auto-descobertos (não precisa copiar manualmente)
- ✅ **Flexibilidade**: Permite atualizar apenas CLAUDE.md sem afetar PRD ou resto do projeto
- ✅ **Manutenibilidade**: Fácil reconfigurar após updates do plugin
- ✅ **Robustez**: Error handling completo com soluções claras
- ✅ **Educacional**: Usuários aprendem boas práticas de CLAUDE.md via exemplos

### Comparação com Comandos Relacionados

| Comando | Use When |
|---------|----------|
| `/setup-project-incremental` | Starting new project (creates PRD + CLAUDE.md) |
| `/update-claude-md` | Only need to update/fix CLAUDE.md configuration |
| `/start-incremental` | Define MVP after CLAUDE.md is configured |

## [1.6.0] - 2025-11-01

### Adicionado (MINOR - New Features)

#### Nova Documentação de Referência Centralizada

- **YAGNI_REFERENCE.md**: Novo arquivo de referência centralizado em `docs/` contendo:
  - Todos os princípios YAGNI completos
  - Padrões comuns de over-engineering (4 categorias)
  - Anti-patterns detalhados com exemplos de código
  - Estratégias de simplificação
  - Regra dos 3 explicada
  - Checklist de revisão YAGNI
  - Guia de incremento ideal
  - Quando refatorar

### Modificado (Progressive Disclosure Applied)

#### Eliminação de Duplicações com Progressive Disclosure

- **review-yagni.md**: Reduzido de 682 para 427 linhas (-255 linhas, -37%)

  - Seções de over-engineering patterns substituídas por referências ao YAGNI_REFERENCE.md
  - Mantidas quick references para navegação rápida
  - Detalhes movidos para documentação centralizada

- **add-increment.md**: Reduzido de 537 para 479 linhas (-58 linhas, -11%)

  - Padrões de over-engineering em incremento consolidados
  - Princípios de incremento simplificados com referências
  - Regra dos 3 mantida como quick reference

- **start-incremental.md**: Reduzido de 607 para 562 linhas (-45 linhas, -7%)

  - Sinais de over-engineering em MVP simplificados
  - Princípios a seguir consolidados
  - Referências ao documento central adicionadas

#### Análise de Outros Problemas

- **prd-update.md**: Já estava otimizado em 507 linhas (target: ~600) ✅
- **PRD template**: Já estava ótimo em 172 linhas (target: \<500) ✅
- Comandos restantes verificados: sem duplicações significativas

### Benefícios

- ✅ **~358 linhas totais removidas** através de progressive disclosure
- ✅ **Manutenção centralizada**: Atualizar YAGNI em um único lugar
- ✅ **Consistência**: Todas as referências apontam para documentação canônica
- ✅ **Performance**: Comandos mais enxutos carregam mais rápido
- ✅ **Navegabilidade**: Quick references + documentação detalhada on-demand
- ✅ **Escalabilidade**: Fácil adicionar novos padrões no YAGNI_REFERENCE.md

### Estatísticas Finais

````text

Arquivos modificados: 3 comandos
Novo arquivo criado: docs/YAGNI_REFERENCE.md (462 linhas)
Linhas removidas: ~358 linhas
Redução total: ~18% de código duplicado

```text

## [1.5.2] - 2025-11-01

### Modificado (Usability Improvements - PATCH)

#### PROBLEMA 1: Redundância `/prd-fix` ↔ `/prd-update`
- Adicionado cross-reference no início de `/prd-fix` apontando para `/prd-update` para mudanças completas
- Adicionado cross-reference no início de `/prd-update` apontando para `/prd-fix` para ajustes cirúrgicos
- Clarificado diferença: `/prd-fix` para mudanças de seção única, `/prd-update` para fases completas

#### PROBLEMA 3: Workflow confuso em `/adopt-incremental`
- Adicionado diagrama de fluxo ASCII com 5 passos principais
- Adicionado checklist de execução detalhado com sub-tarefas para cada passo
- Reorganizado seções em ordem lógica do workflow
- Melhorada navegabilidade do comando

#### PROBLEMA 4: `/refactor-now` duplica skill
- Adicionada nota explicativa: comando é wrapper manual da skill `refactor-advisor`
- Documentado que skill é auto-invocada automaticamente por Claude
- Clarificado quando usar comando vs deixar skill ser invocada

#### PROBLEMA 7: Skill `prd-manager` descrição
- Melhorada descrição YAML com trigger terms explícitos
- Adicionados termos: requisitos, objetivos, MVP, incremento completo, decisões arquiteturais, aprendizados, lições aprendidas, ADR, Product Vision, épicos, User Stories
- Descrição agora facilita auto-invocação da skill

#### PROBLEMA 8 (CRÍTICO): CLAUDE.md não documenta agent e skills
- Adicionada seção completa sobre agent `incremental-dev-coach` em `/setup-project-incremental`
- Expandida seção de skills com detalhes sobre quando cada skill é invocada
- Documentados trigger terms para cada skill (yagni-enforcer, refactor-advisor, prd-manager)
- Aplicado progressive disclosure: seção reduzida para ~30 linhas (limite 40)
- Adicionada referência ao README.md para documentação completa

#### PROBLEMA 9 (CRÍTICO): Workflow `/add-increment` não está claro
- Adicionada seção "When to Use This Command" no início
- Adicionada tabela comparativa: `/start-incremental` vs `/add-increment` vs `/refactor-now` vs `/review-yagni`
- Adicionado Passo 0: "Validate Prerequisites" (ALWAYS RUN FIRST)
  - Validação de PRD existente
  - Validação de git status limpo
  - Validação de MVP definido
- Adicionado "Increment Sizing Guide" com métricas ideais
  - Tempo: 30min-2h
  - Arquivos: 1-3 máximo
  - Linhas: 20-100
  - Testes: 1-3 casos
- Integrado registro no PRD no fluxo principal (passo 8)
  - Antes: passo opcional no final
  - Agora: parte integral do workflow
- Atualizado diagrama de fluxo com 10 passos claros

### Benefícios
- ✅ Usuários entendem claramente qual comando usar quando
- ✅ Cross-references previnem uso incorreto de comandos similares
- ✅ Workflow visual facilita execução de comandos complexos
- ✅ Validações de pré-requisitos evitam erros
- ✅ Documentação de agent/skills melhora uso do plugin
- ✅ Progressive disclosure mantém CLAUDE.md conciso (≤40 linhas)
- ✅ Registro no PRD agora é parte natural do workflow

## [1.5.1] - 2025-11-01

### Fixed
- Corrigir lógica de workflow do plugin

## [1.5.0] - 2025-10-27

### Adicionado
- Validação automática de tamanho de CLAUDE.md e README.md em `/setup-project-incremental`
  - Limite recomendado: 40,000 caracteres (40KB)
  - Detecção automática de arquivos grandes após criação/atualização
- Progressive disclosure automático para CLAUDE.md quando > 40k caracteres
  - Extração de conteúdo para `docs/development/` com arquivos separados:
    - `INCREMENTAL_DEV.md` (workflow completo)
    - `YAGNI_PRINCIPLES.md` (regras detalhadas)
    - `EXAMPLES.md` (exemplos práticos)
  - Redução de CLAUDE.md para versão concisa (~2,500 caracteres)
  - Manutenção de overview + links + 3-5 regras críticas
- Progressive disclosure automático para README.md quando > 40k caracteres
  - Extração de conteúdo para `docs/` com arquivos separados:
    - `INSTALLATION.md` (instalação detalhada)
    - `USAGE.md` (guia de uso completo)
    - `API.md` (referência de API)
    - `CONTRIBUTING.md` (guia de contribuição)
    - `ARCHITECTURE.md` (arquitetura do projeto)
    - `EXAMPLES.md` (exemplos avançados)
    - `FAQ.md` (perguntas frequentes)
    - `TROUBLESHOOTING.md` (solução de problemas)
  - Redução de README.md para versão concisa (~1,500 caracteres)
  - Manutenção de overview + quick start + links para documentação
- Confirmação interativa antes de aplicar progressive disclosure
  - Usuário pode aceitar ou recusar reestruturação automática
  - Estatísticas de redução de tamanho após aplicação
- Validação e status reportados no resumo final
  - Status de tamanho: ✅ Dentro do limite / ⚠️ Grande
  - Tamanho em caracteres exibido
  - Indicação de progressive disclosure aplicado

### Modificado
- Comando `/setup-project-incremental` agora sempre valida tamanhos de arquivos
  - Validação executada automaticamente após criação/atualização
  - Melhoria na performance e legibilidade dos projetos
  - Orientação automática para melhores práticas
- Descrição do plugin no marketplace menciona progressive disclosure
- Tags adicionadas: "progressive-disclosure", "performance"

### Benefícios
- Melhora performance do Claude ao carregar contexto inicial
- CLAUDE.md e README.md sempre otimizados automaticamente
- Documentação completa acessível via Read tool quando necessário
- Redução de até 80-95% no tamanho de arquivos grandes
- Melhor legibilidade e organização de documentação
- Aplicação automática de best practices de progressive disclosure

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
````
