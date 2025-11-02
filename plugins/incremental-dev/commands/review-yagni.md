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

**Para projetos com git history**:
```
🔍 ANÁLISE GIT BLAME (Projeto Legacy)

Analisando histórico de commits para entender quando
código foi adicionado e se ainda está em uso:

- Código antigo (>6 meses) sem alterações → Pode estar obsoleto
- Abstrações adicionadas recentemente → Possivelmente prematura
- Código nunca referenciado em commits recentes → Candidato à remoção

Executando git blame em arquivos suspeitos...
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
📅 Adicionado: 3 meses atrás (git blame)
👤 Por: dev@example.com
💬 Commit: "add factory for future processors"

Código atual:
class AbstractProcessorFactory:
    def create_processor(self, type):
        if type == "email":
            return EmailProcessor()
        # Apenas 1 tipo usado!

# Usado apenas em:
processor = factory.create_processor("email")

💡 YAGNI: Factory com 1 produto é over-engineering
⚠️  "future processors" nunca foram adicionados (3 meses)

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

> **📘 Complete Reference**: See `docs/YAGNI_REFERENCE.md` for comprehensive list of over-engineering patterns, anti-patterns, and simplification strategies.

### Quick Reference - Common Patterns:

**🚨 Categoria 1: Abstrações Prematuras**
- Abstract class with 1 implementation → Use direct function
- Interface for 1-2 implementations → Use simple functions
- Factory without variation → Use direct instantiation

**🚨 Categoria 2: Configuração Excessiva**
- ConfigurationManager for < 10 values → Use dict/constants
- Environment variables wrapper class → Use direct os.getenv

**🚨 Categoria 3: Patterns Desnecessários**
- Singleton for stateless object → Use function
- Observer Pattern without dynamic switching → Use direct call
- Strategy Pattern without runtime variation → Use simple implementation

**🚨 Categoria 4: Código Não Utilizado**
- Functions/classes never called → DELETE
- Unused parameters → REMOVE
- Unused imports → DELETE

**For detailed examples and code snippets**, refer to `docs/YAGNI_REFERENCE.md`.

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

> **📘 Complete Guide**: See `docs/YAGNI_REFERENCE.md` sections:
> - "Simplification Strategies" - Detailed refactoring patterns
> - "Core YAGNI Principles" - Fundamental guidelines

### Quick Reference:

1. **Replace Class with Function** - When class is stateless
2. **Inline Complex Abstraction** - When abstraction used only once
3. **Replace Configuration Class with Constants** - For < 10 config values
4. **Remove Unused Code** - Delete code not called

**For code examples**, see `docs/YAGNI_REFERENCE.md`.

## 💡 Princípios YAGNI

> **📘 Core Principles**: Full list in `docs/YAGNI_REFERENCE.md`

Quick mantras:
- **Delete > Refactor** - Delete unused code, don't improve it
- **Simple > Elegant** - Simple code > "Well-architected" code
- **Direct > Abstract** - Direct call > Complex abstraction
- **Now > Future** - Solve current problem, not hypothetical
- **Measure Use** - Unused 3+ months = probably unnecessary

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