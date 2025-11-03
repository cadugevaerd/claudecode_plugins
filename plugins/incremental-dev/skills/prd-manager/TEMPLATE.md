# PRD - [Nome do Projeto]

**Status**: Documento Vivo
**Última Atualização**: [YYYY-MM-DD]
**Versão**: [Veja Histórico de Versões]

______________________________________________________________________

## 1. 🎯 Visão e Estratégia (A "Estrela Guia")

### Problema

[Descrever o problema específico que este produto resolve. Por quê é importante?]

### Objetivos (Outcomes)

O que queremos mudar ou alcançar com este produto:

- [ ] Objetivo 1: [descrição]
- [ ] Objetivo 2: [descrição]
- [ ] Objetivo 3: [descrição]

### KPIs (Key Performance Indicators)

Como saberemos que estamos vencendo:

- **KPI 1**: [métrica e meta]
- **KPI 2**: [métrica e meta]

### Product Vision

[A visão de longo prazo para este produto. Para onde queremos ir?]

### Roadmap (Now, Next, Later)

Estratégia de priorização flexível:

- **Now (Em andamento)**: [Incremento/épico atual sendo desenvolvido]
- **Next (Próximos)**: [Lista de incrementos priorizados a seguir]
- **Later (Backlog)**: [Ideias a explorar no futuro]

______________________________________________________________________

## 2. 📦 Produto Mínimo Viável (MVP)

### Definição do MVP

Features essenciais para validar a hipótese:

- [ ] Feature essencial 1
- [ ] Feature essencial 2
- [ ] Feature essencial 3

### Hipótese do MVP

"Acreditamos que [estas features] irão [resolver o problema / validar a hipótese]."

### Fora do MVP (YAGNI)

O que **NÃO** faremos agora:

- ❌ Feature prematura 1
- ❌ Feature prematura 2
- ❌ Abstração esperada

______________________________________________________________________

## 3. 🚀 Incrementos de Entrega (O "Diário de Bordo")

*Esta seção é atualizada a cada ciclo de desenvolvimento.*

### Incremento 1: [Nome do Épico ou Objetivo]

**Status**: Concluído
**Data**: [YYYY-MM-DD]

#### User Stories Entregues

- [x] US-1: Como [ator], quero [ação], para [benefício]
  - Acceptance Criteria: [AC1, AC2]
- [x] US-2: ...

#### Design & Decisões (O "Como" para este incremento)

*Como os requisitos foram implementados e que decisões técnicas foram tomadas:*

**Arquitetura**:
[Descrição ou diagrama do que foi construído/alterado neste incremento. NÃO o design futuro, apenas o que foi implementado.]

**Modelagem de Dados**:
[Schemas alterados/criados para este incremento]

**APIs / Contratos**:
[Novos endpoints ou interfaces criadas]

**ADRs Relevantes**:

- ADR-001: [Título da decisão] - [Link ou descrição]
- ADR-002: [Título da decisão] - [Link ou descrição]

#### Validação & Métricas Reais

[Resultados dos testes, métricas coletadas após implementação]

#### Retrospectiva (Lições Aprendidas)

- **O que funcionou**: [Práticas, padrões, decisões que se provaram corretas]
- **O que não funcionou**: [Abordagens que não deram certo]
- **Melhorias para próximo incremento**: [Ajustes baseados nos aprendizados]

______________________________________________________________________

### Incremento 2: [Nome do Épico ou Objetivo]

**Status**: Em Desenvolvimento
**Data de Início**: [YYYY-MM-DD]

#### User Stories Alvo

- [ ] US-3: ...
- [ ] US-4: ...

#### Design & Decisões (O "Como" para este incremento)

*Será preenchido durante o desenvolvimento*

**Arquitetura**:
[...]

**Modelagem de Dados**:
[...]

#### Retrospectiva (Lições Aprendidas)

*Será preenchida ao final do incremento*

______________________________________________________________________

### Incremento 3: [Nome do Épico ou Objetivo]

**Status**: Planejado

#### User Stories Alvo

- [ ] US-5: ...
- [ ] US-6: ...

#### Detalhes

*Detalhes mínimos até o momento. Serão expandidos quando este incremento começar.*

______________________________________________________________________

