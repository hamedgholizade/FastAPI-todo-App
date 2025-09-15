def test_tasks_list_response_401(anon_client):
    response = anon_client.get("/todo/tasks/")
    assert response.status_code == 401
    anon_client.headers.update({"Authorization": "Bearer testtest"})
    response = anon_client.get("/todo/tasks/")
    assert response.status_code == 401
    
def test_tasks_list_response_200(auth_client):
    response = auth_client.get("/todo/tasks/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_tasks_detail_response_200(auth_client, random_task):
    response = auth_client.get(f"/todo/tasks/{random_task.id}")
    assert response.status_code == 200
