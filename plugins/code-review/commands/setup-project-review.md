---
description: Configura CLAUDE.md do projeto com checklist de code review, padrões de qualidade e orientações sobre débito técnico
---

# Setup Project for Code Review

Este comando configura o arquivo `CLAUDE.md` do projeto atual com instruções de code review, padrões de qualidade, segurança e gerenciamento de débito técnico.

## 🎯 Objetivo

Adicionar ao `CLAUDE.md` do projeto instruções claras para que Claude:
- Execute code reviews seguindo padrões do projeto
- Identifique vulnerabilidades de segurança específicas da stack
- Aplique checklist customizado de qualidade
- Gerencie débito técnico de forma estruturada
- Priorize problemas corretamente (Crítico/Importante/Sugestão)

## 📋 Como usar

```bash
/setup-project-review
```

Ou com descrição da stack:

```bash
/setup-project-review "API REST Python com FastAPI + PostgreSQL + Redis"
```

## 🔍 Processo de Execução

### 1. Detectar ou Criar CLAUDE.md

**Se CLAUDE.md existe**:
- Ler arquivo atual
- Adicionar seção "Code Review & Quality Standards" ao final
- Preservar conteúdo existente

**Se CLAUDE.md NÃO existe**:
- Criar arquivo na raiz do projeto
- Adicionar template completo de code review

### 2. Adicionar Instruções de Code Review

O comando deve adicionar a seguinte seção ao `CLAUDE.md`:

```markdown
# Code Review & Quality Standards

**IMPORTANTE**: Este projeto utiliza o plugin `code-review` para análise automática de código e gerenciamento de débito técnico.

## 📋 Padrões de Code Review

### ✅ Checklist Obrigatório

Antes de cada commit/PR, validar:

#### 🔒 Segurança
- [ ] Sem credenciais hardcoded (API keys, passwords, tokens)
- [ ] Sem SQL injection (usar parâmetros, não concatenação)
- [ ] Sem XSS (sanitizar inputs do usuário)
- [ ] Sem funções perigosas (eval, exec, deserialização insegura)
- [ ] Autenticação/autorização implementada corretamente
- [ ] Dados sensíveis criptografados (em trânsito e em repouso)

#### 🐛 Bugs Comuns
- [ ] Sem null pointer/undefined access
- [ ] Error handling adequado (try/catch, validações)
- [ ] Sem race conditions (locks, transações)
- [ ] Sem memory leaks (close, cleanup)
- [ ] Validação de inputs (tipo, range, formato)

#### ✨ Qualidade de Código
- [ ] Nomenclatura clara e consistente
- [ ] Funções pequenas e focadas (< 50 linhas)
- [ ] Sem código duplicado (DRY - Don't Repeat Yourself)
- [ ] Sem magic numbers (usar constantes nomeadas)
- [ ] Complexidade ciclomática baixa (< 10)
- [ ] Acoplamento baixo, coesão alta

#### 🧪 Testes
- [ ] Testes unitários para nova funcionalidade
- [ ] Cobertura ≥ 80% (ou padrão do projeto)
- [ ] Testes de casos de erro (edge cases)
- [ ] Mocks adequados (sem chamadas reais a APIs/DB)
- [ ] Fixtures reutilizáveis (conftest.py)
- [ ] Testes seguros para execução paralela

#### 📚 Documentação
- [ ] Docstrings em funções complexas/públicas
- [ ] README atualizado (se mudou funcionalidade)
- [ ] Comentários explicam "por quê", não "o quê"
- [ ] API endpoints documentados (OpenAPI/Swagger)
- [ ] Changelog atualizado (se aplicável)

#### ⚡ Performance
- [ ] Sem N+1 queries (usar joins, bulk queries)
- [ ] Operações assíncronas quando possível
- [ ] Índices de banco de dados adequados
- [ ] Cache implementado onde necessário
- [ ] Sem loops ineficientes

## 🎯 Priorização de Problemas

### 🔴 Críticos (BLOQUEAR COMMIT)

Problemas que DEVEM ser corrigidos ANTES do commit:

- Credenciais hardcoded
- SQL injection, XSS, CSRF
- Funções perigosas (eval, exec)
- Vazamento de dados sensíveis
- Bugs que quebram funcionalidade existente
- Violação de autenticação/autorização

**Ação**: ❌ NÃO COMMITAR até resolver

### 🟡 Importantes (CORRIGIR EM BREVE)

Problemas que devem ser corrigidos nos próximos dias:

- Falta de testes em código novo
- Funções muito longas (> 50 linhas)
- Código duplicado significativo
- Error handling inadequado
- Performance ruim (N+1, loops ineficientes)
- Falta de documentação em código complexo

**Ação**: ✅ Pode commitar, mas criar issue/task

### 🟢 Sugestões (BACKLOG)

Melhorias que podem ser feitas eventualmente:

- Refatoração para melhor legibilidade
- Adicionar type hints/annotations
- Melhorar nomenclatura
- Otimizações de performance menores
- Documentação adicional
- Testes adicionais de edge cases

**Ação**: ✅ Pode commitar, considerar no backlog

## 📊 Débito Técnico

### Rastreamento em docs/TECHNICAL_DEBT.md

O plugin mantém registro estruturado de débito técnico em `docs/TECHNICAL_DEBT.md`:

**Formato de ID**: `TD-XXX` (incremental, único)

**Status**:
- `Open` - Débito identificado, não resolvido
- `In Progress` - Alguém está trabalhando
- `Resolved` - Débito resolvido

**Categorias**:
- `Security` - Vulnerabilidades de segurança
- `Performance` - Problemas de performance
- `Refactoring` - Código que precisa refatoração
- `Testing` - Falta de testes ou testes ruins
- `Documentation` - Falta de documentação
- `Architecture` - Problemas arquiteturais

**Prioridades**:
- 🔴 `Critical` - Impacto alto, urgente
- 🟡 `Important` - Impacto médio, importante
- 🟢 `Improvement` - Melhoria, não urgente

### Comandos de Débito Técnico

```bash
# Adicionar novo débito
/tech-debt add

