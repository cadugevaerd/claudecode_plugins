---
description: Microprocesso 1.3 - Generate agent spike implementation guide (3-4h) with graph structure, mock tool, tests, and LangSmith validation after validating prerequisites.
---

# 🚀 Microprocesso 1.3: Spike Agentic

**AUTONOMOUS**: This command validates prerequisites and generates a complete implementation guide for your agent spike.

Implement your first agentic architecture in **3-4 hours** with **loop agêntico** (Think → Act → Observe → Think again).

## 🎯 What It Does

1. Validates Microprocesso 1.2 is complete (venv, deps, .env)
2. Checks for README.md from `/brief` (Microprocesso 1.1)
3. **Generates** `docs/microprocesso-1.3-spike-agentic.md` with full implementation guide
4. Shows you what to implement next

## 🚀 Usage

```bash
/spike-agentic
```

**What we'll check:**
- ✅ Virtual environment exists
- ✅ Dependencies installed (langchain, langgraph)
- ✅ .env file with API key
- ✅ README.md from `/brief`

---

## 📋 Implementation Guide Generated

The output file includes:

**Phase 1: Validate Setup** ✅ (Already done by `/setup-local-observability`)

**Phase 2: Build Graph** (60-90 min)
- State definition with TypedDict
- Mock tool implementation
- 4 Nodes (INPUT → AGENT → TOOL → OUTPUT)
- The agentic loop (TOOL → AGENT)
- Route logic function
- Graph compilation

**Phase 3: Run Tests** (30 min)
- Test 1: With tool (validates loop)
- Test 2: Without tool (validates direct response)
- Full test script code

**Phase 4: LangSmith Validation** (30 min)
- Trace verification steps
- Node tree inspection
- Loop confirmation

---

## 💡 The Agentic Loop

```
Without loop (ROUTER):
INPUT → AGENT (decide) → TOOL → OUTPUT → END
         (never observes ❌)

With loop (TRUE AGENT):
INPUT → AGENT (think) → TOOL → AGENT (observe + think) → OUTPUT → END
                           ↑________________________↓
                           (LOOP AGÊNTICO)
```

---

## 📍 Next Steps After Generation

1. Open the generated guide: `docs/microprocesso-1.3-spike-agentic.md`
2. Follow each phase in order
3. Copy code snippets from guide
4. Validate with 2 tests
5. Check LangSmith traces

---

Run it now: `/spike-agentic` 🚀