from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
import logging
import requests # Import requests
import os # Import os

logger = logging.getLogger(__name__)

class UpdateTaskTool(BaseModel):
    """
    Updates an existing todo task. Can update description or due date.
    """
    task_id: int = Field(..., description="The ID of the task to update.")
    description: Optional[str] = Field(None, description="The new description for the task.")
    due_date: Optional[date] = Field(None, description="The new due date for the task in YYYY-MM-DD format.")

    def run(self) -> str:
        logger.info(f"UpdateTaskTool called for task_id={self.task_id} with description='{self.description}' and due_date='{self.due_date}'")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        update_data = {}
        if self.description:
            update_data["description"] = self.description
        if self.due_date:
            update_data["due_date"] = str(self.due_date)

        try:
            response = requests.put(f"{backend_url}/tasks/{self.task_id}", json=update_data)
            response.raise_for_status() # Raise an exception for HTTP errors
            
            updated_task = response.json()
            return f"Task '{updated_task['description']}' (ID: {updated_task['id']}) updated successfully."
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update task {self.task_id}: {e}")
            return f"Failed to update task {self.task_id}: {e}"

if __name__ == "__main__":
    # Example usage (for testing the tool definition)
    tool_instance = UpdateTaskTool(task_id=1, description="A new description")
    print(tool_instance.run())
