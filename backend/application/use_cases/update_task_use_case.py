from fastapi import HTTPException
from infrastructure.repositories.task_repository import TaskRepository
from presentation.dtos.update_task_dto import PartialTaskDto
from presentation.vo.task_vo import TaskVO


class UpdateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def handle(self, task_id: str, task: PartialTaskDto): # type: ignore
        update_data = task.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided")
        task_updated = self.repository.update_one(task_id, {"$set": update_data})
        return TaskVO(title=task_updated["title"], completed=task_updated["completed"], id=str(task_updated["_id"]), description=task_updated["description"])
        