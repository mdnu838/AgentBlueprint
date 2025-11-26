# AgentBlueprint AI Coding Agent Instructions

## Project Overview

AgentBlueprint is a **uv-powered Python mono-repo** for building multi-agent systems. The project supports two workflows: **config-first** (YAML/JSON for beginners) and **code-first** (Python API for developers).

**Current State:** Planning phase - folder structure and documentation exist, but implementation is pending (Phase 1.2 in TASK_TRACKER.md).

## Architecture

### Mono-Repo Structure (uv workspace)

- **4 independent packages** in `packages/`: `core`, `cli`, `tools`, `config`
- Root `pyproject.toml` defines uv workspace with `members = ["packages/*"]`
- Each package has its own `pyproject.toml`, `src/`, `tests/`, and `README.md`
- Dependencies: Pydantic v2.0+ for validation, Click 8.1+ for CLI, httpx/beautifulsoup4 for tools

### Package Responsibilities

1. **agentblueprint-core** - Core runtime: `Tool`, `Agent`, `Workflow`, `Memory`, LLM providers
2. **agentblueprint-config** - YAML/JSON loading, Pydantic schemas, env var substitution
3. **agentblueprint-tools** - Pre-built tools: `WebSearchTool`, `HTTPClientTool`, `ShellTool`, etc.
4. **agentblueprint-cli** - `ab` command with subcommands: `init`, `run`, `config`, `tools list/add`

### Key Design Patterns

- **Abstract base classes** for extensibility (see `ARCHITECTURE.md` lines 45-77 for `Tool` base class)
- **Registry pattern** for tool discovery (`ToolRegistry` in core package)
- **Pydantic models** for config validation and type safety
- **Dual interfaces**: YAML configs (examples/quickstart_config/) AND Python API (examples/quickstart_cli/)

## Critical Developer Workflows

### Implementation Workflow (Must Follow)

```bash
# 1. Pick task from TASK_TRACKER.md (internal_docs/)
# 2. Implement in packages/<package>/src/
# 3. Create validation script in experiments/
python experiments/validate_<module>.py
# 4. Fix issues, re-validate
# 5. Write formal tests in packages/<package>/tests/
pytest packages/<package>/tests/
# 6. Update TASK_TRACKER.md status to ✅
```

**Never skip validation scripts** - they catch integration issues before formal tests.

### Environment Setup

```bash
uv sync                    # Install all workspace dependencies
uv pip list                # Verify packages installed
uv run pytest              # Run all tests
uv run ruff check .        # Lint
uv run mypy packages/      # Type check
```

### Creating New Modules

1. **Follow ARCHITECTURE.md** (internal_docs/) for class designs - full implementations provided
2. **Use validation template** from MODULE_VALIDATION.md (internal_docs/)
3. **Check dependencies** in TASK_TRACKER.md dependency graph before starting
4. **Example**: Tool base class must exist before ToolRegistry, Agent, or any concrete tools

## Project-Specific Conventions

### File Organization

- Source code: `packages/<pkg>/src/agentblueprint_<pkg>/`
- Tests: `packages/<pkg>/tests/test_<module>.py`
- Validation: `experiments/validate_<module>.py`
- Examples: `examples/<use_case>/` with workflow.yaml + README.md

### Gitignored Internal Folders

- **experiments/** - Validation scripts, prototypes, benchmarks (not public)
- **internal_docs/** - Task tracking, architecture decisions, testing guides (not public)
- Public docs go in `docs/` (not created yet) or package READMEs

### Naming Conventions

- Packages: `agentblueprint-<name>` (hyphenated)
- Python modules: `agentblueprint_<name>` (underscored)
- CLI command: `ab` (short for AgentBlueprint)
- Tools: `<Name>Tool` suffix (e.g., `WebSearchTool`)

### Type Hints & Validation

- **Python 3.10+ required** - use modern type hints (`list[str]`, `dict[str, Any]`)
- **Pydantic v2** for all configs - see `AgentConfig` in ARCHITECTURE.md
- **mypy strict mode** - all functions must have return types
- **ruff** configured in root pyproject.toml: line-length=100, select E/F/I/N/W/UP

## Code Examples from Architecture

### Tool Implementation Pattern (from ARCHITECTURE.md)

```python
from agentblueprint_core import Tool

class CustomTool(Tool):
    name = "custom_tool"
    description = "Does something specific"
    
    def run(self, **kwargs) -> str:
        # Implementation
        return result
```

### Config-First Workflow (from examples/quickstart_config/workflow.yaml)

```yaml
agents:
  researcher:
    model: openai:gpt-4
    system_prompt: "You are a researcher..."
    tools: [web_search, python_repl]

workflow:
  type: sequential
  steps:
    - id: research
      agent: researcher
      input: "{{ user_input }}"
      output_var: research_notes
```

## Integration Points

- **LLM Providers**: OpenAI, Anthropic via abstract `LLMProvider` interface (core package)
- **Config Loaders**: YAML/JSON → Pydantic models → Core runtime (config package)
- **CLI → Core**: `ab run` loads YAML → ConfigLoader → Workflow.execute() (cli + config + core)
- **External APIs**: Tools use httpx for HTTP, require API keys in env vars

## What NOT to Do

- ❌ Don't implement without validation script first
- ❌ Don't create files in experiments/ or internal_docs/ that should be public
- ❌ Don't skip dependency order - follow TASK_TRACKER.md dependency graph
- ❌ Don't use Python <3.10 features (no Union[], use `|` instead)
- ❌ Don't install packages individually - use `uv sync` for workspace

## Quick Reference

- **Task list**: `internal_docs/TASK_TRACKER.md` (200+ tasks, 4 phases)
- **Class designs**: `internal_docs/ARCHITECTURE.md` (complete implementations)
- **Validation template**: `internal_docs/MODULE_VALIDATION.md`
- **Current focus**: Phase 1.2 - Implement Tool, ToolRegistry, Agent (see TASK_TRACKER.md)
- **Entry point**: Start with `packages/agentblueprint-core/src/agentblueprint_core/tools.py`

---

**Next Steps for AI Agents:**
1. Read TASK_TRACKER.md to find current task status
2. Follow implementation workflow above
3. Reference ARCHITECTURE.md for exact class implementations
4. Use validation scripts before formal tests
