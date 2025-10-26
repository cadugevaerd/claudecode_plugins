---
description: Criar PRD retroativo para projeto existente - analisa código e gera documentação baseada na realidade
---

# PRD Retrofit (Criar PRD Retroativo)

Este comando cria um **Product Requirements Document (PRD) retroativo** para projetos que já foram desenvolvidos mas nunca tiveram documentação formal de requisitos.

## 🎯 Objetivo

Gerar PRD baseado em código existente:
- Analisar código-fonte para extrair funcionalidades
- Documentar decisões arquiteturais implementadas
- Criar histórico de evolução (via git)
- Estabelecer baseline para futuras evoluções

**Diferença para `/adopt-incremental`**:
- `/adopt-incremental`: Análise COMPLETA + PRD + CLAUDE.md + Roadmap
- `/prd-retrofit`: Apenas cria PRD retroativo (sem configurar YAGNI)

## 📋 Como usar

```bash
# Análise completa automática
/prd-retrofit

# Com descrição do projeto
/prd-retrofit "Sistema de gerenciamento de estoque"

# Especificar versão do PRD
/prd-retrofit --version 2.5.0
```

## 🔍 Processo de Execução

### Passo 1: Detectar Versão do Projeto

```
═══════════════════════════════════════════
📄 CRIAR PRD RETROATIVO
═══════════════════════════════════════════

Detectando versão do projeto...
```

**1.1. Procurar versão em arquivos comuns**:

```python
# Verificar em ordem:
1. pyproject.toml → [tool.poetry.version] ou [project.version]
2. setup.py → version="X.Y.Z"
3. __init__.py → __version__ = "X.Y.Z"
4. package.json → "version": "X.Y.Z"
5. git tags → últi git tag mais recente
```

**Output**:
```
✅ Versão detectada: 2.5.0

Fonte: pyproject.toml
PRD será criado como v2.5.0
```

**Se versão NÃO detectada**:
```
⚠️  Versão não detectada automaticamente

Sugestões:
1. Contar commits: [X] commits → v0.[X].0
2. Usar data: YYYY.MM.DD
3. Iniciar em v1.0.0

Qual versão usar? (ou pressione Enter para v1.0.0)
```

---

### Passo 2: Analisar Estrutura do Código

```
📊 Analisando estrutura do projeto...

[Progresso]
├─ Lendo arquivos fonte...
├─ Detectando funcionalidades...
├─ Analisando arquitetura...
└─ Extraindo decisões técnicas...
```

**2.1. Detectar Framework/Stack**:

```python
# Identificar automaticamente:
- FastAPI: from fastapi import...
- Django: django.conf, models.py
- Flask: from flask import...
- LangChain: from langchain import...
- CLI: argparse, click, typer
```

**Output**:
```
🔧 Stack Detectada:

Framework Web: FastAPI v0.104.0
ORM: SQLAlchemy v2.0.0
Validação: Pydantic v2.5.0
Testing: pytest v7.4.0
```

**2.2. Mapear Funcionalidades**:

Analisar código para extrair funcionalidades:

```python
# Estratégias por framework:

# FastAPI: Endpoints
@app.get("/users") → "Listar usuários"
@app.post("/users") → "Criar usuário"

# Django: Views
def user_list(request) → "Listar usuários"
class UserCreateView → "Criar usuário"

# CLI: Commands
@click.command("migrate") → "Migrar banco de dados"

# LangChain: Chains/Agents
chain = prompt | llm | parser → "Pipeline de processamento"
```

**Output**:
```
🎯 Funcionalidades Identificadas:

1. Autenticação e Autorização
   ├─ POST /auth/login → Login de usuário
   ├─ POST /auth/logout → Logout de usuário
   ├─ POST /auth/refresh → Refresh de token
   └─ GET /auth/me → Obter usuário atual

2. Gerenciamento de Usuários
   ├─ GET /users → Listar usuários (paginado)
   ├─ POST /users → Criar usuário
   ├─ GET /users/{id} → Obter usuário específico
   ├─ PUT /users/{id} → Atualizar usuário
   └─ DELETE /users/{id} → Deletar usuário

3. Gerenciamento de Produtos
   ├─ GET /products → Listar produtos
   ├─ POST /products → Criar produto
   └─ PUT /products/{id} → Atualizar produto

Total: 12 endpoints / 3 módulos principais
```

**2.3. Extrair Decisões Arquiteturais**:

Identificar padrões e decisões via código:

