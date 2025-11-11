---
description: Creates SQL schema and LangGraph State from ARQUITECTURE.md specification
allowed-tools: Read, Write, Glob, AskUserQuestion
model: claude-sonnet-4-5
argument-hint: '[PROJECT_PATH]'
---

# Create Esqueleto

Cria o esqueleto do projeto LangGraph a partir do `ARQUITECTURE.md`, gerando:

- Script SQL para criação do banco de dados (SQLite para desenvolvimento)
- State Schema Python (TypedDict) com todos os fields documentados

## 🎯 Objetivo

Gerar código executável que implementa:

- ✅ Script SQL completo com tabelas, colunas, tipos e relacionamentos
- ✅ State Schema Python com TypedDict, type hints e reducers
- ✅ Comentários documentando propósito de cada field/table
- ✅ Suporte para SQLite (desenvolvimento) com anotações para migração futura
- ✅ Validação de que ARQUITECTURE.md existe e está completo

## 🔧 Instruções

### 1. **Validar Entrada**

1.1 **Determinar Project Path**

- Se `PROJECT_PATH` fornecido: usar esse caminho
- Se não fornecido: usar working directory atual
- Validar que o path existe

1.2 **Verificar ARQUITECTURE.md**

- Usar `Glob(pattern="[PROJECT_PATH]/ARQUITECTURE.md")` para localizar
- Se não existe: erro e sugerir executar `/create-arquitecture` primeiro
- Usar `Read` para carregar conteúdo completo

### 2. **Extrair Especificações**

2.1 **Extrair State Schema**

Do ARQUITECTURE.md, identificar seção `## 🗃️ State Schema`:

- Campos do state (nome, tipo, propósito)
- Reducers necessários (`Annotated[...]`)
- Type hints completos (`str`, `int`, `List[str]`, etc)
- Valores default se especificados

2.2 **Extrair Arquitetura de Dados**

Do ARQUITECTURE.md, identificar seção `## 💾 Arquitetura de Dados`:

- Se "Não usa banco de dados": criar apenas State Schema, pular SQL
- Se usa banco:
  - Tables necessárias
  - Colunas e tipos
  - Chaves primárias
  - Chaves estrangeiras
  - Índices recomendados
  - Relacionamentos entre tabelas

2.3 **Validar Completude**

- State Schema: Pelo menos 1 field documentado
- Se usa banco: Pelo menos 1 table especificada
- Se informações insuficientes: perguntar ao usuário com `AskUserQuestion`

### 3. **Gerar State Schema Python**

3.1 **Criar Arquivo state.py**

Estrutura:

```python
"""
State Schema for [Project Name]
Generated from ARQUITECTURE.md

[Breve descrição do propósito do state]
"""
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
import operator

class AgentState(TypedDict):
    """
    [Descrição geral do state]

    Attributes:
        [field_name]: [Descrição do propósito]
        ...
    """
    # [Comentário explicando o field]
    field_name: type_hint

    # [Comentário para fields com reducers]
    accumulated_field: Annotated[List[str], operator.add]

    # Messages field (comum em agentes)
    messages: Annotated[list, add_messages]
```

3.2 **Escrever state.py**

- Usar `Write(file_path="[PROJECT_PATH]/state.py", content=...)`
- Incluir todos imports necessários
- Adicionar docstrings para classe e fields
- Garantir type hints corretos
- Incluir reducers onde especificado no ARQUITECTURE.md

### 4. **Gerar Script SQL**

4.1 **Criar schema.sql (se usa banco de dados)**

Estrutura para SQLite:

```sql
-- Schema for [Project Name]
-- Generated from ARQUITECTURE.md
-- Database: SQLite (development) / [Target DB] (production)

-- =============================================================================
-- Table: [table_name]
-- Purpose: [Descrição da table]
-- =============================================================================

CREATE TABLE IF NOT EXISTS [table_name] (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [column_name] [type] [constraints],  -- [Comentário]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for [table_name]
CREATE INDEX IF NOT EXISTS idx_[table]_[column] ON [table_name]([column]);

-- =============================================================================
-- Foreign Keys & Relationships
-- =============================================================================

-- [Descrição do relacionamento]
-- [table_a].[column] -> [table_b].[column]

-- =============================================================================
-- Migration Notes
-- =============================================================================
-- SQLite -> PostgreSQL:
--   - INTEGER PRIMARY KEY AUTOINCREMENT -> SERIAL PRIMARY KEY
--   - TIMESTAMP -> TIMESTAMPTZ
-- SQLite -> MySQL:
--   - INTEGER PRIMARY KEY AUTOINCREMENT -> INT AUTO_INCREMENT PRIMARY KEY
--   - TIMESTAMP -> DATETIME
```

