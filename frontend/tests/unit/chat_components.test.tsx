/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import ChatInput from '../../src/components/ChatInput';
import TaskList from '../../src/components/TaskList';

// Mock the next/link component if needed for other tests
// jest.mock('next/link', () => {
//   return ({ children }: { children: React.ReactNode }) => {
//     return children;
//   };
// });

describe('ChatInput', () => {
  it('renders correctly', () => {
    const mockOnSendMessage = jest.fn();
    render(<ChatInput onSendMessage={mockOnSendMessage} isLoading={false} />);
    
    expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
  });
});

describe('TaskList', () => {
  it('renders correctly with no tasks', () => {
    render(<TaskList tasks={[]} />);
    expect(screen.getByText('No tasks to display.')).toBeInTheDocument();
  });

  it('renders correctly with tasks', () => {
    const tasks = [
      { id: 1, description: 'Buy groceries', is_completed: false },
      { id: 2, description: 'Walk the dog', is_completed: true, due_date: '2026-02-09' },
    ];
    render(<TaskList tasks={tasks} />);
    
    expect(screen.getByText('Buy groceries')).toBeInTheDocument();
    expect(screen.getByText('Walk the dog')).toBeInTheDocument();
    expect(screen.getByText('(Due: 2026-02-09)')).toBeInTheDocument();
  });
});
