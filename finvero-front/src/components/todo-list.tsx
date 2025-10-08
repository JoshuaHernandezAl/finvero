import { useEffect, useState } from "react"
import { CardTask } from "./card-task"
import type { Task } from "../interfaces/task.interface";
import { FormTask } from "./form-task";


export const TodoList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addTask = (newTask: Task) => {
    setTasks(prev => [...prev, newTask]);
  };
  const updateTask = (updatedTask: Task) => {
    setTasks(prev => prev.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  useEffect(() => {
    setIsLoading(true);
    fetch("http://127.0.0.1:8000/tasks")
      .then(res => res.json())
      .then(data => {
        setTasks(data.tasks);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return <div>Loading...</div>
  }
  if (tasks.length === 0) {
    return <div>Create a task</div>
  }
  return (
    <>
      <h2>Create new todo</h2>
      <FormTask onTaskCreated={addTask} />
      <div className="mt-5">
        <h2>Todos:</h2>
        <div className="d-flex p-5">
          {
            tasks.map((task) => {
              return <CardTask key={task.id} task={task} onTaskUpdated={updateTask} />
            })
          }
        </div>
      </div>
    </>

  )
}
