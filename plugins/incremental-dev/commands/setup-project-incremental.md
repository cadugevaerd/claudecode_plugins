---
description: Configura CLAUDE.md do projeto para usar desenvolvimento incremental e orientar Claude a seguir princípios YAGNI, além de criar PRD v0.1 inicial
---

# Setup Project for Incremental Development

Este comando configura o projeto para desenvolvimento incremental:
1. Cria/atualiza `CLAUDE.md` com instruções YAGNI
2. Cria `docs/PRD.md v0.1` (Product Requirements Document inicial)

## 🎯 Objetivo

**CLAUDE.md**: Instruções para Claude seguir desenvolvimento incremental
- Comece sempre com MVP mínimo
- Questione funcionalidades prematuras
- Evite over-engineering
- Adicione complexidade apenas quando necessário
- Refatore quando padrões emergirem (Regra dos 3)

**PRD v0.1**: Documento vivo de requisitos
- Registrar problema que o projeto resolve
- Definir objetivos iniciais
- Estabelecer KPIs para medir sucesso
- Evoluir junto com o projeto

## 📋 Como usar

```bash
/setup-project-incremental
```

Ou com descrição do projeto:

```bash
/setup-project-incremental "API REST com LangGraph para processamento de documentos"
```

## 🔍 Processo de Execução

### 1. Detectar ou Criar CLAUDE.md

**Se CLAUDE.md existe**:
- Ler arquivo atual
- Adicionar seção "Desenvolvimento Incremental" ao final
- Preservar conteúdo existente

**Se CLAUDE.md NÃO existe**:
- Criar arquivo na raiz do projeto
- Adicionar template completo de desenvolvimento incremental

### 2. Adicionar Instruções de Desenvolvimento Incremental

O comando deve adicionar a seguinte seção ao `CLAUDE.md`:

```markdown
# Desenvolvimento Incremental

**IMPORTANTE**: Este projeto segue desenvolvimento incremental com princípios YAGNI e Evolutionary Architecture.

## 📋 Regras Obrigatórias

### ✅ SEMPRE Fazer

1. **Começar com MVP Mínimo**
   - Identificar o menor escopo que entrega valor
   - Implementar apenas o caso de uso mais simples
   - Fazer funcionar ANTES de adicionar complexidade

2. **Questionar Funcionalidades**
   - Perguntar: "Isso é necessário AGORA?"
   - Perguntar: "O que acontece se não implementar?"
   - Perguntar: "Isso resolve o problema mínimo?"

3. **Código Simples Primeiro**
   - Preferir funções diretas a classes abstratas
   - Hardcode OK para MVP (refatorar depois)
   - Duplicação OK se < 3 ocorrências
   - Evitar patterns até padrões emergirem

4. **Testar Cada Incremento**
   - MVP deve funcionar 100%
   - Testar antes de adicionar próxima feature
   - Uma funcionalidade por vez

5. **Refatorar no Momento Certo**
   - Aplicar "Regra dos 3": 1-2 ocorrências OK, 3+ refatorar
   - Refatorar quando padrões emergirem
   - Não refatorar antecipadamente

### ❌ NUNCA Fazer

1. **Over-Engineering**
   - ❌ Classes abstratas no MVP
   - ❌ Factory patterns prematuros
   - ❌ Configuração complexa inicial
   - ❌ "Preparar para o futuro"
   - ❌ "Caso precisemos adicionar..."

2. **Antecipação de Requisitos**
   - ❌ Múltiplas features no MVP
   - ❌ Abstração antes de padrão emergir
   - ❌ Generalização prematura
   - ❌ Sistema de plugins sem uso real

3. **Complexidade Desnecessária**
   - ❌ Validação complexa no MVP
   - ❌ Logging sofisticado inicial
   - ❌ Cache/otimização prematura
   - ❌ Middleware de autenticação antes do MVP funcionar

## 🎯 Workflow de Desenvolvimento

### Iteração 1: MVP
```
Objetivo: Fazer o caso mais simples funcionar

Checklist:
- [ ] Definir ação mínima que entrega valor
- [ ] Implementar sem abstrações
- [ ] Testar funcionamento básico
- [ ] NÃO adicionar "nice to have"
```

### Iterações Seguintes: Incremental
```
Para cada nova funcionalidade:

1. Esperar necessidade REAL surgir
2. Implementar apenas o necessário
3. Testar antes de prosseguir
4. Refatorar se padrão emergir (Regra dos 3)
```

## 📚 Exemplos de MVP vs Over-Engineering

### ✅ MVP Correto

```python
# Iteração 1: Apenas processar
def process_email(email: str) -> str:
    if not email:
        return "erro"
    # Lógica mínima
    return "processado"

# ✅ Simples, direto, funciona
```

### ❌ Over-Engineering (NÃO FAZER)

```python
# ❌ OVER-ENGINEERING - NÃO FAZER NO MVP
from abc import ABC, abstractmethod

