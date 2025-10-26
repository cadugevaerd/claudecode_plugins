---
description: Identificar momento certo para refatorar código quando padrões emergem naturalmente
---

# Refactor Now

Este comando identifica o momento APROPRIADO para refatorar código, quando padrões já emergiram naturalmente e refatoração adiciona valor real.

## 🎯 Objetivo

Refatorar no MOMENTO CERTO - nem muito cedo (over-engineering) nem muito tarde (technical debt).

## 📋 Como usar

```
/refactor-now
```

OU especificar escopo:

```
/refactor-now "área específica do código"
```

## 🔍 Processo de Execução

Quando este comando for executado, você DEVE:

### 1. Analisar Código Atual

Ler e analisar codebase identificando:

```
🔄 ANÁLISE DE REFATORAÇÃO

📊 Estado do Código:

Arquivos analisados:
- [arquivo1]: [linhas] linhas
- [arquivo2]: [linhas] linhas
- [arquivo3]: [linhas] linhas

Complexidade geral: [Baixa/Média/Alta]

Procurando padrões...
```

### 2. Detectar Padrões Emergentes

Identificar **PADRÕES REAIS** (não hipotéticos):

```
✅ PADRÕES EMERGENTES DETECTADOS:

1. 🔁 Duplicação de Código
   - Função X duplicada em 3 arquivos
   - Lógica similar em Y, Z e W
   - Copy-paste evidente

2. 🔁 Padrão de Uso Repetido
   - Sequência A → B → C usada 4 vezes
   - Sempre mesma ordem
   - Candidato a abstração

3. 🔁 Estrutura Similar
   - Classes X, Y, Z têm mesma estrutura
   - Apenas diferem em [detalhe]
   - Candidato a herança/composição

❌ PADRÕES NÃO ENCONTRADOS:
(listar o que NÃO precisa refatorar ainda)
```

### 3. Validar "Regra dos 3"

**CRÍTICO**: Apenas refatore se padrão aparece 3+ vezes:

```
📏 VALIDAÇÃO - REGRA DOS 3

Padrão 1: Validação de email
├─ Ocorrência 1: email_processor.py linha 45
├─ Ocorrência 2: sms_processor.py linha 78
└─ Ocorrência 3: notification.py linha 123

✅ 3+ ocorrências: REFATORAR AGORA

Padrão 2: Processamento de dados
├─ Ocorrência 1: data_handler.py linha 33
└─ Ocorrência 2: file_processor.py linha 89

❌ Apenas 2 ocorrências: NÃO REFATORAR AINDA
💡 Espere aparecer 3ª vez para confirmar padrão
```

### 4. Sugerir Refatorações

Para cada padrão validado (3+):

```
✅ REFATORAÇÕES RECOMENDADAS:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Extrair validate_email para utils
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Padrão: Validação de email duplicada 3x

Antes:
# email_processor.py
def process(email):
    if "@" not in email:
        raise ValueError()
    ...

# sms_processor.py
def process(sms):
    email = extract_email(sms)
    if "@" not in email:
        raise ValueError()
    ...

# notification.py
def send(email):
    if "@" not in email:
        raise ValueError()
    ...

Depois:
# utils/validators.py (NOVO)
def validate_email(email: str) -> bool:
    return "@" in email

# email_processor.py
from utils.validators import validate_email

def process(email):
    if not validate_email(email):
        raise ValueError()
    ...

Impacto:
- 3 arquivos modificados
- 1 arquivo novo (utils/validators.py)
- Reduz duplicação
- Facilita mudanças futuras

Refatorar? (s/n)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. Criar abstração Processor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Padrão: 3 processadores com mesma estrutura

Antes:
def process_email(data): ...
def process_sms(data): ...
def process_push(data): ...

Depois:
class Processor:
    def process(self, data):
        raise NotImplementedError

class EmailProcessor(Processor):
    def process(self, data): ...

class SMSProcessor(Processor):
    def process(self, data): ...

class PushProcessor(Processor):
    def process(self, data): ...

Impacto:
- Facilita adicionar novos processadores
- Permite processar uniformemente
- Padrão claro emergiu

Refatorar? (s/n)
```

## 📚 Exemplos Práticos

### Exemplo 1: Quando NÃO Refatorar

```
/refactor-now

🔄 ANÁLISE DE REFATORAÇÃO

📊 Estado do Código:
- 2 arquivos principais
- MVP recém-implementado
- Funcionalidade básica

❌ REFATORAÇÃO NÃO RECOMENDADA

Motivo: Código ainda muito jovem

Padrões detectados:
1. Função similar em 2 lugares (APENAS 2)
   ├─ Ocorrência 1: processor.py
   └─ Ocorrência 2: handler.py

   💡 Espere 3ª ocorrência antes de abstrair

2. Estrutura repetida (2 vezes)
   💡 Pode ser coincidência, não padrão real

✅ RECOMENDAÇÃO:
Continuar adicionando incrementos. Refatorar quando:
- Padrão aparecer 3+ vezes
- Duplicação dificultar manutenção
- Mudança exigir alteração em múltiplos lugares

Continue desenvolvendo com /add-increment
```

