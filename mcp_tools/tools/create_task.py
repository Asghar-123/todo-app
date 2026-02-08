from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
import logging
import requests # Import requests

logger = logging.getLogger(__name__)

class CreateTaskTool(BaseModel):
    """
    Creates a new todo task.
    """
    description: str = Field(..., description="The description of the todo task.")
    due_date: Optional[date] = Field(None, description="The optional due date for the task in YYYY-MM-DD format.")

    def run(self) -> str:
        logger.info(f"CreateTaskTool called with description='{self.description}' and due_date='{self.due_date}'")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000") # Get backend URL from env
        
        task_data = {"description": self.description}
        if self.due_date:
            task_data["due_date"] = str(self.due_date) # Convert date to string for JSON

        try:
            response = requests.post(f"{backend_url}/tasks/", json=task_data)
            response.raise_for_status() # Raise an exception for HTTP errors
            
            created_task = response.json()
            return f"Task '{created_task['description']}' (ID: {created_task['id']}) created successfully."
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create task '{self.description}': {e}")
            return f"Failed to create task '{self.description}': {e}"

if __name__ == "__main__":
    # Example usage (for testing the tool definition)
    tool_instance = CreateTaskTool(description="Buy groceries", due_date=date(2026, 2, 9))
    print(tool_instance.run())

    tool_instance_no_date = CreateTaskTool(description="Read a book")
    print(tool_instance_no_date.run())
