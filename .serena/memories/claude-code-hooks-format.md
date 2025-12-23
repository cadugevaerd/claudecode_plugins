# Formato Correto de Hooks para Claude Code

## PreToolUse Hooks - Formato de Bloqueio

Para bloquear uma ferramenta em um hook PreToolUse, use este formato **exato**:

```python
result = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Sua mensagem de bloqueio aqui"
    }
}
print(json.dumps(result))
sys.exit(0)
```

## Valores de permissionDecision

| Valor | Efeito |
|-------|--------|
| `"allow"` | Bypassa permissões, executa sem perguntar |
| `"deny"` | **Bloqueia** a ferramenta, mostra reason ao Claude |
| `"ask"` | Pergunta ao usuário antes de executar |

## ERROS COMUNS

### ❌ ERRADO - systemMessage separado (NÃO FUNCIONA!)
```python
# Isso NÃO bloqueia - retorna "Success"
result = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny"
    },
    "systemMessage": "Mensagem aqui"  # ERRADO!
}
```

### ✅ CORRETO - permissionDecisionReason dentro de hookSpecificOutput
```python
result = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Mensagem aqui"  # CORRETO!
    }
}
```

## Para Permitir (não bloquear)

```python
print(json.dumps({}))
return
```

## Leitura de Input

Sempre ler de stdin, nunca de env vars:

```python
input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
```

## Referência

- Documentação oficial: https://docs.anthropic.com/en/docs/claude-code/hooks
- Data: 2024-12
