---
name: refactor-advisor
description: Detecta automaticamente quando padrões emergiram naturalmente no código e sugere momento apropriado para refatorar. Use quando código tem duplicação, padrões repetidos, ou complexidade crescente. Aplica "Regra dos 3" e identifica quando refatoração adiciona valor real.
allowed-tools: Read, Grep, Glob
---

# Refactor Advisor

Sou uma skill que detecta automaticamente quando código está maduro para refatoração, identificando padrões que emergiram naturalmente e sugerindo o momento APROPRIADO para simplificar ou abstrair.

## 🎯 Quando Sou Invocado

Você (Claude) DEVE me invocar automaticamente quando:

1. **Código foi modificado 3+ vezes** - Padrões podem ter emergido
2. **Duplicação óbvia detectada** - Copy-paste de código
3. **Classes com estrutura similar** - 3+ classes parecidas
4. **Lógica repetida em múltiplos lugares** - Mesmo código 3+ vezes
5. **Mudança exige tocar múltiplos arquivos** - Acoplamento alto
6. **Após adicionar incremento** - Avaliar se padrão emergiu

## 🔍 O Que Detecto

### ✅ Padrão 1: Regra dos 3 - Duplicação Confirmada

**Detectar quando**:
- Código idêntico ou muito similar em 3+ lugares
- Função copy-paste em múltiplos arquivos
- Lógica repetida com pequenas variações

**Exemplo detectado**:
```python
# arquivo1.py
if "@" not in email:
    raise ValueError("Invalid email")

# arquivo2.py
if "@" not in email:
    raise ValueError("Invalid email")

# arquivo3.py
if "@" not in email:
    raise ValueError("Invalid email")
```

**Sugestão a emitir**:
```
✅ REFATORAÇÃO RECOMENDADA: Regra dos 3

Padrão: Validação de email
Ocorrências: 3x (CONFIRMADO!)

Locais:
├─ arquivo1.py linha 45
├─ arquivo2.py linha 78
└─ arquivo3.py linha 123

💡 Momento CERTO de refatorar: Padrão confirmado

Sugestão:
# utils/validators.py (NOVO)
def validate_email(email: str) -> bool:
    if "@" not in email:
        raise ValueError("Invalid email")
    return True

Impacto:
✅ Elimina duplicação (3 lugares)
✅ Mudança futura em 1 lugar apenas
✅ Mais testável

Refatorar agora? (s/n)
```

### ✅ Padrão 2: Estrutura Similar em 3+ Classes

**Detectar quando**:
- 3+ classes com mesma estrutura de métodos
- Mesmo fluxo de execução em múltiplas classes
- Padrão Template Method emergiu naturalmente

**Exemplo detectado**:
```python
# Classe 1
class EmailProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

# Classe 2
class SMSProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

# Classe 3
class PushProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()
```

**Sugestão a emitir**:
```
✅ REFATORAÇÃO RECOMENDADA: Template Method Emergiu

Padrão: Estrutura process/validate/do_work/cleanup
Ocorrências: 3 classes

Classes similares:
├─ EmailProcessor
├─ SMSProcessor
└─ PushProcessor

💡 Padrão Template Method emergiu NATURALMENTE

Sugestão:
# base.py (NOVO)
class Processor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

    def validate(self):
        raise NotImplementedError

    def do_work(self):
        raise NotImplementedError

    def cleanup(self):
        pass  # default vazio

class EmailProcessor(Processor):
    def validate(self): ...  # específico
    def do_work(self): ...   # específico

Impacto:
✅ Elimina duplicação de estrutura
✅ Facilita adicionar novos processadores
✅ Comportamento comum centralizado

Refatorar agora? (s/n)
```

### ✅ Padrão 3: Mudança Exige Múltiplos Arquivos

**Detectar quando**:
- Para mudar X, precisa alterar 3+ arquivos
- Lógica relacionada espalhada
- Alto acoplamento entre módulos

**Exemplo detectado**:
```
User quer mudar: "Timeout de 30s para 60s"

Arquivos que precisam mudar:
├─ email_processor.py (timeout=30)
├─ sms_processor.py (timeout=30)
├─ webhook_sender.py (timeout=30)
└─ api_client.py (timeout=30)
```

**Sugestão a emitir**:
```
✅ REFATORAÇÃO RECOMENDADA: Centralizar Configuração

Problema: Timeout duplicado em 4 arquivos
Dor: Mudança exige alterar 4 lugares

💡 Sinal de acoplamento e duplicação

Sugestão:
# config.py (NOVO)
TIMEOUT = 30

# Arquivos
from config import TIMEOUT

def process():
    send(..., timeout=TIMEOUT)

Impacto:
✅ Mudança futura em 1 lugar apenas
✅ Consistência garantida
✅ Facilita manutenção

Refatorar agora? (s/n)
```

### ✅ Padrão 4: Lógica Repetida com Variações

**Detectar quando**:
- Mesmo padrão com pequenas diferenças
- if/elif repetido em múltiplos lugares
- Strategy Pattern emergindo

