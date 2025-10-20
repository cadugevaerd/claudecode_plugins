# 03 - Criando um Plugin

## 📋 Visão Geral

Este documento apresenta um guia passo a passo completo para criar seu primeiro plugin do Claude Code, desde a estrutura inicial até testes e validação.

---

## 🎯 Passo a Passo Completo

### Passo 1: Criar a Estrutura Básica

#### 1.1. Criar o Diretório do Plugin

```bash
# Navegue até o diretório de plugins do seu marketplace
cd plugins/

# Crie o diretório do novo plugin
mkdir meu-primeiro-plugin
cd meu-primeiro-plugin

# Crie a estrutura básica
mkdir -p .claude-plugin
mkdir -p commands
mkdir -p agents
mkdir -p hooks
mkdir -p skills
```

**Resultado**:
```
meu-primeiro-plugin/
├── .claude-plugin/
├── commands/
├── agents/
├── hooks/
└── skills/
```

#### 1.2. Criar o Manifesto do Plugin (plugin.json)

Crie o arquivo `.claude-plugin/plugin.json`:

```bash
touch .claude-plugin/plugin.json
```

**Conteúdo**:
```json
{
  "name": "meu-primeiro-plugin",
  "version": "1.0.0",
  "description": "Meu primeiro plugin para Claude Code",
  "author": {
    "name": "Seu Nome",
    "email": "seu@email.com"
  },
  "keywords": ["exemplo", "aprendizado"],
  "license": "MIT"
}
```

---

### Passo 2: Criar Seu Primeiro Comando

#### 2.1. Criar um Comando Simples

Crie o arquivo `commands/hello.md`:

```markdown
---
description: Um comando de exemplo que cumprimenta o usuário
---

Olá! 👋

Este é um comando personalizado do Claude Code.

Você executou o comando `/hello` com sucesso!

## O que você pode fazer agora:

1. Criar mais comandos em `commands/`
2. Adicionar agentes em `agents/`
3. Configurar hooks em `hooks/`
4. Integrar MCP servers

Divirta-se criando plugins incríveis!
```

#### 2.2. Criar um Comando com Parâmetros

Crie o arquivo `commands/greet.md`:

```markdown
---
description: Cumprimenta uma pessoa específica
---

Olá {{name}}! 👋

É um prazer te conhecer!

Hoje é {{date}} e estou aqui para ajudar com suas tarefas de desenvolvimento.

## Como usar:

```
/greet name="João"
```

Você também pode usar variáveis de ambiente:
```
/greet name="${USER}"
```
```

#### 2.3. Criar um Comando Mais Complexo

Crie o arquivo `commands/build.md`:

```markdown
---
description: Executa o build do projeto e mostra o resultado
---

# Build do Projeto

Vou executar o build do seu projeto agora.

## Passos:

1. Verificar dependências
2. Compilar código
3. Executar testes
4. Gerar bundle

Aguarde enquanto processo...

---

**Nota**: Este é um exemplo. Em produção, você configuraria hooks ou agentes para executar tarefas reais.
```

---

### Passo 3: Registrar o Plugin no Marketplace

#### 3.1. Editar o marketplace.json

Edite `.claude-plugin/marketplace.json` na raiz do repositório:

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "meu-marketplace",
  "version": "1.0.0",
  "description": "Meu marketplace de plugins",
  "owner": {
    "name": "Seu Nome",
    "email": "seu@email.com"
  },
  "plugins": [
    {
      "name": "meu-primeiro-plugin",
      "description": "Meu primeiro plugin para Claude Code",
      "source": "./plugins/meu-primeiro-plugin",
      "category": "development",
      "tags": ["exemplo", "tutorial", "aprendizado"]
    }
  ]
}
```

---

### Passo 4: Testar Localmente

#### 4.1. Criar um Marketplace de Teste

Você pode testar seu plugin localmente antes de publicá-lo:

```bash
# Na raiz do seu repositório
cd /caminho/para/seu-marketplace

# Inicialize um repositório Git (se ainda não tiver)
git init

# Adicione os arquivos
git add .
git commit -m "Meu primeiro plugin"
```

#### 4.2. Adicionar o Marketplace Local no Claude Code

No Claude Code:

```bash
# Adicione o marketplace local
/plugin marketplace add file:///caminho/absoluto/para/seu-marketplace

# Ou se já está em um repositório Git remoto
/plugin marketplace add seu-usuario/seu-marketplace
```

#### 4.3. Instalar o Plugin

```bash
# Liste os marketplaces
/plugin marketplace list

# Liste os plugins disponíveis
/plugin list

