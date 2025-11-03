# YAGNI Enforcer - Padrões Detalhados

Exemplos de YAGNI violations e alternativas simples.

## Padrão 1: Abstração Prematura

### ❌ Violação: Classe Abstrata com 1 Implementação

````python

# YAGNI VIOLATION
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self):
        pass

class EmailProcessor(AbstractProcessor):  # ÚNICA implementação!
    def process(self):
        # lógica de email
        pass

```text

**Por que é YAGNI?**
- Abstração sem necessidade (apenas 1 classe)
- Adiciona complexidade sem benefício
- Viola "Não Abstraia Prematuramente"

### ✅ Alternativa Simples

```python
def process_email(data):
    # lógica direta
    pass

# Quando aparecer 3ª tipo (SMS, Push), ENTÃO refatore para classe

```text


## Padrão 2: Antecipação de Futuro

### ❌ Violação: Parâmetros Não Usados

```python

# YAGNI VIOLATION
def process_email(email, retry=3, timeout=30, async_mode=False):
    # retry, timeout, async_mode NÃO são usados!
    send(email)

```text

**Por que é YAGNI?**
- Parâmetros não usados = over-engineering
- "Caso precise" = preparando para futuro hipotético
- Aumenta complexidade sem valor imediato

### ✅ Alternativa Simples

```python
def process_email(email):
    send(email)

# QUANDO precisar de retry (depois de ter falhas):
def process_email(email, retry=3):
    for attempt in range(retry):
        try:
            return send(email)
        except Exception:
            if attempt == retry - 1:
                raise

```text


## Padrão 3: Over-Configuration

### ❌ Violação: ConfigManager para 3 Configs

```python

# YAGNI VIOLATION
class ConfigurationManager:
    def __init__(self):
        self.config = {}
        self.validators = []

    def load_from_yaml(self):
        # carregar YAML
        pass

    def validate_schema(self):
        # validar schema
        pass

    def notify_observers(self):
        # notificar observadores
        pass

    # 150+ linhas para 3 valores!

```text

**Por que é YAGNI?**
- 150 linhas para gerenciar 3 valores
- Complexidade desproporcional
- Dict simples seria suficiente

### ✅ Alternativa Simples

```python
CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "debug": False
}

# Uso
timeout = CONFIG["timeout"]

# QUANDO tiver 10+ configs e necessidade real:

# ENTÃO considerar ConfigurationManager

```text


## Padrão 4: Factory Desnecessário

### ❌ Violação: Factory com 1 Produto

```python

# YAGNI VIOLATION
class ProcessorFactory:
    def create_processor(self, type):
        if type == "email":
            return EmailProcessor()  # ÚNICO tipo!

processor = factory.create_processor("email")

```text

**Por que é YAGNI?**
- Factory para 1 tipo = over-engineering
- Adiciona indireção sem benefício
- Código mais complexo

### ✅ Alternativa Simples

```python
processor = EmailProcessor()  # Criação direta!

# QUANDO tiver 3+ tipos (Email, SMS, Push):

# ENTÃO refatore para Factory ou Dictionary dispatch

```text


## Padrão 5: Patterns Forçados

### ❌ Violação: Singleton para Função Stateless

```python

# YAGNI VIOLATION
class EmailSender:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def send(self, email):
        # função stateless - não precisa singleton!
        pass

sender = EmailSender()
sender.send(email)

```text

**Por que é YAGNI?**
- Singleton para objeto stateless (desnecessário)
- Padrão forçado
- Função seria mais simples

### ✅ Alternativa Simples

```python
def send_email(email):
    # função direta
    pass

send_email(email)

```text


## Padrão 6: Hierarquias Complexas Prematuras

### ❌ Violação: Interface → Abstract → Concrete

```python

# YAGNI VIOLATION
class IProcessor(ABC):
    @abstractmethod
    def process(self):
        pass

class BaseProcessor(IProcessor):
    def preprocess(self):
        pass

    def postprocess(self):
        pass

class EmailProcessor(BaseProcessor):
    def process(self):
        pass

# Apenas 1 implementação concreta!

```text

**Por que é YAGNI?**
- Múltiplos níveis (Interface → Abstract → Concrete)
- Apenas 1 implementação concreta
- Complexidade sem benefício

### ✅ Alternativa Simples

```python
class EmailProcessor:
    def process(self):
        pass

# Refatore para hierarquia quando tiver 3+ tipos

```text


## Checklist de Detecção

Ao implementar código, verificar:

```text

[ ] Estou criando classe abstrata?
    ├─ Tenho 3+ implementações concretas PLANEJADAS? NÃO → ⚠️
    └─ Requisito claro de extensibilidade? NÃO → ⚠️

[ ] Estou usando design pattern?
    ├─ Tenho 3+ casos de uso REAIS? NÃO → ⚠️
    └─ Pattern simplifica código? NÃO → ⚠️

[ ] Estou adicionando parâmetros?
    ├─ Todos são usados AGORA? NÃO → ⚠️
    └─ Requisito concreto? NÃO → ⚠️

[ ] Estou "preparando para o futuro"?
    ├─ "Pode ser útil depois"? → ⚠️ YAGNI
    ├─ "Deixar flexível"? → ⚠️ YAGNI
    └─ Requisito explícito? SIM → OK

[ ] Estou criando configuração?
    ├─ São 10+ valores? NÃO → Dict simples
    └─ Complexa sem razão? → ⚠️ YAGNI

```text


## Regra de Ouro: "Regra dos 3"

**Padrão YAGNI**:
- 1 ocorrência → não abstrair
- 2 ocorrências → anotar, observar
- **3+ ocorrências → ENTÃO refatore/abstraia**

Não abstraia para futuro, abstraia quando padrão realmente emergir.


## Lembrete Final

```text

Simples > Complexo SEMPRE
Funcionando > Elegante
Agora > Futuro
MVP > Overengineered
Delete > Refactor

```text

Se você não usa AGORA, não adicione. Padrão emergirá naturalmente.
````
