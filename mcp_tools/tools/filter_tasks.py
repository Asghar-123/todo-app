from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field
import logging
import requests # Import requests
import os # Import os

logger = logging.getLogger(__name__)

class FilterTasksTool(BaseModel):
    """
    Filters and lists todo tasks based on various criteria.
    """
    is_completed: Optional[bool] = Field(None, description="Filter tasks by completion status. True for complete, False for incomplete.")
    due_date: Optional[date] = Field(None, description="Filter tasks by a specific due date in YYYY-MM-DD format.")

    def run(self) -> str:
        logger.info(f"FilterTasksTool called with is_completed='{self.is_completed}' and due_date='{self.due_date}'")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        params = {}
        if self.is_completed is not None:
            params["is_completed"] = self.is_completed
        if self.due_date is not None:
            params["due_date"] = str(self.due_date)

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
            
            return "Filtered tasks:\n" + "\n".join(task_summaries)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to filter tasks: {e}")
            return f"Failed to filter tasks: {e}"

if __name__ == "__main__":
    # Example usage (for testing the tool definition)
    tool_instance_completed = FilterTasksTool(is_completed=True)
    print(tool_instance_completed.run())

    tool_instance_due_date = FilterTasksTool(due_date=date(2026, 2, 9))
    print(tool_instance_due_date.run())

    tool_instance_all = FilterTasksTool()
    print(tool_instance_all.run())
