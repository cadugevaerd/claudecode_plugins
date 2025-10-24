# MCP Server - LangChain Documentation

Este diretório contém a configuração do **Model Context Protocol (MCP) Server** para acesso direto à documentação oficial do LangChain.

## O que é o MCP Server?

O MCP (Model Context Protocol) permite que Claude acesse documentação em tempo real através de uma API HTTP. Isso garante que você sempre tenha acesso às informações mais atualizadas do LangChain v1 e LangGraph v1.

## Benefícios

✅ **Documentação sempre atualizada**: Acesso direto aos docs oficiais
✅ **Busca precisa**: Claude pode buscar informações específicas
✅ **Exemplos de código**: Acesso a code snippets oficiais
✅ **Referências completas**: APIs, guias, tutoriais

## Instalação

### 1. Instalar o MCP Server

Execute o seguinte comando para adicionar o servidor MCP:

```bash
claude mcp add --transport http docs-langchain https://docs.langchain.com/mcp
```

### 2. Verificar Instalação

Confirme que o servidor foi adicionado:

```bash
claude mcp list
```

Você deve ver `docs-langchain` na lista de servidores configurados.

### 3. Usar nos Comandos

Uma vez instalado, o MCP é usado automaticamente pelos comandos e skills do plugin quando necessário.

## Configuração Manual (Alternativa)

Se preferir configurar manualmente, adicione ao seu `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "docs-langchain": {
      "transport": "http",
      "url": "https://docs.langchain.com/mcp"
    }
  }
}
```

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
```

### Construção de Chain
```bash
/lcel-builder criar RAG pipeline com retrievers
# Claude consulta docs oficiais sobre retrievers via MCP
```

### Debug com Contexto
```python
# Você tem um erro em um chain
chain = prompt | llm | parser

# Claude usa MCP para verificar assinatura correta e sugerir fix
```

## Troubleshooting

### Erro: "MCP server not found"

**Solução**: Reinstale o servidor:
```bash
claude mcp remove docs-langchain
claude mcp add --transport http docs-langchain https://docs.langchain.com/mcp
```

### Erro: "Connection timeout"

**Causa**: Possível problema de rede ou URL indisponível.

**Solução**: Verifique conexão de internet e tente novamente:
```bash
curl https://docs.langchain.com/mcp
```

### MCP não está sendo usado

**Verificar**: Confirme que o servidor está ativo:
```bash
claude mcp status docs-langchain
```

## Desinstalar

Para remover o MCP server:

```bash
claude mcp remove docs-langchain
```

O plugin continuará funcionando, mas sem acesso à documentação em tempo real.

## Recursos Adicionais

- **Documentação MCP**: https://docs.anthropic.com/claude/mcp
- **LangChain Docs**: https://python.langchain.com/docs/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/

---

**Nota**: Este MCP Server é opcional mas altamente recomendado para garantir acesso às informações mais atualizadas do LangChain.