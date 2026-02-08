from typing import Optional
from pydantic import BaseModel, Field
import logging
import requests # Import requests
import os # Import os

logger = logging.getLogger(__name__)

class MarkTaskStatusTool(BaseModel):
    """
    Marks an existing todo task as complete or incomplete.
    """
    task_id: int = Field(..., description="The ID of the task to mark.")
    is_completed: bool = Field(..., description="The completion status to set (True for complete, False for incomplete).")

    def run(self) -> str:
        logger.info(f"MarkTaskStatusTool called for task_id={self.task_id} with is_completed={self.is_completed}")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

        try:
            response = requests.put(f"{backend_url}/tasks/{self.task_id}", json={"is_completed": self.is_completed})
            response.raise_for_status() # Raise an exception for HTTP errors
            
            updated_task = response.json()
            return f"Task '{updated_task['description']}' (ID: {updated_task['id']}) marked as { 'complete' if updated_task['is_completed'] else 'incomplete'}."
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to mark task {self.task_id} status: {e}")
            return f"Failed to mark task {self.task_id} status: {e}"

if __name__ == "__main__":
    # Example usage (for testing the tool definition)
    tool_instance = MarkTaskStatusTool(task_id=1, is_completed=True)
    print(tool_instance.run())