# Listar todos os débitos
/tech-debt list

# Atualizar status de débito
/tech-debt update TD-001

# Resolver débito
/tech-debt resolve TD-001

# Estatísticas de débito
/tech-debt stats
```

## 🔄 Workflow de Code Review

### 1. Antes de Commitar

```bash
# 1. Stage mudanças
git add .

# 2. Executar code review
/review

# 3. Analisar relatório
# - 🔴 Críticos: Corrigir AGORA
# - 🟡 Importantes: Criar task
# - 🟢 Sugestões: Considerar

# 4. Corrigir críticos

# 5. Commitar
/commit
```

### 2. Durante Pull Request

```bash
# 1. Checkout na branch
git checkout feature/new-feature

# 2. Executar review
/review

# 3. Registrar débitos importantes
/tech-debt add  # Se necessário

# 4. Comentar no PR com resultado
```

### 3. Manutenção de Débito Técnico

```bash
# Mensalmente: Revisar débitos acumulados
/tech-debt stats

# Priorizar resolução de:
# 1. 🔴 Critical → Resolver urgente
# 2. 🟡 Important → Planejar sprint
# 3. 🟢 Improvement → Backlog
```

## 🎯 Plugin Code Review

Este projeto usa o plugin `code-review` com os seguintes recursos:

**Comandos**:
- `/review` - Executar code review completo
- `/tech-debt` - Gerenciar débito técnico

**Agentes**:
- `code-reviewer` - Análise de código automática
- `debt-manager` - Gerenciamento de débito técnico

**Análises**:
- Segurança (credenciais, injection, XSS)
- Qualidade (estrutura, nomenclatura, complexidade)
- Testes (cobertura, mocks, fixtures)
- Documentação (docstrings, README)
- Performance (N+1, loops, async)
- Débito técnico (DRY, acoplamento)

---

**Filosofia**: Qualidade > Velocidade | Prevenir > Corrigir | Automatizar > Manual
```

### 3. Adicionar Contexto do Projeto (Se Fornecido)

Se o usuário fornecer descrição da stack, adicionar seção customizada:

```markdown
## 📊 Contexto Deste Projeto

**Stack**: [stack fornecida pelo usuário]

**Checklist Específico**:
- Validações específicas da linguagem
- Frameworks em uso
- Padrões de segurança da stack
- Ferramentas de qualidade recomendadas

**Débito Técnico Comum**:
- Problemas típicos da stack
- Anti-patterns conhecidos
- Otimizações recomendadas
```

### 4. Detectar Stack do Projeto

Analisar projeto para customizar instruções:

- **Python**: Verificar pytest, black, mypy, bandit
- **JavaScript/TypeScript**: Verificar jest, eslint, prettier
- **Java**: Verificar junit, maven, checkstyle
- **Go**: Verificar testing, golint, gofmt
- **Rust**: Verificar cargo test, clippy, rustfmt

