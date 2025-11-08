# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-08

### Added

- Complete plugin structure and documentation
- Command: `/benchmark-llms` - Create comparative LLM benchmarks
- Command: `/create-eval-suite` - Generate complete evaluation suite structure
- Command: `/create-evaluator` - Generate customized evaluator code
- Command: `/eval-metrics` - List and document available evaluation metrics
- Command: `/eval-patterns` - Show common evaluation code patterns
- Command: `/setup-project-eval` - Configure project CLAUDE.md with evaluation patterns
- Agent: `benchmark-specialist` - Specialized agent for LLM benchmarking
- Agent: `eval-developer` - Specialized agent for LLM evaluation development
- Skill: `benchmark-runner` - Execute comparative LLM benchmarks
- Skill: `evaluation-developer` - Develop LLM evaluator code
- Skill: `langchain-test-specialist` - Create unit and integration tests for LangChain/LangGraph
- Skill: `smoke-test` - Smoke testing expertise for critical functionality validation

### Notes

- Plugin integrates with LangSmith for automatic metrics tracking
- Supports BLEU, ROUGE, F1, Exact Match, LLM-as-Judge and custom metrics
- Compatible with LangChain and LangGraph frameworks
- Follows Claude Code best practices for plugin development
