---
description: Adotar desenvolvimento incremental em projeto existente - analisa código, cria PRD retroativo e sugere simplificações
---

# Adopt Incremental Development (Projeto Existente)

Este comando permite adotar desenvolvimento incremental em **projetos já iniciados**, analisando o código existente e criando um PRD retroativo baseado no estado atual.

## 🎯 Objetivo

Permitir que projetos legados adotem YAGNI e desenvolvimento incremental:
- Analisar código existente automaticamente
- Criar PRD retroativo (baseado em código real)
- Identificar over-engineering e débito técnico
- Gerar roadmap de simplificação incremental
- Configurar CLAUDE.md com princípios YAGNI

## 📋 Como usar

```bash
# Análise completa automática
/adopt-incremental

# Com descrição do projeto (ajuda análise)
/adopt-incremental "API REST com FastAPI para gerenciar usuários"
```

## 🔍 Processo de Execução

### Passo 1: Detectar Projeto Existente

```
═══════════════════════════════════════════
🔍 ADOTAR DESENVOLVIMENTO INCREMENTAL
═══════════════════════════════════════════

Analisando projeto existente...
```

**1.1. Verificar se há código no projeto**:

```python
# Procurar por:
- Arquivos Python: *.py
- Arquivos de configuração: requirements.txt, pyproject.toml, setup.py
- Git repository: .git/
- Estrutura de diretórios: src/, app/, lib/
```

**Se NÃO há código**:
```
⚠️  Nenhum código detectado

Este comando é para projetos EXISTENTES.
Para projetos novos, use: /setup-project-incremental

Continuar mesmo assim? (s/n)
```

**Se HÁ código**:
```
✅ Projeto existente detectado!

Estrutura encontrada:
├─ [X] arquivos Python
├─ [X] linhas de código
├─ [X] diretórios principais
└─ Git: [SIM/NÃO]

Prosseguir com análise? (s/n)
```

---

### Passo 2: Análise Automática do Código

```
📊 Analisando código existente...

[Barra de progresso]
├─ Detectando funcionalidades...
├─ Analisando complexidade...
├─ Identificando padrões...
└─ Calculando métricas...
```

**2.1. Coletar Métricas**:

```python
Métricas:
- Total de arquivos: [X]
- Linhas de código: [X]
- Funções/classes: [X]
- Complexidade média: [X]
- Duplicação: [X]%
- Cobertura de testes: [X]% (se detectado)
```

**2.2. Detectar Funcionalidades**:

Analisar código para identificar funcionalidades implementadas:

```python
# Análise baseada em:
1. Nomes de funções/classes (inferir propósito)
2. Endpoints (se FastAPI/Flask/Django)
3. Docstrings
4. Comentários
5. Estrutura de diretórios
```

**Output**:
```
🎯 Funcionalidades Detectadas:

1. Gerenciamento de Usuários
   ├─ Criar usuário (create_user)
   ├─ Listar usuários (list_users)
   ├─ Atualizar usuário (update_user)
   └─ Deletar usuário (delete_user)

2. Autenticação
   ├─ Login (authenticate)
   ├─ Logout (logout)
   └─ Refresh token (refresh_token)

3. Validação de Dados
   ├─ Validar email (validate_email)
   ├─ Validar senha (validate_password)
   └─ Sanitize input (sanitize_input)
```

**2.3. Identificar Over-Engineering**:

```python
# Detectar:
- Classes abstratas com 1 implementação
- Factory patterns com 1-2 produtos
- Configuração complexa para poucos parâmetros
- Código genérico nunca reutilizado
```

**Output**:
```
⚠️  Possível Over-Engineering Detectado:

1. AbstractUserRepository (src/repositories/base.py)
   └─ Apenas 1 implementação: SQLUserRepository
   └─ Sugestão: Remover abstração, usar classe concreta
   └─ Impacto: -80 LOC, +15% legibilidade

2. UserFactory (src/factories/user.py)
   └─ Cria apenas 1 tipo de usuário
   └─ Sugestão: Substituir por função create_user()
   └─ Impacto: -50 LOC, -1 arquivo

3. ConfigManager (src/config/manager.py)
   └─ 200 LOC para gerenciar 5 configs
   └─ Sugestão: Usar dict ou dataclass
   └─ Impacto: -180 LOC, -1 dependência
```

