from datetime import datetime

from pydantic import BaseModel, ConfigDict

class TaskSchema(BaseModel):
    title: str
    description: str
    completed: bool
    created_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
    )