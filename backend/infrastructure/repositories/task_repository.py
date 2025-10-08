import datetime

from bson import ObjectId
from domain.entities.task_schema import TaskSchema
from presentation.dtos.task_dto import TaskDto


class TaskRepository:
    def __init__(self, collection):
        self.collection = collection

    def create(self, task_data: TaskDto) -> dict:
        task = TaskSchema(**task_data.__dict__, created_at=datetime.datetime.now())
        task_dict = task.__dict__
        result = self.collection.insert_one(task_dict)
        task_dict["id"] = str(result.inserted_id)
        return task_dict
    
    def get_all(self):
        return self.collection.find()

    def update_one(self, task_id: str, query: dict):
        self.collection.update_one(
            {"_id": ObjectId(task_id)},
            query
        )
        return self.collection.find_one({"_id": ObjectId(task_id)})
    
    def delete_one(self, task_id: str):
        self.collection.delete_one({"_id": ObjectId(task_id)})