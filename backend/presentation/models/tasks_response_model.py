from pydantic import BaseModel

from presentation.vo.task_vo import TaskVO


class TasksResponseModel(BaseModel):
  tasks: list[TaskVO]