---
description: Setup kubernetes-specialist plugin by updating README with agents, commands, and MCP info, plus creating .env.example
allowed-tools: [Read, Write, Edit, Glob, Bash]
model: claude-sonnet-4-5
argument-hint: ''
---

# Setup Kubernetes Specialist Plugin

Configura o plugin kubernetes-specialist atualizando README.md com informações completas sobre agentes, comandos e MCP kubernetes-toolkit, e criando/atualizando .env.example com variáveis de ambiente necessárias.

## 🎯 Objetivo

- Documentar todos os agentes disponíveis no plugin com descrições e casos de uso
- Documentar todos os comandos slash disponíveis com sintaxe e exemplos
- Adicionar informações sobre integração com MCP kubernetes-toolkit
- Criar ou atualizar `.env.example` com todas as variáveis de ambiente necessárias para o MCP
- Garantir que README.md esteja completo e navegável para novos usuários

## 🔧 Instruções

### 1. **Descobrir Estrutura do Plugin**

1.1 **Localizar diretórios do plugin**

- Usar `Glob` para encontrar plugin kubernetes-specialist:
  - `plugins/kubernetes-specialist/`
- Identificar diretórios existentes: `agents/`, `commands/`, `skills/`, `.mcp.json`

1.2 **Catalogar agentes disponíveis**

- Usar `Glob` para listar: `plugins/kubernetes-specialist/agents/*.md`
- Para cada agente encontrado:
  - Usar `Read` para ler o arquivo
  - Extrair YAML frontmatter (name, description, subagent_type)
  - Extrair seção Responsibilities
  - Documentar casos de uso da seção Examples

1.3 **Catalogar comandos slash disponíveis**

- Usar `Glob` para listar: `plugins/kubernetes-specialist/commands/*.md`
- Para cada comando encontrado:
  - Usar `Read` para ler o arquivo
  - Extrair YAML frontmatter (description, argument-hint)
  - Extrair seção Objetivo
  - Documentar sintaxe de uso da seção Exemplo

1.4 **Verificar integração MCP**

- Usar `Read` para verificar se existe `.mcp.json` no plugin
- Se existe: Extrair configuração de mcpServers
- Identificar nome do servidor MCP (ex: kubernetes-toolkit)
- Listar variáveis de ambiente necessárias (env section)

### 2. **Atualizar README.md do Plugin**

2.1 **Ler README.md existente**

- Usar `Read` para ler: `plugins/kubernetes-specialist/README.md`
- Identificar seções existentes (se houver)
- Determinar se precisa criar novas seções ou atualizar existentes

2.2 **Criar/Atualizar seção de Agentes**

- Adicionar ou atualizar seção `## 🤖 Agentes Disponíveis`
- Para cada agente catalogado:
  - Nome do agente
  - Descrição (do frontmatter)
  - Quando usar (casos de uso)
  - Como invocar (exemplo com Task tool)
- Formato sugerido:

```markdown
## 🤖 Agentes Disponíveis

### agent-name

**Descrição**: [Descrição do frontmatter]

**Quando usar**:
- [Caso de uso 1]
- [Caso de uso 2]

**Como invocar**:
\`\`\`python
Task(subagent_type="agent-name", prompt="[exemplo de prompt]")
\`\`\`
```

2.3 **Criar/Atualizar seção de Comandos**

- Adicionar ou atualizar seção `## ⚡ Comandos Disponíveis`
- Para cada comando catalogado:
  - Nome do comando (com `/`)
  - Descrição
  - Sintaxe (com argument-hint se houver)
  - Exemplo prático
- Formato sugerido:

```markdown
## ⚡ Comandos Disponíveis

### /command-name [ARGS]

**Descrição**: [Descrição do frontmatter]

**Sintaxe**:
\`\`\`bash
/command-name [ARGS]
\`\`\`

**Exemplo**:
\`\`\`bash
/command-name example-input
\`\`\`
```

2.4 **Criar/Atualizar seção de MCP Integration**

- Adicionar ou atualizar seção `## 🔌 MCP Integration`
- Documentar servidor MCP kubernetes-toolkit:
  - Nome do servidor
  - O que fornece (tools disponíveis)
  - Como configurar
  - Variáveis de ambiente necessárias
  - Exemplo de uso
- Formato sugerido:

```markdown
## 🔌 MCP Integration

Este plugin integra com o MCP server **kubernetes-toolkit** para acesso direto à API do Kubernetes.

**Benefícios**:
- Acesso direto à API (mais rápido que kubectl)
- Autenticação automática
- 40+ ferramentas diagnósticas
- Output estruturado

**Configuração**:
1. Instalar o plugin
2. Configurar variáveis de ambiente (ver `.env.example`)
3. Reiniciar Claude Code
4. Verificar status com `/mcp`

**Variáveis de ambiente necessárias**:
- `KUBECONFIG`: Caminho para arquivo kubeconfig
- `KUBERNETES_CONTEXT`: (Opcional) Contexto específico

**Verificar status**:
\`\`\`bash
/mcp
\`\`\`
```

2.5 **Executar atualização do README**

- Se seções existem: Usar `Edit` para atualizar conteúdo
- Se seções não existem: Usar `Edit` para adicionar ao final do README
- Preservar formatação e estrutura existente
- Garantir markdown válido

### 3. **Criar/Atualizar .env.example**

3.1 **Verificar se .env.example existe**

- Usar `Glob` para buscar: `plugins/kubernetes-specialist/.env.example`
- Se não existe: Preparar para criar novo arquivo
- Se existe: Usar `Read` para ler conteúdo atual

3.2 **Identificar variáveis de ambiente necessárias**

Da configuração MCP `.mcp.json`:

- Todas as variáveis em seção `env` de cada mcpServer
- Variáveis com expansão `${VAR}` ou `${VAR:-default}`

Variáveis típicas para kubernetes-toolkit:

- `KUBECONFIG` - Caminho para arquivo kubeconfig
- `KUBERNETES_CONTEXT` - (Opcional) Contexto Kubernetes específico
- `KUBERNETES_NAMESPACE` - (Opcional) Namespace padrão

3.3 **Gerar conteúdo de .env.example**

Formato padrão:

```bash
# Kubernetes MCP Configuration
# Copy this file to .env and fill with your values

# REQUIRED: Path to kubeconfig file
# Example: ~/.kube/config or /path/to/custom/kubeconfig
KUBECONFIG=~/.kube/config

# OPTIONAL: Specific Kubernetes context to use
# Leave empty to use current context from kubeconfig
# KUBERNETES_CONTEXT=my-cluster-context

# OPTIONAL: Default namespace for operations
# Leave empty to use 'default' namespace
# KUBERNETES_NAMESPACE=default
```

3.4 **Criar ou atualizar .env.example**

- Se arquivo não existe: Usar `Write` para criar
- Se arquivo existe:
  - Verificar se variáveis já estão documentadas
  - Usar `Edit` para adicionar variáveis ausentes
  - Preservar comentários e variáveis existentes
  - Não duplicar variáveis

### 4. **Validar Resultado**

4.1 **Verificar README.md**

- Usar `Read` para reler README.md atualizado
- Confirmar presença de seções:
  - Agentes Disponíveis
  - Comandos Disponíveis
  - MCP Integration
- Validar formatação markdown (sem erros de sintaxe)

4.2 **Verificar .env.example**

