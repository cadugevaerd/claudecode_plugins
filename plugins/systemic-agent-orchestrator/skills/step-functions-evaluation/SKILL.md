---
description: "This skill activates when the user asks about workflow orchestration, Step Functions vs Agent decision, external workflows, multi-service coordination, or when to use Step Functions instead of LangGraph. Trigger on: 'Step Functions or agent', 'external workflow', 'orchestrate services', 'multi-step process', 'workflow decision'."
---

# Step Functions vs Agent Evaluation Guide

## Core Decision

For every workflow, evaluate: **Does this belong inside the agent or in AWS Step Functions?**

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION FRAMEWORK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │   LangGraph      │         │  Step Functions  │             │
│  │   Agent          │         │  Workflow        │             │
│  ├──────────────────┤         ├──────────────────┤             │
│  │ • LLM decisions  │         │ • No LLM needed  │             │
│  │ • Conversation   │         │ • Long-running   │             │
│  │ • User context   │         │ • Multi-service  │             │
│  │ • Dynamic flow   │         │ • Audit trail    │             │
│  │ • Memory needed  │         │ • Retry/timeout  │             │
│  └──────────────────┘         └──────────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Decision Matrix

| Characteristic | LangGraph Agent | Step Functions |
|---------------|-----------------|----------------|
| Requires LLM reasoning | ✅ Use Agent | ❌ Overkill |
| Conversational context | ✅ Use Agent | ❌ Not designed for |
| User memory needed | ✅ Use Agent | ❌ Limited |
| Long-running (hours/days) | ⚠️ Consider SF | ✅ Use Step Functions |
| Multi-service orchestration | ⚠️ Consider SF | ✅ Use Step Functions |
| Strict audit requirements | ⚠️ Consider SF | ✅ Use Step Functions |
| Complex retry logic | ⚠️ Consider SF | ✅ Use Step Functions |
| Pure data transformation | ❌ Overkill | ✅ Use Step Functions |
| Scheduled/triggered tasks | ⚠️ Consider SF | ✅ Use Step Functions |

---

## Use LangGraph Agent When

### 1. LLM Decision-Making Required

```python
# Agent handles: understanding intent, generating responses
def router_node(state: AgentState) -> str:
    """LLM decides next step based on conversation."""
    model = get_model_for_node("router")
    # LLM analyzes context and decides
    return decision  # "help", "purchase", "complaint"
```

### 2. Conversational Context Matters

```python
class AgentState(TypedDict):
    messages: Annotated[list, add]  # Conversation history
    user_preferences: dict           # From long-term memory
    context: dict                    # Retrieved context
```

### 3. Dynamic, Unpredictable Flow

The flow changes based on user input at runtime:
- User asks follow-up questions
- Clarification needed
- Multi-turn interactions

### 4. Short Execution Time

Agent responds within seconds/minutes, not hours.

---

## Use Step Functions When

### 1. Pure Orchestration (No LLM)

```json
{
  "StartAt": "FetchOrder",
  "States": {
    "FetchOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:fetchOrder",
      "Next": "ProcessPayment"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:processPayment",
      "Next": "SendConfirmation"
    },
    "SendConfirmation": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:sendEmail",
      "End": true
    }
  }
}
```

### 2. Long-Running Processes

- Order fulfillment (hours to days)
- Background data processing
- Batch operations
- Scheduled reports

### 3. Multi-Service Coordination

Coordinating:
- Multiple Lambda functions
- SQS queues
- SNS topics
- External APIs
- Other AWS services

### 4. Audit and Compliance

Step Functions provides:
- Execution history
- State transition logs
- Visual execution trace
- Built-in retry/timeout

---

## Hybrid Pattern: Agent + Step Functions

Often the best solution combines both:

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Request                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌───────────────────┐                                          │
│  │   LangGraph Agent │  ◀─── Handles conversation               │
│  │   (Quick Response)│       Makes decisions                    │
│  └─────────┬─────────┘       Returns to user                    │
│            │                                                     │
│            │ Triggers                                            │
│            ▼                                                     │
│  ┌───────────────────┐                                          │
│  │  Step Functions   │  ◀─── Handles long-running               │
│  │  (Background)     │       Multi-service                      │
│  └───────────────────┘       Retry/timeout logic                │
│            │                                                     │
│            │ Notifies (SNS/EventBridge)                         │
│            ▼                                                     │
│  ┌───────────────────┐                                          │
│  │   LangGraph Agent │  ◀─── Informs user of result             │
│  │   (Status Update) │                                          │
│  └───────────────────┘                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Example: Order Processing

