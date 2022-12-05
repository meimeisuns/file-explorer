import json


def test_list_directory(client):
    response = client.get("/")
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert len(response_dict) == 3

    nested_dir_response = client.get("/another_dir/")
    assert nested_dir_response.status_code == 200
    nested_dir_response_dict = json.loads(nested_dir_response.data)
    assert len(nested_dir_response_dict) == 1


def test_file_contents(client):
    response = client.get("/baz.py")
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert "hello world!" in response_dict.get("text")


def test_hidden_file_contents(client):
    response = client.get("/.foo")
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert "hidden files" in response_dict.get("text")


def test_create_dir(client):
    post_response = client.post("/", json={"type": "dir", "name": "new_dir"})
    assert post_response.status_code == 200
    get_response = client.get("/new_dir/")
    assert get_response.status_code == 200

    # try again, should fail because file already exists
    post_second_response = client.post("/", json={"type": "dir", "name": "new_dir"})
    assert post_second_response.status_code == 400
    assert "File exists" in post_second_response.text


def test_create_dir_in_bad_dir_fails(client):
    post_response = client.post("/bad_dir/", json={"type": "dir", "name": "new_dir"})
    assert post_response.status_code == 400
    assert "No such file or directory" in post_response.text


def test_create_dir_from_file_fails(client):
    post_response = client.post("/baz.py", json={"type": "dir", "name": "new_dir"})
    assert post_response.status_code == 400
    assert "Unable to create folder in file" in post_response.text