### Exemplo 2: Quando Refatorar - Duplicação Clara

```
/refactor-now

🔄 ANÁLISE DE REFATORAÇÃO

📊 Estado do Código:
- 5 módulos de processamento
- Sistema maduro (20+ incrementos)

✅ REFATORAÇÃO RECOMENDADA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Extrair lógica de retry duplicada
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Padrão: Retry manual em 5 lugares

Ocorrências:
├─ email_processor.py (try/except + retry)
├─ sms_processor.py (try/except + retry)
├─ push_processor.py (try/except + retry)
├─ webhook_sender.py (try/except + retry)
└─ api_client.py (try/except + retry)

Antes (exemplo):
def process_email(email):
    try:
        return send(email)
    except Exception:
        try:
            return send(email)  # retry
        except:
            return "erro"

Depois:
# utils/retry.py (NOVO)
def with_retry(func, *args, retries=1):
    for attempt in range(retries + 1):
        try:
            return func(*args)
        except Exception as e:
            if attempt == retries:
                raise
    return None

# processor.py
from utils.retry import with_retry

def process_email(email):
    return with_retry(send, email, retries=1)

Impacto:
✅ 5 arquivos simplificados
✅ Retry centralizado
✅ Fácil mudar comportamento de retry
✅ Padrão MUITO claro (5 ocorrências!)

Refatorar? (s/n)
```

### Exemplo 3: Quando Refatorar - Abstração Emergiu

```
/refactor-now "processadores"

🔄 ANÁLISE DE REFATORAÇÃO - PROCESSADORES

✅ PADRÃO EMERGENTE DETECTADO

4 processadores com estrutura idêntica:
├─ EmailProcessor
│   ├─ validate()
│   ├─ process()
│   └─ handle_error()
├─ SMSProcessor
│   ├─ validate()
│   ├─ process()
│   └─ handle_error()
├─ PushProcessor
│   ├─ validate()
│   ├─ process()
│   └─ handle_error()
└─ WebhookProcessor
    ├─ validate()
    ├─ process()
    └─ handle_error()

💡 Padrão: Template Method emergiu naturalmente!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFATORAÇÃO: Criar classe base Processor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antes:
class EmailProcessor:
    def validate(self, data):
        # validação específica
        pass

    def process(self, data):
        self.validate(data)
        # processamento
        return result

    def handle_error(self, error):
        # tratamento de erro
        pass

# Repetido em SMS, Push, Webhook...

Depois:
# base.py (NOVO)
class Processor:
    def process(self, data):
        try:
            self.validate(data)
            result = self.do_process(data)
            return result
        except Exception as e:
            return self.handle_error(e)

    def validate(self, data):
        raise NotImplementedError

    def do_process(self, data):
        raise NotImplementedError

    def handle_error(self, error):
        return {"error": str(error)}

# email_processor.py
class EmailProcessor(Processor):
    def validate(self, data):
        # apenas lógica específica
        return "@" in data.get("email", "")

    def do_process(self, data):
        # apenas lógica específica
        return send_email(data)

Impacto:
✅ Elimina duplicação de estrutura
✅ Facilita adicionar novos processadores
✅ Comportamento comum centralizado
✅ Padrão agora está ÓBVIO (4 casos)

Refatorar? (s/n)
```

## ⚠️ Quando NÃO Refatorar

### 🚫 Sinais de Refatoração Prematura

**NÃO refatore se**:

❌ **Apenas 1-2 ocorrências**
```
Função duplicada em 2 lugares
→ ESPERE: Pode não ser padrão real
```

❌ **Código muito novo (< 5 incrementos)**
```
MVP recém-criado com pouco uso
→ ESPERE: Padrões ainda não emergiram
```

❌ **"Preparar para o futuro"**
```
"Vamos criar abstração caso precise adicionar..."
→ YAGNI: Adicione quando realmente precisar
```

❌ **Padrão não confirmado**
```
"Essas duas classes são similares..."
→ ESPERE: Podem divergir com próximos incrementos
```

❌ **Refatoração complexa para ganho pequeno**
```
Refatorar 10 arquivos para eliminar 3 linhas duplicadas
→ NÃO VALE: Custo > Benefício
```

## ✅ Quando Refatorar

### ✅ Sinais de Momento Certo

**Refatore se**:

✅ **Regra dos 3**: Padrão aparece 3+ vezes
```
Mesma lógica em 3+ lugares
→ REFATORE: Padrão confirmado
```

✅ **Dor real**: Mudança exige alterar múltiplos lugares
```
"Para mudar X, preciso alterar 5 arquivos"
→ REFATORE: Abstraia X
```

✅ **Copy-paste evidente**: Código idêntico duplicado
```
if "@" not in email:
    raise ValueError("Invalid email")
# Aparece em 4 arquivos IDÊNTICO
→ REFATORE: Extraia função
```

