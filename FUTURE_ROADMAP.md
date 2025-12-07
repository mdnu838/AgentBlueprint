# Future Enhancements & Roadmap

This document outlines the planned future features and architectural improvements for **AgentBlueprint**.

## 🔮 Phase 7: Advanced Memory & Persistence
- **Vector Database Integration**: Support for Chroma, Pinecone, and Qdrant to allow agents to retrieve documents from a knowledge base.
- **Long-term Persistence**: SQLite or PostgreSQL backend to store conversation history and workflow states efficiently.

## 🔮 Phase 8: Enhanced LLM Support
- **Multi-Provider Support**: Add first-class integrations for:
    - Anthropic (Claude)
    - Google Gemini
    - Ollama (Local LLMs)
- **Token Usage Tracking**: Monitor and report token consumption and costs across agents.

## 🔮 Phase 9: Tool Marketplace & Plugins
- **Plugin System**: Allow users to install tool packs via `ab install <package>`.
- **OpenAPI Integration**: Automatically generate tools from OpenAPI/Swagger specifications.

## 🔮 Phase 10: Enterprise Features
- **Distributed Execution**: Use Celery or Temporal.io for running workflows on distributed worker clusters.
- **REST API Server**: Expose workflows as HTTP endpoints (FastAPI integration).
- **Web UI**: A visual builder and monitoring dashboard for workflows.

## 🔮 Phase 11: Evaluation & Optimization
- **Auto-Evaluation**: Framework for agents to evaluate other agents' outputs.
- **Prompt Optimization**: Tools to auto-tune system prompts based on success metrics.
