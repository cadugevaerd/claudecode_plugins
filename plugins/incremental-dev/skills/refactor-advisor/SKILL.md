---
name: refactor-advisor
description: Detecta automaticamente quando padrões emergiram naturalmente no código e sugere momento apropriado para refatorar. Use quando código tem duplicação, padrões repetidos, ou complexidade crescente. Aplica "Regra dos 3" e identifica quando refatoração adiciona valor real.
allowed-tools: Read, Grep, Glob
---

# Refactor Advisor

Skill que detecta padrões emergentes e identifica o momento APROPRIADO para refatorar, aplicando a "Regra dos 3" para confirmar padrões reais antes de sugerir mudanças.

## 🎯 Quando Me Usar

Invoque automaticamente quando:

1. **Código foi modificado 3+ vezes** - Padrões podem ter emergido
1. **Duplicação óbvia detectada** - Copy-paste de código (3+ lugares)
1. **Classes com estrutura similar** - 3+ classes parecidas
1. **Mudança exige múltiplos arquivos** - Acoplamento alto
1. **Após adicionar incremento** - Avaliar se padrão emergiu

### Termos Gatilho

- "duplicação", "repetido", "copy-paste"
- "3 classes similares", "mesma estrutura"
- "mudar em 3+ arquivos"
- "padrão emergiu", "refatorar"

## 🔍 Padrões de Refatoração

### ✅ Padrão 1: Regra dos 3

Código idêntico/similar em **3+ lugares** = padrão confirmado!

**Exemplos**:

- Mesma função de validação em 3 arquivos
- Código copy-paste repetido em 3+ locais
- Pequenas variações do mesmo padrão

**Refatoração**: Extrair para função/classe compartilhada

### ✅ Padrão 2: Estrutura Similar em Classes

3+ classes com **mesma estrutura** (métodos, fluxo) = Template Method

**Exemplos**:

- EmailProcessor, SMSProcessor, PushProcessor (mesmo fluxo)
- Handlers com validate → process → cleanup

**Refatoração**: Classe base com template method

### ✅ Padrão 3: Mudança Cara

Mudar uma configuração/lógica **exige 3+ arquivos** = acoplamento alto

**Exemplos**:

- Timeout/config espalhado em múltiplos lugares
- Mudança em 1 lugar = precisa mudar em 5 outros

**Refatoração**: Centralizar em arquivo único (config, constants)

### ✅ Padrão 4: Dispatch Repetido

**if/elif** **3+ vezes** para o mesmo tipo = Strategy/Dictionary dispatch

**Exemplos**:

- 3 locais com "if type == email/sms/push"
- Padrão de tipo duplicado em múltiplas funções

**Refatoração**: Dictionary dispatch ou Strategy pattern

## ❌ Quando NÃO Refatorar

| Situação | Ação |
|----------|------|
| **1-2 ocorrências** | Não refatorar ainda (anotar padrão) |
| **Código muito novo** | Esperar padrões reais emergirem (10+ incrementos) |
| **Custo alto vs ganho baixo** | Não vale (refatora 10 arquivos para eliminar 3 linhas) |
| **Refatoração muito complexa** | Deixar duplicação temporária |

**Regra de Ouro**: Refatore apenas quando **Regra dos 3 é satisfeita** E **Custo < Benefício**

## 📊 Métricas de Decisão

### Regra dos 3 (Fundamental)

````text

Ocorrências:
├─ 1x: ❌ Não refatorar
├─ 2x: ⚠️  Anotar padrão
└─ 3+: ✅ REFATORAR

```text

### Maturidade do Código

```text

Incrementos:
├─ 0-5:   ❌ Muito novo
├─ 6-10:  ⚠️  Analisar
└─ 10+:   ✅ Padrões devem emergir

```text

### Custo vs Benefício

```text

Vale refatorar se:
✅ Duplicação significativa (10+ linhas)
✅ Facilita mudanças futuras
✅ Melhora testabilidade
✅ Reduz complexidade
✅ Custo < 2 horas

NÃO vale se:
❌ Ganho mínimo (2-3 linhas)
❌ Muito complexa
❌ Risco alto de quebrar

```text

## 🎯 Fluxo de Detecção

```text

1. Claude modifica código
   ↓
2. Refactor Advisor analisa automaticamente
   ↓
3. Busca padrões emergentes
   ↓
4. Padrão encontrado?
   ├─ NÃO → Prosseguir normalmente
   └─ SIM → Satisfaz Regra dos 3?
       ├─ NÃO → Anotar padrão
       └─ SIM → Custo < Benefício?
           ├─ NÃO → Deixar por enquanto
           └─ SIM → ✅ SUGERIR REFATORAÇÃO

```text

## 💡 Princípios

1. **Regra dos 3**: Refatore com 3+ ocorrências, não menos
2. **Padrões emergem**: Observe código, não planeje prematuramente
3. **Custo vs Benefício**: Refatoração deve valer o esforço
4. **Código maduro**: Deixe código "viver" antes de refatorar
5. **Facilitar mudança futura**: Refatore para próximas mudanças

## 🔗 Integração com Outras Skills

- **PRD Manager**: Autoriza refatoração apenas após incrementos consolidados e alerta sobre divergências
- **YAGNI Enforcer**: Evita refatoração de código simples que segue YAGNI (não force patterns desnecessários)

## 📚 Referência Detalhada

Para exemplos completos e instruções detalhadas:

- **PATTERNS.md** - Padrões de refatoração com exemplos

## ⚡ Lembre-se

✅ Invoco automaticamente ao detectar padrões
✅ Aplico Regra dos 3 rigorosamente
✅ Considero Custo vs Benefício
❌ Não refatoro sozinho (apenas sugiro)

**Objetivo**: Refatorar no momento APROPRIADO - quando padrões reais emergiram e refatoração agrega valor.
````
