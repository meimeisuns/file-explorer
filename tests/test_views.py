import json


def test_list_directory(client):
    response = client.get("/")
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert len(response_dict) == 3

    nested_dir_response = client.get("/another_directory")
    assert nested_dir_response.status_code == 200
    nested_dir_response_dict = json.loads(nested_dir_response.data)
    assert len(nested_dir_response_dict) == 1
