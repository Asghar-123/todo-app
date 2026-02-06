export const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Task {
  id: number;
  description: string;
  is_completed: boolean;
  owner_id: number;
}

interface TaskCreate {
  description: string;
}

interface TaskUpdate {
  description?: string;
  is_completed?: boolean;
}

export async function getTasks(token: string): Promise<Task[]> {
  const response = await fetch(`${BASE_URL}/tasks/`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to fetch tasks");
  }
  return response.json();
}

export async function createTask(task: TaskCreate, token: string): Promise<Task> {
  const response = await fetch(`${BASE_URL}/tasks/`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(task),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to create task");
  }
  return response.json();
}

export async function updateTask(id: number, task: TaskUpdate, token: string): Promise<Task> {
  const response = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(task),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to update task");
  }
  return response.json();
}

export async function deleteTask(id: number, token: string): Promise<{ ok: boolean }> {
  const response = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to delete task");
  }
  return response.json();
}
