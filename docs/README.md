# Guia Completo: Repositório de Plugins Claude Code

## 📋 Índice

1. [Introdução](#introdução)
2. [O que são Plugins do Claude Code?](#o-que-são-plugins-do-claude-code)
3. [Estrutura do Repositório](./01-estrutura-do-repositorio.md)
4. [Configuração do Marketplace](./02-configuracao-marketplace.md)
5. [Criando um Plugin](./03-criando-plugin.md)
6. [Componentes do Plugin](./04-componentes-plugin.md)
7. [Publicação e Distribuição](./05-publicacao-e-distribuicao.md)

---

## Introdução

Este guia documenta o processo completo para criar e manter um **repositório de plugins para o Claude Code**. Você aprenderá desde a estrutura básica até a publicação e distribuição de plugins personalizados.

## O que são Plugins do Claude Code?

Plugins do Claude Code são **coleções personalizadas** que podem incluir:

- ✅ **Slash Commands** (Comandos personalizados)
- ✅ **Agents** (Agentes especializados)
- ✅ **MCP Servers** (Servidores de Model Context Protocol)
- ✅ **Hooks** (Ganchos de ciclo de vida)

### Benefícios dos Plugins

- 🚀 **Instalação com um único comando**: `/plugin install nome-do-plugin`
- 📦 **Reutilização**: Compartilhe funcionalidades entre projetos e equipes
- 🔧 **Personalização**: Adapte o Claude Code às suas necessidades específicas
- 🤝 **Colaboração**: Distribua plugins para toda a equipe ou comunidade

### Como Funciona um Marketplace?

Um **marketplace** é simplesmente um repositório Git (GitHub, GitLab, etc.) ou URL que contém:

```
.claude-plugin/
└── marketplace.json  # Arquivo que lista todos os plugins disponíveis
```

Para hospedar um marketplace, você só precisa de:
- Um repositório Git/GitHub
- Um arquivo `.claude-plugin/marketplace.json` formatado corretamente

## Passo a Passo Rápido

### 1. Criar a Estrutura do Repositório

```bash
mkdir meu-marketplace-plugins
cd meu-marketplace-plugins

# Criar estrutura básica
mkdir -p .claude-plugin
mkdir -p plugins/meu-primeiro-plugin/.claude-plugin
```

### 2. Configurar o Marketplace

Criar `.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "meu-marketplace",
  "version": "1.0.0",
  "description": "Meu marketplace de plugins personalizados",
  "owner": {
    "name": "Seu Nome",
    "email": "seu@email.com"
  },
  "plugins": [
    {
      "name": "meu-primeiro-plugin",
      "description": "Um plugin de exemplo",
      "source": "./plugins/meu-primeiro-plugin"
    }
  ]
}
```

### 3. Criar um Plugin

Criar `plugins/meu-primeiro-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "meu-primeiro-plugin",
  "version": "1.0.0",
  "description": "Plugin de exemplo para Claude Code",
  "author": {
    "name": "Seu Nome"
  }
}
```

### 4. Adicionar Componentes

Criar um comando simples em `plugins/meu-primeiro-plugin/commands/hello.md`:

```markdown
---
description: Um comando de exemplo que cumprimenta o usuário
---

Olá! Este é um comando personalizado do Claude Code.
```

### 5. Publicar no GitHub

```bash
git init
git add .
git commit -m "Initial commit: Meu marketplace de plugins"
git remote add origin https://github.com/seu-usuario/meu-marketplace.git
git push -u origin main
```

### 6. Instalar e Usar

No Claude Code:

```bash
# Adicionar o marketplace
/plugin marketplace add seu-usuario/meu-marketplace

# Instalar um plugin
/plugin install meu-primeiro-plugin

# Usar o comando
/hello
```

## Estrutura de Arquivos Completa

```
meu-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Configuração do marketplace
├── plugins/
│   ├── plugin-1/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Manifesto do plugin
│   │   ├── .mcp.json             # Configuração MCP (opcional)
│   │   ├── commands/             # Comandos personalizados
│   │   │   └── comando.md
│   │   ├── agents/               # Agentes especializados
│   │   │   └── agente.md
│   │   ├── hooks/                # Hooks de ciclo de vida
│   │   │   └── hooks.json
│   │   └── skills/               # Skills para agentes
│   │       └── skill-name/
│   │           └── SKILL.md
│   └── plugin-2/
│       └── ...
├── README.md
└── LICENSE
```

## Componentes Principais

### 1. Commands (Comandos)
Arquivos Markdown que aparecem como comandos `/` no Claude Code.

### 2. Agents (Agentes)
Agentes especializados para tarefas específicas (testes, API, banco de dados, etc.).

### 3. Hooks (Ganchos)
Executam ações em momentos específicos do ciclo de vida do Claude Code.

### 4. MCP Servers
Conectam ferramentas e serviços externos ao Claude Code.

## Recursos Adicionais

- 📚 [Estrutura do Repositório](./01-estrutura-do-repositorio.md)
- ⚙️ [Configuração do Marketplace](./02-configuracao-marketplace.md)
- 🔨 [Criando um Plugin](./03-criando-plugin.md)
- 🧩 [Componentes do Plugin](./04-componentes-plugin.md)
- 🚀 [Publicação e Distribuição](./05-publicacao-e-distribuicao.md)

## Documentação Oficial

- [Claude Code Plugins - Documentação Oficial](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MCP - Model Context Protocol](https://docs.claude.com/en/docs/claude-code/mcp)

## Licença

Este guia é fornecido como está, para fins educacionais.

---

**Próximo passo**: [01 - Estrutura do Repositório →](./01-estrutura-do-repositorio.md)
