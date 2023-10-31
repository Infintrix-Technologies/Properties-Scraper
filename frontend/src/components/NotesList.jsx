import React, { useState } from 'react';
import { Input, Button, List } from 'antd';

const NotesList = () => {
  const [task, setTask] = useState('');
  const [tasks, setTasks] = useState([]);

  const handleTaskChange = (e) => {
    setTask(e.target.value);
  };

  const handleAddTask = () => {
    if (task.trim() !== '') {
      setTasks([...tasks, task]);
      setTask('');
    }
  };

  const handleDeleteTask = (index) => {
    const updatedTasks = tasks.filter((_, i) => i !== index);
    setTasks(updatedTasks);
  };

  return (
    <div>
      <h1>To-Do List</h1>
      <Input
        placeholder="Add a new task"
        value={task}
        onChange={handleTaskChange}
        style={{ width: 300, marginRight: 10 }}
      />
      <Button type="primary" onClick={handleAddTask}>
        Add
      </Button>
      <List
        style={{ marginTop: 20, width: 300 }}
        bordered
        dataSource={tasks}
        renderItem={(item, index) => (
          <List.Item
            actions={[
              <Button
                type="link"
                onClick={() => handleDeleteTask(index)}
              >
                Delete
              </Button>
            ]}
          >
            {item}
          </List.Item>
        )}
      />
    </div>
  );
};

export default NotesList;
