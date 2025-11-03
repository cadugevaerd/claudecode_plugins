# Refactor Advisor - Padrões Detalhados

Exemplos completos e instruções detalhadas para cada padrão de refatoração.

---

## Padrão 1: Regra dos 3 - Duplicação Confirmada

### Exemplo: Validação de Email

**Código duplicado em 3 arquivos**:
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

**Refatoração sugerida**:
```python
# utils/validators.py (NOVO)
def validate_email(email: str) -> bool:
    if "@" not in email:
        raise ValueError("Invalid email")
    return True

# Uso em todos os arquivos
from utils.validators import validate_email

validate_email(email)
```

**Impacto**:
✅ Elimina duplicação (3 lugares)
✅ Mudança futura em 1 lugar apenas
✅ Mais testável

---

## Padrão 2: Estrutura Similar em Classes

### Exemplo: Template Method Pattern

**Código similar em 3 classes**:
```python
class EmailProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

class SMSProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()

class PushProcessor:
    def process(self):
        self.validate()
        self.do_work()
        self.cleanup()
```

**Refatoração sugerida**:
```python
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

# Implementações específicas
class EmailProcessor(Processor):
    def validate(self):
        # validação específica
        pass

    def do_work(self):
        # lógica específica
        pass

class SMSProcessor(Processor):
    def validate(self):
        # validação específica
        pass

    def do_work(self):
        # lógica específica
        pass

class PushProcessor(Processor):
    def validate(self):
        # validação específica
        pass

    def do_work(self):
        # lógica específica
        pass
```

**Impacto**:
✅ Elimina duplicação de estrutura
✅ Facilita adicionar novos processadores
✅ Comportamento comum centralizado

---

## Padrão 3: Mudança Cara - Centralizar Configuração

### Exemplo: Timeout Espalhado

**Problema: Timeout em múltiplos arquivos**:
```
Para mudar timeout de 30s para 60s, precisa alterar:
├─ email_processor.py (timeout=30)
├─ sms_processor.py (timeout=30)
├─ webhook_sender.py (timeout=30)
└─ api_client.py (timeout=30)
```

**Refatoração sugerida**:
```python
# config.py (NOVO)
TIMEOUT = 30
MAX_RETRIES = 3
DEBUG = False

# email_processor.py
from config import TIMEOUT, MAX_RETRIES

def send_email(email, timeout=TIMEOUT):
    # usa TIMEOUT
    pass

# sms_processor.py
from config import TIMEOUT

def send_sms(message, timeout=TIMEOUT):
    # usa TIMEOUT
    pass

# webhook_sender.py
from config import TIMEOUT

def send_webhook(data, timeout=TIMEOUT):
    # usa TIMEOUT
    pass

# api_client.py
from config import TIMEOUT

def call_api(endpoint, timeout=TIMEOUT):
    # usa TIMEOUT
    pass
```

**Impacto**:
✅ Mudança em 1 lugar apenas (não 4)
✅ Consistência garantida
✅ Facilita manutenção futura

---

## Padrão 4: Dispatch Repetido - Strategy Pattern

### Exemplo: if/elif Repetido em 3 Locais

**Código duplicado**:
```python
# Local 1: envio
if type == "email":
    send_email(data)
elif type == "sms":
    send_sms(data)
elif type == "push":
    send_push(data)

# Local 2: processamento (REPETIDO)
if type == "email":
    process_email(data)
elif type == "sms":
    process_sms(data)
elif type == "push":
    process_push(data)

# Local 3: validação (REPETIDO)
if type == "email":
    validate_email(data)
elif type == "sms":
    validate_sms(data)
elif type == "push":
    validate_push(data)
```

**Refatoração sugerida**:
```python
# handlers.py (NOVO)
class EmailHandler:
    def send(self, data):
        # enviar email
        pass

    def process(self, data):
        # processar email
        pass

    def validate(self, data):
        # validar email
        pass

class SMSHandler:
    def send(self, data):
        # enviar SMS
        pass

    def process(self, data):
        # processar SMS
        pass

    def validate(self, data):
        # validar SMS
        pass

class PushHandler:
    def send(self, data):
        # enviar push
        pass

    def process(self, data):
        # processar push
        pass

    def validate(self, data):
        # validar push
        pass

# Registry de handlers
HANDLERS = {
    "email": EmailHandler(),
    "sms": SMSHandler(),
    "push": PushHandler()
}

# Uso em todos os locais
def send_notification(type, data):
    handler = HANDLERS[type]
    handler.send(data)

def process_notification(type, data):
    handler = HANDLERS[type]
    handler.process(data)

def validate_notification(type, data):
    handler = HANDLERS[type]
    handler.validate(data)
```

**Impacto**:
✅ Elimina if/elif duplicado
✅ Facilita adicionar novos tipos
✅ Mais extensível e testável

---

## Checklist de Análise

Quando modificar código, verificar:

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

---

## Regra de Ouro

**Refatore APENAS quando**:
1. ✅ Padrão ocorre 3+ vezes (Regra dos 3)
2. ✅ Custo < Benefício (refatoração compensa)
3. ✅ Código "viveu" o suficiente (10+ incrementos)
4. ✅ Elimina duplicação significativa (10+ linhas)

**NÃO refatore quando**:
1. ❌ 1-2 ocorrências (pode ser coincidência)
2. ❌ Código muito novo (padrões não emergiram)
3. ❌ Custo muito alto vs ganho pequeno
4. ❌ Refatoração muito complexa
