# Code Review Plugin

Plugin genérico de análise estática de código que identifica bugs, vulnerabilidades de segurança e oportunidades de melhoria em qualquer linguagem de programação.

## Instalação

```bash
/plugin marketplace add cadugevaerd/claudecode_plugins
/plugin install code-review
```

## Funcionalidades

- 🔒 **Análise de Segurança**: Detecta credenciais hardcoded, SQL injection, XSS, funções perigosas
- 🐛 **Detecção de Bugs**: Identifica null pointer, race conditions, error handling inadequado
- ✨ **Qualidade de Código**: Verifica estrutura, nomenclatura, complexidade, acoplamento
- 🧪 **Análise de Testes**: Valida cobertura, qualidade dos testes, mocks adequados
- 📚 **Documentação**: Verifica se código crítico está documentado
- 🔧 **Débito Técnico**: Identifica código duplicado, funções longas, magic numbers
- 📊 **Relatório Estruturado**: Problemas priorizados (crítico/importante/sugestão) com soluções

## Comandos Disponíveis

### /review

Executa análise completa e automática do código modificado.

**Uso básico**:
```bash
# Após fazer mudanças
git add .
/review
```

**Detecção automática**:
- Identifica linguagem de programação
- Detecta framework de testes em uso
- Reconhece gerenciador de pacotes
- Aplica boas práticas específicas da stack

**Saída**: Relatório estruturado em markdown com:
- ✅ Pontos positivos
- 🔴 Problemas críticos (devem ser corrigidos antes do commit)
- 🟡 Problemas importantes (devem ser corrigidos em breve)
- 🟢 Sugestões de melhoria
- 📊 Métricas (cobertura, complexidade, etc.)
- 🎯 Ações recomendadas priorizadas

## Agentes

### code-reviewer

Agente especializado em análise de código que executa automaticamente:

1. **Identificação de Contexto**: Analisa `git status` e `git diff`
2. **Análise de Segurança**: Credenciais, injection, funções perigosas
3. **Análise de Qualidade**: Estrutura, nomenclatura, performance
4. **Análise de Testes**: Cobertura e qualidade
5. **Documentação**: Verifica documentação adequada
6. **Débito Técnico**: Código duplicado, complexidade
7. **Relatório Final**: Análise estruturada e acionável

## Exemplos de Uso

### Exemplo 1: Code Review Antes do Commit

```bash
# Cenário: Você fez mudanças e quer validar antes de commitar

# 1. Stage suas mudanças
git add .

# 2. Execute o review
/review

# 3. O plugin analisa e gera relatório
## 🔍 Relatório de Code Review

**Arquivos modificados**: 3
**Linhas**: +120/-45

### ⚠️ Problemas Encontrados

#### 🔴 Críticos
**1. Credencial hardcoded**
- Arquivo: src/config.py:15
- Problema: API key exposta
- Solução: Usar variável de ambiente

#### 🟡 Importantes
**1. Falta cobertura de testes**
- Arquivo: src/utils.py:calculate_discount
- Problema: Função nova sem testes
- Solução: [exemplo de teste]

### 🎯 Ações Recomendadas
1. ✅ Remover API key hardcoded
2. 🟡 Adicionar testes para calculate_discount

# 4. Corrigir problemas e commitar
git commit -m "fix: remove hardcoded credentials"
```

### Exemplo 2: Review de Pull Request

```bash
# Cenário: Revisar PR antes de aprovar

# 1. Checkout na branch
git checkout feature/new-api-endpoint

# 2. Execute review
/review

# 3. Analisa todas as mudanças da branch vs main
## 🔍 Relatório de Code Review

**Projeto**: my-api
**Linguagem**: Python 3.11
**Framework**: FastAPI

### ✅ Pontos Positivos
- Testes cobrem casos de erro
- Documentação clara em endpoints
- Type hints em todas as funções

### ⚠️ Problemas Encontrados

#### 🔴 Críticos
**1. SQL Injection**
- Arquivo: src/database.py:42
- Problema: Query construída com f-string
- Solução: [exemplo usando parâmetros]

#### 🟡 Importantes
**1. Função muito longa**
- Arquivo: src/processor.py:30-120
- Problema: 90 linhas, muitas responsabilidades
- Solução: [exemplo de refatoração]

### 📊 Métricas
- Cobertura: 85% ✅
- Complexidade média: 6 (boa)
- Débito técnico: 2 itens

**Status**: ⚠️ NÃO PRONTO (1 crítico)
```