**2.4. Analisar Histórico Git (se disponível)**:

```bash
# Executar:
git log --oneline --all | wc -l  # Total de commits
git log --format="%an" | sort | uniq -c | sort -rn  # Contribuidores
git log --since="1 year ago" --format="%cr" | head -1  # Último commit
```

**Output**:
```
📚 Histórico do Projeto:

- Total de commits: [X]
- Contribuidores: [X]
- Idade do projeto: [X meses/anos]
- Último commit: [X dias atrás]
- Branch principal: [main/master]
```

---

### Passo 3: Criar PRD Retroativo

```
📝 Gerando PRD retroativo...

Criando docs/PRD.md baseado no código existente...
```

**3.1. Gerar PRD.md**:

Usar template `templates/PRD.md` e preencher com dados da análise:

```markdown
# Product Requirements Document

## Metadados
- **Versão do PRD**: [versão detectada do projeto ou 1.0.0]
- **Status**: Retroativo (criado a partir de código existente)
- **Data de Criação**: [hoje]
- **Última Atualização**: [hoje]

## 1. Visão Geral

### Problema
[Inferir do código/descrição fornecida]

### Solução
[Descrever com base nas funcionalidades detectadas]

## 2. Objetivos

### Objetivos Detectados (baseado em código)
- [Funcionalidade 1]
- [Funcionalidade 2]
- [Funcionalidade 3]

## 3. Funcionalidades Implementadas

### [Grupo de Funcionalidade 1]
- ✅ [Feature A] (implementada)
- ✅ [Feature B] (implementada)

### [Grupo de Funcionalidade 2]
- ✅ [Feature C] (implementada)

## 4. Decisões Arquiteturais (ADRs Retroativos)

### ADR 001: [Decisão detectada]
- **Status**: Implementado
- **Contexto**: [Inferido do código]
- **Decisão**: [Uso de X pattern/framework]
- **Consequências**: [Impacto detectado]

## 5. Oportunidades YAGNI

### Over-Engineering Identificado
1. [Abstração desnecessária 1]
   - Impacto: [métricas]
   - Recomendação: [ação]

2. [Complexidade excessiva 2]
   - Impacto: [métricas]
   - Recomendação: [ação]

## 6. Roadmap de Simplificação

### Fase 1: Simplificações Rápidas (Prioridade Alta)
- [ ] Remover [abstração X]
- [ ] Simplificar [componente Y]

### Fase 2: Refatorações Médias (Prioridade Média)
- [ ] Refatorar [padrão Z]
- [ ] Consolidar [código duplicado]

### Fase 3: Refatorações Complexas (Prioridade Baixa)
- [ ] Redesign de [módulo A]

## 7. Métricas Atuais

- LOC: [X]
- Complexidade: [X]
- Duplicação: [X]%
- Cobertura: [X]%

## 8. Próximos Passos

1. Revisar PRD retroativo
2. Validar funcionalidades detectadas
3. Priorizar simplificações
4. Executar roadmap incremental
```

**3.2. Salvar PRD**:

```bash
# Criar diretório se não existir
mkdir -p docs/

# Salvar PRD
# docs/PRD.md
```

**3.3. Confirmar com usuário**:

```
═══════════════════════════════════════════
📄 PRD RETROATIVO GERADO
═══════════════════════════════════════════

Localização: docs/PRD.md
Versão: [versão]

Conteúdo:
- Funcionalidades detectadas: [X]
- Over-engineering identificado: [X]
- Roadmap de simplificação: [X] itens

═══════════════════════════════════════════

Revisar PRD antes de continuar? (s/n/editar)

- s: Continuar com setup
- n: Cancelar processo
- editar: Ajustar PRD manualmente
═══════════════════════════════════════════
```

---

### Passo 4: Configurar CLAUDE.md

```
⚙️  Configurando CLAUDE.md...

Adicionando instruções de desenvolvimento incremental...
```

**4.1. Chamar `/setup-project-incremental` internamente**:

Executar comando para adicionar seção YAGNI ao CLAUDE.md (se não existir).

