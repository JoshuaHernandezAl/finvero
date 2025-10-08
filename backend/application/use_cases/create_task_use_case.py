from infrastructure.repositories.task_repository import TaskRepository
from presentation.dtos.task_dto import TaskDto
from presentation.vo.task_vo import TaskVO


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def handle(self, task: TaskDto):
        task = self.repository.create(task)
        return TaskVO(title=task["title"], completed=task["completed"], id=task["id"], description=task["description"])
