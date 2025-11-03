---
description: Revisar código identificando e removendo over-engineering seguindo princípio YAGNI
---

# Review YAGNI

Analisa código existente identificando complexidade desnecessária, abstrações prematuras e funcionalidades não utilizadas que podem ser simplificadas.

## Como usar

````bash
/review-yagni
/review-yagni "caminho/do/arquivo.py"
/review-yagni "módulo específico"

```text

## Padrões de over-engineering

### 1. Abstrações Prematuras

```text

❌ Uma classe abstrata com 1 implementação
❌ Interface usada por apenas 1 função
❌ Factory pattern para criar um tipo

```text

### 2. Código Não Utilizado

```text

❌ Funções nunca chamadas
❌ Imports não utilizados
❌ Arquivos sem referência

```text

### 3. Configuração Excessiva

```text

❌ Arquivo config.json com 100 variáveis
❌ Múltiplos ambientes (dev, test, staging, prod) quando não precisa
❌ Feature flags para comportamento simples

```text

### 4. Validação Sofisticada

```text

❌ Regex complexa quando simples check funciona
❌ Múltiplas camadas de validação
❌ Tratamento de casos impossíveis

```text

## Processo

1. **Escanear codebase**:
   - Analisar todos os arquivos
   - Procurar padrões de over-engineering
   - Listar achados por severidade

2. **Identificar abstrações com 1 uso**:
   - Interfaces não implementadas
   - Classes abstratas com 1 filho
   - Padrões sem casos de uso

3. **Encontrar código não utilizado**:
   - Funções nunca chamadas
   - Imports mortos
   - Branches de código obsoleto

4. **Revisar configuração**:
   - Variáveis nunca lidas
   - Settings redundantes
   - Complexidade desnecessária

5. **Gerar relatório**:
   - Listar achados com localização
   - Sugerir simplificações
   - Indicar impacto da remoção

## Output esperado

```text

⚠️ OVER-ENGINEERING DETECTADO

📊 Achados: 12 oportunidades
- Abstrações prematuras: 4
- Código morto: 5
- Configuração excessiva: 3

🔴 CRÍTICO (remover):
- Classe UserValidator (nunca usada)
- Função calculate_hash() (chamada 1x, inline OK)

🟡 AVISO (considerar):
- Interface Database com 1 implementação
- Config com 20 variáveis não lidas

💡 Recomendação:
/refactor-now para refatorar quando padrão emergir

```text

## Próximos comandos

- `/refactor-now` - Refatorar padrões emergentes
- `/add-increment` - Adicionar feature com YAGNI
- `/commit` - Commitar simplificações
````
