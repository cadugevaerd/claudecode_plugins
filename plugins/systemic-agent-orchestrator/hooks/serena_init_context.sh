#!/usr/bin/env bash

# Output Serena initial_instructions reminder as additionalContext
# This ensures Claude calls initial_instructions at session start

cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "**CRITICAL - SERENA MCP INITIALIZATION**\n\nBefore starting ANY task, you MUST call:\n\n```\nmcp__plugin_systemic-agent-orchestrator_serena__initial_instructions\n```\n\nThis loads the Serena Instructions Manual which is ESSENTIAL for:\n- Using symbolic code analysis tools correctly\n- Managing project memories\n- Editing code with semantic precision\n\nDO NOT skip this step. Call initial_instructions NOW before proceeding with any user request.\n\nAfter calling, you will see 'You have hereby read the Serena Instructions Manual' confirming it loaded."
  }
}
EOF

exit 0