**4.2. Adicionar seção específica para projeto legado**:

```markdown
## 🔄 Transição para Desenvolvimento Incremental

**IMPORTANTE**: Este projeto foi iniciado ANTES de adotar princípios YAGNI.

### Status Atual (Análise Automática)

- **LOC**: [X]
- **Complexidade**: [média/alta]
- **Over-engineering detectado**: [X] casos
- **Roadmap de simplificação**: docs/PRD.md

### Regras para Evolução do Projeto

1. **Novas Funcionalidades**: SEMPRE seguir YAGNI
   - Implementar apenas o necessário
   - Evitar abstrações prematuras
   - Código simples primeiro

2. **Código Existente**: Simplificar INCREMENTALMENTE
   - Não refatorar tudo de uma vez
   - Priorizar por impacto (ver PRD.md)
   - Testar após cada simplificação

3. **Débito Técnico**: Pagar gradualmente
   - 1-2 simplificações por sprint
   - Medir melhoria (LOC, complexidade)
   - Documentar decisões no PRD

### Próximas Simplificações (Prioridade)

Consultar **docs/PRD.md → Roadmap de Simplificação**

1. [Simplificação prioritária 1]
2. [Simplificação prioritária 2]
3. [Simplificação prioritária 3]
```

---

### Passo 5: Gerar Roadmap de Ação

```
🗺️  Gerando roadmap de adoção...
```

**Output**:

```
═══════════════════════════════════════════
✅ ADOÇÃO DE DESENVOLVIMENTO INCREMENTAL COMPLETA!
═══════════════════════════════════════════

📊 ANÁLISE DO PROJETO:

Código Existente:
├─ [X] arquivos Python
├─ [X] linhas de código
├─ [X] funcionalidades detectadas
└─ [X] oportunidades de simplificação

Documentação Criada:
├─ docs/PRD.md (PRD retroativo)
└─ CLAUDE.md (instruções YAGNI)

═══════════════════════════════════════════

🗺️  ROADMAP DE ADOÇÃO (Próximos Passos):

FASE 1: Revisar e Validar (1-2 dias)
├─ [ ] Ler docs/PRD.md
├─ [ ] Validar funcionalidades detectadas
├─ [ ] Ajustar roadmap de simplificação
└─ [ ] Confirmar prioridades

FASE 2: Simplificações Rápidas (1 semana)
├─ [ ] Executar: /review-yagni
├─ [ ] Remover abstrações desnecessárias (1-2)
├─ [ ] Medir impacto (LOC, complexidade)
└─ [ ] Atualizar PRD com resultados

FASE 3: Novas Features com YAGNI (contínuo)
├─ [ ] Sempre consultar CLAUDE.md antes de adicionar features
├─ [ ] Executar: /add-increment para novas funcionalidades
├─ [ ] Manter PRD atualizado
└─ [ ] Medir cobertura de testes

FASE 4: Refatorações Incrementais (2-4 semanas)
├─ [ ] Executar: /refactor-now quando padrões emergirem
├─ [ ] Priorizar por impacto (ver PRD)
├─ [ ] 1-2 refatorações por sprint
└─ [ ] Documentar decisões (ADRs)

═══════════════════════════════════════════

💡 COMANDOS ÚTEIS:

Revisar over-engineering:
  /review-yagni

Sugerir refatorações:
  /refactor-now

Adicionar nova feature (YAGNI):
  /add-increment "descrição"

Ver ajuda completa:
  /prd-help

═══════════════════════════════════════════

🎯 META: Simplificar [X] LOC em 1 mês

Próxima ação recomendada:
  1. Ler docs/PRD.md
  2. Executar: /review-yagni
  3. Escolher 1-2 simplificações de alta prioridade
  4. Implementar e medir impacto

═══════════════════════════════════════════
```

---

## 📚 Exemplos de Uso

### Exemplo 1: API FastAPI com Over-Engineering

```bash
/adopt-incremental "API REST para gerenciar produtos"
```

