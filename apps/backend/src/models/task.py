from typing import Optional
from sqlmodel import Field, SQLModel

class TaskBase(SQLModel):
    description: str
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

class TaskUpdate(SQLModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

