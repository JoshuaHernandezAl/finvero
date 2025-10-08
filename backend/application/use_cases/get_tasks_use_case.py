from infrastructure.repositories.task_repository import TaskRepository
from presentation.models.tasks_response_model import TasksResponseModel
from presentation.vo.task_vo import TaskVO


class GetTasksUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def handle(self):
        tasks = self.repository.get_all()
        return TasksResponseModel(
            tasks=[
                TaskVO(
                    title=task["title"],
                    completed=task["completed"],
                    id=str(task["_id"]),
                    description=task["description"]
                )
                for task in tasks
            ]
        )
