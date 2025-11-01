---
description: Commit e push rápido pulando validações extensivas - ideal para commits pequenos e urgentes
---

# ⚡ Quick Commit - Commit e Push Rápido

Comando especializado para **commits rápidos** quando você precisa de velocidade e não quer passar por todas as validações extensivas do `/commit`.

## 🎯 Quando Usar

**✅ Use /quick-commit quando**:
- Commits pequenos e triviais (typos, formatação)
- Mudanças urgentes que precisam ir rápido
- Documentação simples
- Ajustes de configuração
- WIP (Work In Progress) commits
- Você já testou localmente e confia nas mudanças

**❌ NÃO use /quick-commit quando**:
- Mudanças em código crítico
- Refatorações grandes
- Novas funcionalidades importantes
- Mudanças que afetam segurança
- Commits para produção
- **Nestes casos, use `/commit` completo**

## 🚀 Como Usar

```bash
/quick-commit
```

Ou com alias:
```bash
/qcommit
```

## 🔄 O que o Quick Commit faz

### ✅ Validações Mantidas (Segurança)
1. **Verificação de arquivos sensíveis** - SEMPRE verifica
   - `.env`, `.env.*`
   - `*.pem`, `*.key`, `*.pfx`
   - `credentials.*`, `secrets.*`
   - `*password*`, `*token*`, `*api*key*`
   - **Se detectar, PARA IMEDIATAMENTE**

### ⚡ Processo Rápido
2. **Análise rápida de mudanças** - Apenas `git diff --stat`
3. **Mensagem de commit simples** - Conventional Commits básico
4. **Commit automático**
5. **Push automático** (sem perguntar)

### ❌ Validações Puladas (Velocidade)
- ❌ Execução de testes/CI
- ❌ Análise detalhada de diff
- ❌ Verificação de documentação
- ❌ Validação de estrutura de projeto
- ❌ Confirmação de push

## 📋 Processo de Execução

### Passo 1: Validação de Segurança (SEMPRE)

Execute `git status` e verifique arquivos sensíveis:

```bash
git status --short
```

**Se houver arquivos sensíveis, PARE:**
```
⚠️  ALERTA DE SEGURANÇA ⚠️
Arquivos sensíveis detectados:
- .env
- credentials.json

❌ Quick commit BLOQUEADO

Soluções:
1. Adicione ao .gitignore
2. Remove do stage: git rm --cached <arquivo>
3. NUNCA commit arquivos sensíveis!
```

### Passo 2: Análise Rápida

Execute apenas:
```bash
git diff --stat
```

Mostre resumo:
```
📊 Mudanças detectadas:
- 3 arquivos modificados
- +45 linhas adicionadas
- -12 linhas removidas
```

### Passo 3: Gerar Mensagem Simples

**Pergunte ao usuário**:
```
Digite mensagem de commit (ou Enter para auto-gerar):
```

**Se usuário fornecer mensagem**:
- Use a mensagem dele (valide formato conventional commits)

**Se usuário apertar Enter (auto-gerar)**:
- Analise os arquivos modificados
- Gere mensagem simples baseada nos arquivos

**Regras para auto-gerar**:

```python
def auto_generate_message(files_changed):
    # Categorizar por tipo de arquivo
    categories = {
        'docs': ['.md', '.txt', '.rst'],
        'config': ['.json', '.yaml', '.yml', '.toml', '.ini'],
        'style': ['.css', '.scss', '.less'],
        'test': ['test_', '_test.', 'spec.'],
    }

    # Detectar categoria predominante
    if mostly_docs(files_changed):
        return "docs: update documentation"
    elif mostly_config(files_changed):
        return "chore: update configuration"
    elif mostly_tests(files_changed):
        return "test: update tests"
    elif single_file(files_changed):
        return f"chore: update {filename}"
    else:
        return f"chore: update {len(files_changed)} files"
```

**Exemplos de mensagens auto-geradas**:
```
docs: update README
chore: update config files
test: update test cases
fix: update validation logic
chore: update 5 files
```

### Passo 4: Commit e Push

**Execute em sequência**:

```bash
# 1. Add all
git add -A

# 2. Commit
git commit -m "mensagem"

# 3. Fetch e verificar divergências
git fetch origin

# 4. Pull com rebase se necessário
git pull --rebase origin $(git branch --show-current)

# 5. Push
git push origin $(git branch --show-current)
```

**Se houver CONFLITOS durante rebase**:
```
⚠️  CONFLITOS DETECTADOS

Arquivos em conflito:
- src/main.py
- config.json

🛑 Quick commit pausado - resolva manualmente:

1. Resolva conflitos nos arquivos
2. git add <arquivos-resolvidos>
3. git rebase --continue
4. git push

Ou cancele:
   git rebase --abort
```

### Passo 5: Confirmação

Mostre resultado:
```
═══════════════════════════════════════════
⚡ QUICK COMMIT CONCLUÍDO!
═══════════════════════════════════════════

📊 RESUMO:
├─ Arquivos: 3 modificados
├─ Mudanças: +45 / -12 linhas
│
├─ Commit: abc1234 chore: update config files
├─ Branch: main
└─ Push: ✅ REALIZADO

⏱️  Tempo total: ~5 segundos

═══════════════════════════════════════════
```

## 🎨 Exemplos de Uso

### Exemplo 1: Typo no README

