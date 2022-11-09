import requests
import pytest

ENDPOINT = "https://todo.pixegami.io"

def new_task_payload():
    return {
        "content": "some content",
        "user_id": "paula",
        "is_done": False
    }

def create_task():
    payload = new_task_payload()
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task():
    payload = new_task_payload()
    return requests.put(ENDPOINT + "/update-task", json=payload)

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def test_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200



def test_create_task():
    create_task_response = create_task()

    data = create_task_response.json()
    task_id = data["task"]["task_id"]

    get_task_response = get_task(task_id)
    get_task_data = get_task_response.json()
    print(get_task_data)

    assert get_task_response.status_code == 200

@pytest.mark.skip
def test_update_task():
    # create a task
    create_task_response = create_task()
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # update the task
    payload = new_task_payload()
    new_payload = {
        "content": "new content",
        "user_id": payload["user_id"],
        "task_id": task_id,
        "is_done": True
    }

    update_task_response = update_task()
    assert update_task_response.status_code == 200

    # validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_list_tasks():
    user_id = "paula"
    list_tasks_response = requests.get(ENDPOINT + f"/list-tasks/{user_id}")
    assert list_tasks_response.status_code == 200

def test_delete_task():
    create_task_response = create_task()
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # check if deleted task is found
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


