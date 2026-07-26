from pydantic import BaseModel
from typing import Any, Optional

class WorkflowRunRequest(BaseModel):
    workflow_yaml: str
    input_data: Any
    backend: str = "local" # local, celery, temporal

class WorkflowRunResponse(BaseModel):
    run_id: str
    status: str

class WorkflowStatusResponse(BaseModel):
    run_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
