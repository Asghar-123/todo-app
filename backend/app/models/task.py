from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel

class TaskBase(SQLModel):
    description: str
    is_completed: bool = Field(default=False)
    due_date: Optional[date] = Field(default=None, index=True) # Optional due date
    
class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[date] = None # Allow updating due date

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to User (implied by conversation history context - will be linked via AI agent context)
    # For now, tasks are not directly owned by a User model in the database,
    # but rather associated through conversation history for a given user session.
    # If a User model becomes explicit later, this will need to be re-evaluated.
