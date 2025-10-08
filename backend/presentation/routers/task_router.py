from fastapi import APIRouter, Body, Depends, Path

from application.use_cases.delete_use_case import DeleteUseCase
from application.use_cases.update_task_use_case import UpdateTaskUseCase
from domain.adapters.dependencies import create_task_use_case, delete_task_use_case, get_tasks_use_case, update_task_use_case
from presentation.dtos.task_dto import TaskDto
from presentation.dtos.update_task_dto import PartialTaskDto
from presentation.dtos.utils.validation_mongo_id import validate_mongo_id
from presentation.models.tasks_response_model import TasksResponseModel
from presentation.vo.task_vo import TaskVO


task_router = APIRouter(prefix=f"/tasks", tags=["Tasks"])


@task_router.post("/", status_code=201, response_model=TaskVO)
async def create_tasks(
    task: TaskDto = Body(...), create_task_use_case=Depends(create_task_use_case)
):
    return create_task_use_case.handle(task)


@task_router.get("/", response_model=TasksResponseModel, status_code=200)
def get_tasks(get_tasks_use_case=Depends(get_tasks_use_case)):
    return get_tasks_use_case.handle()


@task_router.put("/{task_id}", status_code=200, response_model=TaskVO)
def update_task(
    task_id: str = Path(...), 
    task: PartialTaskDto = Body(...),  # type: ignore
    update_use_case: UpdateTaskUseCase = Depends(update_task_use_case)):
    validate_mongo_id(task_id)
    return update_use_case.handle(task_id, task)


@task_router.delete("/{task_id}", status_code=200, response_model=dict)
def delete_task(task_id: str = Path(...), delete_use_case: DeleteUseCase = Depends(delete_task_use_case)):
    validate_mongo_id(task_id)
    delete_use_case.handle(task_id)
    return {"message": "Task deleted successfully"}
