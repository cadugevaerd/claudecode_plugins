---
description: Corrige ou ajusta seções específicas do PRD.md existente de forma cirúrgica
---

# PRD Fix - Ajustes Cirúrgicos no PRD

Permite fazer correções e ajustes específicos em seções individuais do PRD sem reescrever o documento inteiro.

> **📘 Related Command**: For complete PRD updates (changing entire document or multiple sections), use `/prd-update`. This command (`/prd-fix`) is designed for surgical, single-section modifications only.

## 🎯 Objetivo

Fazer modificações pontuais no PRD.md quando:
- Uma seção precisa ser corrigida
- Novos requisitos surgem
- Detalhes técnicos mudam
- Prioridades são ajustadas
- Métricas de sucesso evoluem

## 📋 Como Usar

### Uso Básico

```bash
# Ajustar uma seção específica
/prd-fix "Adicionar autenticação OAuth2 nos requisitos funcionais"

# Corrigir prioridades
/prd-fix "Mudar prioridade da API de integração para P1 (crítica)"

# Atualizar métricas
/prd-fix "Adicionar métrica: tempo de resposta < 200ms para 95% das requisições"
```

### Uso Interativo

```bash
# Sem argumentos - modo interativo
/prd-fix
```

O comando perguntará:
1. Qual seção deseja ajustar?
2. O que deseja modificar especificamente?
3. Por que essa mudança? (contexto para o histórico)

## 🔍 Processo de Execução

### 1. Detectar PRD Existente

**Verificar se PRD.md existe**:
```bash
# Procurar PRD.md na raiz ou em docs/
test -f PRD.md || test -f docs/PRD.md
```

**Se NÃO existir**:
```
❌ PRD.md não encontrado!

Primeiro crie um PRD usando:
   /start-incremental
   ou
   /prd-update

Depois você poderá usar /prd-fix para ajustes.
```
**PARAR aqui**

**Se existir**: Prosseguir

### 2. Modo de Operação

**Se argumentos fornecidos** (modo direto):
- Ler o PRD.md atual
- Identificar seção(ões) afetada(s) pelo ajuste
- Aplicar modificação
- Atualizar seção de "Histórico de Mudanças"
- Salvar PRD.md

**Se SEM argumentos** (modo interativo):
- Mostrar lista de seções do PRD
- Perguntar qual seção ajustar
- Perguntar o que modificar
- Perguntar o motivo (para histórico)
- Aplicar mudanças

### 3. Modo Interativo - Perguntas

**Pergunta 1: Escolher Seção**
```
═══════════════════════════════════════════
📝 AJUSTAR PRD
═══════════════════════════════════════════

Seções disponíveis no PRD:
1. 📋 Visão Geral
2. 🎯 Objetivos
3. ⚙️ Requisitos Funcionais
4. 🔒 Requisitos Não-Funcionais
5. 👥 Personas e Casos de Uso
6. 📊 Métricas de Sucesso
7. 🚫 Fora de Escopo
8. 🗓️ Cronograma e Marcos
9. 🔗 Dependências
10. ⚠️ Riscos e Mitigações
11. ✅ Critérios de Aceitação

Qual seção deseja ajustar? (número ou nome)
```

**Pergunta 2: Tipo de Ajuste**
```
O que deseja fazer nesta seção?

1. Adicionar novo item
2. Modificar item existente
3. Remover item
4. Reorganizar prioridades
5. Atualizar descrição geral
6. Outro (descrever)

Escolha:
```

**Pergunta 3: Detalhes do Ajuste**
```
Descreva a mudança que deseja fazer:
(Seja específico para aplicar o ajuste correto)

Exemplo: "Adicionar OAuth2 como método de autenticação obrigatório"
```

**Pergunta 4: Motivo (Opcional)**
```
Por que esta mudança é necessária?
(Ajuda a manter histórico de decisões)

Exemplo: "Cliente solicitou integração com Google/GitHub"
```

### 4. Aplicar Ajuste

**Ler PRD atual**:
```bash
cat PRD.md  # ou docs/PRD.md
```

**Identificar seção alvo**:
- Parsear markdown para encontrar seção
- Localizar subsecções se necessário
- Identificar lista de itens se aplicável

**Aplicar modificação**:

**Exemplo - Adicionar item em Requisitos Funcionais**:

ANTES:
```markdown
## ⚙️ Requisitos Funcionais

### RF-001: Autenticação
- Sistema de login com email/senha
- Recuperação de senha por email
```

DEPOIS:
```markdown
## ⚙️ Requisitos Funcionais

### RF-001: Autenticação
- Sistema de login com email/senha
- **OAuth2 com Google e GitHub** ← NOVO
- Recuperação de senha por email
```

**Exemplo - Modificar prioridade**:

ANTES:
```markdown
### RF-005: API de Integração (P2 - Importante)
```

DEPOIS:
```markdown
### RF-005: API de Integração (P1 - Crítica) ← MODIFICADO
```

**Exemplo - Adicionar métrica**:

ANTES:
```markdown
## 📊 Métricas de Sucesso

- Taxa de conversão > 10%
- Usuários ativos mensais > 1000
```

DEPOIS:
```markdown
## 📊 Métricas de Sucesso

- Taxa de conversão > 10%
- Usuários ativos mensais > 1000
- **Tempo de resposta < 200ms (p95)** ← NOVO
```