# Instale seu plugin
/plugin install meu-primeiro-plugin
```

#### 4.4. Testar os Comandos

```bash
# Teste o comando hello
/hello

# Teste o comando greet
/greet name="João"

# Teste o comando build
/build
```

---

### Passo 5: Adicionar Documentação

#### 5.1. Criar README.md do Plugin

Crie `README.md` na raiz do plugin:

```markdown
# Meu Primeiro Plugin

Plugin de exemplo para Claude Code.

## Instalação

```bash
/plugin marketplace add seu-usuario/seu-marketplace
/plugin install meu-primeiro-plugin
```

## Comandos Disponíveis

### /hello

Exibe uma mensagem de boas-vindas.

**Uso**:
```bash
/hello
```

### /greet

Cumprimenta uma pessoa específica.

**Uso**:
```bash
/greet name="João"
```

**Parâmetros**:
- `name` - Nome da pessoa a cumprimentar

### /build

Simula o processo de build do projeto.

**Uso**:
```bash
/build
```

## Autor

Seu Nome - seu@email.com

## Licença

MIT
```

---

## 🎨 Templates de Plugins

### Template: Plugin de Comandos Git

```bash
# Estrutura
plugins/git-helper/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── commit.md
│   ├── push.md
│   └── status.md
└── README.md
```

**plugin.json**:
```json
{
  "name": "git-helper",
  "version": "1.0.0",
  "description": "Comandos úteis para Git",
  "keywords": ["git", "vcs"]
}
```

**commands/commit.md**:
```markdown
---
description: Cria um commit com mensagem formatada
---

Vou criar um commit para você.

Por favor, me informe:
1. O tipo de mudança (feat, fix, docs, etc.)
2. Uma descrição breve
3. Uma descrição detalhada (opcional)

Formato sugerido:
```
tipo(escopo): descrição breve

descrição detalhada (opcional)
```

Exemplo:
```
feat(auth): adiciona autenticação JWT

Implementa sistema completo de autenticação usando JWT,
incluindo login, registro e validação de tokens.
```
```

### Template: Plugin de Testes

```bash
# Estrutura
plugins/test-runner/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── test.md
├── agents/
│   └── test-executor.md
└── README.md
```

**plugin.json**:
```json
{
  "name": "test-runner",
  "version": "1.0.0",
  "description": "Executa e gerencia testes",
  "keywords": ["testing", "quality"]
}
```

**commands/test.md**:
```markdown
---
description: Executa os testes do projeto
---

# Executando Testes

Vou executar os testes do projeto agora.

## Opções:

- `--watch` - Modo watch
- `--coverage` - Com cobertura
- `--unit` - Apenas testes unitários
- `--integration` - Apenas testes de integração

**Nota**: Use o agente test-executor para execução automatizada.
```

**agents/test-executor.md**:
```markdown
---
description: Agente especializado em executar testes
---

# Test Executor Agent

Sou um agente especializado em executar e analisar testes.

## Minhas responsabilidades:

1. Detectar o framework de testes (Jest, Mocha, PyTest, etc.)
2. Executar os testes apropriados
3. Analisar os resultados
4. Sugerir correções para testes falhando

## Como me usar:

Simplesmente peça para executar os testes e eu cuidarei de tudo!
```

### Template: Plugin com MCP Server

```bash
# Estrutura
plugins/database-tools/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── commands/
│   └── query.md
└── servers/
    └── db-mcp/
        └── index.js