**Exemplo detectado**:
```python
# Local 1
if type == "email":
    send_email(data)
elif type == "sms":
    send_sms(data)
elif type == "push":
    send_push(data)

# Local 2 (REPETIDO)
if type == "email":
    process_email(data)
elif type == "sms":
    process_sms(data)
elif type == "push":
    process_push(data)

# Local 3 (REPETIDO)
if type == "email":
    validate_email(data)
elif type == "sms":
    validate_sms(data)
elif type == "push":
    validate_push(data)
```

**Sugestão a emitir**:
```
✅ REFATORAÇÃO RECOMENDADA: Strategy/Dictionary Dispatch

Padrão: if/elif por tipo
Ocorrências: 3 lugares

💡 Pattern: Dispatch baseado em tipo emergiu

Sugestão:
# handlers.py
HANDLERS = {
    "email": EmailHandler(),
    "sms": SMSHandler(),
    "push": PushHandler()
}

# Uso
handler = HANDLERS[type]
handler.send(data)
handler.process(data)
handler.validate(data)

Impacto:
✅ Elimina if/elif duplicado
✅ Facilita adicionar novos tipos
✅ Mais extensível

Refatorar agora? (s/n)
```

## ❌ Quando NÃO Sugerir Refatoração

### 🚫 Padrão 1: Apenas 1-2 Ocorrências

**NÃO refatore**:
```python
# Apenas 2 lugares
def validate_email_1(email):
    return "@" in email

def validate_email_2(email):
    return "@" in email
```

**Resposta**:
```
❌ NÃO REFATORAR AINDA

Padrão: Validação de email
Ocorrências: 2x (insuficiente)

💡 Regra dos 3: Espere 3ª ocorrência
- 2 pode ser coincidência
- Padrão ainda não confirmado
- Pode divergir com próximas iterações

Ação: Anotar padrão, aguardar 3ª ocorrência
```

### 🚫 Padrão 2: Código Muito Novo

**NÃO refatore**:
```
Sistema criado há 2 dias
Apenas 3 incrementos
Poucas interações reais
```

**Resposta**:
```
❌ NÃO REFATORAR AINDA

Motivo: Código muito jovem

💡 Padrões reais ainda não emergiram:
- Código precisa "viver" mais
- Requisitos podem mudar
- Padrões prematuros ≠ padrões reais

Ação: Continue desenvolvendo, reavalie após 10+ incrementos
```

### 🚫 Padrão 3: Refatoração Complexa para Ganho Pequeno

**NÃO refatore**:
```
Custo: Refatorar 10 arquivos, 200 linhas
Ganho: Eliminar 3 linhas duplicadas
```

**Resposta**:
```
❌ NÃO VALE A PENA REFATORAR

Análise Custo vs Benefício:
- Custo: Alto (10 arquivos, 200 linhas)
- Benefício: Baixo (3 linhas duplicadas)
- Risco: Quebrar funcionalidade

💡 Refatoração deve valer o esforço

Ação: Deixar duplicação (OK neste caso)
```

## 📋 Instructions

Quando você (Claude) modificar código, SEMPRE execute este checklist:

### Checklist de Análise

```
[ ] Código foi modificado recentemente?
    → Analisar se padrões emergiram

[ ] Há duplicação de código?
    → Contar ocorrências (3+ = refatorar)

[ ] Classes têm estrutura similar?
    → 3+ classes = considerar Template Method

[ ] Mudança exige múltiplos arquivos?
    → Considerar centralização

[ ] if/elif repetido em múltiplos lugares?
    → 3+ lugares = considerar dispatch

[ ] Código tem > 10 incrementos?
    → Padrões devem ter emergido, analisar

[ ] Duplicação dificulta testes?
    → Considerar refatoração mesmo com 2 ocorrências
```

### Fluxo de Análise

```
1. Claude modifica/adiciona código
   ↓
2. Refactor Advisor analisa automaticamente
   ↓
3. Busca padrões emergentes
   ↓
4. Padrão encontrado?
   │
   ├─ NÃO → Não sugerir refatoração
   │
   └─ SIM → Validar "Regra dos 3"
       ↓
       Padrão 3+ vezes?
       │
       ├─ NÃO → Não refatorar ainda
       │         (anotar e aguardar)
       │
       └─ SIM → ✅ SUGERIR REFATORAÇÃO
           ↓
           Mostrar:
           - Padrão detectado
           - Número de ocorrências
           - Sugestão de refatoração
           - Impacto esperado
           ↓
           Perguntar ao usuário:
           "Refatorar agora? (s/n)"
```

## 🎯 Gatilhos de Detecção

### Quando Analisar Código

**Momentos de análise**:
- Após adicionar incremento (`/add-increment`)
- Após múltiplas modificações no mesmo módulo
- Quando usuário pede análise (`/refactor-now`)
- Após 5+ incrementos (análise periódica)
- Quando detectar copy-paste (via git diff)

**Ferramentas a usar**:
- `Grep` para encontrar padrões duplicados
- `Read` para analisar estrutura de classes
- `Glob` para encontrar arquivos similares

## 📊 Métricas de Decisão

### Regra dos 3 (Fundamental)

