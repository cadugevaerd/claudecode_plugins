---
description: Commit and push rápido - ideal para commits pequenos e urgentes
allowed-tools: Bash(git:*)
argument-hint: ''
---

# Quick Commit - Commit e Push Rápido

Executa commit + push rápido com validação de segurança essencial,
sem testes ou verificações completas.

## Procedimento de Execução

### 1. Validar Segurança

Verifique se há arquivos sensíveis usando `git status --short`:

- `.env`, `.env.*`, `*.pem`, `*.key`, `*.pfx`
- `credentials.*`, `secrets.*`
- Arquivos contendo `password`, `token`, `api_key`, `api-key`

**Se houver arquivo sensível**: PARE imediatamente e exiba:

```text
⚠️  ALERTA DE SEGURANÇA

Arquivos sensíveis detectados:
- .env
- credentials.json

❌ Quick commit BLOQUEADO

Soluções:
1. Adicione ao .gitignore: echo ".env" >> .gitignore
2. Remove do stage: git rm --cached <arquivo>
3. NUNCA commit arquivos sensíveis!
```

### 2. Mostrar Resumo de Mudanças

Execute `git diff --stat` e exiba:

```text
📊 Mudanças detectadas:
- 3 arquivos modificados
- +45 linhas adicionadas
- -12 linhas removidas
```

### 3. Gerar Mensagem de Commit

Peça mensagem ao usuário:

```text
Digite mensagem de commit (ou Enter para auto-gerar):
```

**Se usuário fornecer mensagem**: Use como está (valide formato
Conventional Commits básico).

**Se usuário apertar Enter**: Analise arquivos modificados e
auto-gere:

- `docs: update` se maioria arquivos `.md`
- `chore: update` se maioria arquivos de configuração (`.json`, `.yaml`, `.yml`)
- `test: update` se maioria arquivos de teste
- `style: format` se maioria arquivos de estilo
- `chore: update <nome-arquivo>` se arquivo único
- `chore: update <N> files` se múltiplos arquivos

Exemplos: `docs: update README`, `chore: update config files`, `test: update tests`

### 4. Executar Commit e Push

Execute em sequência:

```bash
git add -A
git commit -m "mensagem"
git fetch origin
git pull --rebase origin $(git branch --show-current)
git push origin $(git branch --show-current)
```

**Se houver conflitos durante rebase**:

```text
⚠️  CONFLITOS DETECTADOS

Arquivos em conflito:
- src/main.py
- config.json

🛑 Resolva manualmente:

1. Edite arquivos e resolva conflitos
2. git add <arquivos-resolvidos>
3. git rebase --continue
4. git push

Ou cancele: git rebase --abort
```

### 5. Exibir Resultado Final

```text
═══════════════════════════════════════════
⚡ QUICK COMMIT CONCLUÍDO!
═══════════════════════════════════════════

📊 RESUMO:
├─ Arquivos: 3 modificados
├─ Mudanças: +45 / -12 linhas
├─ Commit: abc1234 chore: update config files
├─ Branch: main
└─ Push: ✅ REALIZADO

═══════════════════════════════════════════
```

## Segurança

- ✅ SEMPRE verifica arquivos sensíveis (BLOQUEADOR)
- ✅ Valida acesso Git básico
- ❌ NÃO executa testes
- ❌ NÃO valida linters
- ❌ NÃO verifica CI/CD
- ❌ NÃO analisa documentação

Você é responsável por garantir que as mudanças são seguras e testadas localmente.

______________________________________________________________________

Para documentação completa (quando usar, exemplos avançados,
troubleshooting), consulte o README do plugin.
