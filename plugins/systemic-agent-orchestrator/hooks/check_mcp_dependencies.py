#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Check for required MCP server dependencies at session start.
Provides installation guidance if dependencies are missing.
"""
import json
import sys

REQUIRED_PLUGINS = {
    'langchain-ecosystem-helper': {
        'description': 'LangGraph and LangChain documentation',
        'install': 'claude mcp add langchain-ecosystem-helper',
        'mcp_tools': ['SearchDocsByLangChain']
    },
    'aws-documentation-helper': {
        'description': 'AWS documentation and best practices',
        'install': 'claude mcp add aws-documentation-helper',
        'mcp_tools': ['aws___search_documentation', 'aws___read_documentation']
    }
}

RECOMMENDED_PLUGINS = {
    'serena': {
        'description': 'Semantic code analysis and project memories',
        'note': 'Enables API integration memories and semantic code navigation',
        'install': 'Configure in settings.json with serena MCP server'
    }
}


def main():
    try:
        # Build informational message
        lines = [
            "",
            "=== Systemic Agent Orchestrator - MCP Dependencies ===",
            "",
            "This plugin works best with the following MCP servers:",
            "",
            "RECOMMENDED (install for full functionality):",
        ]

        for plugin_name, info in REQUIRED_PLUGINS.items():
            lines.extend([
                f"",
                f"  {plugin_name}:",
                f"    Purpose: {info['description']}",
                f"    Install: {info['install']}",
            ])

        lines.extend([
            "",
            "OPTIONAL (enhanced features):",
        ])

        for plugin_name, info in RECOMMENDED_PLUGINS.items():
            lines.extend([
                f"",
                f"  {plugin_name}:",
                f"    Purpose: {info['description']}",
                f"    Note: {info['note']}",
            ])

        lines.extend([
            "",
            "If you see 'MCP tool not found' errors, install the plugins above.",
            "Use '/systemic-agent-orchestrator:check-deps' to verify dependencies.",
            "",
            "================================================",
            ""
        ])

        result = {
            "systemMessage": "\n".join(lines)
        }
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({
            "systemMessage": f"Warning: MCP dependency check error: {str(e)}"
        }))


if __name__ == "__main__":
    main()
