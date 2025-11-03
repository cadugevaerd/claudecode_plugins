# PRD Manager - Padrões de Invocação

Exemplos de detecção automática de momentos para atualizar PRD.

---

## Padrão 1: Incremento Completado

### Quando Detectar
Usuário menciona:
- "Pronto", "completo", "finalizado"
- Feature específica concluída
- "Funcionando", "testado"

### Exemplo de Detecção

**Conversa**:
```
Usuário: "Pronto! Upload de PDF funcionando com drag-and-drop e validação."
```

**Skill detecta**:
- "Pronto", "funcionando" → Incremento completado
- "Upload de PDF" → Feature específica
- "drag-and-drop", "validação" → Detalhes

**Skill responde**:
```
✅ INCREMENTO COMPLETO DETECTADO

Funcionalidade: Upload de PDF
Features implementadas:
- Drag-and-drop
- Validação

💡 Registrar este incremento no PRD?

Comando: /prd-update incremento

Benefícios:
- Documenta funcionalidades entregues
- Registra aprendizados
- Mantém PRD sincronizado
- Facilita retrospectivas

Deseja registrar? (s/n)
```

---

## Padrão 2: PRD Incompleto para MVP

### Quando Detectar
Usuário menciona:
- "Começar a implementar MVP"
- "Definir MVP"
- "Features principais"

Mas PRD não tem MVP definido

### Exemplo de Detecção

**Conversa**:
```
Usuário: "Vamos começar a implementar o MVP"
```

**Skill verifica PRD**:
- Versão: 0.1 (Descoberta)
- MVP definido: ❌ NÃO

**Skill responde**:
```
⚠️  PRD INCOMPLETO PARA MVP

PRD atual: v0.1 (Descoberta)
Status: Objetivos definidos ✅

Para implementar MVP, PRD precisa de:
- [ ] Product Vision
- [ ] MVP claramente definido
- [ ] Features fora do MVP (YAGNI)
- [ ] Épicos mapeados

Recomendação:
1. Execute: /prd-update planejamento
2. Defina MVP e escopo
3. Depois: /start-incremental

Isso evita implementar features desnecessárias!
```

---

## Padrão 3: YAGNI Violation - Código Fora do MVP

### Quando Detectar
Ao analisar código:
- Feature implementada não está no MVP
- PRD marca como "Fora do MVP"
- Feature não é parte do escopo planejado

### Exemplo de Detecção

**Skill analisa código**:
```python
# src/auth/oauth.py
class OAuthIntegration:
    def authenticate(self):
        # ...
```

**PRD define**:
```
**MVP**:
- Upload PDF
- Extração de texto

**Fora do MVP** (YAGNI):
- ❌ Autenticação OAuth
```

**Skill alerta**:
```
🚨 YAGNI VIOLATION DETECTADA

Código implementado FORA DO MVP:
src/auth/oauth.py - OAuthIntegration

PRD marca como "Fora do MVP":
- ❌ Autenticação OAuth

⚠️  Questões:
1. Por que implementar OAuth AGORA?
2. MVP realmente precisa de autenticação?
3. Isso entrega valor imediato?

Opções:
A) Remover código (seguir MVP)
B) Atualizar PRD (é essencial afinal)
C) Documentar exceção e justificar

Escolha recomendada?
```

---

## Padrão 4: PRD v0.1 Completo → Sugerir Planejamento

### Quando Detectar
PRD v0.1 tem:
- ✅ Problema definido
- ✅ 3+ objetivos
- ✅ KPIs estabelecidos

### Skill Responde
```
📊 PRD PRONTO PARA EVOLUIR

PRD v0.1 (Descoberta) COMPLETO ✅
- Problema: [bem definido]
- Objetivos: [3+ objetivos]
- KPIs: [estabelecidos]

Próxima fase: Planejamento (v1.0)

Execute: /prd-update planejamento

Isso permitirá:
- Definir Product Vision
- Mapear épicos
- Criar MVP claramente
- Identificar features fora do MVP
- Estabelecer roadmap

Pronto? (s/n)
```

---

## Padrão 5: Arquitetura Definida → Registrar Design

### Quando Detectar
Usuário menciona:
- "Stack definido"
- "Arquitetura pronta"
- "Modelagem de dados completa"
- "APIs/contratos definidos"

### Skill Responde
```
🏗️  ARQUITETURA DEFINIDA

Detectei definição de stack/arquitetura

Registrar em PRD como Design (v1.1)?

Comando: /prd-update design

Isso documentará:
- Stack tecnológica escolhida
- Arquitetura de alto nível
- Modelagem de dados
- APIs/contratos
- Decisões arquiteturais

Benefício:
- Referência para implementação
- Rastreabilidade de decisões
- Facilita onboarding de novos

Registrar? (s/n)
```

---

## Padrão 6: Decisão Arquitetural → Sugerir ADR

### Quando Detectar
Usuário menciona:
- "Decidimos usar X padrão"
- "Escolhemos framework Y"
- "Optamos por Z abordagem"
- Decisão com trade-offs considerados

### Skill Responde
```
⚙️  DECISÃO ARQUITETURAL IMPORTANTE

Detectei decisão técnica importante:
"[Descrição da decisão]"

Registrar como ADR (Architectural Decision Record)?

Comando: /prd-update design

Benefícios de registrar:
- Contexto: POR QUE escolhemos
- Alternativas consideradas
- Trade-offs
- Consequências
- Data e quem decidiu

Futuro: Novo dev entende contexto

Registrar? (s/n)
```

---

## Padrão 7: Validação de Completude por Fase

### Fase Descoberta (v0.1)
```
Verificar:
✓ Problema está definido?
✓ 3+ Objetivos claros?
✓ KPIs mensuráveis?

Se NÃO: Alertar PRD incompleto
Se SIM: Pronto para planejamento
```

### Fase Planejamento (v1.0)
```
Verificar:
✓ Product Vision definida?
✓ MVP claramente especificado?
✓ Features fora do MVP?
✓ Épicos/user stories principais?

Se NÃO: Alertar campos faltando
Se SIM: Pronto para design
```

### Fase Design (v1.1)
```
Verificar:
✓ Arquitetura de alto nível?
✓ Stack tecnológica?
✓ Modelagem de dados?
✓ APIs/contratos?

Se NÃO: Alertar campos faltando
Se SIM: Pronto para implementação
```

### Fase Desenvolvimento (v1.x)
```
Verificar:
✓ Incrementos documentados?
✓ Aprendizados registrados?
✓ ADRs importantes?

Se NÃO: Sugerir `/prd-update incremento`
Se SIM: Incremento bem rastreado
```

---

## Checklist de Invocação Automática

Quando Claude estar falando com usuário:

```
[ ] Usuário menciona incremento completo?
    → Sugerir /prd-update incremento

[ ] Usuário quer implementar MVP?
    → Verificar se PRD tem MVP definido
    → Se NÃO → Sugerir /prd-update planejamento

[ ] Usuário define arquitetura/stack?
    → Sugerir /prd-update design

[ ] Código implementa feature fora do MVP?
    → Alertar YAGNI violation

[ ] PRD atual completo para sua fase?
    → Sugerir próxima fase

[ ] Usuário tira dúvida sobre objetivos?
    → Referir ao PRD
```

---

## Princípios de Detecção

1. **Proativo**: Detectar sem esperar usuário pedir
2. **Contextual**: Baseado em conversa e código real
3. **Não invasivo**: Sugerir, não forçar
4. **Educativo**: Explicar POR QUE sugerir
5. **Validador**: Garantir PRD sempre sincronizado
