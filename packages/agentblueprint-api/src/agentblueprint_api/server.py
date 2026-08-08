import uuid
from fastapi import FastAPI, HTTPException
from agentblueprint_api.schemas import WorkflowRunRequest, WorkflowRunResponse, WorkflowStatusResponse
from agentblueprint_api.tasks import run_workflow_task
from celery.result import AsyncResult
from agentblueprint_api.celery_app import celery_app
from temporalio.client import Client
from agentblueprint_api.temporal_app import AgentBlueprintTemporalWorkflow
from fastapi.middleware.cors import CORSMiddleware
import threading

app = FastAPI(title="AgentBlueprint API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allows all origins. Adjust for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory store for local executions
_runs = {}

@app.post("/workflows/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest):
    run_id = str(uuid.uuid4())

    if request.backend == "local":
        _runs[run_id] = {"status": "pending", "result": None, "error": None}

        # Define local runner
        def run_local():
            try:
                from agentblueprint_config.loader import ConfigLoader
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".yaml") as f:
                    f.write(request.workflow_yaml)
                    temp_path = f.name

                loader = ConfigLoader()
                workflow = loader.load_workflow(temp_path)
                result = workflow.run(request.input_data)
                _runs[run_id] = {"status": "completed", "result": result, "error": None}
            except Exception as e:
                _runs[run_id] = {"status": "error", "result": None, "error": str(e)}

        # Start a background thread to execute it without blocking the endpoint
        threading.Thread(target=run_local).start()

        return WorkflowRunResponse(run_id=run_id, status="pending")
    elif request.backend == "celery":
        task = run_workflow_task.apply_async(args=[request.workflow_yaml, request.input_data])
        return WorkflowRunResponse(run_id=task.id, status="pending")
    elif request.backend == "temporal":
        try:
            client = await Client.connect("localhost:7233")
            handle = await client.start_workflow(
                AgentBlueprintTemporalWorkflow.run,
                args=[request.workflow_yaml, request.input_data],
                id=run_id,
                task_queue="agentblueprint-task-queue",
            )
            # Store run_id to indicate it's temporal
            _runs[run_id] = {"backend": "temporal"}
            return WorkflowRunResponse(run_id=run_id, status="pending")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start Temporal workflow: {e}")
    else:
        raise HTTPException(status_code=400, detail=f"Backend '{request.backend}' not fully implemented yet.")

@app.get("/workflows/{run_id}/status", response_model=WorkflowStatusResponse)
async def get_workflow_status(run_id: str):
    if run_id in _runs:
        return WorkflowStatusResponse(
            run_id=run_id,
            status=_runs[run_id]["status"],
            result=_runs[run_id]["result"],
            error=_runs[run_id]["error"]
        )

    # Check Temporal backend
    if run_id in _runs and _runs[run_id].get("backend") == "temporal":
        try:
            client = await Client.connect("localhost:7233")
            handle = client.get_workflow_handle(run_id)

            # This is a basic way to check status, might need describing the workflow to get exact status
            desc = await handle.describe()
            status_map = {
                1: "running",
                2: "completed",
                3: "failed",
                4: "canceled",
                5: "terminated",
                6: "timed_out",
            }
            status_enum = desc.status
            status_str = status_map.get(status_enum, "unknown")

            if status_str == "completed":
                # Note: this awaits result which might block if it's not completed,
                # but we only call it if status_str == completed
                res = await handle.result()
                if isinstance(res, dict):
                     return WorkflowStatusResponse(
                        run_id=run_id,
                        status=res.get("status", "completed"),
                        result=res.get("result"),
                        error=res.get("error")
                    )
                return WorkflowStatusResponse(run_id=run_id, status="completed", result=res)
            else:
                return WorkflowStatusResponse(run_id=run_id, status=status_str)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Check Celery backend
    try:
        task_result = AsyncResult(run_id, app=celery_app)
        if task_result.ready():
            res = task_result.result
            if isinstance(res, dict):
                return WorkflowStatusResponse(
                    run_id=run_id,
                    status=res.get("status", "completed"),
                    result=res.get("result"),
                    error=res.get("error")
                )
            return WorkflowStatusResponse(run_id=run_id, status="completed", result=res)
        else:
            return WorkflowStatusResponse(run_id=run_id, status="pending")
    except Exception as e:
        pass

    raise HTTPException(status_code=404, detail="Run ID not found")

@app.get("/workflows/{run_id}/logs")
async def get_workflow_logs(run_id: str):
    if run_id in _runs:
        return {"logs": ["Log stream not implemented for local backend yet."]}
    raise HTTPException(status_code=404, detail="Run ID not found")
