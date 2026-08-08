from agentblueprint_api.celery_app import celery_app
from agentblueprint_config.loader import ConfigLoader
import json


@celery_app.task(bind=True, name="agentblueprint_api.tasks.run_workflow_task")
def run_workflow_task(self, workflow_yaml: str, input_data: str):
    """
    Executes a workflow from its YAML definition.
    """
    try:
        # Save temporary yaml file for loading
        temp_yaml_path = f"/tmp/{self.request.id}_workflow.yaml"
        with open(temp_yaml_path, "w") as f:
            f.write(workflow_yaml)

        loader = ConfigLoader()
        workflow = loader.load_workflow(temp_yaml_path)

        # Run workflow (currently blocking, which is fine for Celery worker)
        result = workflow.run(input_data)

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
