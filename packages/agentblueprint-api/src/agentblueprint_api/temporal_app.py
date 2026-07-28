import asyncio
from datetime import timedelta

from agentblueprint_config.loader import ConfigLoader
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@activity.defn
async def run_workflow_activity(workflow_yaml: str, input_data: str) -> dict:
    """Activity that actually executes the AgentBlueprint workflow."""
    try:
        import uuid
        temp_yaml_path = f"/tmp/{uuid.uuid4()}_workflow.yaml"

        def write_file():
            with open(temp_yaml_path, "w") as f:
                f.write(workflow_yaml)
        await asyncio.to_thread(write_file)

        loader = ConfigLoader()
        wf = loader.load_workflow(temp_yaml_path)

        # We assume run() is synchronous or we can await it if we wrap it properly
        result = wf.run(input_data)

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@workflow.defn
class AgentBlueprintTemporalWorkflow:
    @workflow.run
    async def run(self, workflow_yaml: str, input_data: str) -> dict:
        return await workflow.execute_activity(
            run_workflow_activity,
            args=[workflow_yaml, input_data],
            schedule_to_close_timeout=timedelta(minutes=5),
        )

async def start_worker():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="agentblueprint-task-queue",
        workflows=[AgentBlueprintTemporalWorkflow],
        activities=[run_workflow_activity],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(start_worker())