class AbstractProcessor(ABC):
    @abstractmethod
    def process(self, data): pass

class EmailProcessorFactory:
    def create_processor(self, type):
        # Complexidade desnecessária para MVP
        pass

# ❌ Abstrações prematuras
```

## 🔄 Quando Refatorar

### Regra dos 3 (Rule of Three)

- **1 ocorrência**: OK, deixe inline
- **2 ocorrências**: OK duplicar (ainda não é padrão)
- **3+ ocorrências**: REFATORAR (padrão confirmado)

**Exemplo**:
```python
# Código aparece em 1 arquivo: OK deixar
def validate_email(email):
    return "@" in email

# Código aparece em 2 arquivos: OK duplicar ainda
def validate_email(email):
    return "@" in email

# Código aparece em 3+ arquivos: REFATORAR AGORA
# Extrair para utils/validators.py
```

## 🚨 Sinais de Alerta

Se você detectar estes padrões, QUESTIONE:

⚠️ **Usar frases como**:
- "Vamos preparar para o futuro..."
- "Caso precisemos adicionar..."
- "Para facilitar expansão..."
- "Seguindo clean architecture..."

⚠️ **Criar múltiplas camadas no MVP**:
- Controllers, Services, Repositories no MVP
- Abstrações sem uso real

⚠️ **Configuração complexa inicial**:
- YAML/JSON config no MVP
- ConfigManager com validação

## 💡 Princípios Guia

1. **YAGNI**: "You Aren't Gonna Need It" - Não adicione até precisar
2. **KISS**: "Keep It Simple, Stupid" - Simples > Complexo
3. **Funcionar > Perfeição**: MVP funcional > Código perfeito
4. **Refatorar quando necessário**: Não antecipadamente

## 🎯 Plugin Incremental-Dev

Este projeto usa o plugin `incremental-dev` com os seguintes comandos:

- `/start-incremental` - Definir MVP inicial
- `/add-increment` - Adicionar próxima funcionalidade
- `/refactor-now` - Verificar se é hora de refatorar
- `/review-yagni` - Revisar código removendo over-engineering

## 🔍 Skills Auto-Invocadas

O plugin possui skills que Claude invoca automaticamente:

- **yagni-enforcer**: Detecta over-engineering ANTES de implementar
- **refactor-advisor**: Detecta quando padrões emergiram (Regra dos 3)

Confie nessas skills para orientar decisões de arquitetura.

---

**Filosofia**: Funcionar > Perfeição | Simples > Complexo | Agora > Futuro
```

### 3. Adicionar Contexto do Projeto (Se Fornecido)

Se o usuário fornecer descrição do projeto, adicionar seção customizada:

```markdown
## 📊 Contexto Deste Projeto

**Descrição**: [descrição fornecida pelo usuário]

**MVP Sugerido**:
- Funcionalidade mínima 1
- Funcionalidade mínima 2
- Funcionalidade mínima 3

**NÃO fazer no MVP**:
- Feature complexa 1
- Feature complexa 2
- Otimização prematura
```

### 4. Confirmar com Usuário

Mostrar preview do que será adicionado:

```
═══════════════════════════════════════════
📝 SETUP INCREMENTAL DEVELOPMENT
═══════════════════════════════════════════

Arquivo: CLAUDE.md

Ação: [CRIAR NOVO / ADICIONAR SEÇÃO]

Conteúdo a ser adicionado:
---
[Preview das instruções]
---

Adicionar ao CLAUDE.md? (s/n)
```

### 5. Criar/Atualizar CLAUDE.md

Se usuário confirmar:
- Criar ou atualizar CLAUDE.md
- Adicionar instruções completas
- Validar que arquivo foi criado corretamente

```
✅ CLAUDE.md configurado com sucesso!

Instruções de desenvolvimento incremental adicionadas.
```

---

### 6. Criar PRD v0.1 (Product Requirements Document)

Após configurar CLAUDE.md, criar documento PRD inicial:

```
📄 CRIANDO PRD INICIAL...

Localização: docs/PRD.md
Versão: 0.1 (Descoberta)
```

**Perguntar ao usuário**:
```
📋 INFORMAÇÕES INICIAIS DO PRD

Para criar o PRD v0.1, preciso de algumas informações:

1. Nome do projeto:
   > [usuário responde]

2. Qual problema este projeto resolve?
   > [usuário responde]

3. Quais os objetivos principais? (separe por vírgula)
   > [usuário responde]

4. Como medirá sucesso? (KPIs - opcional)
   > [usuário responde ou pula]
```

