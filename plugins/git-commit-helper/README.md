# Git Commit Helper

Plugin para Claude Code que automatiza o processo completo de commit Git seguindo as melhores práticas de desenvolvimento.

## 🎯 Funcionalidades

- ✅ **Validação de Segurança** - Detecta e bloqueia commits de arquivos sensíveis
- ✅ **Execução Automática de CI/Testes** - Detecta e executa testes do seu projeto
- ✅ **Análise de Mudanças** - Analisa git diff e sumariza mudanças
- ✅ **Verificação de Documentação** - Identifica docs que precisam atualização
- ✅ **Conventional Commits** - Gera mensagens seguindo padrões
- ✅ **Push Seguro** - Gerencia conflitos e push opcional
- ✅ **Multi-linguagem** - Suporta Node.js, Python, Go, Rust, Java, PHP, Ruby, Terraform
- ✅ **Suporte UV Python** - Detecção automática e uso de uv (universal virtualenv) em projetos Python

## 📦 Instalação

### Adicionar o Marketplace

```bash
/plugin marketplace add seu-usuario/claudecode-plugins
```

### Instalar o Plugin

```bash
/plugin install git-commit-helper
```

## 🚀 Uso

### Comando Principal: /commit

Execute o processo completo de commit:

```bash
/commit
```

O comando irá automaticamente:

1. ✅ Verificar arquivos sensíveis
2. ✅ Executar CI/testes do projeto
3. ✅ Analisar mudanças
4. ✅ Verificar documentação
5. ✅ Gerar mensagem de commit (Conventional Commits)
6. ✅ Executar commit
7. ✅ Perguntar sobre push

### Usando o Agente

Você também pode usar o agente commit-assistant:

```
"Analise as mudanças e faça commit"
"Gere uma mensagem de commit para estas alterações"
"Execute os testes e faça commit se passar"
```

## 🎨 Conventional Commits

O plugin gera mensagens seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(escopo): descrição curta

Corpo da mensagem (opcional)

Rodapé (opcional)
```

### Tipos Suportados

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat(auth): add OAuth2 support` |
| `fix` | Correção de bug | `fix(api): prevent race condition` |
| `refactor` | Refatoração | `refactor(parser): simplify logic` |
| `docs` | Documentação | `docs(readme): update install steps` |
| `test` | Testes | `test(user): add validation tests` |
| `chore` | Manutenção | `chore(deps): update react to 18.2` |
| `style` | Formatação | `style: format code with prettier` |
| `perf` | Performance | `perf(db): add indexes` |
| `ci` | CI/CD | `ci: add caching to workflow` |
| `build` | Build system | `build: update webpack config` |

## 🔧 Detecção Automática de Ferramentas

O plugin detecta automaticamente as ferramentas do seu projeto:

### JavaScript/Node.js
```bash
npm test
npm run lint
npm run build
```

### Python
```bash
pytest --cov
black . --check
flake8 .
mypy .
```

**Com UV (detecção automática)**:
```bash
uv run pytest --cov
uv run black . --check
uv run flake8 .
uv run mypy .
```

### Go
```bash
go test
go vet
go fmt
```

### Rust
```bash
cargo test
cargo check
cargo clippy
```

### Terraform
```bash
terraform fmt -check
terraform validate
tflint
```

### Docker
```bash
docker build -t test .
```

### Scripts Customizados
```bash
./ci.sh
python ci.py
make test
```

## 🐍 Suporte para UV (Universal Virtualenv)

O plugin detecta automaticamente projetos Python que usam **uv** (gerenciador de pacotes extremamente rápido da Astral) e executa comandos usando `uv run`:

### Detecção Automática

O plugin detecta uv quando encontra:
- Arquivo `pyproject.toml` com seção `[tool.uv]`
- Arquivo `uv.lock` na raiz do projeto
- Diretório `.venv` criado por uv

### Benefícios

- 🚀 **80x mais rápido** que python -m venv
- 🔒 **Lockfile cross-platform** para dependências consistentes
- 🔄 **Sincronização automática** de dependências antes de executar
- ✅ **Sem ativação manual** de virtualenv necessária
- 🎯 **Resolução determinística** de dependências

### Exemplo de Uso

**Projeto com uv**:
```bash
$ /commit

🧪 Executando testes...
→ uv run pytest --cov  # Executado automaticamente
✅ Testes: 45 passed (cobertura: 87%)

→ uv run black . --check  # Linting com uv
✅ Linting: passed

→ uv run mypy .  # Type checking com uv
✅ Type checking: passed
```

**Documentação completa**: Veja `skills/uv-python-runner.md` para detalhes.

## 🛡️ Segurança

### Arquivos Sensíveis Bloqueados

O plugin detecta e bloqueia commits de:

