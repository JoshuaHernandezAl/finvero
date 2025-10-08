from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from application.use_cases.create_task_use_case import CreateTaskUseCase
from application.use_cases.delete_use_case import DeleteUseCase
from application.use_cases.get_tasks_use_case import GetTasksUseCase
from application.use_cases.update_task_use_case import UpdateTaskUseCase
from infrastructure.config.db.mongo_connection import MongoConnection
from infrastructure.config.settings import Settings
from infrastructure.repositories.task_repository import TaskRepository


mongo_conn = MongoConnection(db_name=Settings().mongo_db)


def get_settings():
    return Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_conn.connect()
    yield
    mongo_conn.close()

def get_db():
    return mongo_conn.get_db()


def get_task_repository():
    db = get_db()
    collection = db["tasks"]
    return TaskRepository(collection)


def create_task_use_case(repository: TaskRepository = Depends(get_task_repository)):
    return CreateTaskUseCase(repository)

def get_tasks_use_case(repository: TaskRepository = Depends(get_task_repository)):
    return GetTasksUseCase(repository)

def update_task_use_case(repository: TaskRepository = Depends(get_task_repository)):
    return UpdateTaskUseCase(repository)

def delete_task_use_case(repository: TaskRepository = Depends(get_task_repository)):
    return DeleteUseCase(repository)
