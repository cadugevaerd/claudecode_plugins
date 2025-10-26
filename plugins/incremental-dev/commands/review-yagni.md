---
description: Revisar código identificando e removendo over-engineering seguindo princípio YAGNI
---

# Review YAGNI

Este comando analisa código existente identificando complexidade desnecessária, abstrações prematuras e funcionalidades não utilizadas que podem ser simplificadas ou removidas.

## 🎯 Objetivo

Identificar e simplificar código seguindo YAGNI (You Aren't Gonna Need It), removendo over-engineering acumulado.

## 📋 Como usar

```
/review-yagni
```

OU revisar arquivo/módulo específico:

```
/review-yagni "caminho/do/arquivo.py"
```

## 🔍 Processo de Execução

Quando este comando for executado, você DEVE:

### 1. Escanear Codebase

Analisar arquivos identificando sinais de over-engineering:

```
⚠️  REVISÃO YAGNI - PROCURANDO OVER-ENGINEERING

📂 Escaneando arquivos:
- [arquivo1] ... ✅ OK
- [arquivo2] ... ⚠️  Complexidade suspeita
- [arquivo3] ... ✅ OK
- [arquivo4] ... ⚠️  Abstração desnecessária
- [arquivo5] ... ⚠️  Código não utilizado

Analisando...
```

### 2. Detectar Anti-Patterns

Identificar padrões comuns de over-engineering:

```
🚨 OVER-ENGINEERING DETECTADO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ⚠️  Abstração Prematura
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Arquivo: processors/base.py
Problema: AbstractProcessorFactory usado apenas 1 vez

Código atual:
class AbstractProcessorFactory:
    def create_processor(self, type):
        if type == "email":
            return EmailProcessor()
        # Apenas 1 tipo usado!

# Usado apenas em:
processor = factory.create_processor("email")

💡 YAGNI: Factory com 1 produto é over-engineering

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. ⚠️  Configuração Excessiva
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Arquivo: config/manager.py
Problema: 200 linhas para gerenciar 2 configurações

Código atual:
class ConfigurationManager:
    def __init__(self):
        self.config = {}
        self.validators = []
        self.observers = []

    def load_from_yaml(self): ...
    def validate_schema(self): ...
    def notify_observers(self): ...
    # 200 linhas...

# Usado apenas para:
MAX_RETRIES = config.get("max_retries")
TIMEOUT = config.get("timeout")

💡 YAGNI: Dict simples seria suficiente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. ⚠️  Pattern Desnecessário
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Arquivo: validators/email.py
Problema: Strategy Pattern sem necessidade

Código atual:
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data): pass

class EmailValidationStrategy(ValidationStrategy):
    def validate(self, email):
        return "@" in email

class PhoneValidationStrategy(ValidationStrategy):
    def validate(self, phone):
        return len(phone) == 10

# Apenas 2 estratégias, nunca trocadas em runtime

💡 YAGNI: Funções simples são suficientes
```

### 3. Sugerir Simplificações

Para cada problema detectado:

```
✅ SIMPLIFICAÇÕES SUGERIDAS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Remover AbstractProcessorFactory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antes (15 linhas):
class AbstractProcessorFactory:
    def create_processor(self, type):
        if type == "email":
            return EmailProcessor()

factory = AbstractProcessorFactory()
processor = factory.create_processor("email")

Depois (1 linha):
processor = EmailProcessor()  # Direto!

Impacto:
- Remove arquivo base.py (15 linhas)
- Código mais direto
- Sem complexidade desnecessária

Simplificar? (s/n)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. Substituir ConfigurationManager por dict
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antes (200 linhas):
class ConfigurationManager:
    # ... 200 linhas ...

config = ConfigurationManager()
config.load_from_yaml("config.yaml")
MAX_RETRIES = config.get("max_retries")

Depois (3 linhas):
CONFIG = {
    "max_retries": 3,
    "timeout": 30
}

Impacto:
- Remove arquivo manager.py (200 linhas!)
- Config clara e simples
- Fácil de modificar

Simplificar? (s/n)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. Remover Strategy Pattern
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antes (30 linhas):
class ValidationStrategy(ABC): ...
class EmailValidationStrategy(ValidationStrategy): ...
class PhoneValidationStrategy(ValidationStrategy): ...

validator = EmailValidationStrategy()
if validator.validate(email):
    ...

Depois (6 linhas):
def validate_email(email):
    return "@" in email

def validate_phone(phone):
    return len(phone) == 10

if validate_email(email):
    ...

Impacto:
- Remove arquivo strategy.py (30 linhas)
- Funções simples e diretas
- Sem hierarquia desnecessária

Simplificar? (s/n)
```

## 📚 Sinais de Over-Engineering

### 🚨 Categoria 1: Abstrações Prematuras

**Detectar**:

❌ **Classe abstrata com 1 implementação**
```python
class AbstractProcessor(ABC):  # ← Desnecessário!
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):  # Única implementação
    def process(self): ...
```

✅ **Simplificar para**:
```python
def process_email(data):  # Função direta
    ...
```

---

❌ **Interface para 1-2 implementações**
```python
class IValidator(Protocol):  # ← Over-engineering
    def validate(self, data) -> bool: ...

# Apenas 2 implementações
```

✅ **Simplificar para**:
```python
def validate_email(email): ...
def validate_phone(phone): ...
```

---

❌ **Factory sem variação**
```python
class ProcessorFactory:  # ← Desnecessário
    def create(self):
        return EmailProcessor()  # Sempre retorna o mesmo!
```

✅ **Simplificar para**:
```python
processor = EmailProcessor()  # Direto!
```

### 🚨 Categoria 2: Configuração Excessiva

**Detectar**:

❌ **ConfigurationManager complexo**
```python
class ConfigurationManager:
    def __init__(self):
        self.config = {}

    def load_from_yaml(self, path):
        # 50 linhas carregando YAML

    def validate_schema(self):
        # 30 linhas validando

    def get(self, key, default=None):
        # 20 linhas com cache/observers

    # Total: 150+ linhas para 3 configs!
```

✅ **Simplificar para**:
```python
CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "debug": False
}
```

---

❌ **Environment variables com classe gerenciadora**
```python
class EnvManager:
    def get_api_key(self):
        return os.getenv("API_KEY")

    def get_timeout(self):
        return int(os.getenv("TIMEOUT", "30"))

    # 10+ métodos para envs
```

✅ **Simplificar para**:
```python
API_KEY = os.getenv("API_KEY")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
```

### 🚨 Categoria 3: Patterns Desnecessários

**Detectar**:

❌ **Singleton para objeto stateless**
```python
class EmailSender:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def send(self, email):
        # Função stateless - não precisa singleton!
```

✅ **Simplificar para**:
```python
def send_email(email):
    # Função simples!
```

---

❌ **Observer Pattern sem necessidade**
```python
class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer): ...
    def notify(self): ...

class ConcreteObserver:
    def update(self): ...

# Usado apenas em 1 lugar, sem troca dinâmica
```

✅ **Simplificar para**:
```python
def on_event_happened():
    handle_event()  # Chamada direta!
```

---

❌ **Strategy Pattern sem variação runtime**
```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

class QuickSort(SortStrategy): ...
class MergeSort(SortStrategy): ...

# Sempre usa QuickSort, nunca troca
sorter = QuickSort()
```

✅ **Simplificar para**:
```python
data.sort()  # Usa default do Python!
```

### 🚨 Categoria 4: Código Não Utilizado

**Detectar**:

❌ **Funções/classes nunca chamadas**
```python
# Buscar no codebase:
# - Definição existe
# - Nenhuma chamada encontrada

class LegacyProcessor:  # ← Ninguém usa
    def process(self): ...
```

✅ **Ação**:
```
REMOVER completamente
```

---

❌ **Parâmetros não utilizados**
```python
def process_email(email, retry=3, timeout=30, debug=False):
    # retry, timeout, debug nunca usados no código
    send(email)
```

✅ **Simplificar para**:
```python
def process_email(email):
    send(email)
```

---

❌ **Imports não usados**
```python
import requests  # ← Não usado
from typing import Dict, List, Optional  # ← Apenas Dict usado
```

✅ **Simplificar para**:
```python
from typing import Dict
```

## 📊 Análise de Complexidade

Para cada arquivo, calcular:

```
📊 MÉTRICAS DE COMPLEXIDADE

Arquivo: email_processor.py
├─ Linhas: 250
├─ Classes: 5
├─ Funções: 15
├─ Complexidade Ciclomática: 45
├─ Abstrações: 3 (AbstractX, FactoryY, StrategyZ)
└─ Uso real: 30% do código

⚠️  SINAIS DE OVER-ENGINEERING:
1. Apenas 30% do código usado
2. 3 abstrações para funcionalidade simples
3. Complexidade alta (45) para tarefa básica

💡 RECOMENDAÇÃO: Simplificar drasticamente
```

## 📝 Checklist de Revisão

### Para cada arquivo:

```
✅ CHECKLIST DE REVISÃO YAGNI

[ ] Classes abstratas têm 3+ implementações?
    ❌ Menos de 3 → REMOVER abstração

[ ] Factory cria 3+ tipos diferentes?
    ❌ Apenas 1-2 → USAR criação direta

[ ] Pattern usado em 3+ contextos?
    ❌ Apenas 1-2 → SIMPLIFICAR para função

[ ] Configuração gerencia 10+ valores?
    ❌ Menos de 10 → USAR dict/constantes

[ ] Função tem 3+ parâmetros usados?
    ❌ Parâmetros não usados → REMOVER

[ ] Classe tem estado que varia?
    ❌ Stateless → USAR função

[ ] Código foi usado nos últimos 3 meses?
    ❌ Não usado → DELETAR

[ ] Complexidade justificada por requisito real?
    ❌ Complexidade antecipada → SIMPLIFICAR
```

## 🎯 Estratégias de Simplificação

### 1. Replace Class with Function

**Quando**: Classe sem estado (stateless)

```python
# Antes
class EmailValidator:
    def validate(self, email):
        return "@" in email

validator = EmailValidator()
result = validator.validate(email)

# Depois
def validate_email(email):
    return "@" in email

result = validate_email(email)
```

### 2. Inline Complex Abstraction

**Quando**: Abstração usada 1 vez

```python
# Antes
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):
    def process(self):
        return send_email()

processor = EmailProcessor()
result = processor.process()

# Depois
result = send_email()  # Direto!
```

### 3. Replace Configuration Class with Constants

**Quando**: Configuração simples (< 10 valores)

```python
# Antes (50 linhas)
class Config:
    def __init__(self):
        self._config = self._load()

    def _load(self):
        # complexidade...

    def get(self, key):
        # mais complexidade...

config = Config()
max_retries = config.get("max_retries")

# Depois (3 linhas)
MAX_RETRIES = 3
TIMEOUT = 30
```

### 4. Remove Unused Code

**Quando**: Código não chamado

```python
# Antes
class LegacyProcessor:  # Ninguém usa
    def process(self): ...

def old_function():  # Ninguém chama
    ...

# Depois
# [DELETADO]
```

## 💡 Princípios YAGNI

1. **Delete > Refactor**: Se não é usado, delete (não "melhore")
2. **Simple > Elegant**: Código simples > Código "bem arquitetado"
3. **Direct > Abstract**: Chamada direta > Abstração complexa
4. **Now > Future**: Resolva problema atual, não futuro hipotético
5. **Measure Use**: Se não é usado há 3+ meses, provavelmente não é necessário

## 📊 Relatório Final

Após análise completa:

```
═══════════════════════════════════════════
📊 RELATÓRIO YAGNI - RESULTADOS
═══════════════════════════════════════════

Arquivos analisados: 15

🚨 OVER-ENGINEERING DETECTADO:

1. Abstrações desnecessárias: 5
   - AbstractProcessor (1 uso)
   - ProcessorFactory (1 tipo)
   - ValidationStrategy (2 usos)
   - ConfigurationManager (3 configs)
   - SingletonManager (stateless)

2. Código não utilizado: 8 arquivos/funções
   - legacy_processor.py (não usado)
   - old_validator.py (não usado)
   - função helper_x() (não chamada)
   [...]

3. Configuração excessiva: 2
   - ConfigurationManager: 200 linhas → 10 linhas
   - EnvManager: 80 linhas → 5 linhas

✅ SIMPLIFICAÇÕES POSSÍVEIS:

- Remover: 450 linhas
- Simplificar: 300 linhas → 50 linhas
- Total: Redução de ~65% de código!

💡 IMPACTO ESPERADO:
- Código mais simples
- Menos bugs (menos código = menos bugs)
- Manutenção mais fácil
- Novos desenvolvedores entendem mais rápido

═══════════════════════════════════════════

Aplicar todas as simplificações? (s/n)
Ou revisar uma por uma? (r)
```

## 📄 Após Simplificação

Se simplificações significativas foram feitas:

```
✅ SIMPLIFICAÇÃO COMPLETA!

Código simplificado com sucesso.

Registrar aprendizado no PRD? (s/n)
```

**Se SIM**:
```
Adicionando à seção "Lições Aprendidas" do PRD:

📝 Retrospectiva - Simplificação YAGNI
**Data**: [data]
- **O que foi simplificado**:
  - [lista de simplificações]
- **Impacto**:
  - Linhas removidas: [N]
  - Complexidade reduzida: [%]
  - Manutenibilidade: Melhorada
- **Lição aprendida**:
  - [aprendizado sobre over-engineering detectado]

✅ Aprendizado registrado em docs/PRD.md
```

**Exemplos de lições aprendidas**:
- "Abstrações prematuras adicionaram complexidade sem benefício"
- "ConfigurationManager com 200 linhas era desnecessário - dict simples suficiente"
- "Padrões devem emergir, não serem planejados antecipadamente"

---

## ⚡ Lembre-se

- YAGNI = Delete código desnecessário
- Simples > Complexo
- Menos código = Menos bugs
- Abstrações devem emergir, não serem planejadas
- Se não é usado, provavelmente não é necessário
- Código "feio mas funcional" > Código "bonito mas complexo"
- Refatorar = Simplificar, não complicar
- **Registre aprendizados sobre over-engineering no PRD**