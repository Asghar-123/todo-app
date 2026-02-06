from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from apps.backend.src.database import get_session
from apps.backend.src.models.task import Task, TaskCreate, TaskRead, TaskUpdate

router = APIRouter()

@router.post("/tasks/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new task. Temporarily sets owner_id to 1.
    """
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[TaskRead])
def read_tasks(
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks (temporarily without user filtering).
    """
    tasks = session.exec(select(Task)).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID (temporarily without user filtering).
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update an existing task by ID (temporarily without user filtering).
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a task by ID (temporarily without user filtering).
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}