### 5. Atualizar Histórico de Mudanças

**Adicionar entrada no histórico** (no final do PRD):

```markdown
## 📜 Histórico de Mudanças

### 2025-10-25 - Ajuste de Requisitos
**Modificado por**: /prd-fix
**Seção**: Requisitos Funcionais
**Mudança**: Adicionado OAuth2 como método de autenticação
**Motivo**: Cliente solicitou integração com Google/GitHub
**Decisão**: Manter email/senha como fallback, OAuth2 opcional v1

---

[Entradas anteriores...]
```

### 6. Validar e Salvar

**Validar markdown**:
- Sintaxe correta
- Links funcionando
- Formatação consistente

**Salvar arquivo**:
```bash
# Sobrescrever PRD.md com versão atualizada
```

### 7. Confirmar Ajuste

```
✅ PRD ajustado com sucesso!

═══════════════════════════════════════════
📝 AJUSTE APLICADO
═══════════════════════════════════════════

Seção: ⚙️ Requisitos Funcionais
Mudança: Adicionado OAuth2 como método de autenticação
Arquivo: PRD.md (atualizado)

Histórico de mudanças atualizado.

═══════════════════════════════════════════

Próximos passos:
1. Revisar PRD.md para confirmar mudança
2. Comunicar mudança ao time (se aplicável)
3. Atualizar implementação se necessário

Para ver o PRD completo: /prd-view
```

## 🎯 Exemplos de Uso

### Exemplo 1: Adicionar Requisito Funcional

```bash
/prd-fix "Adicionar requisito: Sistema deve suportar modo offline com sincronização automática"

# Resultado:
✅ Adicionado em "Requisitos Funcionais":
   RF-007: Modo Offline (P2 - Importante)
   - Sistema deve funcionar offline
   - Sincronização automática ao reconectar
   - Cache local de dados críticos
```

### Exemplo 2: Atualizar Métrica de Sucesso

```bash
/prd-fix "Aumentar meta de usuários ativos de 1000 para 5000"

# Resultado:
✅ Métrica atualizada:
   Antes: Usuários ativos mensais > 1000
   Depois: Usuários ativos mensais > 5000
   Motivo: Tração do produto superou expectativas
```

### Exemplo 3: Mudar Prioridade

```bash
/prd-fix "Prioridade da API de notificações deve ser P1 (crítica)"

# Resultado:
✅ Prioridade atualizada:
   RF-004: API de Notificações
   Antes: P2 - Importante
   Depois: P1 - Crítica
   Motivo: Feedback de usuários - notificações são essenciais
```

### Exemplo 4: Adicionar Risco

```bash
/prd-fix "Adicionar risco: Dependência de API externa pode causar indisponibilidade"

# Resultado:
✅ Novo risco adicionado:
   R-004: Dependência de API Externa
   Probabilidade: Média
   Impacto: Alto
   Mitigação: Implementar circuit breaker e fallback local
```

### Exemplo 5: Modo Interativo

```bash
/prd-fix

# Fluxo:
> Qual seção? 6 (Métricas de Sucesso)
> O que fazer? 1 (Adicionar novo item)
> Descreva: "NPS > 50 nos primeiros 6 meses"
> Motivo: "Indicador chave de satisfação do cliente"

✅ Métrica adicionada com sucesso!
```

## ⚠️ Regras Importantes

### ✅ SEMPRE Fazer

1. **Registrar no histórico**: Toda mudança vai para "Histórico de Mudanças"
2. **Preservar contexto**: Não remover informações sem motivo
3. **Manter consistência**: Usar mesmo formato do PRD original
4. **Validar impacto**: Avisar se mudança afeta outras seções
5. **Backup automático**: Fazer backup antes de modificar

### ❌ NUNCA Fazer

1. **Reescrever tudo**: Use /prd-update para mudanças grandes
2. **Remover histórico**: Histórico é permanente
3. **Ignorar dependências**: Avisar se mudança afeta outras seções
4. **Modificar sem motivo**: Sempre documentar o porquê
5. **Quebrar formato**: Manter estrutura markdown consistente

## 🔄 Diferença Entre Comandos

| Comando | Quando Usar | Escopo |
|---------|-------------|--------|
| `/start-incremental` | Criar PRD inicial | PRD completo |
| `/prd-update` | Atualizar PRD completo | PRD inteiro |
| `/prd-fix` | Ajuste cirúrgico | Uma seção específica |
| `/prd-view` | Visualizar PRD | Leitura apenas |

## 💡 Dicas

1. **Ajustes pequenos**: Use /prd-fix
2. **Mudanças grandes**: Use /prd-update
3. **Modo interativo**: Útil quando não sabe exatamente qual seção
4. **Histórico**: Sempre revise histórico antes de grandes mudanças
5. **Backup**: PRD.md é versionado no git, use commits frequentes

## 🐛 Troubleshooting

**Problema**: PRD.md não encontrado
```bash
Solução: Execute /start-incremental primeiro
```

**Problema**: Seção não existe
```bash
Solução: Verifique nome correto com /prd-view
```

**Problema**: Formato quebrado após ajuste
```bash
Solução: Reverta com git e use modo interativo
```

---

**Desenvolvido para incremental-dev** - Ajustes precisos sem burocracia! 🎯