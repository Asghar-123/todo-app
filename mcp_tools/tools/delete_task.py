from pydantic import BaseModel, Field
import logging
import requests # Import requests
import os # Import os

logger = logging.getLogger(__name__)

class DeleteTaskTool(BaseModel):
    """
    Deletes an existing todo task by its ID.
    """
    task_id: int = Field(..., description="The ID of the task to delete.")

    def run(self) -> str:
        logger.info(f"DeleteTaskTool called for task_id={self.task_id}")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

        try:
            response = requests.delete(f"{backend_url}/tasks/{self.task_id}")
            response.raise_for_status() # Raise an exception for HTTP errors
            
            return f"Task ID {self.task_id} deleted successfully."
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete task {self.task_id}: {e}")
            return f"Failed to delete task {self.task_id}: {e}"

if __name__ == "__main__":
    # Example usage (for testing the tool definition)
    tool_instance = DeleteTaskTool(task_id=1)
    print(tool_instance.run())
