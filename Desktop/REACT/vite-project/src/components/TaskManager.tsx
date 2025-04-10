import React, { useState, useEffect } from 'react';

interface Task {
  id: number;
  text: string;
}

const TaskManager: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState('');
  const [editId, setEditId] = useState<number | null>(null);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) setTasks(JSON.parse(savedTasks));
  }, []);

  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  const handleAddTask = () => {
    if (!newTask.trim()) return;
    if (editId !== null) {
      setTasks(tasks.map(task => task.id === editId ? { ...task, text: newTask } : task));
      setEditId(null);
    } else {
      setTasks([...tasks, { id: Date.now(), text: newTask }]);
    }
    setNewTask('');
  };

  const handleEdit = (id: number, text: string) => {
    setNewTask(text);
    setEditId(id);
  };

  const handleDelete = (id: number) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  return (
    <div className={darkMode ? 'container dark' : 'container'}>
      <h1>Task Manager</h1>
      <div className="controls">
        <input
          value={newTask}
          onChange={e => setNewTask(e.target.value)}
          placeholder="Enter task"
        />
        <button onClick={handleAddTask}>{editId !== null ? 'Update' : 'Add'}</button>
        <button onClick={toggleDarkMode}>{darkMode ? 'Light Mode' : 'Dark Mode'}</button>
      </div>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            {task.text}
            <div className="actions">
              <button onClick={() => handleEdit(task.id, task.text)}>Edit</button>
              <button onClick={() => handleDelete(task.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskManager;