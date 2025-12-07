# Publishing to PyPI

This project is configured to automatically publish to PyPI using GitHub Actions when changes are pushed to `main`.

## Setup Checklist

Before the first publish can succeed, you must configure **Trusted Publishing** on PyPI.

1.  **Create PyPI Projects**:
    You need to register the following package names on [PyPI](https://pypi.org/) (or ensure they are available):
    *   `agentblueprint`
    *   `agentblueprint-core`
    *   `agentblueprint-cli`
    *   `agentblueprint-tools`
    *   `agentblueprint-config`
    
    *If these names are taken, you will need to rename them in the respective `pyproject.toml` files.*

2.  **Configure Trusted Publishing**:
    For **EACH** package above on PyPI:
    *   Go to **Manage Project** > **Publishing**.
    *   Choose **GitHub** as the publisher.
    *   **Owner**: `mdnu838` (your GitHub username)
    *   **Repository code**: `AgentBlueprint`
    *   **Workflow name**: `publish.yml`
    *   **Environment**: (Leave empty or set to `pypi`)

3.  **Versioning**:
    PyPI does not allow overwriting versions. Before merging to `main`, ensure you have bumped the `version` in the `pyproject.toml` of any package you modified.

## How it works

The workflow in `.github/workflows/publish.yml`:
1.  Installs `uv`.
2.  Builds all 5 packages (root + 4 workspace members) into `dist/`.
3.  Uploads all artifacts to PyPI using `pypa/gh-action-pypi-publish`.
