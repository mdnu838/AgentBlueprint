from agentblueprint_api.celery_app import celery_app
from agentblueprint_config.loader import ConfigLoader
import json
import asyncio
import tempfile
import os

@celery_app.task(bind=True, name="agentblueprint_api.tasks.run_workflow_task")
def run_workflow_task(self, workflow_yaml: str, input_data: str):
    """
    Executes a workflow from its YAML definition.
    """
    temp_yaml_path = None
    try:
        # Save temporary yaml file for loading
        with tempfile.NamedTemporaryFile(mode="w", suffix="_workflow.yaml", delete=False) as f:
            temp_yaml_path = f.name
            f.write(workflow_yaml)

        loader = ConfigLoader()
        workflow = loader.load_workflow(temp_yaml_path)

        # Run workflow (currently blocking, which is fine for Celery worker)
        result = workflow.run(input_data)

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        if temp_yaml_path and os.path.exists(temp_yaml_path):
            os.unlink(temp_yaml_path)