```

**plugin.json**:
```json
{
  "name": "database-tools",
  "version": "1.0.0",
  "description": "Ferramentas para banco de dados"
}
```

**.mcp.json**:
```json
{
  "database": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/db-mcp/index.js"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

---

## 🚀 Exemplos Práticos Completos

### Exemplo 1: Plugin de Produtividade

**Objetivo**: Criar comandos para tarefas comuns do dia a dia

**Estrutura**:
```bash
plugins/productivity/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── daily-standup.md
│   ├── create-task.md
│   └── time-tracker.md
└── README.md
```

**commands/daily-standup.md**:
```markdown
---
description: Template para daily standup
---

# Daily Standup - {{date}}

## O que fiz ontem?

-

## O que vou fazer hoje?

-

## Bloqueios/Impedimentos?

-

---

**Dica**: Responda de forma concisa e objetiva.
```

### Exemplo 2: Plugin de Deploy

**Objetivo**: Automatizar processos de deploy

**Estrutura**:
```bash
plugins/deploy-automation/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy-staging.md
│   ├── deploy-production.md
│   └── rollback.md
├── agents/
│   └── deploy-assistant.md
└── hooks/
    └── hooks.json
```

**commands/deploy-production.md**:
```markdown
---
description: Inicia deploy para produção
---

# 🚀 Deploy para Produção

⚠️ **ATENÇÃO**: Você está prestes a fazer deploy para PRODUÇÃO!

## Checklist Pré-Deploy:

- [ ] Testes passando
- [ ] Code review aprovado
- [ ] QA validado
- [ ] Documentação atualizada
- [ ] Changelog atualizado

Tem certeza que deseja continuar?

Digite `yes` para confirmar ou `no` para cancelar.
```

---

## ✅ Checklist de Criação

Antes de considerar seu plugin pronto, verifique:

### Estrutura
- [ ] Diretório `.claude-plugin/` criado
- [ ] Arquivo `plugin.json` configurado
- [ ] Pelo menos um componente adicionado (command/agent/hook)

### Configuração
- [ ] Nome único e descritivo
- [ ] Versão seguindo semantic versioning
- [ ] Descrição clara e concisa
- [ ] Informações do autor preenchidas

### Conteúdo
- [ ] Comandos têm descrições no frontmatter
- [ ] Comandos são úteis e bem documentados
- [ ] README.md criado e completo

### Testes
- [ ] Plugin instalado localmente com sucesso
- [ ] Todos os comandos testados
- [ ] Sem erros ou warnings

### Marketplace
- [ ] Plugin adicionado ao `marketplace.json`
- [ ] Categoria apropriada definida
- [ ] Tags relevantes adicionadas

---

## 🛠️ Comandos Úteis

### Criar Plugin Rapidamente

Script bash para criar estrutura:

```bash
#!/bin/bash
# create-plugin.sh

PLUGIN_NAME=$1

if [ -z "$PLUGIN_NAME" ]; then
    echo "Uso: ./create-plugin.sh nome-do-plugin"
    exit 1
fi

echo "Criando plugin: $PLUGIN_NAME"

# Criar estrutura
mkdir -p "plugins/$PLUGIN_NAME/.claude-plugin"
mkdir -p "plugins/$PLUGIN_NAME/commands"
mkdir -p "plugins/$PLUGIN_NAME/agents"
mkdir -p "plugins/$PLUGIN_NAME/hooks"
mkdir -p "plugins/$PLUGIN_NAME/skills"

# Criar plugin.json
cat > "plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" <<EOF
{
  "name": "$PLUGIN_NAME",
  "version": "0.1.0",
  "description": "Descrição do $PLUGIN_NAME",
  "author": {
    "name": "Seu Nome",
    "email": "seu@email.com"
  }
}
EOF

# Criar README
cat > "plugins/$PLUGIN_NAME/README.md" <<EOF
# $PLUGIN_NAME

Descrição do plugin.

## Instalação

\`\`\`bash
/plugin install $PLUGIN_NAME
\`\`\`

## Uso

[Adicione instruções aqui]
EOF

# Criar comando exemplo
cat > "plugins/$PLUGIN_NAME/commands/hello.md" <<EOF
---
description: Comando de exemplo
---

Olá do $PLUGIN_NAME!
EOF

echo "✅ Plugin $PLUGIN_NAME criado com sucesso!"
echo "📁 Localização: plugins/$PLUGIN_NAME"
```

**Uso**:
```bash
chmod +x create-plugin.sh
./create-plugin.sh meu-novo-plugin
```

---

## 🐛 Troubleshooting

### Problema: Plugin não aparece após instalação

**Soluções**:
1. Verifique se o `marketplace.json` está correto
2. Verifique se o caminho em `source` está correto
3. Reinicie o Claude Code
4. Execute `/plugin refresh`

### Problema: Comandos não funcionam

**Soluções**:
1. Verifique o frontmatter do comando
2. Verifique se o arquivo está em `commands/`
3. Verifique se o plugin está habilitado: `/plugin list`
4. Execute `/help` para ver se o comando aparece

### Problema: Plugin.json inválido

**Soluções**:
1. Valide o JSON em um validador online
2. Verifique vírgulas e chaves
3. Verifique campos obrigatórios (name, version, description)

---

## 🚀 Próximos Passos

Agora que você criou seu plugin, aprenda sobre:

➡️ [04 - Componentes do Plugin](./04-componentes-plugin.md)

Ou publique seu plugin:

➡️ [05 - Publicação e Distribuição](./05-publicacao-e-distribuicao.md)

---

[⬅️ Anterior: Configuração do Marketplace](./02-configuracao-marketplace.md) | [⬅️ Voltar ao Índice](./README.md) | [➡️ Próximo: Componentes do Plugin](./04-componentes-plugin.md)
