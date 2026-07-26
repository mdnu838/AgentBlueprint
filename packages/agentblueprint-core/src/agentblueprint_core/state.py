"""
State persistence for workflows.
"""
from typing import Dict, Any
import json
from pydantic import BaseModel, Field

class WorkflowStateStore(BaseModel):
    """Abstract base class for storing workflow states."""

    def save_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        """Save workflow state."""
        raise NotImplementedError

    def load_state(self, workflow_id: str) -> Dict[str, Any]:
        """Load workflow state."""
        raise NotImplementedError

try:
    from sqlalchemy import create_engine, Column, String, Text, DateTime
    from sqlalchemy.orm import declarative_base, sessionmaker
    import datetime

    StateBase = declarative_base()

    class WorkflowState(StateBase):
        __tablename__ = 'workflow_states'
        workflow_id = Column(String(255), primary_key=True)
        state_json = Column(Text)
        updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

except ImportError:
    StateBase = None
    WorkflowState = None

_state_engine_cache = {}

def _get_state_engine_and_session(db_url: str):
    if StateBase is None:
        raise ImportError("sqlalchemy is required for SQLWorkflowStateStore. Install with `pip install sqlalchemy`.")

    if db_url not in _state_engine_cache:
        engine = create_engine(db_url)
        StateBase.metadata.create_all(engine)
        session_maker = sessionmaker(bind=engine)
        _state_engine_cache[db_url] = (engine, session_maker)

    return _state_engine_cache[db_url]


class SQLWorkflowStateStore(WorkflowStateStore):
    """
    SQL-backed workflow state store using SQLAlchemy.
    """
    db_url: str

    engine: Any = Field(default=None, exclude=True)
    session_maker: Any = Field(default=None, exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.engine, self.session_maker = _get_state_engine_and_session(self.db_url)

    def save_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        session = self.session_maker()
        try:
            # Check if exists
            db_state = session.query(WorkflowState).filter_by(workflow_id=workflow_id).first()
            state_json_str = json.dumps(state)

            if db_state:
                db_state.state_json = state_json_str
            else:
                db_state = WorkflowState(workflow_id=workflow_id, state_json=state_json_str)
                session.add(db_state)

            session.commit()
        finally:
            session.close()

    def load_state(self, workflow_id: str) -> Dict[str, Any]:
        session = self.session_maker()
        try:
            db_state = session.query(WorkflowState).filter_by(workflow_id=workflow_id).first()
            if db_state and db_state.state_json:
                return json.loads(db_state.state_json)
            return {}
        finally:
            session.close()
