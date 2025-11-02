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

### 1. Detectar Tipo de Projeto (Novo vs Legacy)

**IMPORTANTE**: Antes de configurar, detectar se é projeto novo ou existente.

**Detectar projeto LEGACY se**:
- Existem arquivos de código (.py, .js, .ts, etc.)
- Estrutura de diretórios já existe (src/, lib/, app/)
- Arquivo de dependências existe (package.json, pyproject.toml, requirements.txt)
- Git history existe (commits anteriores)

**Se projeto LEGACY detectado**:
```
⚠️  PROJETO EXISTENTE DETECTADO
═══════════════════════════════════════════

Detectei que este projeto já possui código existente.

Para projetos legacy, recomendo usar comandos especializados:

🔄 Opção 1: Adoção Completa de YAGNI
   /adopt-incremental
   └─ Analisa código existente
   └─ Identifica over-engineering
   └─ Cria PRD retroativo
   └─ Gera roadmap de simplificação
   └─ Configura CLAUDE.md

📋 Opção 2: Apenas Criar PRD Retroativo
   /prd-retrofit
   └─ Analisa código existente
   └─ Gera PRD a partir do código
   └─ Útil para documentar projeto sem mudanças

⚙️  Opção 3: Configurar CLAUDE.md e Continuar
   Continuar com /setup-project-incremental
   └─ Configura CLAUDE.md apenas
   └─ Útil se já conhece o projeto

Escolha (1, 2 ou 3):
```

**Se usuário escolher 1**: Redirecionar para `/adopt-incremental`
**Se usuário escolher 2**: Redirecionar para `/prd-retrofit`
**Se usuário escolher 3**: Continuar com o setup normalmente

---

### 2. Detectar ou Criar CLAUDE.md

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

Este projeto usa o plugin `incremental-dev` para desenvolvimento incremental.

### 🤖 Agent Disponível

- **incremental-dev-coach**: Use via Task tool para orientação autônoma em YAGNI, MVP e refatoração
  - Analisa codebase, identifica over-engineering, valida PRD

### 🔍 Skills Auto-Invocadas (Automáticas)

- **yagni-enforcer**: Detecta over-engineering ANTES de implementar
- **refactor-advisor**: Detecta quando padrões emergiram (Regra dos 3)
- **prd-manager**: Gerencia PRD automaticamente, sugere atualizações

**Skills são auto-invocadas - você NÃO precisa chamar manualmente!**

### 📋 Principais Comandos

- `/start-incremental` - Definir MVP inicial
- `/add-increment` - Adicionar próxima funcionalidade
- `/adopt-incremental` - Adotar YAGNI em projeto legacy
- `/prd-view` - Visualizar PRD
- `/prd-update` - Atualizar PRD completo
- `/refactor-now` - Verificar se é hora de refatorar

**📖 Documentação completa**: `plugins/incremental-dev/README.md`

**Nota**: Comandos e skills são auto-descobertos pelo Claude Code na inicialização.

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

5. Formato preferido para Spikes de Validação Técnica:

🔬 FORMATO DE SPIKES DE VALIDAÇÃO

Quando precisar fazer Spikes de Validação Técnica (exploração de tecnologias,
protótipos, provas de conceito), qual formato você prefere?

📓 Opção 1: Notebooks (.ipynb)
   ✅ Exploração interativa e incremental
   ✅ Documentação inline com markdown
   ✅ Visualizações e gráficos integrados
   ✅ Histórico de experimentação preservado
   ✅ Fácil compartilhamento de aprendizados
   ⚠️  Requer Jupyter/VS Code com suporte

📄 Opção 2: Scripts Python (.py)
   ✅ Mais leve e simples
   ✅ Funciona em qualquer editor
   ✅ Mais fácil versionamento
   ⚠️  Menos interativo

💡 Recomendação: Notebooks são melhores para exploração técnica

Sua escolha (1=notebooks, 2=scripts, ou "pular" para decidir depois):
   > [usuário responde: 1, 2, ou "pular"]
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

### 7. Validar Tamanho do CLAUDE.md

**CRÍTICO**: Após criar/atualizar CLAUDE.md, SEMPRE validar tamanho do arquivo.

**Executar validação**:
```bash
wc -c CLAUDE.md
```

**Limite recomendado**: 40,000 caracteres (40KB)

**Se CLAUDE.md > 40k caracteres**:

```
⚠️  CLAUDE.md MUITO GRANDE DETECTADO
═══════════════════════════════════════════

Tamanho atual: [N] caracteres
Limite recomendado: 40,000 caracteres

Arquivos grandes podem impactar performance e contexto.

🔄 APLICAR PROGRESSIVE DISCLOSURE AUTOMATICAMENTE?

Ações propostas:
1. Criar diretório docs/development/
2. Mover conteúdo detalhado para arquivos separados:
   - docs/development/INCREMENTAL_DEV.md
   - docs/development/YAGNI_PRINCIPLES.md
   - docs/development/EXAMPLES.md
3. Manter em CLAUDE.md apenas:
   - Overview (3-5 linhas)
   - Links para documentação detalhada
   - 3-5 regras críticas

Aplicar progressive disclosure? (s/n)
```