**Adicionar ao CLAUDE.md**:

```markdown
## 🔧 Stack Detectada

**Linguagem**: [detectada]
**Framework**: [detectado]
**Gerenciador de Pacotes**: [detectado]
**Framework de Testes**: [detectado]

**Ferramentas Recomendadas**:
- Linter: [específico da linguagem]
- Formatter: [específico da linguagem]
- Security Scanner: [específico da linguagem]
- Coverage Tool: [específico do framework de testes]
```

### 5. Confirmar com Usuário

Mostrar preview do que será adicionado:

```
═══════════════════════════════════════════
📝 SETUP CODE REVIEW
═══════════════════════════════════════════

Arquivo: CLAUDE.md

Ação: [CRIAR NOVO / ADICIONAR SEÇÃO]

Stack Detectada:
- Linguagem: [linguagem]
- Framework: [framework]
- Testes: [framework de testes]

Conteúdo a ser adicionado:
---
[Preview das instruções]
---

Adicionar ao CLAUDE.md? (s/n)
```

### 6. Criar/Atualizar Arquivo

Se usuário confirmar:
- Criar ou atualizar CLAUDE.md
- Adicionar instruções completas
- Preservar conteúdo existente (NUNCA sobrescrever)
- Validar que arquivo foi criado corretamente

```
✅ CLAUDE.md configurado com sucesso!

Instruções de code review adicionadas.

Stack detectada:
- Linguagem: Python
- Framework: FastAPI
- Testes: pytest

Próximos passos:
1. Revisar CLAUDE.md
2. Customizar checklist (se necessário)
3. Executar: /review
4. Gerenciar débitos: /tech-debt

Claude agora está orientado a:
✓ Executar code reviews com padrões do projeto
✓ Identificar vulnerabilidades de segurança
✓ Gerenciar débito técnico estruturadamente
✓ Priorizar problemas corretamente
```

## 📚 Exemplos de Uso

### Exemplo 1: Novo Projeto Python

```bash
/setup-project-review "API REST Python com FastAPI + PostgreSQL"
```

**Resultado**:
- Cria `CLAUDE.md` na raiz do projeto
- Adiciona checklist específico para Python/FastAPI
- Inclui validações de segurança SQL
- Configura padrões pytest
- Orienta sobre async/await

### Exemplo 2: Projeto Existente JavaScript

```bash
/setup-project-review "Frontend React + TypeScript + Jest"
```

**Resultado**:
- Detecta `CLAUDE.md` existente
- Adiciona seção de code review ao final
- Preserva conteúdo existente
- Inclui validações de TypeScript
- Configura padrões Jest/Testing Library

### Exemplo 3: Projeto Multi-Linguagem

```bash
/setup-project-review "Backend Go + Frontend Vue.js"
```

**Resultado**:
- Detecta múltiplas linguagens
- Adiciona checklist para ambas
- Configura padrões Go testing + Vitest
- Orienta sobre APIs REST entre frontend/backend

## ⚠️ Importante

### Não Sobrescrever Conteúdo Existente

Se `CLAUDE.md` já existe:
- ❌ NUNCA sobrescrever conteúdo
- ✅ SEMPRE adicionar ao final
- ✅ Usar separador claro: `---`

### Detectar Linguagem e Framework

Analisar projeto para customizar instruções:
- Verificar arquivos: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Detectar framework: FastAPI, Express, Spring Boot, Django
- Identificar gerenciador de pacotes: pip, npm, cargo, go mod

### Validar Sintaxe Markdown

Após criar/atualizar:
- Verificar que markdown está válido
- Headers bem formatados
- Code blocks fechados corretamente
- Links funcionando

## 🚀 Após Executar Este Comando

O usuário terá:

1. ✅ `CLAUDE.md` configurado com padrões de code review
2. ✅ Claude orientado a seguir checklist do projeto
3. ✅ Workflow claro de review antes de commits
4. ✅ Gerenciamento de débito técnico estruturado
5. ✅ Priorização automática de problemas

**Próximo passo**: Executar `/review` para validar código atual!

## 💡 Dica

Após configurar o projeto, sempre execute code review antes de commits:

```bash
git add .
/review
# Corrigir críticos
/commit
```

Isso garantirá qualidade consistente e prevenção de problemas de segurança.