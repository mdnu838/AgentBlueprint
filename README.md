# AgentBlueprint

**AgentBlueprint** is a lightweight, fast, and flexible project scaffolding tool for Python frameworks and AI agents. It focuses on simplicity, essential features, and clean starter templates — without unnecessary complexity.

Terminal command prefix: **`ab`**

---

## 🚀 Overview

AgentBlueprint helps you quickly generate structured, ready-to-run project templates. Whether you're starting a Flask API, a FastAPI service, a Django project, or an AI Agent, AgentBlueprint sets up the folders, configs, and basic code so you can start building immediately.

---

## ✨ Core Features (Simplified)

### 🔧 Clean, Minimal Framework Scaffolding

Generate basic project structures for:

* **FastAPI**
* **Flask**
* **Django**
* **OpenAPI-based services**
* **TensorFlow inference API basics**
* **Simple combinations** (e.g., FastAPI + OpenAI)

No over-complicated integrations. Only essential boilerplate.

### 🧠 Agent Generator (`ab agent`)

Bootstrap an AI agent with:

* Basic agent loop
* Configurable tool system
* A small set of built-in tools:

  * Search
  * Math/Calculator
  * File Reader
  * Simple HTTP Request tool

The goal: a clean starting point, not an overloaded framework.

### 🧩 Optional Tool Packs (Simplified)

Add minimal optional packs:

```
ab agent --toolpack basic
ab agent --toolpack ai
```

These packs remain lightweight.

### 🔨 Optional DevOps Essentials

(Optional, not required)

* Dockerfile
* requirements.txt
* Basic GitHub Actions workflow

### 📘 Documentation Templates

* Simple README
* Basic API docs (if generating FastAPI)

---

## 🧱 Example Folder Structure

```
myproject/
  app/
    main.py
  agent/
    core.py
    tools/
  config/
    settings.yaml
  requirements.txt
  README.md
```

---

## 🖥 Basic Commands

### Create a web project

```
ab fastapi
ab flask
ab django
```

### Create an AI agent

```
ab agent
ab agent --toolpack basic
```

### Add optional devops

```
ab deploy docker
```

---

## 🧭 Roadmap (Simplified)

* Expand clean templates for more frameworks
* Add a few more lightweight tools for agents
* Improve CLI help & ergonomics

---

## 📄 License

MIT

---

## 🤝 Contributions

Contributions welcome — keep additions simple and focused.

---

## 🌟 Summary

AgentBlueprint is a **simple, clean, and practical** scaffolding generator for Python projects and AI agents. It avoids bloat and focuses on what developers need most: a strong, minimal foundation to build on.