**Se usuário responder "s" (SIM)**:

1. Criar estrutura:
```bash
mkdir -p docs/development
```

2. Extrair conteúdo para arquivos separados:

**docs/development/INCREMENTAL_DEV.md**:
- Seção completa "Desenvolvimento Incremental"
- Todos os exemplos, workflows e princípios

**docs/development/YAGNI_PRINCIPLES.md**:
- Regras detalhadas (SEMPRE/NUNCA)
- Exemplos de MVP vs Over-Engineering
- Sinais de alerta

**docs/development/EXAMPLES.md**:
- Exemplos práticos completos
- Casos de uso por linguagem/framework

3. Reduzir CLAUDE.md para versão concisa:

```markdown
# Desenvolvimento Incremental

**IMPORTANTE**: Este projeto segue desenvolvimento incremental com princípios YAGNI e Evolutionary Architecture.

## 📚 Documentação Completa

- **[Guia Completo](./docs/development/INCREMENTAL_DEV.md)** - Workflow, iterações e processo
- **[Princípios YAGNI](./docs/development/YAGNI_PRINCIPLES.md)** - Regras, anti-patterns e sinais de alerta
- **[Exemplos Práticos](./docs/development/EXAMPLES.md)** - Casos de uso e código de exemplo

## ⚡ Regras Críticas (Quick Reference)

### ✅ SEMPRE
- Começar com MVP mínimo (menor escopo que entrega valor)
- Questionar: "Isso é necessário AGORA?"
- Aplicar "Regra dos 3": 1-2 ocorrências OK, 3+ refatorar

### ❌ NUNCA
- Over-engineering (abstrações no MVP)
- Antecipação de requisitos ("preparar para o futuro")
- Complexidade desnecessária (otimização prematura)

## 🎯 Plugin Incremental-Dev

Comandos disponíveis: `/start-incremental`, `/add-increment`, `/refactor-now`, `/review-yagni`, `/adopt-incremental`, `/prd-view`

**Skills auto-invocadas**: yagni-enforcer, refactor-advisor

---

**Filosofia**: Funcionar > Perfeição | Simples > Complexo | Agora > Futuro
```

4. Confirmar resultado:
```
✅ PROGRESSIVE DISCLOSURE APLICADO!

Estrutura criada:
├─ ✅ CLAUDE.md (reduzido: ~2,500 caracteres)
└─ ✅ docs/development/
    ├─ INCREMENTAL_DEV.md (workflow completo)
    ├─ YAGNI_PRINCIPLES.md (regras detalhadas)
    └─ EXAMPLES.md (exemplos práticos)

Tamanho anterior: [N] caracteres
Tamanho atual: ~2,500 caracteres
Redução: [N]%

Claude terá acesso à documentação completa quando necessário
via Read tool, mas contexto inicial otimizado!
```

**Se usuário responder "n" (NÃO)**:
```
⚠️  Mantendo CLAUDE.md atual.

Nota: Arquivo grande pode impactar performance.
Considere aplicar progressive disclosure manualmente quando necessário.
```

**Se CLAUDE.md <= 40k caracteres**:
```
✅ Tamanho do CLAUDE.md validado!

Tamanho: [N] caracteres
Status: ✅ Dentro do limite recomendado (40k)
```

---

### 8. Validar Tamanho do README.md (Se Existir)

**Verificar se README.md existe no projeto**:
```bash
test -f README.md && echo "README.md encontrado"
```

**Se README.md existe, validar tamanho**:
```bash
wc -c README.md
```

**Limite recomendado**: 40,000 caracteres (40KB)

**Se README.md > 40k caracteres**:

```
⚠️  README.md MUITO GRANDE DETECTADO
═══════════════════════════════════════════

Tamanho atual: [N] caracteres
Limite recomendado: 40,000 caracteres

READMEs grandes impactam legibilidade e performance.

🔄 APLICAR PROGRESSIVE DISCLOSURE AUTOMATICAMENTE?

Ações propostas:
1. Criar diretório docs/ (se não existir)
2. Mover conteúdo detalhado para arquivos separados:
   - docs/INSTALLATION.md (instalação detalhada)
   - docs/USAGE.md (guia de uso completo)
   - docs/API.md (referência de API)
   - docs/CONTRIBUTING.md (guia de contribuição)
   - docs/ARCHITECTURE.md (arquitetura do projeto)
3. Manter em README.md apenas:
   - Overview do projeto (2-3 parágrafos)
   - Quick start (instalação básica + exemplo mínimo)
   - Links para documentação detalhada

Aplicar progressive disclosure? (s/n)
```

**Se usuário responder "s" (SIM)**:

1. Criar estrutura:
```bash
mkdir -p docs
```

2. Analisar conteúdo atual do README.md e identificar seções

3. Extrair conteúdo para arquivos separados:

**Identificar seções comuns**:
- Instalação detalhada → docs/INSTALLATION.md
- Guia de uso completo → docs/USAGE.md
- Referência de API → docs/API.md
- Guia de contribuição → docs/CONTRIBUTING.md
- Arquitetura/Design → docs/ARCHITECTURE.md
- Exemplos avançados → docs/EXAMPLES.md
- FAQ → docs/FAQ.md
- Troubleshooting → docs/TROUBLESHOOTING.md

4. Reduzir README.md para versão concisa:

**Template do novo README.md**:
```markdown
# [Nome do Projeto]

[Descrição concisa em 2-3 parágrafos sobre o que o projeto faz e por que existe]

## 📚 Documentação

- **[Installation Guide](./docs/INSTALLATION.md)** - Instalação detalhada e configuração
- **[Usage Guide](./docs/USAGE.md)** - Guia completo de uso
- **[API Reference](./docs/API.md)** - Referência de API
- **[Architecture](./docs/ARCHITECTURE.md)** - Arquitetura e design
- **[Contributing](./docs/CONTRIBUTING.md)** - Como contribuir
- **[Examples](./docs/EXAMPLES.md)** - Exemplos práticos
- **[FAQ](./docs/FAQ.md)** - Perguntas frequentes

## ⚡ Quick Start

### Installation
```bash
[comando de instalação mais básico]
```

### Basic Usage
```[linguagem]
[exemplo mínimo que funciona em 5-10 linhas]
```

## 📖 Next Steps

1. Read the [Usage Guide](./docs/USAGE.md) for detailed examples
2. Check [API Reference](./docs/API.md) for full API documentation
3. See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) to contribute

## 📄 License

[Licença]

---

**Full documentation**: [docs/](./docs/)
```

5. Confirmar resultado:
```
✅ PROGRESSIVE DISCLOSURE APLICADO NO README.md!

Estrutura criada:
├─ ✅ README.md (reduzido: ~1,500 caracteres)
└─ ✅ docs/
    ├─ INSTALLATION.md
    ├─ USAGE.md
    ├─ API.md
    ├─ ARCHITECTURE.md
    ├─ CONTRIBUTING.md
    ├─ EXAMPLES.md
    └─ FAQ.md

Tamanho anterior: [N] caracteres
Tamanho atual: ~1,500 caracteres
Redução: [N]%

README.md agora é conciso e focado em quick start!
Documentação completa disponível em docs/
```

**Se usuário responder "n" (NÃO)**:
```
⚠️  Mantendo README.md atual.

Nota: README grande pode impactar legibilidade.
Considere aplicar progressive disclosure manualmente:
- Mover instalação detalhada para docs/INSTALLATION.md
- Mover API reference para docs/API.md
- Manter apenas overview + quick start no README.md
```

**Se README.md <= 40k caracteres**:
```
✅ Tamanho do README.md validado!

Tamanho: [N] caracteres
Status: ✅ Dentro do limite recomendado (40k)
```

---

### 9. Resumo Final

```
═══════════════════════════════════════════
✅ SETUP COMPLETO!
═══════════════════════════════════════════

Arquivos criados/atualizados:
├─ ✅ CLAUDE.md - Instruções de desenvolvimento incremental
│   └─ Tamanho: [N] caracteres ([STATUS])
├─ ✅ docs/PRD.md v0.1 - Product Requirements Document inicial
└─ [Se aplicável]
    └─ ✅ README.md validado/otimizado
        └─ Tamanho: [N] caracteres ([STATUS])

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

2. PROJETO NOVO - Iniciar desenvolvimento incremental:
   /start-incremental "descrição do objetivo"

   OU

   PROJETO EXISTENTE - Adotar YAGNI:
   /adopt-incremental       (análise completa)
   /prd-retrofit           (só PRD retroativo)

3. Conforme projeto evolui:
   - /prd-update planejamento  (após definir MVP)
   - /prd-update design        (após definir arquitetura)
   - /prd-update incremento    (após cada incremento)

4. Visualizar PRD a qualquer momento:
   /prd-view

5. Revisar over-engineering:
   /review-yagni

6. Verificar momento de refatorar:
   /refactor-now

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

### Projetos Novos
- `/start-incremental` - Definir MVP inicial
- `/add-increment` - Adicionar funcionalidade incremental
- `/refactor-now` - Verificar momento de refatorar
- `/review-yagni` - Remover over-engineering

### Projetos Legacy
- `/adopt-incremental` - Adotar YAGNI em projeto existente
- `/prd-retrofit` - Criar PRD retroativo

### Gestão de PRD
- `/prd-view` - Visualizar PRD
- `/prd-update` - Atualizar PRD
- `/prd-fix` - Ajuste cirúrgico

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