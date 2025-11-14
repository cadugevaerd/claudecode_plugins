---
description: Creates initial LangGraph project structure by invoking initial-setup agent
allowed-tools: Task
model: claude-haiku-4-5
---

# Create Setup

Cria estrutura inicial de projetos LangGraph invocando o agente `initial-setup` que configura diretórios, arquivos de configuração e skeleton de código seguindo padrão oficial LangGraph.

## 🎯 Objetivo

- Invocar agente `initial-setup` via Task tool para criar estrutura de projeto LangGraph
- Agente irá questionar usuário sobre configurações necessárias (nome, gerenciador, API keys)
- Criar estrutura completa: diretórios, langgraph.json, .env, skeleton files
- Reportar estrutura criada e próximos passos ao usuário

## 🔧 Instruções

1. **Invocar Agente Initial-Setup**

   Usar `Task` tool para chamar o agente:

   ```python
   Task(
     description: "Setup initial LangGraph project",
     prompt: "Create initial LangGraph project structure following official application structure. Ask user for project name, dependency manager (requirements.txt/pyproject.toml/package.json), agent name, API keys needed, and target directory.",
     subagent_type: "initial-setup"
   )
   ```

2. **Aguardar Execução do Agente**

   O agente `initial-setup` irá:
   - Questionar usuário (AskUserQuestion)
   - Criar estrutura de diretórios
   - Gerar arquivos de configuração
   - Gerar skeleton files
   - Validar estrutura
   - Reportar resultados

3. **Apresentar Resultado ao Usuário**

   Após agente completar, apresentar sumário:
   - ✅ Estrutura criada com sucesso
   - 📂 Diretório do projeto
   - 📋 Arquivos gerados
   - 🔧 Próximos passos

## 📊 Formato de Saída

```text
🔄 Invocando agente initial-setup...

[Agente executa e reporta resultados]

✅ Setup inicial concluído!

Estrutura criada pelo agente initial-setup.
Consulte output acima para detalhes e próximos passos.
```

## ✅ Critérios de Sucesso

- [ ] Task tool invocado com subagent_type="initial-setup"
- [ ] Agente executado sem erros
- [ ] Estrutura de projeto criada (diretórios + arquivos)
- [ ] Arquivos de configuração gerados (langgraph.json, .env, .gitignore)
- [ ] Skeleton files criados (agent.py/ts, utils/)
- [ ] Próximos passos reportados ao usuário

## 📝 Exemplo

```bash
/create-setup
```

**O que acontece:**

1. Comando invoca agente `initial-setup` via Task tool
2. Agente questiona usuário sobre:
   - Nome do projeto
   - Gerenciador de dependências (requirements.txt, pyproject.toml, package.json)
   - Nome do agente (default: "agent")
   - API keys necessárias
   - Diretório de destino
3. Agente cria estrutura completa conforme configurações
4. Agente reporta arquivos gerados e próximos passos
5. Comando confirma conclusão

**Exemplo de interação:**

```text
/create-setup

🔄 Invocando agente initial-setup...

? Nome do projeto: my-chatbot
? Gerenciador: requirements.txt
? Nome do agente: chatbot
? API Keys: OPENAI_API_KEY
? Diretório: ./projects

✅ Estrutura criada com sucesso!

📂 Diretório: /home/user/projects/my-chatbot
📋 Arquivos gerados:
  - langgraph.json
  - requirements.txt
  - .env
  - .gitignore
  - my_chatbot/__init__.py
  - my_chatbot/agent.py
  - my_chatbot/utils/__init__.py
  - my_chatbot/utils/state.py
  - my_chatbot/utils/nodes.py
  - my_chatbot/utils/tools.py

🔧 Próximos passos:
1. cd my-chatbot
2. pip install -r requirements.txt
3. Edite .env e adicione sua OPENAI_API_KEY
4. Implemente seus nodes em my_chatbot/utils/nodes.py
5. Configure seu graph em my_chatbot/agent.py

✅ Setup inicial concluído!
```