**Resultado**:
```
✅ Análise completa!

Funcionalidades detectadas:
- CRUD de produtos (4 endpoints)
- Autenticação JWT
- Validação com Pydantic

Over-engineering identificado:
1. AbstractRepository com 1 implementação
   → Remover: -120 LOC
2. Factory pattern para criar produtos
   → Simplificar: -60 LOC
3. ConfigManager para 3 configs
   → Usar dict: -90 LOC

Total de simplificação possível: -270 LOC (18%)

PRD criado em: docs/PRD.md
```

### Exemplo 2: Projeto Django Legado

```bash
/adopt-incremental
```

**Resultado**:
```
✅ Projeto Django detectado!

Apps detectados:
- users (autenticação)
- products (catálogo)
- orders (pedidos)

Complexidade:
- LOC: 5,200
- Apps: 3
- Models: 12
- Views: 24

Oportunidades YAGNI:
- 3 managers customizados (poderiam ser querysets)
- 5 mixins com 1 uso cada
- Signals complexos (poderiam ser métodos)

Roadmap de simplificação: 15 itens
Redução potencial: -800 LOC (15%)
```

### Exemplo 3: Projeto sem Git

```bash
/adopt-incremental "CLI tool Python"
```

**Resultado**:
```
⚠️  Git não detectado

Análise limitada (sem histórico):
- Funcionalidades: detectadas via código
- Métricas: calculadas
- Over-engineering: identificado

Recomendação: Inicializar git para melhor análise
  git init
  git add .
  git commit -m "Initial commit"

Continuar sem git? (s/n)
```

---

## ⚠️ Limitações

### Análise Automática

A análise é baseada em heurísticas e pode:
- ❌ Não detectar todas as funcionalidades
- ❌ Marcar código complexo necessário como over-engineering
- ❌ Não entender requisitos de negócio

**Solução**: Sempre revisar PRD gerado e ajustar manualmente.

### Funcionalidades Não Detectáveis

Algumas funcionalidades podem não ser detectadas:
- Lógica de negócio muito específica
- Integrações externas sem indicadores claros
- Background jobs/tasks
- Configurações de deploy

**Solução**: Adicionar manualmente ao PRD após análise.

### Over-Engineering Falso Positivo

Código pode parecer over-engineering mas ser necessário:
- Abstrações para testes
- Padrões exigidos por frameworks
- Requisitos de escalabilidade futura REAIS

**Solução**: Validar cada sugestão antes de simplificar.

---

## 🎯 Quando Usar

### ✅ Use `/adopt-incremental` quando:

1. **Projeto Legado**: Código existente precisa de simplificação
2. **Sem Documentação**: PRD nunca foi criado
3. **Over-Engineering**: Código muito complexo sem motivo claro
4. **Adoção YAGNI**: Quer adotar desenvolvimento incremental

### ❌ NÃO use `/adopt-incremental` quando:

1. **Projeto Novo**: Use `/setup-project-incremental`
2. **PRD Existe**: Use `/prd-update` ou `/prd-fix`
3. **Já Segue YAGNI**: Use `/review-yagni` ou `/refactor-now`

---

## 🔗 Comandos Relacionados

- `/setup-project-incremental` - Para projetos NOVOS
- `/prd-retrofit` - Criar apenas PRD retroativo (sem setup)
- `/review-yagni` - Revisar over-engineering
- `/refactor-now` - Sugerir refatorações
- `/prd-help` - Ajuda completa do plugin

---

## 💡 Dicas

### Revisar PRD Gerado

Sempre revisar e ajustar:
```bash
# Após /adopt-incremental
vim docs/PRD.md

# Validar:
- Funcionalidades detectadas estão corretas?
- Over-engineering identificado é real?
- Roadmap de simplificação está priorizado?
```

### Medir Impacto

Antes de simplificar:
```bash
# Baseline
wc -l **/*.py  # Total LOC
# Anotar: [X] LOC

# Após simplificação
wc -l **/*.py  # Novo total
# Calcular: [Y] LOC removido
# Atualizar PRD.md
```

### Simplificar Incrementalmente

**NÃO** refatorar tudo de uma vez:
```
❌ ERRADO: Reescrever 50% do código em 1 semana
✅ CORRETO: Remover 1-2 abstrações por semana, testando cada mudança
```

---

**Desenvolvido para incremental-dev - Suporte a Projetos Legados** 🔄