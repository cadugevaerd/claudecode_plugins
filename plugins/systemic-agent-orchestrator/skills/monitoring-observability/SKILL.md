---
description: "This skill activates when the user asks about monitoring, observability, CloudWatch, Langsmith tracing, alerts, dashboards, or debugging agents in production. Trigger on: 'monitoring', 'observability', 'CloudWatch logs', 'Langsmith traces', 'alerts', 'dashboard', 'debug production'."
---

# Monitoring & Observability Guide

## Overview

Three pillars of observability for AI agents:
1. **Langsmith** - LLM traces, prompts, evaluations
2. **CloudWatch** - Infrastructure logs and metrics
3. **Custom Metrics** - Business KPIs

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 OBSERVABILITY STACK                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    LANGSMITH                               │ │
│  │  • LLM call traces                                         │ │
│  │  • Token usage                                             │ │
│  │  • Latency per model                                       │ │
│  │  • Prompt versions                                         │ │
│  │  • Evaluation datasets                                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   CLOUDWATCH                               │ │
│  │  Logs:                                                     │ │
│  │  • Agent runtime logs                                      │ │
│  │  • API Gateway access logs                                 │ │
│  │  • ECS container logs                                      │ │
│  │                                                            │ │
│  │  Metrics:                                                  │ │
│  │  • ECS CPU/Memory                                          │ │
│  │  • API Gateway latency                                     │ │
│  │  • Aurora connections                                      │ │
│  │                                                            │ │
│  │  Alarms:                                                   │ │
│  │  • Error rate > threshold                                  │ │
│  │  • Latency > SLA                                           │ │
│  │  • Memory > 80%                                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                 CUSTOM METRICS                             │ │
│  │  • Conversations completed                                 │ │
│  │  • Resolution rate                                         │ │
│  │  • User satisfaction                                       │ │
│  │  • Escalation rate                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Langsmith Integration

### Configuration

```python
import os

# Environment variables (required)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."
os.environ["LANGCHAIN_PROJECT"] = "my-agent-prod"
```

### Trace Metadata

Add context to traces:

```python
from langchain_core.tracers import LangChainTracer

tracer = LangChainTracer(
    project_name="my-agent-prod",
    tags=["production", "v1.2.0"],
)

# In node functions
def planner_node(state: AgentState) -> dict:
    model = get_model_for_node("planner")
    
    # Add run metadata
    response = model.invoke(
        formatted_prompt,
        config={
            "callbacks": [tracer],
            "metadata": {
                "user_id": state.get("user_id"),
                "session_id": state.get("session_id"),
                "version": "1.2.0",
            }
        }
    )
    return {"messages": [response]}
```

### Custom Feedback

```python
from langsmith import Client

client = Client()

# Log feedback for evaluation
client.create_feedback(
    run_id=run_id,
    key="user_rating",
    score=5.0,
    comment="User marked as helpful"
)
```

---

## CloudWatch Logs

### Log Retention Enforcement

| Environment | Retention |
|-------------|-----------|
| Development | 1 day |
| Homologation | 3 days |
| Production | 7 days |

### Structured Logging

```python
import json
import logging
from datetime import datetime

class StructuredLogger:
    """Structured JSON logging for CloudWatch."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log(self, level: str, message: str, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        self.logger.info(json.dumps(log_entry))

# Usage
logger = StructuredLogger("agent")

logger.log(
    "INFO",
    "Request processed",
    user_id="user-123",
    session_id="sess-456",
    node="planner",
    duration_ms=245,
    tokens_used=150
)
```

### CloudWatch Insights Queries

**Error analysis:**
```sql
fields @timestamp, @message, level, node, error
| filter level = "ERROR"
| stats count(*) as error_count by node
| sort error_count desc
| limit 10
```

**Latency by node:**
```sql
fields @timestamp, node, duration_ms
| filter duration_ms > 0
| stats avg(duration_ms) as avg_latency, p95(duration_ms) as p95_latency by node
| sort avg_latency desc
```

**Token usage:**
```sql
fields @timestamp, node, tokens_used
| stats sum(tokens_used) as total_tokens by node
| sort total_tokens desc
```

---

## CloudWatch Alarms

### Terraform Configuration

```hcl
# modules/monitoring/alarms.tf

resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "${var.project_name}-${var.environment}-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5XXError"
  namespace           = "AWS/ApiGateway"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "API error rate too high"
  
  dimensions = {
    ApiId = var.api_gateway_id
  }
  
  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
  
  tags = var.common_tags
}

resource "aws_cloudwatch_metric_alarm" "high_latency" {
  alarm_name          = "${var.project_name}-${var.environment}-high-latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "IntegrationLatency"
  namespace           = "AWS/ApiGateway"
  period              = 60
  extended_statistic  = "p95"
  threshold           = 5000  # 5 seconds
  alarm_description   = "API latency p95 > 5s"
  
  dimensions = {
    ApiId = var.api_gateway_id
  }
  
  alarm_actions = [aws_sns_topic.alerts.arn]
  
  tags = var.common_tags
}

resource "aws_cloudwatch_metric_alarm" "ecs_high_memory" {
  alarm_name          = "${var.project_name}-${var.environment}-ecs-high-memory"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "ECS memory > 80%"
  
  dimensions = {
    ClusterName = var.ecs_cluster
    ServiceName = var.ecs_service
  }
  
  alarm_actions = [aws_sns_topic.alerts.arn]
  
  tags = var.common_tags
}
```

