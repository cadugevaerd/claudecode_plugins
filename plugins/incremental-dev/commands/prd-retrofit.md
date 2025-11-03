---
description: Criar PRD retroativo para projeto existente - analisa código e gera documentação baseada na realidade
---

# PRD Retrofit

Cria um **Product Requirements Document (PRD) retroativo** para projetos que já foram desenvolvidos mas não têm documentação formal de requisitos.

## Como usar

````bash
/prd-retrofit
/prd-retrofit "Sistema de gerenciamento de estoque"

```text

## Diferença para `/adopt-incremental`

| Comando | O que faz |
|---------|-----------|
| `/prd-retrofit` | **Apenas** cria PRD retroativo a partir do código |
| `/adopt-incremental` | PRD + identifica over-engineering + cria roadmap de simplificação + configura CLAUDE.md |

Use `prd-retrofit` se só precisa de documentação.

Use `adopt-incremental` se quer adotar YAGNI completo.

## Processo

1. **Detectar versão do projeto**:
   - Procurar em: `pyproject.toml`, `setup.py`, `__init__.py`, `package.json`
   - Se não encontrar: sugerir `v1.0.0` ou usar `YYYY.MM.DD`

2. **Analisar estrutura**:
   - Detectar framework/stack (FastAPI, Django, React, etc)
   - Listar arquivos-chave
   - Identificar padrão de organização

3. **Extrair funcionalidades**:
   - Ler código-fonte
   - Documentar features implementadas
   - Listar endpoints, modelos, componentes
   - Extrair decisões arquiteturais visíveis

4. **Gerar PRD.md**:
   - Estrutura: Visão geral, Stack, Features, Arquitetura, Histórico
   - Salvar em `docs/PRD.md` ou `PRD.md` (raiz)
   - Mostrar resultado ao usuário

5. **Validar**:
   - Usuário revisa PRD gerado
   - Faz ajustes se necessário com `/prd-fix`

## Output esperado

```text

✅ PRD RETROATIVO CRIADO

📄 docs/PRD.md (v1.2.3)

✨ Destacado:
- Stack: FastAPI + PostgreSQL + React
- Features principais: 12 funcionalidades
- ADRs implícitas: 5 decisões detectadas
- Linhas de código: 2,453

🔧 Próximos passos:
- Revisar PRD gerado
- Usar /prd-fix para ajustes
- Use /adopt-incremental para análise de over-engineering

```text

## Próximos comandos

- `/prd-view` - Visualizar PRD gerado
- `/prd-fix` - Ajustar seções específicas
- `/adopt-incremental` - Análise completa + roadmap
- `/add-increment` - Começar a adicionar features incrementalmente
````
