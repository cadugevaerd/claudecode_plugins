---
description: Adicionar próxima funcionalidade incremental ao código existente seguindo YAGNI
---

# Add Increment

Este comando orienta a adição de uma ÚNICA funcionalidade incremental ao código existente, garantindo que apenas o necessário seja implementado.

## 🎯 Objetivo

Adicionar a próxima funcionalidade de forma MÍNIMA e INCREMENTAL, evitando antecipar requisitos futuros.

## 📋 Como usar

```
/add-increment "descrição da funcionalidade"
```

## 🔍 Processo de Execução

Quando este comando for executado, você DEVE:

### 1. Analisar Estado Atual

Antes de adicionar qualquer coisa:

```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- Funcionalidades existentes: [listar]
- Arquivos principais: [listar]
- Complexidade atual: [simples/moderada/complexa]

📝 Novo Requisito: [descrição fornecida]

Analisando...
```

### 2. Definir Incremento Mínimo

Identificar a MENOR mudança possível:

```
✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] Mudança 1 (mínima e necessária)
- [ ] Mudança 2 (mínima e necessária)
- [ ] Mudança 3 (mínima e necessária)

Onde adicionar:
- Arquivo: [nome do arquivo]
- Função/Classe: [onde modificar]
- Linhas aproximadas: [contexto]

❌ NÃO ADICIONAR AGORA (YAGNI):
- Feature relacionada mas não pedida
- Validação excessiva
- Abstração prematura
- Tratamento de erros elaborado
- Configuração complexa
- Cache/otimização

💡 Princípio: Adicione APENAS o que foi pedido

Implementar este incremento? (s/n)
```

### 3. Questionar Necessidade

**SEMPRE perguntar**:
- "Esta funcionalidade é realmente necessária AGORA?"
- "Existe um caso de uso REAL para isso?"
- "O que acontece se não implementarmos isso agora?"

### 4. Validar Impacto

Avaliar impacto da mudança:

```
📊 IMPACTO DO INCREMENTO:

Complexidade: [Baixa/Média/Alta]

Arquivos afetados:
- [arquivo1]: [tipo de mudança]
- [arquivo2]: [tipo de mudança]

Testes necessários:
- [ ] Teste 1 (caso básico)
- [ ] Teste 2 (edge case mínimo)

⚠️  Refatoração necessária? [SIM/NÃO]

Se SIM: Este é o momento de refatorar porque [padrão emergiu / duplicação clara / etc]
Se NÃO: Adicione de forma direta no código atual
```

## 📚 Exemplos Práticos

### Exemplo 1: Adicionar Validação de Email

**Estado atual**: Sistema processa emails básicos (MVP funcionando)

**Requisito**: "Adicionar validação de email"

**Resposta correta**:
```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- MVP funciona: processa emails
- Arquivo principal: email_processor.py
- Função: process_email(email: str)

📝 Novo Requisito: Validação de email

✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] Função validate_email(email: str) -> bool
- [ ] Validação básica (contém "@")
- [ ] Chamar antes de processar

Código:
def validate_email(email: str) -> bool:
    return "@" in email  # Validação mínima!

def process_email(email: str):
    if not validate_email(email):
        return "erro: email inválido"
    # resto do processamento...

❌ NÃO ADICIONAR AGORA:
- Regex complexo de validação
- Verificar domínio DNS
- Múltiplos tipos de validação
- Classe EmailValidator
- Sistema de erros customizados
- Logging de validações

💡 Validação mínima funciona. Adicionar complexidade APENAS quando necessário.

Implementar? (s/n)
```

### Exemplo 2: Adicionar Retry em LangGraph

**Estado atual**: API LangGraph com 1 node funcionando (MVP)

**Requisito**: "Adicionar retry quando der erro"

**Resposta correta**:
```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- LangGraph com 1 node: process_node
- API endpoint: POST /process
- Sem tratamento de erro

📝 Novo Requisito: Retry quando der erro

✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] Try/except no node
- [ ] Retry simples (1 tentativa)
- [ ] Retornar erro se falhar

Código:
def process_node(state):
    try:
        result = do_processing(state)
        return {"result": result}
    except Exception as e:
        # Retry UMA vez
        try:
            result = do_processing(state)
            return {"result": result}
        except:
            return {"result": "erro", "error": str(e)}

❌ NÃO ADICIONAR AGORA:
- Biblioteca de retry (tenacity, backoff)
- Retry exponencial
- Configuração de max_retries
- Logging estruturado
- Métricas de falhas
- Dead letter queue
- Circuit breaker

💡 Retry simples resolve. Adicionar complexidade APENAS quando padrão emergir.

Implementar? (s/n)
```

### Exemplo 3: Adicionar Logging