```python
# Detectar:
1. Padrões de design (Repository, Factory, Strategy)
2. Estrutura de diretórios (Clean Architecture, MVC)
3. Bibliotecas importantes (ORM, validação, auth)
4. Configurações (env vars, configs)
```

**Output**:
```
🏗️  Arquitetura Detectada:

Padrão: Clean Architecture (camadas detectadas)
├─ Domain: src/domain/ (models, entities)
├─ Application: src/application/ (use cases)
├─ Infrastructure: src/infrastructure/ (repos, DB)
└─ Presentation: src/api/ (controllers, routes)

Decisões Técnicas:
- Repository Pattern para acesso a dados
- Dependency Injection via FastAPI
- JWT para autenticação
- Pydantic para validação
```

---

### Passo 3: Analisar Histórico Git (se disponível)

```
📚 Analisando histórico Git...
```

**3.1. Extrair métricas do repositório**:

```bash
# Executar:
git log --all --format="%h|%an|%ae|%ad|%s" --date=short > /tmp/git_history.txt

# Processar:
- Total de commits
- Principais contribuidores
- Período de desenvolvimento
- Frequência de commits
- Features principais (via mensagens de commit)
```

**Output**:
```
📖 Histórico do Projeto:

Período: Jan 2023 - Out 2025 (22 meses)
Commits: 487 total
Contribuidores:
  - João Silva (245 commits)
  - Maria Santos (156 commits)
  - Pedro Costa (86 commits)

Marcos Principais (via git tags):
  - v1.0.0 (Jan 2023): Release inicial
  - v1.5.0 (Jun 2023): Autenticação JWT
  - v2.0.0 (Dez 2023): Refatoração arquitetura
  - v2.5.0 (Out 2025): Multi-tenancy

Features por Commit Messages:
  - feat: autenticação (12 commits)
  - feat: produtos (18 commits)
  - feat: relatórios (8 commits)
  - fix: bugs diversos (67 commits)
  - refactor: arquitetura (15 commits)
```

---

### Passo 4: Gerar PRD Retroativo

```
📝 Gerando PRD retroativo...

Criando docs/PRD.md v[versão]...
```

**4.1. Template do PRD Retroativo**:

```markdown
# Product Requirements Document (Retroativo)

## Metadados
- **Versão do PRD**: [versão detectada]
- **Status**: Retroativo (gerado a partir de código existente)
- **Data de Criação do PRD**: [hoje]
- **Data de Início do Projeto**: [primeiro commit git ou "Desconhecida"]
- **Última Atualização do Código**: [último commit ou hoje]

---

## 1. Visão Geral

### 1.1. Contexto
[Descrição fornecida pelo usuário ou placeholder]

Este documento foi criado RETROATIVAMENTE a partir da análise do código-fonte existente.
As informações refletem o ESTADO ATUAL do projeto conforme implementado.

### 1.2. Problema Resolvido
[Inferir do código ou usar descrição]

### 1.3. Solução Implementada
[Descrever baseado nas funcionalidades detectadas]

Sistema implementado usando [stack] com [X] módulos principais:
- [Módulo 1]
- [Módulo 2]
- [Módulo 3]

---

## 2. Objetivos (Inferidos)

### 2.1. Objetivos de Negócio
[Inferir das funcionalidades implementadas]

### 2.2. Objetivos Técnicos
- [Stack/framework usado]
- [Padrões arquiteturais]
- [Bibliotecas principais]

---

## 3. Funcionalidades Implementadas

### 3.1. [Módulo 1]
- ✅ [Funcionalidade A] - Implementada
  - Endpoint: [método] [rota]
  - Descrição: [inferida do código]

- ✅ [Funcionalidade B] - Implementada
  - Endpoint: [método] [rota]
  - Descrição: [inferida do código]

### 3.2. [Módulo 2]
- ✅ [Funcionalidade C] - Implementada
- ✅ [Funcionalidade D] - Implementada

---

## 4. Requisitos Não-Funcionais (Detectados)

### 4.1. Performance
- [Detectado via código: caching, otimizações]

### 4.2. Segurança
- Autenticação: [JWT/Session/OAuth detectado]
- Autorização: [Roles/Permissions detectado]
- Validação: [Pydantic/outras libs]

### 4.3. Escalabilidade
- [Async/workers detectados]
- [Cache/queue systems]

---

## 5. Arquitetura

### 5.1. Stack Tecnológica
- **Backend**: [framework e versão]
- **Database**: [detectado de configs]
- **Autenticação**: [lib detectada]
- **Validação**: [lib detectada]
- **Testes**: [framework detectado]

### 5.2. Estrutura de Diretórios
```
[Árvore de diretórios do projeto]
```

### 5.3. Padrões Arquiteturais
- [Padrões detectados no código]
- [Camadas identificadas]

---

## 6. Decisões Arquiteturais (ADRs Retroativos)

### ADR 001: Uso de [Framework]
- **Data**: [primeiro commit com framework ou "Desconhecida"]
- **Status**: Implementado
- **Contexto**: [Inferir necessidade]
- **Decisão**: Usar [framework]
- **Consequências**:
  - ✅ [Benefício 1]
  - ⚠️ [Trade-off 1]

### ADR 002: [Padrão Arquitetural]
- **Data**: [git blame do arquivo relevante]
- **Status**: Implementado
- **Contexto**: [Inferir do código]
- **Decisão**: Implementar [padrão]
- **Consequências**: [Impacto detectado]

[Adicionar mais ADRs conforme detectados]

---

## 7. Métricas Atuais

### 7.1. Código
- **Total de Arquivos**: [X]
- **Linhas de Código**: [X]
- **Complexidade Ciclomática**: [Média]
- **Duplicação**: [X]%
- **Cobertura de Testes**: [X]% (se detectado)

### 7.2. Funcionalidades
- **Endpoints/Comandos**: [X]
- **Modelos/Entidades**: [X]
- **Módulos Principais**: [X]

### 7.3. Desenvolvimento
- **Commits Totais**: [X]
- **Contribuidores**: [X]
- **Idade do Projeto**: [X meses]
- **Último Commit**: [X dias atrás]

---

## 8. Histórico de Versões (Git Tags)

| Versão | Data | Descrição |
|--------|------|-----------|
| [v1.0.0] | [data] | Release inicial |
| [v1.5.0] | [data] | [Feature principal] |
| [v2.0.0] | [data] | [Breaking change] |
| [v2.5.0] | [data] | Versão atual |

---

## 9. Roadmap Futuro (Placeholder)

**NOTA**: Esta seção precisa ser preenchida manualmente com base em requisitos futuros.

### Próximas Features
- [ ] [Feature a ser implementada]
- [ ] [Feature a ser implementada]

### Melhorias Técnicas
- [ ] [Melhoria sugerida]
- [ ] [Débito técnico a pagar]

---

## 10. Observações

### 10.1. Limitações deste PRD
- ✅ Funcionalidades: Extraídas automaticamente do código
- ⚠️ Requisitos de Negócio: Inferidos (necessitam validação)
- ⚠️ Contexto Histórico: Limitado ao git history
- ❌ Decisões Futuras: Não documentadas (adicionar manualmente)

### 10.2. Próximos Passos
1. Revisar e validar funcionalidades detectadas
2. Adicionar contexto de negócio real
3. Documentar decisões futuras
4. Manter PRD atualizado com novas features

---

**Este PRD foi gerado automaticamente via `/prd-retrofit`**
**Última atualização**: [data de geração]
```

**4.2. Salvar PRD**:

```bash
# Criar diretório
mkdir -p docs/

# Salvar
# docs/PRD.md
```

---

### Passo 5: Confirmação

```
═══════════════════════════════════════════
✅ PRD RETROATIVO CRIADO!
═══════════════════════════════════════════

Localização: docs/PRD.md
Versão: [versão]

📊 Conteúdo Gerado:

Análise Automática:
├─ [X] funcionalidades detectadas
├─ [X] decisões arquiteturais documentadas
├─ [X] ADRs retroativos criados
└─ [X] métricas calculadas

Histórico Git:
├─ [X] commits analisados
├─ [X] versões documentadas
└─ [X] contribuidores listados

═══════════════════════════════════════════

⚠️  IMPORTANTE: Revisar PRD

Este PRD foi gerado AUTOMATICAMENTE e pode conter:
- Funcionalidades mal interpretadas
- Contexto de negócio incorreto
- ADRs incompletos

Próximos passos:
1. Ler docs/PRD.md
2. Validar funcionalidades detectadas
3. Adicionar contexto de negócio real
4. Corrigir interpretações incorretas
5. Documentar decisões futuras

═══════════════════════════════════════════

Editar PRD agora? (s/n)
```

---

## 📚 Exemplos de Uso

### Exemplo 1: Projeto FastAPI sem Documentação

```bash
/prd-retrofit "API de gerenciamento de usuários"
```

