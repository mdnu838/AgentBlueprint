# AgentBlueprint Internal Documentation

This folder contains internal development documentation, task tracking, and design decisions.

**⚠️ This folder is gitignored and not part of the public repository.**

---

## 📋 Contents

- **[TASK_TRACKER.md](TASK_TRACKER.md)** - Master task list with status tracking
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed architecture decisions
- **[MODULE_VALIDATION.md](MODULE_VALIDATION.md)** - Validation checklist for each module
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing strategy and checklist

---

## 🔄 Development Workflow

1. Check **[TASK_TRACKER.md](TASK_TRACKER.md)** for next task
2. Implement in appropriate package under `packages/`
3. Create validation script in `experiments/`
4. Run validation and update task status
5. Write tests in package `tests/` folder
6. Update documentation

---

## 🧪 Experiments Folder Usage

The `experiments/` folder is for:
- Quick validation scripts for each module
- Prototyping new features
- Performance benchmarks
- Integration testing before writing formal tests

### Naming Convention

```
experiments/
├── validate_agent.py           # Validates agentblueprint-core/agent.py
├── validate_workflow.py        # Validates agentblueprint-core/workflow.py
├── validate_cli_init.py        # Validates agentblueprint-cli/commands/init.py
├── benchmarks/                 # Performance tests
└── prototypes/                 # Feature prototypes
```

---

## 📊 Status Indicators

- ⬜ **Not Started** - Task not begun
- 🚧 **In Progress** - Currently being worked on
- ✅ **Complete** - Implementation done and validated
- ⚠️ **Blocked** - Waiting on dependencies
- 🔄 **Review** - Ready for code review

---

## 🎯 Current Focus

**Phase:** 1.2 - Core Infrastructure
**Next Tasks:** 
1. Implement Tool base class
2. Implement ToolRegistry
3. Implement Agent class

---

**Last Updated:** 26 November 2025
