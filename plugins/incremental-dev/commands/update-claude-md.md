---
name: update-claude-md
description: Update project's CLAUDE.md with incremental-dev plugin configuration following best practices
---

# Update CLAUDE.md

Atualiza ou cria `CLAUDE.md` do projeto com instruções de desenvolvimento incremental e referências ao plugin `incremental-dev`.

## Como usar

````bash
/update-claude-md

```text

## O que atualiza

Adiciona ou atualiza em `CLAUDE.md`:

### 1. Seção de Desenvolvimento Incremental
- Princípios YAGNI explicados
- Regra dos 3 para refatoração
- MVP primeiro, depois iterar

### 2. Comandos do Plugin
- Referência rápida dos 10 comandos
- Quando usar cada um
- Workflow recomendado

### 3. Links para Documentação
- `/prd-help` para dúvidas
- Exemplos de uso
- Próximos passos

### 4. Boas Práticas
- Não sobre-engenheirar
- Simples > Elegante
- Funcionar > Perfeito
- Agora > Futuro hipotético

## Processo

1. **Ler CLAUDE.md atual** (se existir):
   - Preservar conteúdo existente
   - Adicionar seção incremental se falta

2. **Atualizar seções**:
   - Adicionar/atualizar referências
   - Manter coerência com projeto
   - Validar links

3. **Salvar CLAUDE.md**:
   - Manter < 40KB se possível
   - Validar markdown
   - Garantir organização

## Output esperado

```text

✅ CLAUDE.md ATUALIZADO

📝 Seções adicionadas:
- Desenvolvimento Incremental (YAGNI)
- Comandos disponíveis
- Workflow recomendado
- Links úteis

🔗 Referências:
- /prd-help - Central de ajuda
- Documentação completa no README

✨ Pronto para usar!

```text

## Próximos comandos

- `/setup-project-incremental` - Configuração completa
- `/start-incremental` - Criar PRD
- `/prd-help` - Aprender sobre o plugin
````
