---
description: Analisa configuração de slash command e valida boas práticas
allowed-tools: [Read, Grep, Glob, SlashCommand]
model: sonnet
argument-hint: COMMAND_NAME
---

# Slash Command Analyzer

Analisa a configuração de um slash command existente e valida se ele segue todas as boas práticas de arquitetura, YAML frontmatter e padrões de projeto.

## 🎯 Objetivo

- Validar estrutura YAML frontmatter do comando
- Verificar conformidade com naming conventions
- Analisar qualidade da descrição e argumentos
- Identificar anti-patterns e problemas de design
- Sugerir melhorias específicas e acionáveis

## 🔧 Instruções

1. **Localizar o Comando**

   - Buscar arquivo em `.claude/commands/[COMMAND_NAME].md`
   - Se não encontrado, buscar em subdiretórios (`.claude/skills/*/commands/`)
   - Se múltiplos encontrados, listar e pedir confirmação

1. **Validar YAML Frontmatter**

   - Verificar se existe delimitador `---` no início e fim
   - Validar campo `description` (40-80 caracteres, acionável)
   - Validar campo `allowed-tools` (array, ferramentas válidas)
   - Validar campo `model` **OBRIGATÓRIO**: Deve ser "sonnet", "haiku", ou valores parciais como "claude-sonnet-4-5", "claude-haiku-4-5". Não pode ser vazio ou ter valores inválidos.
   - Validar campo `argument-hint` (formato claro, \<50 caracteres)

1. **Validar Nome do Comando**

   - Deve estar em kebab-case (minúsculas, hífens)
   - Máximo 3 palavras
   - Deve ser acionável (verbo + substantivo)
   - Não deve usar CamelCase, underscores ou espaços

1. **Analisar Estrutura do Conteúdo**

   - Verificar seções essenciais:
     - ✅ Título claro
     - ✅ Objetivo com lista de resultados
     - ✅ Instruções numeradas e imperativas
     - ✅ Formato de Saída definido
     - ✅ Critérios de Sucesso em checklist
     - ✅ Exemplos práticos
   - Verificar se instruções são concisas (\<200 linhas total)

1. **Detectar Anti-Patterns**

   - ❌ Muitos argumentos (>5 posicionais)
   - ❌ Escopo muito amplo (múltiplas responsabilidades)
   - ❌ Descrição vaga ou genérica (\<40 caracteres)
   - ❌ Sem allowed-tools definidos
   - ❌ Campo `model` vazio ou com valor inválido (deve ser "sonnet", "haiku", ou valores parciais como "claude-sonnet-4-5")
   - ❌ Instruções vagas ou não imperativas
   - ❌ Faltando exemplos executáveis

1. **Gerar Relatório de Análise**

   - Apresentar scorecard de conformidade (0-100%)
   - Listar problemas encontrados por categoria
   - Sugerir correções específicas
   - Priorizar melhorias por impacto

1. **Correção Automática se Score < 85**

   - Se score total < 85 pontos:
     - Informar usuário sobre score baixo e necessidade de melhorias
     - Executar automaticamente `/update-slash-command [COMMAND_NAME]`
     - Passar lista de problemas críticos e moderados como contexto
     - Permitir que `/update-slash-command` guie o processo de correção
   - Se score >= 85 pontos:
     - Pular este passo e ir para passo 8 (correção opcional)

1. **Oferecer Correção Opcional (se Score >= 85)**

   - Se problemas não-críticos detectados, perguntar se deseja corrigir
   - Aplicar correções validadas
   - Criar backup antes de modificar

## 📊 Formato de Saída

```markdown
# 📋 Análise do Comando: /[nome-do-comando]

**Score de Conformidade:** [X/100] [🟢|🟡|🔴]

## ✅ Validações Aprovadas
- [Item validado com sucesso]
- [Item validado com sucesso]

## ⚠️ Problemas Encontrados

### 🔴 Críticos (Bloqueadores)
- [Problema crítico com descrição]
- [Problema crítico com descrição]

### 🟡 Moderados (Recomendações)
- [Problema moderado com descrição]
- [Problema moderado com descrição]

### 🔵 Melhorias Sugeridas
- [Melhoria opcional com descrição]
- [Melhoria opcional com descrição]

## 🔧 Correções Sugeridas

### Correção 1: [Título]
**Problema:** [Descrição do problema]
**Solução:** [Solução específica]
**Impacto:** [Alto|Médio|Baixo]

### Correção 2: [Título]
**Problema:** [Descrição do problema]
**Solução:** [Solução específica]
**Impacto:** [Alto|Médio|Baixo]

## 📈 Scorecard Detalhado

| Categoria | Score | Status |
|-----------|-------|--------|
| YAML Frontmatter | [X/20] | [🟢|🟡|🔴] |
| Nome e Convenções | [X/15] | [🟢|🟡|🔴] |
| Descrição | [X/15] | [🟢|🟡|🔴] |
| Estrutura de Conteúdo | [X/25] | [🟢|🟡|🔴] |
| Argumentos | [X/10] | [🟢|🟡|🔴] |
| Exemplos | [X/10] | [🟢|🟡|🔴] |
| Anti-Patterns Evitados | [X/5] | [🟢|🟡|🔴] |
| **TOTAL** | **[X/100]** | **[🟢|🟡|🔴]** |

---
**Legenda:**
- 🟢 Excelente (80-100%)
- 🟡 Necessita Melhorias (50-79%)
- 🔴 Crítico (<50%)
```