- Usar `Read` para reler .env.example
- Confirmar todas as variáveis necessárias estão presentes
- Validar formato (KEY=value, comentários com #)

4.3 **Reportar resultado**

- Listar arquivos modificados ou criados
- Resumir mudanças aplicadas
- Indicar próximos passos para usuário

## 📊 Formato de Saída

### Saída Padrão

```text
✅ Setup do plugin kubernetes-specialist concluído!

📝 Arquivos atualizados:

1. README.md
   ✅ Seção "Agentes Disponíveis" - [X agentes documentados]
   ✅ Seção "Comandos Disponíveis" - [Y comandos documentados]
   ✅ Seção "MCP Integration" - kubernetes-toolkit configurado

2. .env.example
   ✅ Criado/Atualizado com [Z variáveis de ambiente]
   ✅ Documentação e exemplos inclusos

📋 Agentes documentados:
   - [agent-1]: [Breve descrição]
   - [agent-2]: [Breve descrição]

⚡ Comandos documentados:
   - /command-1: [Breve descrição]
   - /command-2: [Breve descrição]

🔌 MCP Integration:
   - Servidor: kubernetes-toolkit
   - Tools: 40+ ferramentas diagnósticas
   - Status: Configurado

📖 Próximos passos:
   1. Revisar README.md em: plugins/kubernetes-specialist/README.md
   2. Copiar .env.example para .env e preencher valores
   3. Reiniciar Claude Code para ativar MCP
   4. Verificar com: /mcp
```

## ✅ Critérios de Sucesso

- [ ] Todos os agentes do plugin catalogados
- [ ] Todos os comandos slash catalogados
- [ ] Configuração MCP identificada e documentada
- [ ] README.md atualizado com seções obrigatórias:
  - [ ] Agentes Disponíveis (com exemplos de invocação)
  - [ ] Comandos Disponíveis (com sintaxe e exemplos)
  - [ ] MCP Integration (com configuração e variáveis)
- [ ] `.env.example` criado ou atualizado com:
  - [ ] Todas as variáveis necessárias para MCP
  - [ ] Comentários explicativos para cada variável
  - [ ] Exemplos de valores
- [ ] Markdown válido (sem erros de sintaxe)
- [ ] Formatação consistente e navegável
- [ ] Próximos passos documentados para usuário

## ❌ Anti-Patterns

### ❌ Erro 1: Documentação Incompleta

Não documente apenas alguns agentes ou comandos:

```markdown
❌ Errado:
## Agentes
- k8s-troubleshooter: Troubleshoots pods
[Faltam outros agentes existentes]

✅ Correto:
## 🤖 Agentes Disponíveis

### k8s-troubleshooter
[Documentação completa com casos de uso e exemplos]

### k8s-deployer
[Documentação completa com casos de uso e exemplos]

[Todos os agentes documentados]
```

### ❌ Erro 2: .env.example Sem Comentários

Não crie .env.example sem explicações:

```bash
❌ Errado:
KUBECONFIG=~/.kube/config
KUBERNETES_CONTEXT=

✅ Correto:
# REQUIRED: Path to kubeconfig file
# Example: ~/.kube/config or /path/to/custom/kubeconfig
KUBECONFIG=~/.kube/config

# OPTIONAL: Specific Kubernetes context to use
# Leave empty to use current context from kubeconfig
# KUBERNETES_CONTEXT=my-cluster-context
```

### ❌ Erro 3: Sobrescrever README Existente

Não substitua todo o README se ele já tem conteúdo:

```markdown
❌ Errado:
[Ler README → Ignorar conteúdo → Criar do zero]

✅ Correto:
[Ler README → Identificar seções → Edit/adicionar apenas o necessário]
```

### ❌ Erro 4: Variáveis de Ambiente Hardcoded

Não coloque valores reais em .env.example:

```bash
❌ Errado:
KUBECONFIG=/home/myuser/.kube/config
KUBERNETES_CONTEXT=production-cluster-real

✅ Correto:
KUBECONFIG=~/.kube/config
# KUBERNETES_CONTEXT=my-cluster-context
```

### ❌ Erro 5: MCP Integration Genérica

Não documente MCP de forma vaga:

```markdown
❌ Errado:
## MCP
Este plugin usa MCP.

✅ Correto:
## 🔌 MCP Integration

Este plugin integra com o MCP server **kubernetes-toolkit** para acesso direto à API do Kubernetes.

**Benefícios**:
- Acesso direto à API (mais rápido que kubectl)
- Autenticação automática
- 40+ ferramentas diagnósticas

**Configuração**:
[Passos detalhados com comandos]

**Variáveis necessárias**:
[Lista completa com exemplos]
```

## 📝 Exemplo

### Uso Básico

```bash
/setup-kubernetes-specialist
```

**O que acontece**:

1. 🔍 Descobre estrutura do plugin

   - Encontra 3 agentes em `agents/`
   - Encontra 2 comandos em `commands/`
   - Encontra `.mcp.json` com kubernetes-toolkit

1. 📝 Atualiza README.md

   - Adiciona seção "Agentes Disponíveis" com 3 agentes
   - Adiciona seção "Comandos Disponíveis" com 2 comandos
   - Adiciona seção "MCP Integration" com kubernetes-toolkit

1. ⚙️ Cria .env.example

   - Adiciona KUBECONFIG (required)
   - Adiciona KUBERNETES_CONTEXT (optional)
   - Adiciona KUBERNETES_NAMESPACE (optional)
   - Inclui comentários e exemplos

1. ✅ Valida resultado

   - README.md completo e formatado
   - .env.example válido e documentado
   - Reporta resumo das mudanças

**Resultado esperado**:

- README.md atualizado com documentação completa
- .env.example criado e pronto para copiar
- Usuário tem todas as informações para usar o plugin