4.2 **Mapear Tipos SQLite**

Usar tipos apropriados:

- Texto: `TEXT`, `VARCHAR(n)`
- Números: `INTEGER`, `REAL`
- Booleanos: `INTEGER` (0/1)
- Timestamps: `TIMESTAMP`
- JSON: `TEXT` (SQLite armazena como string)

4.3 **Adicionar Migration Comments**

Incluir comentários para migração futura:

- PostgreSQL equivalents
- MySQL equivalents
- Diferenças de sintaxe

4.4 **Escrever schema.sql**

- Usar `Write(file_path="[PROJECT_PATH]/schema.sql", content=...)`
- Incluir todos CREATE TABLE statements
- Adicionar índices recomendados
- Documentar relacionamentos
- Incluir migration notes

### 5. **Criar README de Implementação**

5.1 **Gerar IMPLEMENTATION.md**

```markdown
# Implementation Guide

## Setup Database

### Development (SQLite)

\`\`\`bash
sqlite3 [project].db < schema.sql
\`\`\`

### Verify Schema

\`\`\`bash
sqlite3 [project].db ".schema"
\`\`\`

## Use State Schema

\`\`\`python
from state import AgentState

# Example: Initialize state
initial_state = AgentState(
    field_name="value",
    messages=[]
)
\`\`\`

## Next Steps

1. [ ] Execute schema.sql para criar database
2. [ ] Import AgentState em seus nodes
3. [ ] Implementar nodes conforme ARQUITECTURE.md
4. [ ] Configurar checkpointer se usa persistence
5. [ ] Testar state updates em cada node
```

5.2 **Escrever IMPLEMENTATION.md**

- Usar `Write(file_path="[PROJECT_PATH]/IMPLEMENTATION.md", content=...)`
- Incluir comandos práticos para setup
- Adicionar exemplos de uso
- Listar próximos passos

### 6. **Validar Arquivos Criados**

6.1 **Checklist de Validação**

- [ ] state.py criado com imports corretos
- [ ] AgentState tem todos fields do ARQUITECTURE.md
- [ ] Type hints e reducers corretos
- [ ] schema.sql criado (se usa banco)
- [ ] Todas tables especificadas criadas
- [ ] Índices adicionados onde apropriado
- [ ] Migration comments incluídos
- [ ] IMPLEMENTATION.md criado com instruções

6.2 **Apresentar Resumo**

```text
✅ Esqueleto criado com sucesso!

📊 Arquivos Gerados:
- state.py: [X fields, Y reducers]
- schema.sql: [Z tables, W indexes] (ou "Não criado - state transiente")
- IMPLEMENTATION.md: Guia de setup

📁 Localização: [PROJECT_PATH]/

📋 Próximos Passos:
1. Executar schema.sql (se aplicável)
2. Importar AgentState nos nodes
3. Implementar nodes conforme ARQUITECTURE.md
```

## 📊 Formato de Saída

### Arquivo state.py

```python
"""
State Schema for [Project]
Generated from ARQUITECTURE.md
"""
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
import operator

class AgentState(TypedDict):
    """State compartilhado entre nodes do agente."""
    messages: Annotated[list, add_messages]
    context: str
    final_output: str
```

### Arquivo schema.sql (se usa banco)

```sql
-- Schema for [Project]
-- Database: SQLite (dev)

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Arquivo IMPLEMENTATION.md

Guia prático de setup e uso dos arquivos gerados.

### Mensagem de Confirmação

```text
✅ Esqueleto criado com sucesso!

📊 Arquivos Gerados:
- state.py: 4 fields, 2 reducers
- schema.sql: 3 tables, 5 indexes
- IMPLEMENTATION.md: Guia de setup

📁 Localização: /path/to/project/

