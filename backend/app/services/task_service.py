from typing import List, Optional
from datetime import date
from sqlmodel import Session, select
from backend.app.models.task import Task, TaskCreate, TaskUpdate
from fastapi import HTTPException

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_create: TaskCreate) -> Task:
        """Creates a new task."""
        task = Task.model_validate(task_create)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_tasks(self, is_completed: Optional[bool] = None, due_date: Optional[date] = None, skip: int = 0, limit: int = 100) -> List[Task]:
        """Retrieves a list of tasks, optionally filtered by completion status or due date."""
        query = select(Task)
        if is_completed is not None:
            query = query.where(Task.is_completed == is_completed)
        if due_date is not None:
            query = query.where(Task.due_date == due_date)
        
        tasks = self.session.exec(query.offset(skip).limit(limit)).all()
        return tasks

    def mark_task_status(self, task_id: int, is_completed: bool) -> Task:
        """Marks a task as complete or incomplete."""
        task = self.session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.is_completed = is_completed
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        """Updates a task's description or due date."""
        task = self.session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
            
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int):
        """Deletes a task by its ID."""
        task = self.session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        self.session.delete(task)
        self.session.commit()
        return {"ok": True}