---

## CloudWatch Dashboard

```hcl
# modules/monitoring/dashboard.tf

resource "aws_cloudwatch_dashboard" "agent" {
  dashboard_name = "${var.project_name}-${var.environment}"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "text"
        x      = 0
        y      = 0
        width  = 24
        height = 1
        properties = {
          markdown = "# ${var.project_name} Agent Dashboard - ${upper(var.environment)}"
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 1
        width  = 8
        height = 6
        properties = {
          title   = "API Requests"
          region  = var.aws_region
          metrics = [
            ["AWS/ApiGateway", "Count", "ApiId", var.api_gateway_id, { stat = "Sum" }]
          ]
          period = 300
        }
      },
      {
        type   = "metric"
        x      = 8
        y      = 1
        width  = 8
        height = 6
        properties = {
          title   = "API Latency (p95)"
          region  = var.aws_region
          metrics = [
            ["AWS/ApiGateway", "IntegrationLatency", "ApiId", var.api_gateway_id, { stat = "p95" }]
          ]
          period = 300
        }
      },
      {
        type   = "metric"
        x      = 16
        y      = 1
        width  = 8
        height = 6
        properties = {
          title   = "Errors"
          region  = var.aws_region
          metrics = [
            ["AWS/ApiGateway", "5XXError", "ApiId", var.api_gateway_id, { stat = "Sum", color = "#d62728" }],
            ["AWS/ApiGateway", "4XXError", "ApiId", var.api_gateway_id, { stat = "Sum", color = "#ff7f0e" }]
          ]
          period = 300
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 7
        width  = 12
        height = 6
        properties = {
          title   = "ECS CPU & Memory"
          region  = var.aws_region
          metrics = [
            ["AWS/ECS", "CPUUtilization", "ClusterName", var.ecs_cluster, "ServiceName", var.ecs_service],
            ["AWS/ECS", "MemoryUtilization", "ClusterName", var.ecs_cluster, "ServiceName", var.ecs_service]
          ]
          period = 300
        }
      },
      {
        type   = "log"
        x      = 12
        y      = 7
        width  = 12
        height = 6
        properties = {
          title  = "Recent Errors"
          region = var.aws_region
          query  = "SOURCE '/agent/${var.project_name}/${var.environment}' | filter level = 'ERROR' | sort @timestamp desc | limit 20"
        }
      }
    ]
  })
}
```

---

## Custom Business Metrics

```python
import boto3
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')

def emit_metric(metric_name: str, value: float, dimensions: dict):
    """Emit custom metric to CloudWatch."""
    cloudwatch.put_metric_data(
        Namespace='AgentMetrics',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': k, 'Value': v}
                    for k, v in dimensions.items()
                ],
                'Timestamp': datetime.utcnow()
            }
        ]
    )

# Usage in nodes
def end_conversation_node(state: AgentState) -> dict:
    """End conversation and emit metrics."""
    
    # Emit conversation completed
    emit_metric(
        'ConversationsCompleted',
        1,
        {
            'Agent': 'my-agent',
            'Environment': 'prod',
            'Resolution': state.get('resolution_type', 'unknown')
        }
    )
    
    # Emit resolution time
    if state.get('start_time'):
        duration = (datetime.utcnow() - state['start_time']).total_seconds()
        emit_metric(
            'ResolutionTime',
            duration,
            {'Agent': 'my-agent'}
        )
    
    return {"phase": "complete"}
```

---

## Debugging Production Issues

### 1. Check Langsmith Traces

1. Go to https://smith.langchain.com
2. Filter by project and time range
3. Look for:
   - High latency runs
   - Failed runs
   - Unusual token counts

### 2. Check CloudWatch Logs

```bash
# Recent errors
aws logs filter-log-events \
  --log-group-name /agent/my-agent/prod \
  --filter-pattern "ERROR" \
  --start-time $(date -d '1 hour ago' +%s000)

# Specific user
aws logs filter-log-events \
  --log-group-name /agent/my-agent/prod \
  --filter-pattern "user-123"
```

### 3. Check ECS Task Status

```bash
# List running tasks
aws ecs list-tasks \
  --cluster my-agent-prod \
  --service-name my-agent-agent

# Describe task
aws ecs describe-tasks \
  --cluster my-agent-prod \
  --tasks <task-arn>
```

---

## DO and DON'T

### DO:
- Enable Langsmith tracing in all environments
- Use structured JSON logging
- Set up alarms for critical metrics
- Create dashboards per environment
- Log user/session IDs for debugging
- Enforce log retention limits

### DON'T:
- Log sensitive user data
- Skip CloudWatch alarms
- Use unstructured logs
- Ignore Langsmith feedback
- Exceed log retention (cost!)
- Forget custom business metrics
