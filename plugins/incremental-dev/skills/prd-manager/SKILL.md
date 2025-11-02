---
name: prd-manager
description: Automatically manages and updates PRD (Product Requirements Document) by detecting appropriate update moments based on project phase. Use when working with PRD, requirements, product documentation, MVP definition, architectural decisions, learnings from increments, or transitioning between development phases (discovery, planning, design, increments). Trigger terms - requisitos, objetivos, MVP, incremento completo, decisões arquiteturais, aprendizados, lições aprendidas, ADR, Product Vision, épicos, User Stories.
allowed-tools: Read, Write, Edit, Grep, Bash
---

# PRD Manager Skill

Gerencia automaticamente o PRD (Product Requirements Document) do projeto, sugerindo atualizações no momento apropriado e validando consistência entre código e documentação.

## 🎯 Quando Usar Esta Skill

Claude invoca automaticamente esta skill quando detectar:

### Termos de Gatilho
- **PRD**: "atualizar PRD", "consultar PRD", "PRD atual"
- **Requisitos**: "requisitos do projeto", "documentação de requisitos"
- **Fases**: "descoberta", "planejamento", "design", "incremento completo"
- **Decisões**: "decisão arquitetural", "ADR", "architectural decision"
- **Aprendizados**: "lição aprendida", "retrospectiva", "aprendizado do incremento"

### Cenários de Uso
1. Usuário menciona conclusão de incremento
2. Usuário faz pergunta sobre objetivos do projeto
3. Usuário menciona decisão técnica importante
4. Projeto parece divergir dos requisitos
5. Comandos do plugin solicitam interação com PRD

---

## 📋 Responsabilidades da Skill

### 1. Detecção Automática de Momento de Atualização

**Monitorar sinais**:
- Incremento foi completado → sugerir `/prd-update incremento`
- Planejamento de MVP finalizado → sugerir `/prd-update planejamento`
- Arquitetura definida → sugerir `/prd-update design`
- Decisão técnica importante tomada → sugerir registrar ADR

**Exemplo**:
```
[Usuário]: "Terminamos de implementar upload de PDF com drag-and-drop"

[Skill detecta]: Incremento completo
[Skill sugere]:
"✅ Incremento completo!

💡 Deseja registrar este incremento no PRD?
   /prd-update incremento

Isso documentará:
- Funcionalidades implementadas
- Aprendizados obtidos
- Decisões técnicas tomadas
"
```

---

### 2. Validação de Completude do PRD

Verificar se seções do PRD estão completas para cada fase:

**Fase Descoberta (v0.1)**:
- [ ] Problema definido
- [ ] Objetivos claros (3+ objetivos)
- [ ] KPIs estabelecidos

**Fase Planejamento (v1.0)**:
- [ ] Product Vision
- [ ] Épicos identificados
- [ ] MVP definido
- [ ] Features fora do MVP (YAGNI)
- [ ] User Stories principais

**Fase Design (v1.1)**:
- [ ] Arquitetura de alto nível
- [ ] Stack tecnológica
- [ ] Modelagem de dados
- [ ] APIs/Contratos

**Fase Desenvolvimento (v1.x)**:
- [ ] Incrementos documentados
- [ ] Aprendizados registrados
- [ ] ADRs para decisões importantes

**Alertar se incompleto**:
```
⚠️  PRD INCOMPLETO

Fase atual: Planejamento (v1.0)

Faltando:
- [ ] User Stories principais
- [ ] Roadmap de incrementos

Recomendação: Complete PRD antes de prosseguir
```

---

### 3. Sugerir Próxima Fase do PRD

Baseado em progresso do projeto:

**Exemplo**:
```
[Análise]:
- PRD v0.1 completo ✅
- Objetivos definidos ✅
- MVP ainda não planejado ❌

[Sugestão]:
"📊 PRD pronto para evoluir!

Próxima fase sugerida: Planejamento (v1.0)

Execute: /prd-update planejamento

Isso permitirá:
- Definir MVP claramente
- Mapear épicos
- Criar roadmap de incrementos
- Estabelecer User Stories
"
```

