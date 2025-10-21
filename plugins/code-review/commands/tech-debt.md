---
description: Gerencia débito técnico - adicionar, listar, atualizar, resolver e estatísticas
---

# Technical Debt Management

Comando para gerenciar débito técnico de forma estruturada e profissional. Mantém registro em `docs/TECHNICAL_DEBT.md` seguindo as melhores práticas da indústria.

## Como funciona

Este comando invoca o agente especializado `debt-manager` que:

- Cria/atualiza arquivo `docs/TECHNICAL_DEBT.md`
- Gera IDs únicos incrementais (TD-001, TD-002, etc.)
- Rastreia status (Open → In Progress → Resolved)
- Categoriza débitos (Security, Performance, Refactoring, Testing, Documentation, Architecture)
- Prioriza débitos (🔴 Critical, 🟡 Important, 🟢 Improvement)
- Fornece estatísticas e métricas

## Sintaxe

```bash
# Modo interativo (mostra menu de opções)
/tech-debt

# Adicionar novo débito
/tech-debt add

# Listar todos os débitos
/tech-debt list

# Listar com filtros
/tech-debt list --status open
/tech-debt list --priority critical
/tech-debt list --category security

# Atualizar status de débito
/tech-debt update TD-XXX

# Marcar débito como resolvido
/tech-debt resolve TD-XXX

# Mostrar estatísticas
/tech-debt stats
```

## Operações

### 1. Adicionar Débito (`add`)

Adiciona um novo débito técnico ao registro.

**Uso**:

```bash
/tech-debt add
```

**O agente perguntará**:

1. Título curto do problema
2. Categoria (Security/Performance/Refactoring/Testing/Documentation/Architecture)
3. Prioridade (Critical/Important/Improvement)
4. Localização no código (arquivo:linha)
5. Esforço estimado (horas/dias)
6. Impacto se não resolver
7. Descrição detalhada
8. Plano de resolução
9. Responsável (opcional)

**Exemplo de interação**:

```
/tech-debt add

Título: SQL Injection vulnerability in user query
Categoria: Security
Prioridade: Critical
Localização: src/database.py:42
Esforço estimado: 2 hours
Impacto: Security risk - SQL injection could expose user data
Descrição: Query uses f-string concatenation instead of parameterized queries
Plano de resolução:
1. Replace f-string with parameterized query
2. Add input validation
3. Add security tests
Responsável: @backend-team

✅ Débito TD-005 adicionado com sucesso em docs/TECHNICAL_DEBT.md!
```

### 2. Listar Débitos (`list`)

Lista todos os débitos técnicos registrados.

**Uso**:

```bash
# Listar todos
/tech-debt list

# Filtrar por status
/tech-debt list --status open
/tech-debt list --status in-progress
/tech-debt list --status resolved

# Filtrar por prioridade
/tech-debt list --priority critical
/tech-debt list --priority important
/tech-debt list --priority improvement

# Filtrar por categoria
/tech-debt list --category security
/tech-debt list --category performance
/tech-debt list --category refactoring
```

**Saída exemplo**:

```markdown
## Débitos Técnicos

### 🔴 Critical (2)
- [TD-001] SQL Injection vulnerability (Open) - src/database.py:42
- [TD-005] API credentials hardcoded (Open) - src/config.py:15

### 🟡 Important (3)
- [TD-002] Long function with high complexity (In Progress) - src/processor.py:30
- [TD-003] Missing test coverage (Open) - src/utils.py:calculate_discount
- [TD-004] Outdated dependencies (Open) - requirements.txt

### 🟢 Improvement (1)
- [TD-006] Add type hints to public API (Open) - src/api.py

**Total**: 6 débitos (Open: 4 | In Progress: 1 | Resolved: 1)
```

### 3. Atualizar Status (`update`)

Atualiza o status de um débito existente.

**Uso**:

```bash
/tech-debt update TD-005
```

**O agente perguntará**:

```
Status atual: Open

Novo status?
1. Open
2. In Progress
3. Resolved

Escolha (1/2/3):
```

**Resultado**:

```
✅ TD-005 atualizado para "In Progress"
```

### 4. Resolver Débito (`resolve`)

Marca um débito como resolvido e move para a seção de resolvidos.

