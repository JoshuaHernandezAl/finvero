from pydantic import BaseModel


class TaskVO(BaseModel):
  id: str
  title: str
  completed: bool
  description: str