## 4. 🛠️ Definições "As-Built" (O Estado Atual do Produto)

*Esta seção reflete o estado ATUAL do produto em produção/deployment.
É atualizada a cada incremento completado.*

### Arquitetura de Alto Nível (Atual)

[Diagrama ou descrição da arquitetura do sistema como ele existe HOJE]

### Stack Tecnológica (Atual)

- **Backend**: [tecnologias e versões]
- **Frontend**: [tecnologias e versões]
- **Banco de Dados**: [tecnologias e versões]
- **Infraestrutura**: [cloud provider, containers, CI/CD]

### Ambientes & Monitoramento

- **Desenvolvimento**: [URL/config]
- **Homologação**: [URL/config]
- **Produção**: [URL/config]
- **Dashboards**: [Links para observabilidade, logs, métricas]

### Contratos de API (Atual)

[Link para Swagger/OpenAPI ou documentação de endpoints]

### ADRs (Consolidado)

[Link para diretório de Architecture Decision Records ou lista consolidada]

______________________________________________________________________

## 5. 📊 Histórico de Versões

| Versão | Data | Status | Incrementos Completados | Mudanças |
|--------|------|--------|-------------------------|----------|
| 0.1 | YYYY-MM-DD | Descoberta | - | Versão inicial - Problema, Objetivos, KPIs |
| 1.0 | YYYY-MM-DD | MVP Definido | - | MVP definido, YAGNI esclarecido, Roadmap Now/Next/Later |
| 1.1 | YYYY-MM-DD | Incremento 1 Completo | Incremento 1 | [Descrição do que mudou] |
| 1.2 | YYYY-MM-DD | Incremento 2 Completo | Incrementos 1-2 | [Descrição do que mudou] |
| 2.0 | YYYY-MM-DD | Produto Estável | Incrementos 1-N | Documento final (as-built) |

______________________________________________________________________

## 📝 Notas sobre o Uso deste Template

### Filosofia Incremental & YAGNI

Este PRD é estruturado para suportar **desenvolvimento incremental** e **YAGNI (You Ain't Gonna Need It)**:

1. **Design "Just-In-Time"**: O design técnico (arquitetura, dados, APIs) é documentado *dentro* de cada incremento, não antecipadamente. Isso evita sobre-engenharia.

1. **Incrementos, Não Fases**: Não há "Fases de Planejamento" ou "Fases de Design". O design emerge continuamente a cada incremento.

1. **Roadmap Flexível**: "Now, Next, Later" permite repriorização baseada em aprendizados. O Gantt foi substituído por flexibilidade.

1. **As-Built, Não Up-Front**: A seção de "Definições As-Built" reflete o estado *real* do sistema, não o "como gostaríamos que fosse".

1. **Lições Aprendidas por Incremento**: Cada incremento tem sua própria retrospectiva, capturando aprendizados imediatamente para informar os próximos.

### Quando Usar Cada Seção

- **Seção 1 (Visão)**: Mude raramente. Este é o "norte" do produto.
- **Seção 2 (MVP)**: Mude apenas quando a hipótese do MVP for validada/invalidada.
- **Seção 3 (Incrementos)**: Mude a cada ciclo. Esta é a área de **máxima mudança**.
- **Seção 4 (As-Built)**: Atualize após cada incremento completado.
- **Seção 5 (Histórico)**: Atualize a versão ao final de cada incremento significativo.

### Exemplos de Mudanças de Versão

- **v0.1 → v1.0**: Quando o MVP é claramente definido.
- **v1.0 → v1.1**: Quando o Incremento 1 é completado.
- **v1.x → v2.0**: Quando o MVP foi validado e o produto evolui significativamente (mudança de estratégia, novo mercado, etc.).

______________________________________________________________________

## 🎯 Próximas Ações

1. Preencha a **Seção 1** com a visão, problema e KPIs.
1. Defina o **MVP** na **Seção 2**.
1. Comece o primeiro incremento e documente o design **dentro** da **Seção 3**.
1. Após cada incremento, atualize a **Seção 4** (As-Built) com o estado real do sistema.
1. Use a **Seção 5** para rastrear versões e marcos.

**Este é um documento vivo. Adapte conforme necessário!**