```python
# Agent handles initial request
def process_order_node(state: AgentState) -> dict:
    """Agent confirms order and triggers Step Functions."""
    order = state['pending_order']
    
    # Quick validations (agent)
    if not validate_order(order):
        return {"messages": [AIMessage("I found an issue with your order...")]}
    
    # Trigger Step Functions for fulfillment (background)
    sfn = boto3.client('stepfunctions')
    sfn.start_execution(
        stateMachineArn=ORDER_FULFILLMENT_ARN,
        input=json.dumps(order),
    )
    
    return {
        "messages": [AIMessage("Order confirmed! I'll notify you when it ships.")]
    }
```

---

## Integration Patterns

### Agent Triggers Step Functions

```python
import boto3
import json

def trigger_workflow_node(state: AgentState) -> dict:
    """Trigger external workflow from agent."""
    sfn = boto3.client('stepfunctions')
    
    execution = sfn.start_execution(
        stateMachineArn='arn:aws:states:...:workflow',
        input=json.dumps({
            'user_id': state['user_id'],
            'action': state['requested_action'],
            'data': state['action_data'],
        }),
    )
    
    return {
        "workflow_execution_arn": execution['executionArn'],
        "messages": [AIMessage("I've started the process...")]
    }
```

### Step Functions Calls Agent

```json
{
  "StartAt": "AnalyzeData",
  "States": {
    "AnalyzeData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:analyzeData",
      "Next": "DecideWithAgent"
    },
    "DecideWithAgent": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:callAgent",
      "Parameters": {
        "query": "Based on this data, what action should we take?",
        "context.$": "$.analysisResult"
      },
      "Next": "ExecuteDecision"
    }
  }
}
```

### Agent Monitors Step Functions

```python
def check_workflow_status_node(state: AgentState) -> dict:
    """Check status of running workflow."""
    sfn = boto3.client('stepfunctions')
    
    execution = sfn.describe_execution(
        executionArn=state['workflow_execution_arn']
    )
    
    status = execution['status']
    
    if status == 'SUCCEEDED':
        output = json.loads(execution['output'])
        return {
            "messages": [AIMessage(f"Your request is complete! {output['summary']}")]
        }
    elif status == 'RUNNING':
        return {
            "messages": [AIMessage("Still processing, I'll check again in a moment.")]
        }
    else:
        return {
            "messages": [AIMessage(f"There was an issue: {status}")]
        }
```

---

## Evaluation Checklist

Before implementing, ask:

1. **Does the workflow require natural language understanding?**
   - Yes → Agent
   - No → Step Functions

2. **Is the workflow triggered by user conversation?**
   - Yes → Agent (possibly triggering SF)
   - No → Step Functions

3. **How long does execution take?**
   - Seconds to minutes → Agent
   - Hours to days → Step Functions

4. **Is there complex retry/timeout logic?**
   - Simple or none → Agent
   - Complex → Step Functions

5. **Are multiple AWS services coordinated?**
   - Few, simple → Agent with tools
   - Many, complex → Step Functions

---

## Documentation Pattern

When making a Step Functions decision, document it:

```markdown
# Workflow Decision: {workflow_name}

## Chosen Approach: {Agent / Step Functions / Hybrid}

## Rationale
- {reason_1}
- {reason_2}

## If Agent
- Nodes involved: ...
- Response time expected: ...

## If Step Functions
- State machine name: ...
- Lambda functions: ...
- Estimated duration: ...

## If Hybrid
- Agent responsibilities: ...
- Step Functions responsibilities: ...
- Integration point: ...
```

Save as Serena memory: `arch_workflow_{name}.md`

---

## DO and DON'T

### DO:
- Evaluate every workflow explicitly
- Document the decision rationale
- Use hybrid patterns when appropriate
- Consider execution duration
- Plan for error scenarios

### DON'T:
- Put long-running tasks in agent
- Use agent for pure orchestration
- Skip the evaluation step
- Forget to handle SF failures in agent
- Mix concerns inappropriately