**Resultado**:
```
✅ PRD Criado!

Versão detectada: 1.5.0 (via git tag)
Stack: FastAPI + SQLAlchemy + Pydantic

Funcionalidades extraídas:
- 15 endpoints REST
- 5 modelos de dados
- Autenticação JWT
- Validação Pydantic

ADRs gerados: 4
- ADR 001: Uso de FastAPI
- ADR 002: Repository Pattern
- ADR 003: JWT Authentication
- ADR 004: Clean Architecture

Arquivo: docs/PRD.md (gerado)
```

### Exemplo 2: CLI Tool Python

```bash
/prd-retrofit --version 2.0.0
```

**Resultado**:
```
✅ PRD Criado (v2.0.0)!

Tipo: CLI Tool
Framework: Click

Comandos detectados:
- init: Inicializar projeto
- build: Build do projeto
- deploy: Deploy para produção
- test: Executar testes

Estrutura:
- src/cli/ (comandos)
- src/core/ (lógica)
- tests/ (testes)

Arquivo: docs/PRD.md
```

### Exemplo 3: Projeto Django Legado

```bash
/prd-retrofit
```

**Resultado**:
```
✅ PRD Criado!

Versão: 3.2.0 (de apps/core/__init__.py)
Framework: Django 4.2

Apps detectados:
- users (autenticação)
- products (catálogo)
- orders (pedidos)
- analytics (relatórios)

Models: 18
Views: 32
Templates: 45

Histórico Git:
- 1,245 commits
- 5 anos de desenvolvimento
- 8 contribuidores

Arquivo: docs/PRD.md (3,500 linhas geradas)
```

---

## ⚠️ Limitações

### Análise Automática é Heurística

PRD gerado é baseado em:
- ✅ Código fonte (estrutura, imports, funções)
- ✅ Git history (commits, tags, contributors)
- ⚠️ Inferências (propósito, contexto de negócio)
- ❌ Requisitos reais de negócio (não detectáveis)

**Solução**: Sempre revisar e complementar manualmente.

### Contexto de Negócio Limitado

Código não revela:
- Por que decisões foram tomadas
- Requisitos de negócio originais
- Motivação de features
- Roadmap futuro

**Solução**: Adicionar seções manualmente no PRD.

### Git History Pode Ser Incompleto

Se projeto tem:
- Poucos commits informativos
- Mensagens genéricas ("fix", "update")
- Histórico reescrito (rebase)
- Sem tags de versão

**Resultado**: PRD terá menos contexto histórico.

---

## 🎯 Quando Usar

### ✅ Use `/prd-retrofit` quando:

1. **Projeto sem PRD**: Código existe mas nunca foi documentado
2. **Documentação Desatualizada**: PRD antigo não reflete código atual
3. **Baseline para Futuro**: Quer documentar estado atual antes de evoluir
4. **Auditoria de Código**: Precisa entender projeto legado rapidamente

### ❌ NÃO use `/prd-retrofit` quando:

1. **Projeto Novo**: Use `/setup-project-incremental`
2. **Quer Setup Completo**: Use `/adopt-incremental` (PRD + CLAUDE.md + Roadmap)
3. **PRD Existe e Está Correto**: Use `/prd-update` ou `/prd-fix`

---

## 🔗 Comandos Relacionados

- `/adopt-incremental` - Análise completa + PRD + Setup YAGNI
- `/setup-project-incremental` - Para projetos novos
- `/prd-update` - Atualizar PRD existente
- `/prd-view` - Ver PRD atual
- `/prd-help` - Ajuda completa

---

## 💡 Dicas

### Revisar Funcionalidades Detectadas

```bash
# Após gerar PRD
grep "✅" docs/PRD.md

# Validar:
- Todas as funcionalidades foram detectadas?
- Alguma foi mal interpretada?
- Falta algo importante?
```

### Adicionar Contexto de Negócio

```markdown
# Editar docs/PRD.md

## 1. Visão Geral

### 1.1. Contexto
[Substituir placeholder gerado por contexto real]

Problema REAL que o projeto resolve:
- [Adicionar manualmente]
```

### Documentar Decisões Futuras

```markdown
## 9. Roadmap Futuro

### Próximas Features (Manual)
- [ ] Implementar multi-tenancy
- [ ] Adicionar relatórios avançados
- [ ] Integrar com sistema X

Razão: [Explicar por quê]
Prioridade: [Alta/Média/Baixa]
```

### Manter PRD Atualizado

```bash
# Após adicionar nova feature
/prd-update "Adicionei feature X"

# Ou editar manualmente
vim docs/PRD.md
```

---

**Desenvolvido para incremental-dev - PRD Retroativo Automático** 📄