## ✅ Critérios de Sucesso

- [ ] Comando localizado com sucesso (arquivo .md existe)
- [ ] YAML frontmatter validado (todos os campos presentes e válidos)
- [ ] Nome validado (kebab-case, acionável, \<3 palavras)
- [ ] Descrição validada (40-80 caracteres, clara)
- [ ] Estrutura de conteúdo validada (seções essenciais presentes)
- [ ] Argumentos validados (\<5 posicionais, bem documentados)
- [ ] Anti-patterns detectados e reportados
- [ ] Score de conformidade calculado (0-100%)
- [ ] Relatório apresentado com sugestões acionáveis
- [ ] Opção de correção automática oferecida se problemas detectados

## ❌ Anti-Patterns

### ❌ Erro 1: Comando Não Encontrado

Não assuma o caminho do comando:

```bash
# ❌ Errado
Read /some/random/path/comando.md

# ✅ Correto
1. Glob pattern: .claude/commands/*.md
2. Grep: Buscar por nome
3. Se não encontrado: Buscar em subdiretórios
```

### ❌ Erro 2: Validação Incompleta

Não validar apenas um aspecto:

```markdown
# ❌ Errado
"O comando tem YAML frontmatter válido" → Aprovado

# ✅ Correto
Validar TODOS os critérios:
- YAML frontmatter
- Nome e convenções
- Descrição
- Estrutura
- Argumentos
- Exemplos
- Anti-patterns
```

### ❌ Erro 3: Score Subjetivo

Não calcular score manualmente ou arbitrariamente:

```markdown
# ❌ Errado
"O comando parece bom, score: 85%"

# ✅ Correto
Score baseado em critérios objetivos:
- YAML Frontmatter: 20 pontos (5 campos × 4 pontos)
  - description: 4 pontos
  - allowed-tools: 4 pontos
  - model (OBRIGATÓRIO): 4 pontos (sonnet ou haiku, não vazio)
  - argument-hint: 4 pontos
  - delimitadores: 4 pontos
- Nome: 15 pontos (3 critérios × 5 pontos)
- Descrição: 15 pontos (tamanho + clareza)
- Estrutura: 25 pontos (5 seções × 5 pontos)
- Argumentos: 10 pontos (<5 args + documentação)
- Exemplos: 10 pontos (presença + executável)
- Anti-patterns: 5 pontos (nenhum detectado)
```

### ❌ Erro 4: Sugestões Vagas

Não dar feedback genérico:

```markdown
# ❌ Errado
"Melhore a descrição do comando"

# ✅ Correto
**Problema:** Descrição muito curta (28 caracteres, mínimo 40)
**Solução:** Expandir para incluir verbo de ação e contexto
**Exemplo:** "Analisa configuração de slash command e valida boas práticas" (68 caracteres)
**Impacto:** Alto (descrição é primeiro contato do usuário)
```

### ❌ Erro 5: Não Oferecer Correção

Não apenas reportar problemas:

```markdown
# ❌ Errado
"Encontrados 5 problemas. Análise concluída."

# ✅ Correto
"Encontrados 5 problemas. Deseja que eu corrija automaticamente?
[Sim/Não/Mostrar correções primeiro]"
```

### ❌ Erro 6: Não Validar Campo Model

Campo `model` deve ser validado rigorosamente:

```markdown
# ❌ Errado
"Campo model: presente ✅"

# ✅ Correto
Validar campo model:
- ❌ CRÍTICO: Campo model está vazio (deve ser "sonnet", "haiku", ou valores parciais)
- ❌ CRÍTICO: Campo model com valor inválido "gpt-4" (deve ser "sonnet", "haiku", ou começar com "claude-")
- ✅ Campo model: "sonnet" (válido para tarefa complexa)
- ✅ Campo model: "haiku" (válido para tarefa simples)
- ✅ Campo model: "claude-sonnet-4-5" (válido - versão parcial do Sonnet)
- ✅ Campo model: "claude-haiku-4-5" (válido - versão parcial do Haiku)

**Problema:** Campo model vazio ou inválido (-4 pontos)
**Solução:** Definir model="sonnet" (ou "claude-sonnet-4-5") para tarefas complexas (validações, análises) ou model="haiku" (ou "claude-haiku-4-5") para tarefas simples (listagens, formatação)
**Impacto:** Alto (afeta performance e custo da execução)
```

## 📝 Exemplo

```bash
/slash-analyzer create-slash-command
```

**O que acontece:**

1. Localiza `.claude/commands/create-slash-command.md`
1. Valida YAML frontmatter
1. Verifica nome em kebab-case
1. Analisa descrição (comprimento, clareza)
1. Verifica estrutura de seções
1. Detecta anti-patterns
1. Calcula score de conformidade
1. Apresenta relatório com:
   - Score: 92/100 🟢
   - 2 melhorias sugeridas
   - 0 problemas críticos
1. Oferece aplicar correções automaticamente

______________________________________________________________________

**Uso Típico:**

```bash
# Analisar comando específico
/slash-analyzer meu-comando

# Analisar e corrigir
/slash-analyzer meu-comando
# → Relatório apresentado
# → "Deseja corrigir automaticamente? [Sim/Não]"
```