### Exemplo 3: Review Rápido de Hotfix

```bash
# Cenário: Hotfix urgente, precisa garantir qualidade

# 1. Faça o fix
vim src/payment.py

# 2. Review rápido
git add src/payment.py
/review

# 3. Plugin foca apenas no arquivo modificado
## 🔍 Relatório de Code Review

**Arquivos modificados**: 1 (src/payment.py)
**Linhas**: +5/-2

### ✅ Pontos Positivos
- Fix é mínimo e focado
- Não introduz novas dependências
- Error handling adequado

### ⚠️ Problemas Encontrados

#### 🟡 Importantes
**1. Falta teste para o bugfix**
- Arquivo: tests/test_payment.py
- Problema: Não há teste que valide o fix
- Solução: [exemplo de teste de regressão]

### 🎯 Ações Recomendadas
1. 🟡 Adicionar teste de regressão

**Status**: ✅ PODE COMMITAR (sem críticos)
```

## Linguagens Suportadas

O plugin é **completamente genérico** e suporta qualquer linguagem:

### Linguagens Detectadas Automaticamente

- **Python**: pytest, unittest, black, mypy
- **JavaScript/TypeScript**: jest, eslint, prettier
- **Java**: junit, maven, gradle
- **Go**: built-in testing, go fmt
- **Rust**: cargo test, rustfmt
- **Ruby**: rspec, rubocop
- **PHP**: phpunit, psalm
- **C#**: xunit, dotnet test
- **C/C++**: gtest, clang-format
- **Kotlin**: junit, ktlint
- **Swift**: xctest, swiftlint
- **Scala**: scalatest, scalafmt

### Frameworks de Teste Detectados

- Python: pytest, unittest, nose, hypothesis
- JavaScript: jest, mocha, jasmine, vitest, ava
- Java: junit, testng, spock
- Go: testing package
- Rust: built-in test framework
- Ruby: rspec, minitest
- PHP: phpunit, codeception
- C#: xunit, nunit, mstest

### Análises Genéricas

Se a linguagem não for reconhecida especificamente, o plugin aplica análises genéricas:

- Procura por padrões de segurança universais (credenciais, SQL, etc.)
- Analisa estrutura de arquivos
- Verifica documentação
- Identifica código duplicado
- Calcula métricas básicas

## Análises Realizadas

### 1. Segurança 🔒

**Credenciais Hardcoded**:
```python
# ❌ Detectado
API_KEY = "sk-1234567890"
PASSWORD = "admin123"

# ✅ Recomendado
API_KEY = os.getenv("API_KEY")
```

**SQL Injection**:
```python
# ❌ Detectado
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Recomendado
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**Funções Perigosas**:
```python
# ❌ Detectado
eval(user_input)
exec(code_from_api)

# ✅ Recomendado
# Evitar ou validar rigorosamente
```

### 2. Qualidade de Código ✨

**Código Duplicado**:
```python
# ❌ Detectado (repetido 3x)
if user.is_active and user.email_verified:
    send_email(user)

# ✅ Recomendado
def can_receive_email(user):
    return user.is_active and user.email_verified
```

**Funções Longas**:
```python
# ❌ Detectado (120 linhas)
def process_order(order):
    # ... 120 linhas de código

# ✅ Recomendado
def process_order(order):
    validated = validate_order(order)
    calculated = calculate_totals(validated)
    return save_order(calculated)
```

**Magic Numbers**:
```python
# ❌ Detectado
if count > 100:
    raise ValueError("Too many")

# ✅ Recomendado
MAX_ITEMS = 100
if count > MAX_ITEMS:
    raise ValueError(f"Máximo {MAX_ITEMS} itens")
```

### 3. Testes 🧪

**Cobertura**:
```python
# ⚠️ Detectado: função sem testes
def calculate_discount(price, percentage):
    return price * (1 - percentage / 100)

# ✅ Adicionar testes
def test_calculate_discount_valid():
    assert calculate_discount(100, 10) == 90

