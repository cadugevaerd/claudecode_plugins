---
description: Iniciar desenvolvimento incremental definindo MVP mínimo e escopo da primeira iteração
---

# Start Incremental Development

Este comando inicia o processo de desenvolvimento incremental identificando o **Minimum Viable Product (MVP)** e definindo claramente o que FAZER e o que NÃO FAZER na primeira iteração.

## 🎯 Objetivo

Definir o menor escopo possível que entrega valor, evitando funcionalidades prematuras e over-engineering.

## 📋 Como usar

```
/start-incremental "descrição do objetivo geral"
```

## 🔍 Processo de Execução

Quando este comando for executado, você DEVE:

### 1. Verificar Existência do PRD

```
🔍 VERIFICANDO PRD...

Procurando docs/PRD.md...
```

**Se PRD NÃO existe**:
```
⚠️  PRD não encontrado

💡 Recomendação: Executar /setup-project-incremental primeiro
   Isso cria CLAUDE.md + PRD v0.1 com informações iniciais

Continuar sem PRD? (s/n)
```

**Se PRD existe**:
```
✅ PRD encontrado (versão [versão])

Consultando objetivos e MVP definidos no PRD...
```

Extrair do PRD:
- Objetivos do projeto
- MVP definido (se fase >= Planejamento)
- Funcionalidades fora do MVP (YAGNI)

---

### 2. Questionar o Objetivo

Perguntar ao usuário:
- Qual o problema REAL que precisa resolver AGORA?
- Quem é o usuário final?
- Qual a ação mínima que entrega valor?

**Se PRD existe**: Alinhar com objetivos documentados no PRD

### 2. Definir MVP (Iteração 1)

Identificar apenas o ESSENCIAL:

```
📦 DESENVOLVIMENTO INCREMENTAL - MVP

Objetivo: [descrição do objetivo]

🎯 MVP (Iteração 1):
- [ ] Funcionalidade 1 (mínima)
- [ ] Funcionalidade 2 (mínima)
- [ ] Funcionalidade 3 (mínima)

❌ NÃO FAZER AGORA (YAGNI):
- Feature prematura 1
- Feature prematura 2
- Abstração desnecessária
- Configuração complexa
- Validações avançadas
- Sistema de erros elaborado
- Logging sofisticado
- Cache/otimização prematura

💡 Princípio: Fazer o caso mais simples funcionar primeiro

Características do MVP:
• Sem abstrações (código direto)
• Sem patterns (adicionar quando padrões emergirem)
• Validações mínimas
• Configuração hardcoded OK para MVP
• Foco em FUNCIONAR, não em "código bonito"

Começar implementação? (s/n)
```

### 3. Aplicar Princípios YAGNI

**SEMPRE questionar**:
- "Você precisa disso AGORA?"
- "O que acontece se não implementar isso?"
- "Isso resolve o problema mínimo?"

**Evitar frases como**:
- ❌ "Vamos preparar para o futuro..."
- ❌ "Caso precise adicionar..."
- ❌ "Para facilitar expansão..."
- ❌ "Seguindo clean architecture..."

**Preferir frases como**:
- ✅ "Vamos fazer funcionar primeiro"
- ✅ "Podemos adicionar isso quando necessário"
- ✅ "Foco no caso de uso atual"
- ✅ "Refatoramos quando o padrão emergir"

## 📚 Exemplos Práticos

### Exemplo 1: Sistema de Processamento de Emails

**Objetivo do usuário**: "Criar sistema de processamento de emails com validação, fila e logging"

**Resposta correta do MVP**:
```
📦 MVP - PROCESSAMENTO DE EMAIL

🎯 MVP (Iteração 1):
- [ ] Receber um email (string)
- [ ] Processar (função process_email simples)
- [ ] Retornar "processado" ou "erro"

❌ NÃO FAZER AGORA:
- Sistema de filas (RabbitMQ, Celery)
- Validação complexa de email
- Múltiplos processadores
- Logging estruturado
- Rate limiting
- Retry automático
- Métricas e monitoramento

💡 Código MVP:
def process_email(email: str) -> str:
    # Apenas processar caso mais simples
    if not email:
        return "erro"
    # Lógica mínima aqui
    return "processado"

Implementar este MVP? (s/n)
```

### Exemplo 2: API REST com LangGraph

**Objetivo do usuário**: "Criar API REST com LangGraph para processar documentos, com cache, validação, retry e monitoramento"

**Resposta correta do MVP**:
```
📦 MVP - API LANGGRAPH DOCUMENTOS

🎯 MVP (Iteração 1):
- [ ] Endpoint POST /process
- [ ] Receber documento (texto simples)
- [ ] LangGraph com 1 node (process)
- [ ] Retornar resultado

❌ NÃO FAZER AGORA:
- Cache Redis
- Validação Pydantic complexa
- Retry logic
- Middleware de autenticação
- Logging estruturado
- Métricas Prometheus
- Múltiplos nodes no graph
- State complexo

💡 Código MVP:
from fastapi import FastAPI
from langgraph.graph import StateGraph

app = FastAPI()

def process_node(state):
    return {"result": "processed"}

graph = StateGraph(dict)
graph.add_node("process", process_node)
graph.set_entry_point("process")
graph.set_finish_point("process")
app_graph = graph.compile()

@app.post("/process")
def process_doc(text: str):
    result = app_graph.invoke({"text": text})
    return result

Implementar este MVP? (s/n)
```

## ⚠️ Sinais de Over-Engineering

Se você detectar estes padrões, ALERTE o usuário:

❌ **Classes abstratas no MVP**
```python
# OVER-ENGINEERING
class AbstractProcessor(ABC):
    @abstractmethod
    def process(self): pass
```

✅ **Função simples no MVP**
```python
# MVP CORRETO
def process_email(email):
    return "processed"
```

---

❌ **Factory Pattern no MVP**
```python
# OVER-ENGINEERING
class ProcessorFactory:
    def create_processor(self, type): ...
```

✅ **Chamada direta no MVP**
```python
# MVP CORRETO
result = process_email(email)
```

---

❌ **Configuração complexa no MVP**
```python
# OVER-ENGINEERING
config = ConfigManager()
config.load_from_yaml()
config.validate_schema()
```

✅ **Hardcode no MVP**
```python
# MVP CORRETO
MAX_RETRIES = 3  # OK para MVP!
```

## 🎓 Princípios a Seguir

### 1. YAGNI (You Aren't Gonna Need It)
Não implemente funcionalidades até que sejam REALMENTE necessárias.

### 2. Simplicidade Primeiro
Código simples e direto é melhor que abstrações prematuras.

### 3. Evolutionary Architecture
A arquitetura evolui conforme novos requisitos surgem, não antes.

### 4. Feedback Rápido
MVP permite testar hipóteses rapidamente com menos código.

### 5. Refatoração no Momento Certo
Refatore quando PADRÕES EMERGIREM, não antecipadamente.

## 🚀 Próximos Passos Após MVP

Após implementar o MVP:

1. **Testar**: Garantir que funciona para o caso mais simples
2. **Executar**: Colocar em uso real (mesmo que limitado)
3. **Observar**: Identificar próxima funcionalidade REALMENTE necessária
4. **Iterar**: Usar `/add-increment` para adicionar próxima feature

**IMPORTANTE**: Não planejar múltiplas iterações antecipadamente! Cada iteração revela o que a próxima deve ser.

## 💡 Lembre-se

- MVP não precisa ser "código bonito"
- Hardcode é OK para MVP
- Abstrações vêm depois, quando padrões emergirem
- Funcionar > Perfeição
- Simples > Complexo
- Agora > Futuro hipotético