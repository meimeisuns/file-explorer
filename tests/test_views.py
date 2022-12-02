import json


def test_list_directory(client):
    response = client.get("/")
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert len(response_dict) == 3
