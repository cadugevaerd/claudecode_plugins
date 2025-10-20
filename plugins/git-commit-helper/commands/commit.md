---
description: Realiza commit com validações completas, conventional commits e CI/CD
---

# Comando: /commit

Este comando automatiza o processo completo de commit seguindo as melhores práticas.

## ⚠️ Instruções Importantes

**Não questione nenhum dos passos abaixo, apenas os execute.**

---

## 📋 Processo de Commit

### 1. Validações de Segurança

**1.1.** Execute `git status` para verificar o estado atual do repositório

**1.2.** Verifique se há **arquivos sensíveis** nos arquivos modificados:
- `.env`, `.env.*`
- `*.pem`, `*.key`, `*.pfx`, `*.p12`
- `credentials.*`, `secrets.*`, `secret.*`
- `*password*`, `*token*`, `*api?key*`
- `.aws/credentials`, `.ssh/id_*`

**1.3.** Se houver arquivos sensíveis, **PARE IMEDIATAMENTE** e alerte:

```
⚠️  ALERTA DE SEGURANÇA ⚠️
Os seguintes arquivos sensíveis foram detectados:
- [lista de arquivos]

❌ Estes arquivos NÃO devem ser commitados.

Soluções:
1. Adicione ao .gitignore
2. Remove do stage: git rm --cached <arquivo>
3. Use variáveis de ambiente ou gerenciadores de secrets
```

---

### 2. Execução de CI/CD e Testes

**2.1.** Detecte e execute o CI/CD/Testes do projeto:

**Detecção automática** (em ordem de prioridade):

1. **CI Script Customizado**:
   ```bash
   # Se existir ci.py, ci.sh, ou validate.sh
   python ci.py        # ou
   ./ci.sh            # ou
   ./validate.sh
   ```

2. **GitHub Actions** (local):
   ```bash
   # Se .github/workflows/ existir
   act -l  # Listar workflows
   act     # Executar workflows
   ```

3. **npm/Node.js**:
   ```bash
   # Se package.json existir
   npm test           # Testes
   npm run lint       # Linting
   npm run build      # Build (se existir)
   ```

4. **Python**:
   ```bash
   # Se requirements.txt ou setup.py existir
   pytest --cov=. --cov-report=term-missing  # Testes com cobertura
   black . --check                           # Formatação
   flake8 .                                  # Linting
   mypy .                                    # Type checking (se configurado)
   ```

5. **Terraform/IaC**:
   ```bash
   terraform fmt -check -recursive    # Formatação
   terraform validate                 # Validação
   tflint                            # Linting (se instalado)
   ```

6. **Docker**:
   ```bash
   docker build -t test-build .      # Build do container
   ```

7. **Make**:
   ```bash
   # Se Makefile existir
   make test          # ou make validate, make ci
   ```

**2.2.** Se o CI/Testes **FALHAREM**:
- **PARE IMEDIATAMENTE**
- Mostre o erro completo
- Liste as correções necessárias:
  ```
  ❌ CI/Testes falharam!

  Erros encontrados:
  - [erro 1]
  - [erro 2]

  Correções necessárias:
  1. [correção 1]
  2. [correção 2]

  ⚠️  O commit está BLOQUEADO até que os testes passem.
  ```
- **NÃO PROSSIGA** com o commit

**2.3.** Se o CI/Testes **PASSAREM**:
```
✅ CI/Testes passaram com sucesso!
- Testes: ✓
- Linting: ✓
- Build: ✓
- Cobertura: X%

Prosseguindo para análise de mudanças...
```

---

### 3. Análise de Mudanças

**3.1.** Execute `git log --oneline -10` para entender o padrão de commits recentes

**3.2.** Execute `git diff --stat` para resumo das mudanças

**3.3.** Execute `git diff` para mudanças detalhadas
- Se muito extenso (>100 linhas), limite a visualização
- Foque nas mudanças mais importantes

**3.4.** Categorize as mudanças:
- Novos arquivos criados
- Arquivos modificados
- Arquivos deletados
- Tipos de mudanças (código, docs, config, testes)

---

### 4. Verificação de Documentação

**4.1.** Analise se as mudanças **requerem atualização** em:

