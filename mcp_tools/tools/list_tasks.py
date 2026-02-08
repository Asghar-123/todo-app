from typing import List, Optional
from pydantic import BaseModel, Field
import logging
import requests
import os # Import os

logger = logging.getLogger(__name__)

class ListTasksTool(BaseModel):
    """
    Lists all existing todo tasks.
    Can optionally filter by completion status.
    """
    is_completed: Optional[bool] = Field(None, description="Filter tasks by completion status. True for completed, False for incomplete. Leave empty to list all tasks.")

    def run(self) -> str:
        logger.info(f"ListTasksTool called with is_completed='{self.is_completed}'")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        params = {}
        if self.is_completed is not None:
            params["is_completed"] = self.is_completed # requests handles boolean to string conversion

        try:
            response = requests.get(f"{backend_url}/tasks/", params=params)
            response.raise_for_status() # Raise an exception for HTTP errors
            
            tasks = response.json()
            if not tasks:
                return "No tasks found matching the criteria."
            
            task_summaries = []
            for t in tasks:
                due_date_str = f" (Due: {t['due_date']})" if t.get('due_date') else ""
                task_summaries.append(f"- ID: {t['id']}, {t['description']} (Completed: {t['is_completed']}){due_date_str}")
            
            return "Your tasks:\n" + "\n".join(task_summaries)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list tasks: {e}")
            return f"Failed to list tasks: {e}"

if __name__ == "__main__":
    # Example usage (for testing the tool definition)
    tool_instance_all = ListTasksTool()
    print(tool_instance_all.run())

    tool_instance_completed = ListTasksTool(is_completed=True)
    print(tool_instance_completed.run())