```
Ocorrências:
├─ 1x: ❌ Não refatorar (único caso)
├─ 2x: ⚠️  Anotar padrão (pode não ser real)
└─ 3+: ✅ REFATORAR (padrão confirmado!)
```

### Maturidade do Código

```
Incrementos:
├─ 0-5:   ❌ Muito novo (não refatorar)
├─ 6-10:  ⚠️  Analisar padrões
└─ 10+:   ✅ Padrões devem ter emergido
```

### Custo vs Benefício

```
Refatoração vale se:
✅ Elimina duplicação significativa (10+ linhas)
✅ Facilita mudanças futuras
✅ Melhora testabilidade
✅ Reduz complexidade
✅ Custo < 2 horas de trabalho

Refatoração NÃO vale se:
❌ Apenas "código mais bonito"
❌ Ganho mínimo (2-3 linhas)
❌ Muito complexa para implementar
❌ Risco alto de quebrar funcionalidade
```

## 💡 Exemplos de Invocação

### Exemplo 1: Detectar Padrão Confirmado (3x)

```
Claude: Acabei de adicionar terceiro processador com estrutura similar

Refactor Advisor (ATIVADO AUTOMATICAMENTE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PADRÃO EMERGIU - MOMENTO DE REFATORAR

Tipo: Template Method
Ocorrências: 3 classes

Classes detectadas:
├─ EmailProcessor
│   ├─ validate()
│   ├─ process()
│   └─ cleanup()
├─ SMSProcessor
│   ├─ validate()
│   ├─ process()
│   └─ cleanup()
└─ PushProcessor
    ├─ validate()
    ├─ process()
    └─ cleanup()

💡 Estrutura IDÊNTICA em 3 classes = padrão confirmado!

✅ SUGESTÃO DE REFATORAÇÃO:

Criar classe base Processor:

class Processor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

    # Métodos abstratos
    def validate(self): raise NotImplementedError
    def do_work(self): raise NotImplementedError
    def cleanup(self): pass

Impacto:
✅ Elimina duplicação de estrutura (3 classes)
✅ Facilita adicionar novos processadores
✅ Comportamento comum centralizado

Refatorar agora? (s/n)
```

### Exemplo 2: NÃO Refatorar Ainda (2x)

```
Claude: Tenho validação similar em 2 lugares

Refactor Advisor (ATIVADO AUTOMATICAMENTE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ NÃO REFATORAR AINDA

Padrão: Validação de email
Ocorrências: 2x (insuficiente)

Locais:
├─ email_processor.py
└─ sms_processor.py

💡 Regra dos 3 não satisfeita:
- Apenas 2 ocorrências
- Pode ser coincidência
- Padrão ainda não confirmado

✅ AÇÃO RECOMENDADA:
1. Anotar este padrão
2. Continuar desenvolvendo
3. Se aparecer 3ª ocorrência → REFATORAR

Duplicação < 3x é OK! Continue desenvolvendo.
```

### Exemplo 3: Detectar Mudança Cara

```
Claude: Preciso mudar timeout em múltiplos lugares

Refactor Advisor (ATIVADO AUTOMATICAMENTE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ REFATORAÇÃO RECOMENDADA: Centralizar Config

Problema: Timeout duplicado em 5 arquivos

Para mudar timeout, precisa alterar:
├─ email_processor.py
├─ sms_processor.py
├─ webhook_sender.py
├─ api_client.py
└─ batch_processor.py

💡 Sinal: Mudança cara (5 arquivos)

✅ SUGESTÃO DE REFATORAÇÃO:

# config.py (NOVO)
DEFAULT_TIMEOUT = 30

# Usar em todos os arquivos
from config import DEFAULT_TIMEOUT

Impacto:
✅ Mudança em 1 lugar apenas (não 5)
✅ Consistência garantida
✅ Facilita manutenção futura

Refatorar agora? (s/n)
```

## 🎓 Princípios

1. **Regra dos 3**: Refatore apenas com 3+ ocorrências
2. **Padrões emergem**: Não planeje, observe
3. **Custo vs Benefício**: Refatoração deve valer o esforço
4. **Código maduro**: Espere código "viver" antes de refatorar
5. **Facilitar mudança**: Refatore para facilitar PRÓXIMA mudança

## ⚡ Lembre-se

Como skill automática:
- ✅ Sou invocado automaticamente por Claude
- ✅ Analiso código em busca de padrões
- ✅ Aplico "Regra dos 3" rigorosamente
- ✅ Sugiro refatoração quando vale a pena
- ✅ Bloqueio refatoração prematura
- ❌ NÃO refatoro sozinho (apenas sugiro)

**Meu valor**: Identificar o momento CERTO de refatorar - nem muito cedo (over-engineering) nem muito tarde (technical debt).

---

**Quando Claude deve me invocar**:
- Após adicionar incrementos
- Quando detectar duplicação
- Após múltiplas modificações
- Quando código tem 5+ incrementos
- Ao detectar classes similares

**Objetivo**: Refatorar no momento APROPRIADO, quando padrões reais emergiram naturalmente e refatoração adiciona valor concreto.