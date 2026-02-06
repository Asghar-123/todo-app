"use client";

import { useState, useEffect, FormEvent } from "react";
import { getTasks, createTask, updateTask, deleteTask } from "../../../lib/tasks"; // Adjust path as needed

interface Task {
  id: number;
  description: string;
  is_completed: boolean;
}

// Dummy token for testing without login/signup
// In a real application, this would come from authentication context
const DUMMY_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTczNTY4OTYwMH0.B-26WlT9g3a1Jz7N02hLw8-fX2m6Ff6F5g5Q5F5Q5F5"; // Replace with a valid token if you have one, or generate a dummy one

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editingTaskDescription, setEditingTaskDescription] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const fetchedTasks = await getTasks(DUMMY_TOKEN);
      setTasks(fetchedTasks);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: FormEvent) => {
    e.preventDefault();
    if (!newTaskDescription.trim()) return;

    try {
      await createTask({ description: newTaskDescription }, DUMMY_TOKEN);
      setNewTaskDescription("");
      fetchTasks(); // Refresh tasks
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleUpdateTask = async (id: number, updates: { description?: string; is_completed?: boolean }) => {
    try {
      await updateTask(id, updates, DUMMY_TOKEN);
      fetchTasks(); // Refresh tasks
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await deleteTask(id, DUMMY_TOKEN);
      fetchTasks(); // Refresh tasks
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <div className="p-4">Loading tasks...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">My Todo List</h1>

      <form onSubmit={handleCreateTask} className="w-full max-w-md bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">Add New Task</h2>
        <div className="flex gap-2">
          <input
            type="text"
            value={newTaskDescription}
            onChange={(e) => setNewTaskDescription(e.target.value)}
            placeholder="What needs to be done?"
            className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-5 py-3 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Add Task
          </button>
        </div>
      </form>

      <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">Tasks</h2>
        {tasks.length === 0 ? (
          <p className="text-gray-500">No tasks yet. Add one above!</p>
        ) : (
          <ul>
            {tasks.map((task) => (
              <li key={task.id} className="flex items-center justify-between bg-gray-50 p-3 rounded-md mb-3 last:mb-0 shadow-sm">
                {editingTaskId === task.id ? (
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      handleUpdateTask(task.id, { description: editingTaskDescription });
                      setEditingTaskId(null); // Exit edit mode
                    }}
                    className="flex-grow flex items-center gap-2"
                  >
                    <input
                      type="text"
                      value={editingTaskDescription}
                      onChange={(e) => setEditingTaskDescription(e.target.value)}
                      className="flex-grow p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      type="submit"
                      className="bg-green-500 text-white px-3 py-1 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 text-sm"
                    >
                      Save
                    </button>
                    <button
                      type="button"
                      onClick={() => setEditingTaskId(null)}
                      className="bg-gray-500 text-white px-3 py-1 rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 text-sm"
                    >
                      Cancel
                    </button>
                  </form>
                ) : (
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={task.is_completed}
                      onChange={() => handleUpdateTask(task.id, { is_completed: !task.is_completed })}
                      className="mr-3 h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
                    />
                    <span className={`text-lg ${task.is_completed ? "line-through text-gray-500" : "text-gray-800"}`}>
                      {task.description}
                    </span>
                  </div>
                )}
                <div className="flex gap-2 ml-4">
                  {editingTaskId !== task.id && ( // Only show edit button if not currently editing
                    <button
                      onClick={() => {
                        setEditingTaskId(task.id);
                        setEditingTaskDescription(task.description);
                      }}
                      className="bg-yellow-500 text-white px-3 py-1 rounded-md hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 text-sm"
                    >
                      Edit
                    </button>
                  )}
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 text-sm"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