**Uso**:

```bash
/tech-debt resolve TD-005
```

**O agente perguntará** (opcional):

```
Como foi resolvido? (resumo breve):
```

**Resultado**:

```
✅ TD-005 marcado como resolvido!
- Movido para seção de débitos resolvidos
- Data de resolução: 2025-10-21
- Resumo da resolução registrado
```

### 5. Estatísticas (`stats`)

Mostra estatísticas completas sobre os débitos técnicos.

**Uso**:

```bash
/tech-debt stats
```

**Saída exemplo**:

```markdown
# 📊 Estatísticas de Débito Técnico

## Resumo Geral
- **Total de débitos**: 15
- **Open**: 8 (53%)
- **In Progress**: 3 (20%)
- **Resolved**: 4 (27%)

## Por Prioridade
- 🔴 **Critical**: 2 (13%)
- 🟡 **Important**: 6 (40%)
- 🟢 **Improvement**: 7 (47%)

## Por Categoria
- Security: 3 (20%)
- Performance: 4 (27%)
- Refactoring: 5 (33%)
- Testing: 2 (13%)
- Documentation: 1 (7%)

## Métricas de Tempo
- **Idade média (Open)**: 12 dias
- **Tempo médio de resolução**: 5 dias
- **Taxa de resolução**: 27% (4 de 15)

## Débitos Mais Antigos
1. TD-001 - 45 dias (Critical - Security)
2. TD-003 - 32 dias (Important - Performance)
3. TD-007 - 28 dias (Important - Refactoring)

## Recomendação
⚠️ Você tem 2 débitos críticos abertos há mais de 30 dias.
   Considere priorizar TD-001 e TD-003.
```

### 6. Modo Interativo (sem argumentos)

Quando executado sem argumentos, mostra um menu interativo.

**Uso**:

```bash
/tech-debt
```

**Menu**:

```
📊 Technical Debt Management

Escolha uma operação:

1. ➕ Adicionar novo débito
2. 📋 Listar débitos
3. 🔄 Atualizar status de débito
4. ✅ Resolver débito
5. 📈 Ver estatísticas
6. ❌ Cancelar

Opção (1-6):
```

## Categorias Disponíveis

### 🔒 Security

Vulnerabilidades e problemas de segurança:

- Credenciais hardcoded
- SQL Injection
- XSS vulnerabilities
- Input sem sanitização
- Autenticação fraca
- Dependências vulneráveis

### ⚡ Performance

Problemas de performance e otimização:

- N+1 queries
- Loops desnecessários
- Chamadas síncronas em série
- Cache ausente
- Queries não otimizadas
- Indexes ausentes

### 🔧 Refactoring

Qualidade e manutenibilidade do código:

- Código duplicado (DRY)
- Funções muito longas
- Complexidade ciclomática alta
- Acoplamento forte
- Magic numbers
- Nomes genéricos

### 🧪 Testing

Cobertura e qualidade de testes:

- Falta de testes
- Mocks inadequados
- Testes dependentes
- Assertions genéricas
- Apenas happy path
- Setup/teardown complexo

### 📚 Documentation

Documentação e comentários:

- Funções sem docstrings
- README desatualizado
- API sem documentação
- TODOs sem contexto
- Type hints ausentes
- Comentários inadequados

### 🏗️ Architecture

Decisões arquiteturais e estrutura:

- Violação de SOLID
- Estrutura desorganizada
- Dependências circulares
- Abstrações ausentes
- Decisões técnicas temporárias

## Níveis de Prioridade

### 🔴 Critical (Alta)

**Quando usar**:

- Vulnerabilidades de segurança
- Bugs críticos em produção
- Bloqueadores de funcionalidades
- Dados em risco

**SLA recomendado**: Resolver em 1-3 dias

**Exemplos**:

- SQL Injection vulnerability
- API credentials exposed in code
- Data corruption risk
- Production outage potential

### 🟡 Important (Média)

**Quando usar**:

- Débito técnico que afeta manutenibilidade
- Performance não-crítica
- Refatorações importantes
- Testes ausentes em código crítico

**SLA recomendado**: Resolver em 1-2 semanas

**Exemplos**:

- Long function with high complexity
- Missing test coverage
- N+1 query problem
- Outdated dependencies