📋 Próximos Passos:
1. sqlite3 project.db < schema.sql
2. from state import AgentState
3. Implementar nodes do ARQUITECTURE.md
```

## ✅ Critérios de Sucesso

- [ ] ARQUITECTURE.md localizado e lido completamente
- [ ] State Schema extraído com todos fields
- [ ] Arquitetura de dados extraída (ou confirmado state transiente)
- [ ] state.py criado com TypedDict correto
- [ ] Todos fields documentados com type hints
- [ ] Reducers aplicados onde especificado
- [ ] Imports corretos (typing, langgraph, operator)
- [ ] schema.sql criado se projeto usa banco
- [ ] Todas tables especificadas implementadas
- [ ] Tipos SQLite corretos usados
- [ ] Índices adicionados para otimização
- [ ] Migration comments incluídos (SQLite → PostgreSQL/MySQL)
- [ ] IMPLEMENTATION.md criado com guia prático
- [ ] Validação executada antes de confirmar
- [ ] Resumo apresentado ao usuário
- [ ] Arquivos válidos e executáveis

## 📝 Exemplos

### Exemplo 1 - Projeto simples sem banco

```bash
/create-esqueleto
```

**Comportamento:**

1. Lê `ARQUITECTURE.md` do diretório atual
1. Encontra: "Não usa banco de dados. State é transiente."
1. Cria apenas `state.py` com 3 fields
1. Cria `IMPLEMENTATION.md` sem comandos SQL
1. Resumo: "1 arquivo gerado (state.py)"

### Exemplo 2 - Projeto com banco de dados

```bash
/create-esqueleto
```

**Comportamento:**

1. Lê `ARQUITECTURE.md`
1. Extrai State Schema: 5 fields (messages, context, documents, embeddings, output)
1. Extrai DB Architecture: 2 tables (documents, embeddings)
1. Cria `state.py` com 5 fields + 2 reducers
1. Cria `schema.sql` com 2 tables + 3 indexes
1. Cria `IMPLEMENTATION.md` com setup SQLite
1. Resumo: "3 arquivos gerados"

### Exemplo 3 - Projeto com path customizado

```bash
/create-esqueleto /path/to/my-langgraph-project
```

**Comportamento:**

1. Busca `ARQUITECTURE.md` em `/path/to/my-langgraph-project/`
1. Gera arquivos em `/path/to/my-langgraph-project/`:
   - `state.py`
   - `schema.sql`
   - `IMPLEMENTATION.md`

### Exemplo 4 - ARQUITECTURE.md incompleto

```bash
/create-esqueleto
```

**Comportamento:**

1. Lê `ARQUITECTURE.md`
1. Não encontra seção `State Schema` completa
1. Usa `AskUserQuestion` para solicitar fields do state
1. Usuário fornece fields manualmente
1. Cria `state.py` com informações fornecidas

## ❌ Anti-Patterns

### ❌ Erro 1: Não validar ARQUITECTURE.md

Não criar arquivos sem validar especificação:

```bash
# ❌ Errado - Criar sem ler ARQUITECTURE.md
Write state.py direto

# ✅ Correto - Sempre ler ARQUITECTURE.md primeiro
Read ARQUITECTURE.md → Extract specs → Generate files
```

### ❌ Erro 2: Type hints incorretos

Não usar types genéricos sem especificação:

```python
# ❌ Errado - Type hint vago
class AgentState(TypedDict):
    messages: list  # list de quê?
    data: dict      # dict com quais keys?

# ✅ Correto - Type hints específicos
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    data: Dict[str, Any]
```

### ❌ Erro 3: Esquecer reducers

Não omitir reducers para fields acumulados:

```python
# ❌ Errado - Falta reducer
class AgentState(TypedDict):
    tools_used: List[str]  # Será sobrescrito, não acumulado

# ✅ Correto - Com reducer
class AgentState(TypedDict):
    tools_used: Annotated[List[str], operator.add]  # Acumula
```

### ❌ Erro 4: SQL sem comentários

Não criar schema SQL sem documentação:

```sql
-- ❌ Errado - Sem contexto
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- ✅ Correto - Documentado
-- =============================================================================
-- Table: users
-- Purpose: Armazena informações de usuários do sistema
-- =============================================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  -- Nome completo do usuário
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ❌ Erro 5: Não incluir migration notes

Não esquecer comentários para migração futura:

```sql
-- ❌ Errado - SQLite only
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

-- ✅ Correto - Com migration notes
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT  -- PostgreSQL: SERIAL PRIMARY KEY
);

-- Migration Notes:
-- SQLite -> PostgreSQL:
--   INTEGER PRIMARY KEY AUTOINCREMENT -> SERIAL PRIMARY KEY
```
