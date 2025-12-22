---
name: Triggers and Events
description: This skill should be used when the user asks about Composio triggers, webhooks, event-driven workflows, real-time notifications, polling, or automated actions. Trigger on questions like 'set up webhook with Composio', 'trigger on new email', 'event-driven agent', 'real-time notifications', 'automated workflows'.
version: 1.0.0
---

# Composio Triggers and Events

Provide comprehensive guidance on Composio's trigger system for event-driven AI agent workflows.

## When to Use This Skill

Use when user asks about:
- Setting up webhooks for events
- Real-time notifications
- Event-driven agent workflows
- Polling-based triggers
- Automated actions on events
- Trigger configuration

## Core Concepts

### What are Triggers?

Triggers allow AI agents to respond to real-time events:
- **New email received** → Agent processes and responds
- **GitHub issue created** → Agent triages and labels
- **Slack message** → Agent answers questions
- **Calendar event** → Agent sends reminders

### Trigger Types

1. **Webhook-based**: Real-time push notifications
2. **Polling-based**: Periodic checks for changes
3. **Custom**: Define your own trigger logic

## Implementation

### Setting Up a Trigger

```python
from composio import ComposioToolSet, Trigger

toolset = ComposioToolSet()

# Create trigger listener
listener = toolset.create_trigger_listener()

# Subscribe to specific trigger
@listener.on(Trigger.GMAIL_NEW_EMAIL)
def handle_new_email(event):
    """Called when new email arrives"""
    print(f"New email from: {event.data['from']}")
    print(f"Subject: {event.data['subject']}")

    # Process with AI agent
    response = agent.run(f"Summarize this email: {event.data['body']}")
    return response

# Start listening
listener.start()
```

```typescript
import { ComposioToolSet, Trigger } from "@composio/core";

const toolset = new ComposioToolSet();

const listener = toolset.createTriggerListener();

listener.on(Trigger.GMAIL_NEW_EMAIL, async (event) => {
    console.log(`New email from: ${event.data.from}`);

    // Process with AI agent
    const response = await agent.run(
        `Summarize this email: ${event.data.body}`
    );
    return response;
});

listener.start();
```

### Available Triggers

| App | Trigger | Event |
|-----|---------|-------|
| Gmail | GMAIL_NEW_EMAIL | New email received |
| Slack | SLACK_NEW_MESSAGE | Message in channel |
| GitHub | GITHUB_NEW_ISSUE | Issue created |
| GitHub | GITHUB_NEW_PR | Pull request opened |
| Calendar | CALENDAR_EVENT_START | Event starting soon |
| Notion | NOTION_PAGE_UPDATED | Page modified |

### Configuring Trigger Parameters

```python
# Trigger with filters
@listener.on(
    Trigger.GITHUB_NEW_ISSUE,
    filters={
        "repo": "myorg/myrepo",
        "labels": ["bug"]
    }
)
def handle_bug_issues(event):
    """Only triggered for bug issues in specific repo"""
    pass
```

### Entity-Scoped Triggers

```python
# Triggers for specific user
listener = toolset.create_trigger_listener(
    entity_id="user_123"
)

@listener.on(Trigger.GMAIL_NEW_EMAIL)
def handle_user_email(event):
    # Only this user's emails
    pass
```

## Event Data Structure

```python
event = {
    "trigger": "GMAIL_NEW_EMAIL",
    "entity_id": "user_123",
    "timestamp": "2025-01-15T10:30:00Z",
    "data": {
        "from": "sender@example.com",
        "to": "user@example.com",
        "subject": "Meeting Tomorrow",
        "body": "...",
        "attachments": []
    }
}
```

## Use Cases

### Email Auto-Responder

```python
@listener.on(Trigger.GMAIL_NEW_EMAIL)
def auto_respond(event):
    # Analyze email with AI
    analysis = agent.run(f"""
        Analyze this email and draft a response:
        From: {event.data['from']}
        Subject: {event.data['subject']}
        Body: {event.data['body']}
    """)

    # Send response using Gmail action
    toolset.execute_action(
        action="GMAIL_SEND_EMAIL",
        params={
            "to": event.data['from'],
            "subject": f"Re: {event.data['subject']}",
            "body": analysis
        },
        entity_id=event.entity_id
    )
```

### GitHub Issue Triage

```python
@listener.on(Trigger.GITHUB_NEW_ISSUE)
def triage_issue(event):
    # AI classifies the issue
    classification = agent.run(f"""
        Classify this GitHub issue:
        Title: {event.data['title']}
        Body: {event.data['body']}

        Return: bug, feature, question, or docs
    """)

    # Add label
    toolset.execute_action(
        action="GITHUB_ADD_LABELS",
        params={
            "issue_number": event.data['number'],
            "labels": [classification]
        },
        entity_id=event.entity_id
    )
```

### Slack Q&A Bot

```python
@listener.on(Trigger.SLACK_NEW_MESSAGE)
def answer_questions(event):
    if event.data['text'].startswith("@bot"):
        question = event.data['text'].replace("@bot", "").strip()

        answer = agent.run(f"Answer: {question}")

        toolset.execute_action(
            action="SLACK_SEND_MESSAGE",
            params={
                "channel": event.data['channel'],
                "text": answer
            },
            entity_id=event.entity_id
        )
```

## Best Practices

1. **Filter Events**: Use filters to reduce noise
2. **Error Handling**: Wrap handlers in try/catch
3. **Idempotency**: Handle duplicate events gracefully
4. **Rate Limiting**: Don't overwhelm external APIs
5. **Logging**: Log all trigger events for debugging

## Webhook Configuration

### Setting Up Webhook URL

```python
# Get webhook URL for your trigger
webhook_url = toolset.get_trigger_webhook_url(
    trigger=Trigger.GITHUB_NEW_ISSUE,
    entity_id="user_123"
)

# Configure in GitHub settings
print(f"Add this webhook to GitHub: {webhook_url}")
```

## Documentation Sources

> **Note**: Use GitHub sources as `docs.composio.dev` may block automated requests.

### Primary Sources (GitHub - Always Works)
- **README**: https://raw.githubusercontent.com/ComposioHQ/composio/master/README.md
- **Python SDK**: https://raw.githubusercontent.com/ComposioHQ/composio/master/python/README.md

### Search for Specific Docs
Use WebSearch: `Composio triggers webhooks site:docs.composio.dev`

Fetch latest documentation from GitHub for current trigger availability.
