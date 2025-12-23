#!/usr/bin/env bash

# Output Serena initial_instructions reminder
# Uses systemMessage for visible output + additionalContext for Claude's context

cat << 'EOF'
{
  "systemMessage": "Serena MCP: Call mcp__plugin_systemic-agent-orchestrator_serena__initial_instructions before any task.",
  "additionalContext": "**CRITICAL - SERENA MCP INITIALIZATION**\n\nBefore starting ANY task, you MUST call:\nmcp__plugin_systemic-agent-orchestrator_serena__initial_instructions\n\nThis loads the Serena Instructions Manual. DO NOT skip this step."
}
EOF

exit 0
