# MCP Server - LangChain Documentation

Este diretório documenta a configuração do **Model Context Protocol (MCP) Server** para acesso direto à documentação oficial do LangChain.

## ✨ Instalação Automática

**O MCP Server é instalado AUTOMATICAMENTE quando você habilita este plugin!**

O arquivo `.mcp.json` no root do plugin configura o servidor `langchain-docs` que usa o [mcpdoc](https://github.com/langchain-ai/mcpdoc) para acessar:

- 📚 **LangChain Python**: https://python.langchain.com/llms.txt
- 🔄 **LangGraph**: https://langchain-ai.github.io/langgraph/llms.txt

## O que é o MCP Server?

O MCP (Model Context Protocol) permite que Claude acesse documentação em tempo real através de llms.txt files. Isso garante que você sempre tenha acesso às informações mais atualizadas do LangChain v1 e LangGraph v1.

## Benefícios

✅ **Documentação sempre atualizada**: Acesso direto aos docs oficiais via llms.txt
✅ **Busca precisa**: Claude pode buscar informações específicas
✅ **Exemplos de código**: Acesso a code snippets oficiais
✅ **Referências completas**: APIs, guias, tutoriais
✅ **Instalação automática**: Nenhuma configuração manual necessária

## Pré-requisitos

O plugin requer que você tenha `uvx` instalado (parte do `uv`):

````bash

# Instalar uv (inclui uvx)
curl -LsSf https://astral.sh/uv/install.sh | sh

```text

## Verificar Instalação

Para confirmar que o MCP server está ativo:

```bash

# Listar MCP servers ativos
claude mcp list

# Você deve ver: langchain-docs

```text

## Configuração (Automática)

O arquivo `.mcp.json` no root do plugin contém:

```json
{
  "mcpServers": {
    "langchain-docs": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "LangChain:https://python.langchain.com/llms.txt",
        "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt",
        "--transport",
        "stdio"
      ]
    }
  }
}

```text

Esta configuração:
- Usa `uvx` para executar `mcpdoc` sem instalação global
- Acessa llms.txt files do LangChain e LangGraph
- Usa transporte `stdio` para comunicação local

## Como Funciona

Quando você usa comandos como `/langchain-help` ou `/lcel-builder`, Claude pode:

1. **Consultar documentação em tempo real** para informações atualizadas
2. **Buscar exemplos específicos** de código oficial
3. **Verificar APIs** e assinaturas de métodos
4. **Acessar guias de migração** mais recentes

## Exemplos de Uso

### Consulta Simples

```bash
/langchain-help LCEL

# Claude acessa docs via MCP para trazer info atualizada

```text

### Construção de Chain

```bash
/lcel-builder criar RAG pipeline com retrievers

# Claude consulta docs oficiais sobre retrievers via MCP

```text

### Debug com Contexto

```python

# Você tem um erro em um chain
chain = prompt | llm | parser

# Claude usa MCP para verificar assinatura correta e sugerir fix

```text

## Troubleshooting

### Erro: "uvx command not found"

**Causa**: `uv` não está instalado no sistema.

**Solução**: Instale `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```text

Depois reinicie o plugin:

```bash
/plugin refresh

```text

### Erro: "MCP server not starting"

**Causa**: Problema com mcpdoc ou llms.txt URLs.

**Solução**: Teste manualmente:

```bash
uvx --from mcpdoc mcpdoc \
  --urls \
  "LangChain:https://python.langchain.com/llms.txt" \
  "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt" \
  --transport stdio

```text

Se funcionar manualmente mas não no plugin, verifique se `.mcp.json` existe no root do plugin.

### MCP server não aparece na lista

**Verificar**: Confirme que o servidor está configurado:

```bash
claude mcp list

```text

Se `langchain-docs` não aparecer:
1. Verifique se o plugin está habilitado
2. Verifique se `.mcp.json` existe
3. Reinicie o plugin: `/plugin refresh`

### Verificar llms.txt URLs

Teste se os URLs estão acessíveis:

```bash
curl https://python.langchain.com/llms.txt
curl https://langchain-ai.github.io/langgraph/llms.txt

```text

Ambos devem retornar conteúdo de documentação.

## Recursos Adicionais

- **Documentação MCP**: https://docs.anthropic.com/claude/mcp
- **LangChain Docs**: https://python.langchain.com/docs/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/


**Nota**: Este MCP Server é opcional mas altamente recomendado para garantir acesso às informações mais atualizadas do LangChain.
````