✅ **Padrão óbvio**: Estrutura similar em múltiplas classes
```
4 classes com mesma estrutura (validate, process, error)
→ REFATORE: Template Method ou Strategy
```

✅ **Testes difíceis**: Duplicação dificulta testes
```
Para testar comportamento, preciso mockar em 5 lugares
→ REFATORE: Centralize lógica
```

## 🎯 Estratégias de Refatoração

### 1. Extract Function (Mais comum)

**Quando**: Código duplicado em múltiplos lugares

```python
# Antes (3+ lugares)
if "@" not in email:
    raise ValueError("Invalid")

# Depois (utils/validators.py)
def validate_email(email):
    if "@" not in email:
        raise ValueError("Invalid")
```

### 2. Extract Class

**Quando**: Grupo de funções relacionadas

```python
# Antes (várias funções soltas)
def validate_email(email): ...
def validate_phone(phone): ...
def validate_cpf(cpf): ...

# Depois (apenas se TODAS usadas juntas frequentemente)
class Validator:
    def email(self, email): ...
    def phone(self, phone): ...
    def cpf(self, cpf): ...
```

### 3. Template Method

**Quando**: 3+ classes com mesma estrutura

```python
# Antes (3+ classes similares)
class EmailProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

# Depois
class Processor:  # Base
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()
```

### 4. Replace Conditional with Polymorphism

**Quando**: if/elif repetido em múltiplos lugares

```python
# Antes (3+ lugares)
if type == "email":
    process_email()
elif type == "sms":
    process_sms()

# Depois
processors = {
    "email": EmailProcessor(),
    "sms": SMSProcessor()
}
processors[type].process()
```

## 📊 Decision Matrix

| Situação | Ação | Motivo |
|----------|------|--------|
| Código duplicado em 1-2 lugares | ❌ NÃO REFATORAR | Pode não ser padrão |
| Código duplicado em 3+ lugares | ✅ REFATORAR | Padrão confirmado |
| Código novo (< 5 incrementos) | ❌ NÃO REFATORAR | Padrões não emergiram |
| Código maduro (10+ incrementos) | ✅ ANALISAR | Padrões já devem ter emergido |
| Mudança exige alterar 3+ arquivos | ✅ REFATORAR | Abstrair lógica comum |
| Estrutura similar em 3+ classes | ✅ REFATORAR | Template Method/Strategy |
| "Preparar para futuro" | ❌ NÃO REFATORAR | YAGNI |
| Testes difíceis por duplicação | ✅ REFATORAR | Melhorar testabilidade |

## 🚀 Processo de Refatoração Segura

Quando refatorar:

```
1. ✅ Garantir testes existem (ou criar)

2. 🔄 Refatorar pequenas partes por vez

3. ✅ Rodar testes após cada mudança

4. 💾 Commit após cada refatoração bem-sucedida

5. 🔄 Próxima refatoração ou próximo incremento
```

## 💡 Princípios

1. **Refatore quando padrões EMERGIREM, não quando antecipar**
2. **Regra dos 3**: Espere 3+ ocorrências
3. **Custo vs Benefício**: Refatoração deve valer o esforço
4. **Incremental**: Refatore aos poucos, não tudo de uma vez
5. **Seguro**: Sempre com testes

## 📄 Após Refatoração Bem-Sucedida

Se refatoração envolveu **decisão arquitetural importante**:

```
✅ REFATORAÇÃO COMPLETA!

Esta refatoração envolveu decisão arquitetural? (s/n)
```

**Se SIM**:
```
💡 Registrar como ADR (Architectural Decision Record) no PRD

Detalhes da decisão:
1. Contexto: Por que essa decisão foi necessária?
   > [usuário responde]

2. Decisão: O que foi decidido?
   > [padrão extraído / classe base criada / etc]

3. Consequências positivas:
   > [reduz duplicação / facilita extensão / etc]

4. Consequências negativas:
   > [adiciona complexidade / requer manutenção / etc]

Registrando ADR no PRD...

✅ ADR-[N] registrado em docs/PRD.md!
```

**Exemplos de decisões arquiteturais**:
- ✅ Criar classe base para eliminar duplicação
- ✅ Extrair pattern que emergiu (Strategy, Template Method)
- ✅ Escolher biblioteca/framework
- ✅ Mudar estrutura de dados
- ❌ Renomear variável (não é decisão arquitetural)
- ❌ Extrair função simples (não é decisão arquitetural)

---

## ⚡ Lembre-se

- Padrões emergem com o tempo, não no design inicial
- Duplicação < 3x é OK (pode não ser padrão real)
- Refatoração prematura = Over-engineering
- Refatoração tardia = Technical debt
- Momento certo = Quando padrão ÓBVIO emergir
- Refatore para facilitar PRÓXIMA mudança, não "código bonito"
- **Registre decisões arquiteturais importantes como ADRs no PRD**