- `.env`, `.env.*`
- `*.pem`, `*.key`, `*.pfx`
- `credentials.*`, `secrets.*`
- `*password*`, `*token*`, `*api*key*`
- `.aws/credentials`, `.ssh/id_*`

### Validações de Segurança

Se configurado, executa:
- `npm audit` (Node.js)
- `pip-audit` (Python)
- `cargo audit` (Rust)
- `bundle audit` (Ruby)
- `trivy` (containers e IaC)

## 📝 Exemplos

### Exemplo 1: Feature Nova

```bash
$ /commit

🔍 Verificando segurança...
✅ Nenhum arquivo sensível detectado

🧪 Executando testes...
✅ Testes: 45 passed (cobertura: 87%)
✅ Linting: passed
✅ Build: success

📊 Analisando mudanças...
Arquivos modificados: 3
- src/auth/oauth.js (nova)
- src/api/routes.js (modificado)
- tests/auth/oauth.test.js (nova)

📝 Gerando mensagem de commit...

tipo(escopo): feat(auth): add OAuth2 authentication support

✅ Commit realizado!
[abc123] feat(auth): add OAuth2 authentication support

🚀 Deseja fazer push? (s/n)
```

### Exemplo 2: Bug Fix

```bash
$ /commit

🔍 Verificando segurança...
✅ OK

🧪 Executando testes...
✅ Todos os testes passaram

📊 Mudanças:
- src/utils/parser.js (corrigido)
- tests/utils/parser.test.js (adicionado teste)

📝 Mensagem:
fix(parser): prevent crash on empty input

✅ Commit realizado!
```

## ⚙️ Configuração

### Script CI Customizado

Crie um script `ci.sh`, `ci.py` ou `validate.sh` na raiz do projeto:

```bash
#!/bin/bash
# ci.sh

set -e

echo "Running tests..."
npm test

echo "Running linter..."
npm run lint

echo "Building..."
npm run build

echo "✅ All checks passed!"
```

O plugin detectará e executará automaticamente.

### Pre-commit Hooks

Configure hooks para executar antes do commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash
npm test || exit 1
```

### Commitizen (Opcional)

Para CLI interativo:

```bash
npm install -g commitizen
```

## 🎓 Boas Práticas

### Commits Atômicos

✅ **Faça**:
- Um commit = uma mudança lógica
- Commits que passam em testes individualmente
- Mensagens claras e descritivas

❌ **Não faça**:
- Commits com código quebrado
- Commits com testes falhando
- Mensagens vagas ("fixed stuff")

### Quando Fazer Commit

**Faça commit quando**:
- ✅ Funcionalidade completa implementada
- ✅ Testes passando
- ✅ Código formatado
- ✅ Documentação atualizada

**NÃO faça commit de**:
- ❌ Código WIP (work in progress)
- ❌ Testes falhando
- ❌ Commented code
- ❌ Debug logs

### Breaking Changes

Para mudanças que quebram compatibilidade:

```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: API responses now follow JSON:API spec.
Clients must update their response parsers.

Migration guide: https://docs.example.com/migration/v2
```

## 🐛 Troubleshooting

### Plugin não detecta ferramentas

**Problema**: CI/testes não são executados

**Solução**:
1. Verifique se as ferramentas estão instaladas
2. Crie um script `ci.sh` customizado
3. Configure `package.json` com scripts `test`, `lint`, `build`

### Testes sempre falham

**Problema**: Commit é bloqueado

**Solução**:
1. Execute testes manualmente: `npm test`
2. Corrija os testes falhando
3. Use `git commit --no-verify` apenas para emergências

### Arquivos sensíveis não detectados

**Problema**: Arquivo sensível passou

**Solução**:
1. Adicione ao `.gitignore`
2. Use `git rm --cached <arquivo>`
3. Adicione pattern customizado no plugin (futuro)

## 📚 Recursos Adicionais

### Documentação
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Best Practices](https://git-scm.com/book)

### Ferramentas Recomendadas
- [commitizen](https://github.com/commitizen/cz-cli) - CLI interativo
- [commitlint](https://commitlint.js.org/) - Validar mensagens
- [husky](https://typicode.github.io/husky/) - Git hooks
- [lint-staged](https://github.com/okonet/lint-staged) - Lint staged files

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças (usando este plugin! 😉)
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](../../LICENSE) para detalhes.

## 👥 Autor

**Claude Code Community**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- Issues: [GitHub Issues](https://github.com/seu-usuario/claudecode-plugins/issues)

## 🙏 Agradecimentos

Inspirado por ferramentas como:
- commitizen
- commitlint
- conventional-changelog
- semantic-release

---

**Desenvolvido com ❤️ pela Claude Code Community**

⭐ Se este plugin foi útil, dê uma estrela no repositório!