- `README.md` - Documentação principal do projeto
- `CHANGELOG.md` - Log de mudanças
- `docs/` - Documentação técnica
- Docstrings/comentários de código alterado
- `CONTRIBUTING.md` - Se mudou workflow
- `package.json`, `setup.py`, etc. - Metadados do projeto

**4.2.** Se documentação estiver **desatualizada**:

```
⚠️  DOCUMENTAÇÃO DESATUALIZADA

Arquivos que podem precisar atualização:
- README.md: [motivo]
- CHANGELOG.md: [motivo]
- [outros arquivos]

Deseja atualizar a documentação antes do commit? (s/n)
```

**4.3.** Se usuário escolher **SIM**:
- Ajude a atualizar a documentação necessária
- Volte ao **Passo 2** (executar CI/Testes novamente)

---

### 5. Geração da Mensagem de Commit

**5.1.** Use **Conventional Commits** seguindo o padrão:

```
tipo(escopo): descrição curta

Corpo da mensagem (opcional):
- Detalhe 1
- Detalhe 2

Rodapé (opcional):
BREAKING CHANGE: descrição
Closes #123
```

**Tipos de commit**:

| Tipo | Quando Usar | Exemplo |
|------|-------------|---------|
| `feat` | Nova funcionalidade | `feat(auth): adicionar login com OAuth` |
| `fix` | Correção de bug | `fix(api): corrigir timeout em requisições` |
| `refactor` | Refatoração (sem mudança de comportamento) | `refactor(parser): simplificar lógica de parsing` |
| `docs` | Apenas documentação | `docs(readme): atualizar instruções de instalação` |
| `test` | Adição/modificação de testes | `test(user): adicionar testes de validação` |
| `chore` | Manutenção (deps, config, build) | `chore(deps): atualizar dependencies` |
| `style` | Formatação (sem mudança lógica) | `style: formatar código com prettier` |
| `perf` | Melhorias de performance | `perf(db): otimizar queries com índices` |
| `ci` | Mudanças em CI/CD | `ci: adicionar workflow de deploy` |
| `build` | Build system ou dependências | `build: atualizar webpack config` |
| `revert` | Reverter commit anterior | `revert: desfazer commit abc123` |

**Escopos comuns** (adapte ao seu projeto):
- `api`, `ui`, `auth`, `db`, `config`
- `docs`, `tests`, `ci`, `build`
- Nome de módulos/componentes específicos

**Regras para descrição**:
- ✅ Máximo 72 caracteres
- ✅ Começar com letra minúscula
- ✅ NÃO terminar com ponto
- ✅ Usar imperativo ("adicionar" não "adicionado")
- ✅ Ser clara e concisa

**Exemplos de boas mensagens**:
```
feat(user): adicionar validação de email
fix(api): corrigir race condition em /users endpoint
refactor(auth): extrair lógica de JWT para módulo separado
docs(api): documentar endpoints REST com OpenAPI
test(integration): adicionar testes E2E para checkout
chore(deps): atualizar react de 17.0.2 para 18.2.0
perf(image): implementar lazy loading de imagens
ci: adicionar cache de dependências no GitHub Actions
```

**5.2.** Se houver **múltiplos tipos de mudanças**, use o tipo mais significativo

**5.3.** Se for **breaking change**, adicione `BREAKING CHANGE:` no rodapé:
```
feat(api): mudar formato de resposta para JSON:API

BREAKING CHANGE: API agora retorna dados no formato JSON:API spec.
Clientes precisam atualizar parsers de resposta.
```

---

### 6. Commit

**6.1.** Adicione todos os arquivos modificados:
```bash
git add -A
```

**6.2.** Verifique os arquivos que serão commitados:
```bash
git diff --cached --name-status
```

**6.3.** Execute o commit usando **HEREDOC** para mensagem formatada:

```bash
git commit -m "$(cat <<'EOF'
tipo(escopo): descrição curta

Corpo da mensagem (se necessário):
- Mudança 1
- Mudança 2

Rodapé (se necessário):
Closes #123
EOF
)"
```

**6.4.** Verifique sucesso do commit:
```bash
git log -1 --oneline
git show --stat
```

---

### 7. Push (OPCIONAL)

**7.1.** **PERGUNTE ao usuário**:
```
Deseja fazer push das mudanças para o remote? (s/n)
```

**7.2.** Se **SIM**:

1. Fetch do remote:
   ```bash
   git fetch origin
   ```

2. Verifique se há mudanças remotas:
   ```bash
   git status
   ```

3. Se houver mudanças no remote:
   ```bash
   git pull --rebase origin $(git branch --show-current)
   ```

4. Se houver **CONFLITOS**:
   ```
   ⚠️  CONFLITOS DETECTADOS

   Arquivos em conflito:
   - [lista de arquivos]

   Resolva os conflitos manualmente:
   1. Edite os arquivos conflitantes
   2. git add <arquivos resolvidos>
   3. git rebase --continue
   4. Execute /commit novamente para push
   ```
   **PARE** aqui

5. Se **SEM conflitos**, faça push:
   ```bash
   git push origin $(git branch --show-current)
   ```

**7.3.** Mostre resultado do push:
```
✅ Push realizado com sucesso!

Branch: main
Remote: origin
Commit: abc123 - feat(api): adicionar endpoint users
URL: https://github.com/user/repo/commit/abc123
```

---

### 8. Confirmação Final

**8.1.** Mostre resumo completo:

```
═══════════════════════════════════════════
✅ COMMIT REALIZADO COM SUCESSO!
═══════════════════════════════════════════

📊 RESUMO:
├─ Arquivos modificados: X
├─ Inserções: +XXX linhas
├─ Deleções: -XXX linhas
│
├─ ✅ Testes: PASSOU (cobertura: XX%)
├─ ✅ Linting: PASSOU
├─ ✅ Build: PASSOU
├─ ✅ Security: SEM VULNERABILIDADES
│
├─ Commit: [abc123] tipo(escopo): mensagem
├─ Branch: main
└─ Push: ✅ REALIZADO / ⏸️  NÃO REALIZADO

═══════════════════════════════════════════
```

**8.2.** Se push **NÃO** foi realizado:
```
💡 LEMBRE-SE: Faça push quando estiver pronto

   git push origin $(git branch --show-current)

   Ou use /push para executar com validações
```

**8.3.** Próximos passos sugeridos:
```
🚀 PRÓXIMOS PASSOS:

1. [ ] Verificar CI/CD no GitHub/GitLab
2. [ ] Criar Pull Request (se estiver em feature branch)
3. [ ] Atualizar issue/ticket relacionado
4. [ ] Notificar equipe sobre mudanças
```

---

## 🛠️ Casos Especiais

### Commit Rápido (Skip Tests)

Use apenas para mudanças triviais (typos em docs, etc.):

```bash
# Adicione flag --no-verify para pular hooks
git commit --no-verify -m "docs: fix typo in README"
```

⚠️ **Use com cuidado!** Testes existem por uma razão.

### Commit Vazio

Para forçar rebuild de CI:

```bash
git commit --allow-empty -m "chore: trigger CI rebuild"
```

### Amend (Corrigir último commit)

Se cometeu erro no último commit:

```bash
# Edite os arquivos necessários
git add .
git commit --amend --no-edit  # Mantém mensagem
# ou
git commit --amend            # Edita mensagem
```

---

## 📝 Notas Importantes

- ⚠️ **CI/Testes são SEMPRE executados** - não há exceções (exceto --no-verify)
- ⚠️ **Se CI falhar, commit é BLOQUEADO** até correções
- ⚠️ **Arquivos sensíveis NUNCA devem ser commitados**
- 💡 **Push é OPCIONAL** - sempre pergunta antes de executar
- 💡 **Conventional Commits** facilita geração de changelogs automáticos
- 💡 **Documentação atualizada** previne débito técnico

---

## 🔧 Customização

Para adaptar este comando ao seu projeto, você pode:

1. **Criar script CI personalizado**:
   - `ci.sh`, `ci.py`, `validate.sh`
   - O comando detectará e executará automaticamente

2. **Configurar pre-commit hooks**:
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash
   npm test && npm run lint
   ```

3. **Usar ferramentas de commit**:
   - [commitizen](https://github.com/commitizen/cz-cli) - CLI interativo
   - [commitlint](https://commitlint.js.org/) - Validar mensagens
   - [husky](https://typicode.github.io/husky/) - Git hooks fáceis

---

## 📚 Recursos Adicionais

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Best Practices](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)

---

**Desenvolvido com ❤️ pela Claude Code Community**
