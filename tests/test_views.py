import json

# NOTE: these tests were set to run in the sample_dir/ directory
# in the tests folder. Please run these tests by running:
#
# docker run -e DIR=/tests/sample_dir/ file-explorer
#
# (see README for build instructions.)


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

    # try again, should fail because directory already exists
    post_second_response = client.post("/", json={"type": "dir", "name": "new_dir"})
    assert post_second_response.status_code == 400
    assert "File exists" in post_second_response.text


def test_create_in_bad_dir_fails(client):
    post_response = client.post("/bad_dir/", json={"type": "dir", "name": "new_dir"})
    assert post_response.status_code == 400
    assert "Please use the path for an existing directory" in post_response.text


def test_create_from_file_fails(client):
    post_response = client.post("/baz.py", json={"type": "dir", "name": "new_dir"})
    assert post_response.status_code == 400
    assert "Unable to create new directory or file in file" in post_response.text


def test_create_without_type_fails(client):
    post_response = client.post("/", json={"name": "new_dir"})
    assert post_response.status_code == 400
    assert "Please specify type" in post_response.text


def test_create_without_name_fails(client):
    post_response = client.post("/", json={"type": "dir"})
    assert post_response.status_code == 400
    assert "Please provide name" in post_response.text


def test_create_file(client):
    # with text and with empty contents
    post_response = client.post(
        "/another_dir/",
        json={"type": "file", "name": "new_file.txt", "contents": "new text file!"},
    )
    assert post_response.status_code == 200
    get_response = client.get("/another_dir/new_file.txt")
    assert get_response.status_code == 200
    response_dict = json.loads(get_response.data)
    assert "new text file" in response_dict.get("text")

    post_response = client.post(
        "/another_dir/", json={"type": "file", "name": "empty_file.txt", "contents": ""}
    )
    assert post_response.status_code == 200
    get_response = client.get("/another_dir/empty_file.txt")
    assert get_response.status_code == 200
    response_dict = json.loads(get_response.data)
    assert response_dict.get("text") == ""


def test_create_file_no_ending_slash(client):
    post_response = client.post(
        "/another_dir",
        json={"type": "file", "name": "new_file.txt", "contents": "new text file!"},
    )
    assert post_response.status_code == 200
    get_response = client.get("/another_dir/new_file.txt")
    assert get_response.status_code == 200
    response_dict = json.loads(get_response.data)
    assert "new text file" in response_dict.get("text")


def test_create_file_no_contents_fails(client):
    # for validation only. should be able to have empty file
    post_response = client.post("/", json={"type": "file", "name": "new_file.txt"})
    assert post_response.status_code == 400
    assert "Please provide contents" in post_response.text
