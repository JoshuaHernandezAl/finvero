import pytest
from bson import ObjectId


def test_create_task_success(client):
    payload = {"title": "Task A", "description": "Desc A", "completed": False}
    resp = client.post("/tasks/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert set(data.keys()) == {"id", "title", "completed"}
    assert data["title"] == payload["title"]
    assert data["completed"] is False
    assert ObjectId.is_valid(data["id"]) is True


def test_create_task_validation_error(client):
    payload = {"title": "a", "description": "ok", "completed": False}
    resp = client.post("/tasks/", json=payload)
    assert resp.status_code == 422


def test_get_tasks_list(client):
    client.post("/tasks/", json={"title": "Task 1", "description": "Desc 1", "completed": False})
    client.post("/tasks/", json={"title": "Task 2", "description": "Desc 2", "completed": True})

    resp = client.get("/tasks/")
    assert resp.status_code == 200
    data = resp.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 2
    for item in data["tasks"]:
        assert set(item.keys()) == {"id", "title", "completed"}
        assert ObjectId.is_valid(item["id"]) is True


def test_update_task_success(client):
    create = client.post("/tasks/", json={"title": "Old", "description": "Desc", "completed": False})
    assert create.status_code == 201
    task_id = create.json()["id"]

    resp = client.put(f"/tasks/{task_id}", json={"title": "New"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == task_id
    assert data["title"] == "New"
    assert data["completed"] is False


def test_update_task_no_data_provided(client):
    create = client.post("/tasks/", json={"title": "Old2", "description": "Desc", "completed": False})
    assert create.status_code == 201
    task_id = create.json()["id"]

    resp = client.put(f"/tasks/{task_id}", json={})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "No data provided"


def test_update_task_invalid_id_format(client):
    bad_id = "not-a-valid-objectid"
    resp = client.put(f"/tasks/{bad_id}", json={"title": "Xxx"})
    assert resp.status_code == 400
    assert resp.json()["detail"].startswith("Invalid ObjectId:")


def test_delete_task_success(client):
    create = client.post("/tasks/", json={"title": "Del", "description": "Desc", "completed": False})
    assert create.status_code == 201
    task_id = create.json()["id"]

    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Task deleted successfully"}


def test_delete_task_invalid_id_format(client):
    bad_id = "123"
    resp = client.delete(f"/tasks/{bad_id}")
    assert resp.status_code == 400
    assert resp.json()["detail"].startswith("Invalid ObjectId:")