### 🟢 Improvement (Baixa)

**Quando usar**:

- Otimizações menores
- Melhorias de código
- Sugestões de qualidade
- Nice-to-have features

**SLA recomendado**: Backlog / quando houver tempo

**Exemplos**:

- Add type hints to functions
- Improve variable naming
- Add code comments
- Extract magic numbers

## Integração com Code Review

O comando `/review` pode invocar automaticamente `/tech-debt` após análise.

**Fluxo**:

1. Executar `/review`
2. Code review identifica problemas
3. Agente pergunta: "Deseja registrar os X débitos técnicos identificados? (s/n)"
4. Se sim: `/tech-debt` adiciona débitos automaticamente
5. Categorização automática baseada no tipo de problema

**Mapeamento automático**:

- "SQL Injection" → Security + Critical
- "Credencial hardcoded" → Security + Critical
- "Função longa" → Refactoring + Important
- "Falta testes" → Testing + Important
- "Missing type hints" → Documentation + Improvement

## Estrutura do Arquivo

O arquivo `docs/TECHNICAL_DEBT.md` é criado automaticamente com:

- **Header**: Metadata (última atualização, totais)
- **Seção 🔴 Critical**: Débitos críticos
- **Seção 🟡 Important**: Débitos importantes
- **Seção 🟢 Improvement**: Melhorias
- **Seção ✅ Resolved**: Débitos resolvidos (histórico)

Cada débito inclui 10 campos essenciais:

1. ID único (TD-XXX)
2. Status (Open/In Progress/Resolved)
3. Category
4. Created date
5. Owner
6. Location (arquivo:linha)
7. Estimated Effort
8. Impact
9. Description
10. Resolution Plan

## Boas Práticas

### ✅ Faça

- Registre débitos assim que identificados
- Seja específico na descrição
- Inclua localização exata do código
- Defina plano de resolução claro
- Estime esforço realisticamente
- Atualize status regularmente
- Resolva débitos críticos rapidamente

### ❌ Evite

- Débitos vagos sem location
- Duplicatas de problemas já registrados
- Registrar problemas triviais (<5 min para resolver)
- Deixar débitos críticos abertos por muito tempo
- Esquecer de atualizar status
- Registrar opiniões sem impacto técnico

## Exemplos de Uso Comum

### Cenário 1: Após Code Review

```bash
# 1. Executar review
/review

# 2. Review encontra 3 problemas
# 3. Plugin pergunta: "Registrar débitos? (s/n)"
# 4. Responder: s

# Resultado:
# ✅ 3 débitos técnicos adicionados:
# - TD-015: SQL Injection (Critical - Security)
# - TD-016: Long function (Important - Refactoring)
# - TD-017: Missing tests (Important - Testing)
```

### Cenário 2: Gerenciamento Manual

```bash
# Adicionar débito durante desenvolvimento
/tech-debt add

# Verificar débitos abertos
/tech-debt list --status open

# Começar a trabalhar em um
/tech-debt update TD-015
# Escolher: 2 (In Progress)

# Após resolver
/tech-debt resolve TD-015
# Resumo: "Refactored to use parameterized queries"
```

### Cenário 3: Sprint Planning

```bash
# Ver estatísticas para planejamento
/tech-debt stats

# Listar críticos para priorizar
/tech-debt list --priority critical

# Listar débitos de security
/tech-debt list --category security
```

## Localização do Arquivo

**Default**: `docs/TECHNICAL_DEBT.md`

O agente cria automaticamente:

1. Diretório `docs/` se não existir
2. Arquivo `TECHNICAL_DEBT.md` com template inicial
3. Estrutura completa com todas as seções

Se você preferir outro local, edite manualmente o caminho no agente `debt-manager`.

## Compatibilidade

Este comando funciona com **qualquer linguagem de programação** e **qualquer tipo de projeto**:

- Python, JavaScript, TypeScript, Java, Go, Rust, C++, C#, Ruby, PHP, etc.
- Monorepos e multiplos projetos
- Frameworks e bibliotecas diversos

O formato é genérico e focado no débito técnico, não na stack específica.

---

**Desenvolvido por Carlos Araujo para gerenciamento profissional de débito técnico** 📊