def test_calculate_discount_invalid():
    with pytest.raises(ValueError):
        calculate_discount(100, 150)
```

**Qualidade dos Testes**:
```python
# ❌ Detectado: teste ruim
def test_process():
    result = process(data)  # chamada real à API
    assert result  # assertion genérica

# ✅ Recomendado
def test_process_with_valid_data(mocker):
    """Deve processar dados válidos com sucesso"""
    mock_api = mocker.patch('module.api_call')
    mock_api.return_value = {"status": "ok"}

    result = process(valid_data)

    assert result.status == "ok"
    mock_api.assert_called_once()
```

### 4. Performance ⚡

**Loops Ineficientes**:
```python
# ❌ Detectado (N+1 queries)
for user_id in user_ids:
    user = db.get_user(user_id)  # query por iteração

# ✅ Recomendado
users = db.get_users(user_ids)  # query única
```

**Operações Síncronas**:
```python
# ❌ Detectado (chamadas em série)
result1 = api.get_data_1()  # 1s
result2 = api.get_data_2()  # 1s
# Total: 2s

# ✅ Recomendado (paralelo)
async def fetch_all():
    results = await asyncio.gather(
        api.get_data_1(),
        api.get_data_2()
    )
# Total: 1s
```

### 5. Documentação 📚

**Funções Complexas**:
```python
# ⚠️ Falta documentação
def retry_with_backoff(func, max_attempts=3):
    # código complexo...

# ✅ Recomendado
def retry_with_backoff(func, max_attempts=3):
    """
    Executa função com retry e backoff exponencial.

    Args:
        func: Função a ser executada
        max_attempts: Tentativas máximas (default: 3)

    Returns:
        Resultado da função

    Raises:
        Exception: Se todas as tentativas falharem
    """
```

## Melhores Práticas

### 1. Execute Antes de Cada Commit

```bash
# Adicione ao seu workflow
git add .
/review  # Valida mudanças
# Corrige problemas críticos
git commit -m "..."
```

### 2. Integre com Pull Requests

```bash
# Ao revisar PRs
git checkout feature-branch
/review
# Comenta problemas no PR
```

### 3. Use em Pipelines CI/CD

O plugin pode ser integrado em pipelines:

```yaml
# .github/workflows/code-review.yml
- name: Code Review
  run: |
    claude /review
    # Falha se houver problemas críticos
```

### 4. Customize para Seu Projeto

O plugin se adapta automaticamente, mas você pode:

- Configurar linters específicos (.eslintrc, .pylintrc)
- Definir cobertura mínima de testes
- Adicionar regras customizadas de projeto

### 5. Priorize Correções

Siga a ordem recomendada:
1. 🔴 **Críticos**: Sempre corrigir antes do commit
2. 🟡 **Importantes**: Corrigir em breve (próximos dias)
3. 🟢 **Sugestões**: Considerar no backlog

## Limitações

- **Análise Estática**: Não executa código (não detecta bugs de runtime)
- **Contexto Limitado**: Analisa apenas mudanças locais (não dependências externas completas)
- **Heurísticas**: Usa padrões comuns (pode ter falsos positivos)
- **Ferramentas Externas**: Não substitui linters/formatters especializados

## Roadmap

Funcionalidades planejadas:

- [ ] Integração com SonarQube/CodeClimate
- [ ] Análise de dependências vulneráveis (npm audit, pip-audit)
- [ ] Sugestões automáticas de refatoração
- [ ] Detecção de anti-patterns por framework
- [ ] Métricas de tendência (débito técnico crescendo?)
- [ ] Configuração customizável (.codereview.yml)

## Troubleshooting

**Problema**: Plugin não detecta linguagem
```bash
# Solução: Verifique extensões dos arquivos
ls -la src/
```

**Problema**: Testes não executados
```bash
# Solução: Verifique se framework está instalado
pip list | grep pytest
npm list jest
```

**Problema**: Muitos falsos positivos
```bash
# Solução: Configure linter do projeto
# .eslintrc, .pylintrc, etc.
```

## Autor

Carlos Araujo - cadu.gevaerd@gmail.com

## Licença

MIT

---

**Qualidade de código automatizada para qualquer linguagem** 🔍✨
