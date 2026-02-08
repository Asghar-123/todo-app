"use client";

import React from 'react';

interface Task {
  id: number;
  description: string;
  is_completed: boolean;
  due_date?: string; // Optional due date, as string for display
}

interface TaskListProps {
  tasks: Task[];
}

const TaskList: React.FC<TaskListProps> = ({ tasks }) => {
  if (tasks.length === 0) {
    return <div className="p-4 text-gray-500">No tasks to display.</div>;
  }

  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <li key={task.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={task.is_completed}
              readOnly // Tasks are updated via chat, not direct UI interaction here
              className="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-not-allowed"
            />
            <span className={`ml-3 text-lg ${task.is_completed ? "line-through text-gray-500" : "text-gray-800"}`}>
              {task.description}
            </span>
            {task.due_date && (
              <span className="ml-3 text-sm text-gray-400">
                (Due: {task.due_date})
              </span>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