```bash
$ /quick-commit

⚡ Quick Commit - Validando segurança...
✅ Nenhum arquivo sensível detectado

📊 Mudanças:
 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

Digite mensagem (Enter para auto):
# Usuário aperta Enter

📝 Mensagem gerada: docs: update README

⚡ Commitando e fazendo push...
✅ Commit: abc1234
✅ Push: origin/main

⏱️  Concluído em 4s
```

### Exemplo 2: Atualizar configuração

```bash
$ /quick-commit

⚡ Quick Commit - Validando segurança...
✅ Nenhum arquivo sensível detectado

📊 Mudanças:
 .github/workflows/ci.yml | 5 +++--
 package.json             | 1 +
 2 files changed, 4 insertions(+), 2 deletions(-)

Digite mensagem (Enter para auto): chore(ci): add cache to workflow

✅ Mensagem customizada aceita

⚡ Commitando e fazendo push...
✅ Commit: def5678
✅ Push: origin/main

⏱️  Concluído em 5s
```

### Exemplo 3: Arquivo sensível detectado

```bash
$ /quick-commit

⚡ Quick Commit - Validando segurança...

⚠️  ALERTA DE SEGURANÇA ⚠️

Arquivos sensíveis detectados:
- .env (credenciais)

❌ Quick commit BLOQUEADO

Ações:
1. Adicione ao .gitignore:
   echo ".env" >> .gitignore

2. Remove do stage:
   git rm --cached .env

3. NUNCA commit arquivos sensíveis!

🛑 Processo cancelado
```

## 🔐 Segurança

**O que SEMPRE é verificado**:
- ✅ Arquivos sensíveis (.env, credenciais, keys)
- ✅ Validação básica de Git (branch, remote)

**O que NÃO é verificado** (você é responsável):
- ❌ Testes não são executados
- ❌ Linters não são executados
- ❌ CI/CD não é validado
- ❌ Documentação não é verificada

**⚠️ IMPORTANTE**: Use quick-commit apenas quando você:
1. Já testou as mudanças localmente
2. Confia que não vai quebrar nada
3. Sabe que as mudanças são seguras
4. Quer velocidade ao invés de validação completa

## 🆚 Quick Commit vs Commit Normal

| Feature | /quick-commit | /commit |
|---------|--------------|---------|
| **Velocidade** | ⚡ ~5 segundos | 🐢 ~30-60 segundos |
| **Validação de segurança** | ✅ Sim | ✅ Sim |
| **Execução de testes** | ❌ Não | ✅ Sim |
| **Análise detalhada** | ❌ Não | ✅ Sim |
| **Verificação de docs** | ❌ Não | ✅ Sim |
| **Push automático** | ✅ Sim | ❓ Pergunta |
| **Mensagem auto-gerada** | ✅ Simples | ✅ Detalhada |
| **Ideal para** | Commits triviais | Commits importantes |

## 💡 Dicas de Uso

### Quando Usar Quick Commit
```bash
# ✅ Typos e correções simples
/quick-commit  # "Fix typo in README"

# ✅ Ajustes de formatação
/quick-commit  # "style: format code"

# ✅ Atualizar configuração
/quick-commit  # "chore: update config"

# ✅ Documentação simples
/quick-commit  # "docs: update examples"

# ✅ WIP commits
/quick-commit  # "wip: progress on feature"
```

### Quando Usar Commit Normal
```bash
# ✅ Nova funcionalidade
/commit  # Executa testes, valida tudo

# ✅ Bug fix importante
/commit  # Garante que testes passam

# ✅ Refatoração
/commit  # Valida estrutura e docs

# ✅ Mudanças em produção
/commit  # Segurança máxima
```

## 🚨 Avisos e Limitações

**⚠️ Quick commit NÃO**:
- ❌ Executa testes
- ❌ Valida linters
- ❌ Verifica CI/CD
- ❌ Analisa documentação
- ❌ Pergunta antes de push
- ❌ Valida estrutura de código

**✅ Quick commit SEMPRE**:
- ✅ Verifica arquivos sensíveis
- ✅ Valida acesso ao Git
- ✅ Usa conventional commits
- ✅ Gerencia conflitos de merge
- ✅ Mostra resultado final

**💡 Recomendação**: Para commits críticos, sempre use `/commit` completo!

## 🛠️ Troubleshooting

### Push falhou

**Problema**: `error: failed to push`

**Solução**:
```bash
# 1. Verificar status
git status

# 2. Pull com rebase
git pull --rebase origin main

# 3. Resolver conflitos se houver

# 4. Push novamente
git push origin main
```

### Conflitos após pull

**Problema**: Conflitos durante rebase

**Solução**:
```bash
# 1. Resolver conflitos manualmente
# Edite arquivos com conflito

# 2. Adicionar arquivos resolvidos
git add <arquivo>

# 3. Continuar rebase
git rebase --continue

# 4. Push
git push origin main
```

### Commit acidental

**Problema**: Fez quick-commit por engano

**Solução**:
```bash
# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Ou desfazer commit e push
git reset --hard HEAD~1
git push --force origin main  # ⚠️ CUIDADO!
```

## 📚 Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Rebase Documentation](https://git-scm.com/docs/git-rebase)
- [Git Best Practices](https://www.git-scm.com/book/en/v2)

---

**Desenvolvido por Carlos Araujo para claudecode_plugins** 🚀