---

### 4. Validar Consistência Código vs PRD

Detectar divergências:

**Exemplo de Divergência Detectada**:
```
⚠️  DIVERGÊNCIA DETECTADA

PRD define MVP:
- Upload de PDF ✅
- Extração de texto ✅
- Exibição de resultado ❌ (NÃO IMPLEMENTADO)

Código implementa:
- Upload de PDF ✅
- Extração de texto ✅
- Dashboard completo ⚠️  (FORA DO MVP!)

💡 Ações sugeridas:
1. Atualizar PRD para refletir implementação real
2. OU remover código fora do MVP (YAGNI)
3. Documentar por que divergiu do planejado
```

---

### 5. Alertar Sobre YAGNI Violations

Se código implementa features **fora do MVP** definido no PRD:

```
🚨 YAGNI VIOLATION DETECTADA

PRD marca como "Fora do MVP":
- ❌ Autenticação OAuth
- ❌ API REST completa
- ❌ Múltiplos formatos (PDF, DOCX, TXT)

Código implementa:
- ⚠️  OAuth integration em progress (auth.py)

💡 Questionar:
"Por que implementar OAuth agora?
 MVP define apenas upload básico sem autenticação.

 Isso é realmente necessário AGORA?"
```

---

## 🔍 Instruções Detalhadas

### Passo 1: Verificar Existência do PRD

```bash
# Verificar se PRD existe
test -f docs/PRD.md && echo "PRD existe" || echo "PRD não existe"
```

**Se PRD não existe**:
```
💡 PRD não encontrado

Sugestão: Execute /setup-project-incremental
Isso cria PRD v0.1 inicial com:
- Problema a resolver
- Objetivos do projeto
- KPIs para medir sucesso
```

**Se PRD existe**:
```
✅ PRD encontrado

Analisando versão e completude...
```

---

### Passo 2: Extrair Informações do PRD

Ler `docs/PRD.md` e extrair:

```python
# Informações a extrair:
- versao_atual: str  # Regex: **Versão**: (\d+\.\d+)
- ultima_atualizacao: str
- status: str
- problema: str
- objetivos: List[str]
- mvp_definido: bool
- features_fora_mvp: List[str]
- incrementos_implementados: List[dict]
- adrs: List[dict]
```

---

### Passo 3: Determinar Fase Atual

```python
def determinar_fase(versao: str) -> str:
    if versao == "0.1":
        return "Descoberta"
    elif versao == "1.0":
        return "Planejamento"
    elif versao == "1.1":
        return "Design"
    elif versao.startswith("1.") and int(versao.split(".")[1]) > 1:
        return "Desenvolvimento"
    elif versao == "2.0":
        return "Finalizado (As-Built)"
    else:
        return "Desconhecida"
```

---

### Passo 4: Sugerir Atualização se Apropriado

**Gatilhos para sugestão**:

1. **Incremento completado** (detectar em conversa):
   - Usuário menciona "implementado", "finalizado", "completo"
   - Código novo foi adicionado
   → Sugerir: `/prd-update incremento`

2. **MVP planejado** (detectar em conversa):
   - Usuário define features do MVP
   - MVP claramente discutido
   → Sugerir: `/prd-update planejamento`

3. **Arquitetura definida**:
   - Stack tecnológica escolhida
   - Modelagem de dados criada
   → Sugerir: `/prd-update design`

4. **Decisão arquitetural importante**:
   - Padrão extraído em refatoração
   - Framework/biblioteca escolhida
   → Sugerir: Registrar ADR no PRD

---

### Passo 5: Validar Completude de Seção

Para fase atual, verificar se campos obrigatórios estão preenchidos:

