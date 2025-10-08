import os
import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
from typing import Dict, Any


class InMemoryTaskRepository:
    def __init__(self):
        self.items: Dict[str, Dict[str, Any]] = {}

    def create(self, task_data):
        _id = ObjectId()
        doc = {
            "_id": _id,
            "title": task_data.title,
            "description": getattr(task_data, "description", ""),
            "completed": getattr(task_data, "completed", False),
        }
        self.items[str(_id)] = doc
        return {"id": str(_id), "title": doc["title"], "completed": doc["completed"]}

    def get_all(self):
        return list(self.items.values())

    def update_one(self, task_id: str, query: dict):
        doc = self.items.get(task_id)
        if not doc:
            raise KeyError("Not found")
        if "$set" in query:
            for k, v in query["$set"].items():
                if k in ("title", "description", "completed"):
                    doc[k] = v
        self.items[task_id] = doc
        return {"_id": ObjectId(task_id), "title": doc["title"], "completed": doc["completed"]}

    def delete_one(self, task_id: str):
        self.items.pop(task_id, None)


@pytest.fixture
def fake_repo():
    return InMemoryTaskRepository()


@pytest.fixture
def client(fake_repo):
    os.environ.setdefault("MONGO_DB", "testdb")
    os.environ.setdefault("MONGO_HOST", "localhost")
    os.environ.setdefault("MONGO_PORT", "27017")
    os.environ.setdefault("MONGO_USERNAME", "user")
    os.environ.setdefault("MONGO_PASSWORD", "pass")
    os.environ.setdefault("MONGO_AUTH_SOURCE", "admin")

    from main import app
    import domain.adapters.dependencies as deps

    deps.mongo_conn.connect = lambda: None
    deps.mongo_conn.close = lambda: None

    app.dependency_overrides[deps.get_task_repository] = lambda: fake_repo

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
