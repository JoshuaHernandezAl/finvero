import type { Task } from "../interfaces/task.interface"

export const CardTask = ({ task, onTaskUpdated }: { task: Task, onTaskUpdated: (task: Task) => void }) => {
  function handleTaskUpdated(e: React.MouseEvent) {
    e.preventDefault();
    const updatedTask = {
      ...task,
      completed: !task.completed,
    };
    const url = `http://127.0.0.1:8000/tasks/${task.id}`;
    fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedTask),
    }).then(() => {
      onTaskUpdated(updatedTask);
    }).catch(err => console.error(err));
  }
  return (
    <div className="card m-3">
      <div className="card-body flex-fill">
        <h5 className="card-title ">{task.title}</h5>
        <p className="card-text fw-bold">What is this task about?</p>
        <p className="card-text">{task.description}</p>
        <p className="card-text"><strong>Status:</strong> {task.completed ? "Completed" : "Not completed"}</p>
        {!task.completed ?
          <button className="btn btn-primary" onClick={handleTaskUpdated}>Complete</button> :

          <button className="btn btn-primary" onClick={handleTaskUpdated}>Uncomplete</button>
        }
      </div>
    </div>
  )
}
