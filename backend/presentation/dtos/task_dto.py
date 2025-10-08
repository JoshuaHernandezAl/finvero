from pydantic import BaseModel, Field


class TaskDto(BaseModel):
  title: str = Field(..., min_length=3, max_length=100)
  description: str = Field(..., min_length=3, max_length=100)
  completed: bool = Field(default=False)