**Estado atual**: Sistema funciona sem logs

**Requisito**: "Adicionar logging"

**Resposta correta**:
```
🔄 ADICIONAR INCREMENTO

📍 Estado Atual:
- Sistema funciona sem logs
- Difícil debugar problemas

📝 Novo Requisito: Logging

✅ INCREMENTO MÍNIMO:

O que adicionar:
- [ ] print() nos pontos críticos
- [ ] Logar entrada e saída

Código:
def process_email(email: str):
    print(f"Processing: {email}")  # Log simples!
    result = do_something(email)
    print(f"Result: {result}")
    return result

❌ NÃO ADICIONAR AGORA:
- Biblioteca logging configurada
- Múltiplos níveis (DEBUG, INFO, ERROR)
- Formatação estruturada (JSON)
- Rotação de logs
- Envio para serviço externo (Datadog, Sentry)
- Context managers
- Logging assíncrono

💡 print() funciona perfeitamente para começar. Trocar por logging quando necessário.

Implementar? (s/n)
```

## ⚠️ Detectar Over-Engineering no Incremento

Se você detectar estes padrões ao adicionar incremento, ALERTE:

### ❌ Padrão 1: Criar Classe para Função Simples

```python
# OVER-ENGINEERING ao adicionar validação
class EmailValidator:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def validate(self, email):
        for rule in self.rules:
            if not rule.check(email):
                return False
        return True

validator = EmailValidator()
validator.add_rule(HasAtSymbolRule())
```

**✅ Incremental correto**:
```python
def validate_email(email):
    return "@" in email  # Função simples!
```

---

### ❌ Padrão 2: Adicionar Configuração Complexa

```python
# OVER-ENGINEERING ao adicionar retry
config = {
    "retry": {
        "max_attempts": 3,
        "backoff": "exponential",
        "initial_delay": 1,
        "max_delay": 60,
        "exceptions": [NetworkError, TimeoutError]
    }
}
```

**✅ Incremental correto**:
```python
MAX_RETRIES = 1  # Constante simples!
```

---

### ❌ Padrão 3: Criar Abstração Prematura

```python
# OVER-ENGINEERING ao adicionar segundo processador
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self, data): pass

class EmailProcessor(AbstractProcessor):
    def process(self, data): ...

class SMSProcessor(AbstractProcessor):
    def process(self, data): ...
```

**✅ Incremental correto**:
```python
def process_email(email): ...
def process_sms(sms): ...  # Duas funções por enquanto!
```

**Quando criar abstração?**: Quando tiver 3+ processadores E padrão claro emergir.

## 🎯 Estratégia de Incremento

### 1. Regra dos 3
Espere ter **3 casos similares** antes de criar abstração:
- 1 caso: função direta
- 2 casos: duas funções (repetição OK!)
- 3 casos: AGORA abstrair (padrão emergiu)

### 2. Add, Don't Modify (quando possível)
Prefira adicionar código novo a modificar existente:
- Menos risco de quebrar
- Fácil de reverter
- Padrão fica mais claro

### 3. Test After Each Increment
Após cada incremento:
```
✅ CHECKLIST PÓS-INCREMENTO:
- [ ] Código compilou/executou sem erro
- [ ] Funcionalidade funciona (teste manual)
- [ ] Código antigo ainda funciona
- [ ] Commit do incremento
```

## 🚀 Fluxo de Incremento

```
1. /add-increment "nova feature"
   ↓
2. Analisar estado atual
   ↓
3. Definir incremento MÍNIMO
   ↓
4. Questionar necessidade
   ↓
5. Implementar (código simples)
   ↓
6. Testar incremento
   ↓
7. Commit
   ↓
8. Próximo incremento OU refatorar (se padrão emergiu)
```

## 💡 Princípios do Incremento

1. **Um incremento por vez**: Não adicionar múltiplas features juntas
2. **Simples primeiro**: Código direto antes de abstrações
3. **Funcionar > Perfeição**: Incremente funciona > Código "bonito"
4. **Reversível**: Incremento pequeno é fácil de reverter
5. **Testável**: Incremente pequeno é fácil de testar

## 🔄 Quando Refatorar?

**NÃO refatore durante incremento** a menos que:
- ✅ Padrão claro emergiu (3+ casos similares)
- ✅ Duplicação óbvia (copy-paste exato)
- ✅ Código impossível de adicionar incremento sem refatorar

**Use** `/refactor-now` após alguns incrementos, não durante.

## ⚡ Lembre-se

- Incremento = MÍNIMO necessário
- Simplicidade > Elegância
- Funcionar > Padrões
- Agora > Futuro
- Adicione apenas o que foi PEDIDO
- Refatore depois, não durante