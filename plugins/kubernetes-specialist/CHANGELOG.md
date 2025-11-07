# Changelog - Kubernetes Specialist Plugin

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-07

### Added

- **MCP Integration**: Added `kubernetes-toolkit` MCP server for direct Kubernetes API access

  - 40+ tools for resource management and diagnostics
  - Direct API integration (faster than kubectl)
  - Automatic authentication via kubeconfig
  - `.mcp.json` configuration with environment variable support
  - `.env.example` template for MCP configuration

- **Skill**: `k8s-troubleshooting-patterns` - Diagnostic patterns for common pod failures

  - Covers: CrashLoopBackOff, OOMKilled, ImagePullBackOff, Pending pods, CreateContainerConfigError
  - Includes: kubectl debug commands, diagnostic decision trees, prevention strategies
  - 2025 best practices: Exponential backoff, exit codes, ephemeral containers
  - 426 lines of diagnostic guidance and examples

- **Agent Enhancements**: Both agents now reference skills and MCP toolkit

  - `k8s-resource-analyzer`: Loads knowledge from skills before execution, prefers MCP tools
  - `k8s-troubleshooter`: Enhanced with priority-ordered tool access (Skills → MCP → kubectl)

### Changed

- Updated `k8s-resource-analyzer` agent (82 → 112 lines)

  - Added "Load Knowledge from Skills" step (FIRST priority)
  - MCP kubernetes-toolkit as preferred method for resource collection
  - kubectl as fallback with documented commands
  - New "Tools Available" section with priority ordering

- Updated `k8s-troubleshooter` agent (85 → 118 lines)

  - Added "Load Troubleshooting Knowledge" step (ALWAYS FIRST)
  - MCP tool priority: Skills → MCP → WebSearch → kubectl
  - Enhanced failure classification with skill cross-references
  - New comprehensive "Tools Available" section with priority guidance

- Enhanced README.md

  - Added "MCP Server Integration" section with configuration details
  - Security best practices for 2025 documented
  - Read-only mode configuration for production use
  - Environment variables for MCP customization

### Technical Details

- **Version Bump**: 1.0.0 → 1.1.0 (MINOR - new features, backward compatible)
- **Plugin Tags**: Added "mcp" and "model-context-protocol"
- **Agent Health Scores**:
  - `k8s-resource-analyzer`: 88/100 → 95/100 ⬆️
  - `k8s-troubleshooter`: 90/100 → 96/100 ⬆️

### Security

- ✅ All API traffic encrypted with TLS
- ✅ Authentication via kubeconfig certificates
- ✅ Optional read-only mode prevents destructive operations
- ✅ No hardcoded credentials in configuration
- ✅ RBAC validation enforced
- ✅ Audit logging for all operations

______________________________________________________________________

## [1.0.0] - 2025-11-06

### Initial Release

- Kubernetes Specialist plugin with 3 slash commands
- 2 specialized agents for resource analysis and troubleshooting
- 1 comprehensive skill for best practices
- Support for Kubernetes 1.25+
- Full documentation and examples