**Criar diretório docs/**:
```bash
mkdir -p docs
```

**Popular PRD v0.1**:
Usar template de `${CLAUDE_PLUGIN_ROOT}/templates/PRD.md` e preencher:
- Nome do projeto
- Problema identificado
- Objetivos (checklist)
- KPIs (se fornecidos)
- Data atual em "Última Atualização"

```
✅ PRD v0.1 CRIADO!

Arquivo: docs/PRD.md
Versão: 0.1 (Descoberta)

Seções preenchidas:
├─ ✅ Problema
├─ ✅ Objetivos ([N] objetivos)
└─ ✅ KPIs

Próximas fases do PRD:
- v1.0: /prd-update planejamento
- v1.1: /prd-update design
- v1.x: /prd-update incremento (após cada incremento)
```

---

### 7. Resumo Final

```
═══════════════════════════════════════════
✅ SETUP COMPLETO!
═══════════════════════════════════════════

Arquivos criados/atualizados:
├─ ✅ CLAUDE.md - Instruções de desenvolvimento incremental
└─ ✅ docs/PRD.md v0.1 - Product Requirements Document inicial

Claude agora está orientado a:
✓ Começar com MVP
✓ Questionar over-engineering
✓ Refatorar no momento certo
✓ Evitar YAGNI violations

PRD criado e pronto para evoluir com o projeto!

═══════════════════════════════════════════
PRÓXIMOS PASSOS
═══════════════════════════════════════════

1. Revisar arquivos criados:
   - cat CLAUDE.md
   - cat docs/PRD.md

2. Iniciar desenvolvimento incremental:
   /start-incremental "descrição do objetivo"

3. Conforme projeto evolui:
   - /prd-update planejamento  (após definir MVP)
   - /prd-update design        (após definir arquitetura)
   - /prd-update incremento    (após cada incremento)

4. Visualizar PRD a qualquer momento:
   /prd-view

═══════════════════════════════════════════

Projeto configurado para desenvolvimento incremental! 🚀
```

## 📚 Exemplos de Uso

### Exemplo 1: Novo Projeto

```bash
/setup-project-incremental "API REST com LangGraph para processamento de documentos"
```

**Resultado**:
- Cria `CLAUDE.md` na raiz do projeto
- Adiciona instruções completas de desenvolvimento incremental
- Inclui contexto específico sobre API + LangGraph
- Sugere MVP inicial

### Exemplo 2: Projeto Existente

```bash
/setup-project-incremental
```

**Resultado**:
- Detecta `CLAUDE.md` existente
- Adiciona seção "Desenvolvimento Incremental" ao final
- Preserva conteúdo existente
- Não sobrescreve instruções anteriores

### Exemplo 3: Projeto com CLAUDE.md Complexo

```bash
/setup-project-incremental "Sistema de pagamentos com múltiplos gateways"
```

**Resultado**:
- Lê CLAUDE.md existente
- Identifica que já tem muitas instruções
- Adiciona seção focada e concisa
- Customiza MVP sugerido para pagamentos

## 🎯 Template do CLAUDE.md Completo

Se o arquivo não existir, criar com este template completo:

```markdown
# CLAUDE.md

Este arquivo contém instruções para Claude Code sobre como trabalhar neste projeto.

## Desenvolvimento Incremental

[Instruções completas conforme descrito acima]

## Convenções do Projeto

- Linguagem: [detectar automaticamente]
- Framework: [detectar automaticamente]
- Gerenciador de pacotes: [detectar automaticamente]
- Estrutura de diretórios: [analisar automaticamente]

## Comandos Úteis

- `/start-incremental` - Definir MVP inicial
- `/add-increment` - Adicionar funcionalidade incremental
- `/refactor-now` - Verificar momento de refatorar
- `/review-yagni` - Remover over-engineering

---

**Desenvolvido com princípios YAGNI e Evolutionary Architecture**
```

## ⚠️ Importante

### Não Sobrescrever Conteúdo Existente

Se `CLAUDE.md` já existe:
- NUNCA sobrescrever conteúdo
- SEMPRE adicionar ao final
- Usar separador claro: `---`

### Detectar Linguagem e Framework

Analisar projeto para customizar instruções:
- Python + LangGraph → Exemplos específicos LangGraph
- JavaScript + React → Exemplos React
- API REST → Exemplos FastAPI/Express

### Validar Sintaxe Markdown

Após criar/atualizar:
- Verificar que markdown está válido
- Headers bem formatados
- Code blocks fechados corretamente

## 🚀 Após Executar Este Comando

O usuário terá:

1. ✅ `CLAUDE.md` configurado com instruções incrementais
2. ✅ Claude orientado a seguir YAGNI
3. ✅ Workflow claro de MVP → Incrementos → Refatoração
4. ✅ Skills auto-invocadas para prevenir over-engineering
5. ✅ Comandos disponíveis documentados

**Próximo passo**: Executar `/start-incremental` para definir MVP do projeto!

## 💡 Dica

Após configurar o projeto, sempre comece com:

```bash
/start-incremental "descrição do objetivo"
```

Isso garantirá que Claude começa com MVP e evita over-engineering desde o início.