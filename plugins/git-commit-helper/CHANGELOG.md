# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2025-10-23

### Adicionado

- **Skill UV Python Runner** - Detecção automática e uso de uv (universal virtualenv) em projetos Python
  - Detecta automaticamente projetos que usam uv (pyproject.toml com [tool.uv] ou uv.lock)
  - Transforma comandos Python para usar `uv run` automaticamente
  - Garante sincronização de dependências antes de executar comandos
  - Suporte para pytest, black, flake8, mypy, pylint, ruff e outras ferramentas
  - Documentação completa em `skills/uv-python-runner.md`

### Melhorado

- README.md atualizado com seção sobre suporte UV
- Documentação de comandos Python inclui exemplos com uv
- Tags no marketplace incluem "python" e "uv"

## [1.0.0] - 2025-10-20

### Adicionado

- Release inicial do plugin git-commit-helper
- Comando `/commit` para processo completo de commit
- Agente `commit-assistant` para auxiliar em commits
- Validação de segurança de arquivos sensíveis
- Execução automática de CI/testes
- Análise de mudanças com git diff
- Verificação de documentação
- Geração de mensagens Conventional Commits
- Push seguro com gerenciamento de conflitos
- Suporte multi-linguagem: Node.js, Python, Go, Rust, Java, PHP, Ruby, Terraform
- Detecção automática de ferramentas de CI/CD
- Documentação completa no README.md

---

## Formato do Changelog

### Tipos de Mudança

- **Adicionado** - Para novas funcionalidades
- **Modificado** - Para mudanças em funcionalidades existentes
- **Descontinuado** - Para funcionalidades que serão removidas
- **Removido** - Para funcionalidades removidas
- **Corrigido** - Para correções de bugs
- **Segurança** - Para correções de vulnerabilidades

### Versionamento Semântico

- **MAJOR** (X.0.0) - Mudanças incompatíveis na API
- **MINOR** (X.Y.0) - Novas funcionalidades compatíveis
- **PATCH** (X.Y.Z) - Correções de bugs compatíveis
