"use client";

import React, { useState, useEffect } from 'react';
import ChatInput from './components/ChatInput';
import TaskList from './components/TaskList';

interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
}

interface Task {
  id: number;
  description: string;
  is_completed: boolean;
  due_date?: string;
}

interface ConversationHistoryEntry {
  id: number;
  user_id: string;
  message_content: string;
  message_type: 'user' | 'bot';
  timestamp: string; // ISO format string
}

async function sendChatMessage(message: string, userId: string): Promise<{ response: string; tasks?: Task[] }> {
  try {
    const res = await fetch('http://localhost:8000/chat/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, user_id: userId }),
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'Failed to fetch');
    }

    const data = await res.json();
    return data;
  } catch (error: any) {
    console.error('Error sending message:', error);
    return { response: `Error: ${error.message}` };
  }
}

async function fetchChatHistory(userId: string): Promise<ConversationHistoryEntry[]> {
  try {
    const res = await fetch(`http://localhost:8000/chat/history/${userId}`);
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'Failed to fetch chat history');
    }
    const data: ConversationHistoryEntry[] = await res.json();
    return data;
  } catch (error: any) {
    console.error('Error fetching chat history:', error);
    return [];
  }
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState("dummy_user"); // Hardcoded for now, will come from auth later
  const [error, setError] = useState<string | null>(null); // New error state

  useEffect(() => {
    const loadHistory = async () => {
      setError(null); // Clear previous errors
      const history = await fetchChatHistory(userId);
      if (history === null) { // Handle potential error from fetchChatHistory
        setError("Failed to load chat history.");
        return;
      }
      const formattedMessages: ChatMessage[] = history.map(entry => ({
        sender: entry.message_type,
        text: entry.message_content,
      }));
      setMessages(formattedMessages);
      if (formattedMessages.length === 0) {
        setMessages([{ sender: 'bot', text: 'Hello! How can I help you with your tasks today?' }]);
      }
    };
    loadHistory();
  }, [userId]);


  const handleSendMessage = async (text: string) => {
    const userMessage: ChatMessage = { sender: 'user', text };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setIsLoading(true);
    setError(null); // Clear previous errors

    try {
      const botResponse = await sendChatMessage(text, userId);
      
      const botChatMessage: ChatMessage = { sender: 'bot', text: botResponse.response };
      setMessages((prevMessages) => [...prevMessages, botChatMessage]);

      if (botResponse.tasks) {
        setTasks(botResponse.tasks);
      }
    } catch (err: any) {
      setError(err.message || "An unknown error occurred while sending message.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 text-gray-800">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <h1 className="text-2xl font-bold">AI Todo Chatbot</h1>
      </header>

      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {error && ( // Display error message
          <div className="text-red-600 bg-red-100 p-3 rounded-md mb-4">
            Error: {error}
          </div>
        )}
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs p-3 rounded-lg shadow-md ${
                msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-xs p-3 rounded-lg shadow-md bg-gray-200 text-gray-800">
              Bot is typing...
            </div>
          </div>
        )}
        
        {tasks.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-2">Current Tasks:</h2>
            <TaskList tasks={tasks} />
          </div>
        )}
      </div>

      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default App;