```python
def validar_descoberta(prd: dict) -> List[str]:
    faltando = []
    if not prd["problema"] or prd["problema"] == "[Descrever problema]":
        faltando.append("Problema não definido")
    if len(prd["objetivos"]) < 3:
        faltando.append("Menos de 3 objetivos definidos")
    if not prd["kpis"]:
        faltando.append("KPIs não estabelecidos")
    return faltando

def validar_planejamento(prd: dict) -> List[str]:
    faltando = []
    if not prd["product_vision"]:
        faltando.append("Product Vision não criada")
    if not prd["mvp_definido"]:
        faltando.append("MVP não definido")
    if len(prd["epicos"]) == 0:
        faltando.append("Épicos não mapeados")
    return faltando
```

---

### Passo 6: Detectar Divergências

Comparar PRD com código implementado:

```bash
# Buscar features no código
grep -r "class.*Processor" src/
grep -r "def upload" src/
grep -r "OAuth" src/

# Comparar com features_fora_mvp do PRD
```

Se feature **fora do MVP** foi implementada → Alertar YAGNI violation

---

## 📚 Exemplos de Invocação Automática

### Exemplo 1: Incremento Completado

**Conversa**:
```
Usuário: "Pronto! Upload de PDF funcionando com drag-and-drop e validação."
```

**Skill detecta**:
- "Pronto", "funcionando" → Incremento completado
- "Upload de PDF" → Feature específica
- "drag-and-drop", "validação" → Detalhes de implementação

**Skill responde**:
```
✅ Incremento completo detectado!

Funcionalidade: Upload de PDF
Features implementadas:
- Drag-and-drop
- Validação

💡 Registrar este incremento no PRD?

Comando: /prd-update incremento

Benefícios:
- Documenta funcionalidades entregues
- Registra aprendizados
- Mantém PRD sincronizado com código
- Facilita retrospectivas futuras

Deseja registrar? (s/n)
```

---

### Exemplo 2: PRD Incompleto

**Conversa**:
```
Usuário: "Vamos começar a implementar o MVP"
```

**Skill verifica PRD**:
- Versão: 0.1 (Descoberta)
- MVP definido: NÃO ❌

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

### Exemplo 3: YAGNI Violation Detectada

**Skill analisa código** e encontra:
```python
# src/auth/oauth.py
class OAuthIntegration:
    def authenticate(self): ...
```

**PRD define**:
```
**Fora do MVP** (YAGNI):
- ❌ Autenticação OAuth
```

**Skill alerta**:
```
🚨 YAGNI VIOLATION

Detectado código FORA DO MVP:
src/auth/oauth.py - OAuthIntegration

PRD marca como "Fora do MVP":
- ❌ Autenticação OAuth

⚠️  Questões a considerar:
1. Por que implementar OAuth AGORA?
2. MVP realmente precisa de autenticação?
3. Isso entrega valor imediato?

Opções:
A) Remover código (seguir MVP definido)
B) Atualizar PRD (OAuth é essencial afinal)
C) Manter mas documentar exceção no PRD

Escolha: [A/B/C]
```

---

## 🎯 Métricas de Sucesso da Skill

Esta skill é bem-sucedida quando:

✅ PRD é atualizado após cada incremento (não fica desatualizado)
✅ Divergências código vs PRD são detectadas cedo
✅ YAGNI violations são questionadas automaticamente
✅ Usuário é lembrado de documentar aprendizados
✅ Fase do PRD evolui junto com o projeto
✅ ADRs são registrados para decisões importantes

---

## 💡 Princípios da Skill

1. **Proativo, não invasivo**: Sugerir, não forçar
2. **Contextual**: Sugestões baseadas em momento real
3. **Educativo**: Explicar POR QUE sugerir atualização
4. **Validador**: Garantir consistência código ↔ documentação
5. **Orientador YAGNI**: Alertar sobre features fora do MVP

---

## 🔗 Integração com Comandos

Esta skill trabalha em conjunto com:

- `/prd-update [fase]` - Executado quando skill sugere
- `/prd-view` - Para mostrar estado atual do PRD
- `/setup-project-incremental` - Cria PRD v0.1 inicial
- `/add-increment` - Solicita skill para sugerir registro
- `/refactor-now` - Solicita skill para sugerir ADR

---

**PRD Manager: Mantendo documentação viva e sincronizada!**
