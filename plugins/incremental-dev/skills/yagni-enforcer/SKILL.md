---
name: yagni-enforcer
description: Detecta automaticamente quando código está sendo criado "para o futuro" ou tem complexidade desnecessária. Use quando implementar funcionalidades, criar classes/abstrações, ou adicionar configurações. Detecta over-engineering, abstrações prematuras, e antecipação de requisitos futuros.
allowed-tools: Read, Grep, Glob
---

# YAGNI Enforcer

Sou uma skill que detecta automaticamente quando você (Claude) está prestes a criar código complexo desnecessário, abstrações prematuras, ou funcionalidades antecipadas que violam o princípio YAGNI (You Aren't Gonna Need It).

## 🎯 Quando Sou Invocado

Você (Claude) DEVE me invocar automaticamente quando:

1. **Criar classes abstratas** - "Vou criar AbstractX..."
2. **Implementar patterns** - "Usando Factory/Strategy/Observer..."
3. **Adicionar configuração complexa** - "ConfigManager para..."
4. **Antecipar funcionalidades** - "Para facilitar no futuro..."
5. **Criar múltiplos níveis de abstração** - "Interface → Abstract → Concrete"
6. **Implementar features não pedidas** - "Vou adicionar também..."

## 🔍 O Que Detecto

### ⚠️ Padrão 1: Abstração Prematura

**Detectar quando**:
- Classe abstrata com 1 implementação
- Interface para 1-2 implementações
- Hierarquia complexa sem justificativa
- Pattern design sem 3+ casos de uso

**Exemplo detectado**:
```python
# ⚠️ OVER-ENGINEERING
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):  # Única implementação!
    def process(self): ...
```

**Alerta a emitir**:
```
⚠️  YAGNI VIOLATION: Abstração Prematura

Detectei: AbstractProcessor com 1 implementação

❌ Problema:
- Abstração sem necessidade (apenas 1 classe)
- Complexidade desnecessária
- Viola princípio YAGNI

✅ Alternativa simples:
def process_email(data):  # Função direta!
    ...

💡 Regra: Abstraia quando tiver 3+ implementações, não antes
```

### ⚠️ Padrão 2: Antecipação de Futuro

**Detectar quando**:
- Comentários "para o futuro"
- Parâmetros não usados "caso precise"
- Configurações para features não implementadas
- Código preparando para "expansão futura"

**Exemplo detectado**:
```python
# ⚠️ OVER-ENGINEERING
def process_email(email, retry=3, timeout=30, async_mode=False):
    # retry, timeout, async_mode não usados ainda!
    send(email)
```

**Alerta a emitir**:
```
⚠️  YAGNI VIOLATION: Antecipação de Futuro

Detectei: Parâmetros não utilizados

❌ Problema:
- retry, timeout, async_mode não usados no código
- Preparando para futuro hipotético
- Aumenta complexidade sem benefício

✅ Alternativa simples:
def process_email(email):  # Apenas o necessário!
    send(email)

💡 Adicione parâmetros QUANDO precisar, não antes
```

### ⚠️ Padrão 3: Over-Configuration

**Detectar quando**:
- ConfigurationManager para < 10 configs
- Sistema elaborado para valores simples
- Validação complexa de configuração
- Observer pattern para config changes

**Exemplo detectado**:
```python
# ⚠️ OVER-ENGINEERING
class ConfigurationManager:
    def __init__(self):
        self.config = {}
        self.validators = []

    def load_from_yaml(self): ...
    def validate_schema(self): ...
    def notify_observers(self): ...
    # 150+ linhas para 3 configs!
```

**Alerta a emitir**:
```
⚠️  YAGNI VIOLATION: Over-Configuration

Detectei: ConfigurationManager complexo

❌ Problema:
- 150+ linhas para gerenciar 3 valores
- Complexidade desproporcional
- Sistema elaborado sem necessidade

✅ Alternativa simples:
CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "debug": False
}

💡 Dict simples é suficiente para < 10 configurações
```

### ⚠️ Padrão 4: Factory Desnecessário

**Detectar quando**:
- Factory criando apenas 1 tipo
- Factory sem variação runtime
- Factory com if/elif simples

**Exemplo detectado**:
```python
# ⚠️ OVER-ENGINEERING
class ProcessorFactory:
    def create_processor(self, type):
        if type == "email":
            return EmailProcessor()  # Apenas 1 tipo!
```

**Alerta a emitir**:
```
⚠️  YAGNI VIOLATION: Factory Desnecessário

Detectei: Factory criando 1 tipo

❌ Problema:
- Factory para 1 produto = over-engineering
- Adiciona camada sem benefício
- Código mais complexo sem motivo

✅ Alternativa simples:
processor = EmailProcessor()  # Criação direta!

💡 Factory faz sentido com 3+ tipos, não com 1
```

### ⚠️ Padrão 5: Patterns Desnecessários

**Detectar quando**:
- Singleton para objeto stateless
- Observer sem necessidade de notificação
- Strategy sem variação runtime
- Template Method para 1-2 classes

**Exemplo detectado**:
```python
# ⚠️ OVER-ENGINEERING
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def send_email(self, email):
        # Função stateless - não precisa singleton!
```

**Alerta a emitir**:
```
⚠️  YAGNI VIOLATION: Pattern Desnecessário

Detectei: Singleton para função stateless

❌ Problema:
- Singleton sem necessidade (sem estado)
- Complexidade desnecessária
- Pattern forçado

✅ Alternativa simples:
def send_email(email):  # Função direta!
    ...

💡 Singleton faz sentido para estado compartilhado, não funções
```

## 📋 Instructions

Quando você (Claude) for implementar qualquer código, SEMPRE execute este checklist mental:

### Checklist de Detecção

```
[ ] Estou criando classe abstrata?
    → Tenho 3+ implementações? NÃO → ⚠️ ALERTA

[ ] Estou usando design pattern?
    → Tenho 3+ casos de uso? NÃO → ⚠️ ALERTA

[ ] Estou adicionando configuração?
    → São 10+ valores? NÃO → ⚠️ ALERTA (use dict)

[ ] Estou criando factory?
    → Crio 3+ tipos diferentes? NÃO → ⚠️ ALERTA

[ ] Estou adicionando parâmetros?
    → Todos serão usados AGORA? NÃO → ⚠️ ALERTA

[ ] Estou "preparando para o futuro"?
    → Requisito concreto AGORA? NÃO → ⚠️ ALERTA

[ ] Estou criando hierarquia de classes?
    → Realmente necessária? NÃO → ⚠️ ALERTA
```

### Fluxo de Detecção

```
1. Claude vai implementar código
   ↓
2. YAGNI Enforcer analisa intenção
   ↓
3. Detecta pattern suspeito?
   │
   ├─ NÃO → Prosseguir normalmente
   │
   └─ SIM → Emitir alerta ⚠️
       ↓
       Mostrar:
       - O que foi detectado
       - Por que é YAGNI violation
       - Alternativa mais simples
       ↓
       Perguntar ao usuário:
       "Implementar versão simples? (s/n)"
```

## 🎯 Gatilhos de Detecção

Termos que devem ativar análise YAGNI:

### 🚨 Gatilhos de Linguagem

**Frases suspeitas**:
- "para o futuro"
- "caso precise"
- "para facilitar expansão"
- "seguindo clean architecture"
- "preparar para"
- "pode ser útil"
- "deixar flexível"
- "para reutilização"

**Ações suspeitas**:
- Criar Abstract/Interface
- Implementar Factory/Strategy/Observer
- Adicionar ConfigurationManager
- Criar hierarquia profunda
- Adicionar parâmetros não usados
- Comentários "TODO: adicionar X no futuro"

## 📊 Níveis de Alerta

### 🔴 CRÍTICO - Bloqueie Implementação

Violação grave de YAGNI:
- Abstração com 0 implementações concretas
- Factory sem produtos
- Pattern sem caso de uso

**Ação**: Não implementar, sugerir alternativa simples

### 🟡 MODERADO - Aviso Forte

Provável over-engineering:
- Abstração com 1 implementação
- Configuração complexa para poucos valores
- Pattern com apenas 2 casos

**Ação**: Alertar fortemente, sugerir simplificação

### 🟢 LEVE - Sugestão

Possível simplificação:
- Parâmetro opcional não usado ainda
- Estrutura que pode ser mais simples

**Ação**: Sugerir alternativa mais simples

## 💡 Exemplos de Invocação

### Exemplo 1: Detectar Abstração Prematura

```
Claude: "Vou criar uma classe AbstractProcessor para facilitar adicionar
novos processadores no futuro"

YAGNI Enforcer (ATIVADO AUTOMATICAMENTE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  YAGNI VIOLATION DETECTADA

Tipo: Abstração Prematura
Severidade: 🟡 MODERADO

❌ Problema:
Você está criando AbstractProcessor mas:
- Não há requisito de múltiplos processadores AGORA
- Está antecipando necessidade futura
- Adiciona complexidade sem benefício imediato

Código proposto:
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass

class EmailProcessor(AbstractProcessor):
    def process(self): ...

✅ Alternativa YAGNI:
def process_email(data):  # Função direta!
    ...

💡 Princípio: Adicione abstração quando tiver 3+ tipos, não antes

Implementar versão simples? (s/n)
```

### Exemplo 2: Detectar Over-Configuration

```
Claude: "Vou criar um ConfigurationManager para gerenciar as 3 configurações"

YAGNI Enforcer (ATIVADO AUTOMATICAMENTE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  YAGNI VIOLATION DETECTADA

Tipo: Over-Configuration
Severidade: 🟡 MODERADO

❌ Problema:
Você está criando ConfigurationManager mas:
- Apenas 3 configurações
- Complexidade desproporcional
- Dict simples seria suficiente

Código proposto:
class ConfigurationManager:
    def load_from_yaml(self): ...
    def validate(self): ...
    # Dezenas de linhas...

✅ Alternativa YAGNI:
CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "debug": False
}

💡 Use ConfigurationManager quando tiver 10+ configs, não 3

Implementar versão simples? (s/n)
```

### Exemplo 3: Detectar Antecipação de Futuro

```
Claude: "Vou adicionar parâmetros de retry e timeout para quando precisar"

YAGNI Enforcer (ATIVADO AUTOMATICAMENTE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  YAGNI VIOLATION DETECTADA

Tipo: Antecipação de Futuro
Severidade: 🟡 MODERADO

❌ Problema:
Você está adicionando retry e timeout mas:
- Não há requisito AGORA
- Parâmetros não serão usados
- "Para quando precisar" = YAGNI violation

Código proposto:
def process_email(email, retry=3, timeout=30):
    send(email)  # retry/timeout não usados!

✅ Alternativa YAGNI:
def process_email(email):
    send(email)  # Apenas o necessário

💡 Adicione retry quando PRECISAR (após ter problemas de falha)

Implementar versão simples? (s/n)
```

## 🎓 Regras de Ouro

Aplique estas regras na detecção:

1. **Regra dos 3**: Abstraia apenas com 3+ casos
2. **Se não usa AGORA, não adicione**: YAGNI puro
3. **Simples > Complexo**: Sempre preferir simplicidade
4. **Funcionar > Elegante**: MVP funcional > código "bonito"
5. **Delete > Refactor**: Se não é necessário, não adicione

## ⚡ Lembre-se

Como skill automática:
- ✅ Sou invocado automaticamente por Claude
- ✅ Analiso código ANTES de implementar
- ✅ Emito alertas quando detectar YAGNI violations
- ✅ Sugiro alternativas mais simples
- ❌ NÃO implemento código (apenas alerto)
- ❌ NÃO bloqueio totalmente (usuário decide final)

**Meu valor**: Prevenir over-engineering ANTES que aconteça, mantendo código simples e focado no problema atual.

---

**Quando Claude deve me invocar**:
- Antes de criar classes abstratas
- Antes de implementar design patterns
- Antes de adicionar configuração complexa
- Quando adicionar "para o futuro"
- Ao criar hierarquias de classes
- Quando antecipar requisitos

**Objetivo**: Manter desenvolvimento INCREMENTAL e SIMPLES, sem complexidade prematura.