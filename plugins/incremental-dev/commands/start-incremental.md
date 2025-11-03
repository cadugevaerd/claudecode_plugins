---
description: Iniciar desenvolvimento incremental definindo MVP mínimo e escopo da primeira iteração
allowed-tools: Read, Write, Bash(git:*)
---

# Start Incremental

Inicia desenvolvimento incremental identificando o **Minimum Viable Product (MVP)** e definindo claramente o que FAZER e o que NÃO FAZER na primeira iteração.

## Como usar

```bash
/start-incremental "objetivo do projeto"
```

Ou modo interativo sem argumentos:

```bash
/start-incremental
```

## Processo

### 1. Detectar tipo de projeto

**Se detectar projeto LEGACY** (código existente):

```
⚠️ PROJETO EXISTENTE DETECTADO

Este comando é para NOVOS projetos.

Para projetos legacy, use:
- /adopt-incremental (análise completa + PRD + roadmap)
- /prd-retrofit (apenas criar PRD retroativo)

Continuar mesmo assim? (s/n)
```

**Se novo**: Prosseguir

### 2. Coletar informações (Modo Interativo)

Se nenhuma descrição foi fornecida, fazer perguntas:

1. **O que quer construir?** (1-2 frases)
2. **Que problema resolve?** (dor/necessidade real)
3. **Quem vai usar?** (persona/papel)
4. **Qual funcionalidade principal?** (a MAIS importante)
5. **Outras funcionalidades?** (lista de "pode ser útil")
6. **O que NÃO fazer?** (YAGNI - explicitamente fora de escopo)
7. **MVP prioridade #1?** (qual é o mínimo absoluto)
8. **Métrica de sucesso?** (como medir se funciona)
9. **Prazo/urgência?** (deadline, contexto)
10. **Formato de spikes?** (notebooks ou scripts para exploração técnica)

### 3. Resumo e confirmação

Exibir resumo:

```
═══════════════════════════════════════════
📋 RESUMO DO SEU PRD
═══════════════════════════════════════════

Projeto: [descrição]
Problema: [problema]
Usuário: [usuario_final]

🎯 MVP (Prioridade #1):
- [mvp_prioridade]

⚙️ Outras Funcionalidades:
- [funcionalidades_extras]

❌ Fora de Escopo (YAGNI):
- [fora_de_escopo]

Este resumo está correto? (s/n/editar)
```

### 4. Criar PRD.md

Usar template em `skills/prd-manager/TEMPLATE.md` e preencher com respostas.

Salvar em `docs/PRD.md` ou `PRD.md` (raiz).

## MVP Anti-Patterns

❌ **Evite**:
- Abstrações (use funções diretas)
- Padrões (adicione quando repetir 3x)
- Configuração complexa (hardcode OK para MVP!)
- Validações sofisticadas (mínimas)
- Logging estruturado (print OK)
- Cache/otimização (sem prematura)

✅ **Prefira**:
- Código simples e direto
- Sem patterns
- Funcionalidade mínima
- Funciona para caso mais simples

## Exemplos de MVP

### Exemplo 1: Sistema de Email

❌ GRANDE: "Sistema de processamento com fila, validação, logging e retry"

✅ MVP:
```
- [ ] Receber um email (string)
- [ ] Processar (função simples)
- [ ] Retornar "processado" ou "erro"
```

### Exemplo 2: API REST com LangGraph

❌ GRANDE: "API com cache, validação, retry, autenticação, logging, métricas"

✅ MVP:
```
- [ ] Endpoint POST /process
- [ ] Receber documento (texto simples)
- [ ] LangGraph com 1 node
- [ ] Retornar resultado
```

## Princípios YAGNI

**SEMPRE questionar**:
- "Você precisa AGORA?"
- "O que acontece se não implementar?"
- "Isso resolve o problema MÍNIMO?"

**Evitar frases como**:
- ❌ "Vamos preparar para o futuro..."
- ❌ "Caso precise adicionar..."
- ❌ "Para facilitar expansão..."

**Preferir frases como**:
- ✅ "Vamos fazer funcionar primeiro"
- ✅ "Podemos adicionar quando necessário"
- ✅ "Foco no caso atual"

## Próximos passos

1. **Entender MVP** → Revisar arquivo PRD.md gerado
2. **Implementar MVP** → Começar pelo mínimo
3. **Testar** → Garantir funcionamento
4. **Executar** → Colocar em uso
5. **Iterar** → Usar `/add-increment` para próxima feature

## ⚠️ Depois do MVP

**Não** planeje múltiplas iterações antecipadamente!

Cada iteração revela o que a próxima deve ser.

Use:
- `/add-increment` para adicionar features
- `/refactor-now` para refatorar quando padrões emergirem
- `/review-yagni` para detectar over-engineering
- `/prd-update` para atualizar PRD com aprendizados

**Importante**: MVP não precisa ser "código bonito"!
Hardcode é OK. Refatore quando padrões emergirem (3+ casos).
